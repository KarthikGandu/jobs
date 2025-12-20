"""
Karthik's Job Search Site - Flask Backend with ML-powered filtering
"""
from flask import Flask, render_template, request, jsonify, send_file
import re

from flask_cors import CORS
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import io
from job_matcher import JobMatcher
from keyword_expander import KeywordExpander
from company_scraper import CompanyScraper

# Add jobspy2 to path
sys.path.insert(0, str(Path(__file__).parent / "jobspy2" / "src"))
sys.path.insert(0, str(Path(__file__).parent / "jobsparser" / "src"))

from jobspy2 import scrape_jobs

# Initialize ML-powered job matcher, keyword expander, and company scraper
matcher = JobMatcher()
expander = KeywordExpander()
company_scraper = CompanyScraper()

app = Flask(__name__)
CORS(app)

# Create output directory
OUTPUT_DIR = Path("job_results")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get list of all scrapable companies"""
    try:
        companies = company_scraper.get_company_list()
        
        # Group by category
        by_category = {}
        for company in companies:
            category = company['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(company)
        
        return jsonify({
            'success': True,
            'companies': companies,
            'by_category': by_category,
            'total': len(companies)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape-companies', methods=['POST'])
def scrape_companies_only():
    """Scrape ALL jobs from all 24 companies (no search filter)"""
    try:
        print("Starting to scrape all 24 companies...")
        
        # Scrape all companies without search filter
        all_results = company_scraper.scrape_all_companies(search_term=None, categories=None)
        
        # Combine all jobs
        all_jobs = []
        jobs_by_company = {}
        
        for company_id, jobs in all_results.items():
            company_info = company_scraper.companies[company_id]
            company_name = company_info['name']
            
            jobs_by_company[company_name] = len(jobs)
            
            for job in jobs:
                all_jobs.append({
                    'title': job.get('title'),
                    'company': job.get('company'),
                    'location': job.get('location'),
                    'job_url': job.get('url'),
                    'date_posted': job.get('posted_date'),
                    'site': 'company_career_page',
                    'category': job.get('category'),
                    'job_type': None,
                    'is_remote': 'remote' in job.get('location', '').lower(),
                    'description': None,
                    'relevance_score': 1.0
                })
        
        if not all_jobs:
            return jsonify({'error': 'No jobs found from any companies'}), 404
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"company_jobs_all_firms_{timestamp}.csv"
        filepath = OUTPUT_DIR / filename
        
        df = pd.DataFrame(all_jobs)
        df.to_csv(filepath, index=False)
        
        print(f"✓ Scraped {len(all_jobs)} total jobs from {len(all_results)} companies")
        
        return jsonify({
            'success': True,
            'jobs_count': len(all_jobs),
            'companies_scraped': len(all_results),
            'jobs': all_jobs,
            'jobs_by_company': jobs_by_company,
            'download_url': f'/api/download/{filename}'
        })
        
    except Exception as e:
        print(f"Error scraping companies: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/expand-keywords', methods=['POST'])
def expand_keywords():
    """Endpoint to get keyword expansion suggestions"""
    try:
        data = request.json
        keywords = data.get('keywords', [])
        
        # Get expansions for all keywords
        expanded = expander.expand_keywords(keywords, max_total=10)
        
        return jsonify({
            'success': True,
            'original': keywords,
            'expanded': expanded,
            'count': len(expanded)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        
        # Extract parameters
        search_terms = data.get('search_terms', [])
        auto_expand = data.get('auto_expand', False)
        
        # Auto-expand keywords if requested
        if auto_expand and search_terms:
            search_terms = expander.expand_keywords(search_terms, max_total=10)
        location = data.get('location', '')
        sites = data.get('sites', ['indeed'])  # Default to indeed instead of linkedin
        
        # Check if company scraping is requested
        scrape_companies = data.get('scrape_companies', False)
        selected_companies = data.get('selected_companies', [])
        job_types = data.get('job_types', [])
        is_remote = data.get('is_remote', False)
        results_wanted = data.get('results_wanted', 20)
        distance = data.get('distance', 50)
        hours_old = data.get('hours_old', None)
        experience_levels = data.get('experience_levels', [])  # New: years-based experience
        
        # Map experience levels to LinkedIn levels
        linkedin_experience_levels = []
        for exp in experience_levels:
            linkedin_experience_levels.extend(matcher.map_experience_level(exp))
        linkedin_experience_levels = list(set(linkedin_experience_levels)) if linkedin_experience_levels else []
        
        # Validate required fields
        if not search_terms or not location:
            return jsonify({'error': 'Search term and location are required'}), 400
        
        # Process each search term separately with ML filtering
        jobs_by_search_term = {}  # Store jobs per search term for separate CSVs
        
        # First, scrape from company career pages if requested
        if scrape_companies:
            print(f"Scraping company career pages...")
            for search_term in search_terms:
                company_jobs = []
                
                if selected_companies:
                    # Scrape specific companies
                    for company_id in selected_companies:
                        try:
                            jobs = company_scraper.scrape_company(company_id, search_term)
                            company_jobs.extend(jobs)
                        except Exception as e:
                            print(f"Error scraping company {company_id}: {e}")
                else:
                    # Scrape all companies
                    try:
                        all_company_jobs = company_scraper.scrape_all_companies(search_term)
                        for company_id, jobs in all_company_jobs.items():
                            company_jobs.extend(jobs)
                    except Exception as e:
                        print(f"Error scraping companies: {e}")
                
                if company_jobs:
                    # Convert company jobs to consistent format
                    formatted_jobs = []
                    for job in company_jobs:
                        formatted_jobs.append({
                            'title': job.get('title'),
                            'company': job.get('company'),
                            'location': job.get('location'),
                            'job_url': job.get('url'),
                            'date_posted': job.get('posted_date'),
                            'site': 'company_career_page',
                            'job_type': None,
                            'is_remote': 'remote' in job.get('location', '').lower(),
                            'description': None,
                            'relevance_score': 1.0  # Company jobs are highly relevant
                        })
                    
                    if search_term not in jobs_by_search_term:
                        jobs_by_search_term[search_term] = []
                    jobs_by_search_term[search_term].extend(formatted_jobs)
                    print(f"Found {len(formatted_jobs)} jobs from company pages for '{search_term}'")
        
        # Then scrape from regular job sites
        for search_term in search_terms:
            term_jobs = []
            
            for site in sites:
                try:
                    print(f"Attempting to scrape {site} for '{search_term}'...")
                    
                    # Prepare scraping parameters
                    scrape_params = {
                        'site_name': site,
                        'search_term': search_term,
                        'location': location,
                        'results_wanted': results_wanted,
                        'hours_old': hours_old,
                        'country_indeed': 'USA',
                        'job_type': job_types[0] if job_types else None,
                        'is_remote': is_remote,
                        'distance': distance,
                        'linkedin_fetch_description': False,  # Faster without descriptions
                        'description_format': 'markdown',
                        'linkedin_experience_levels': linkedin_experience_levels if linkedin_experience_levels else None,
                        'offset': 0,  # Start from beginning
                    }
                    
                    # Site-specific adjustments
                    if site.lower() == 'google':
                        # Google Jobs needs google_search_term instead of search_term
                        scrape_params['google_search_term'] = search_term
                        scrape_params.pop('search_term', None)
                    elif site.lower() == 'glassdoor':
                        # Glassdoor may have limitations - try with fewer results
                        scrape_params['results_wanted'] = min(results_wanted, 15)
                        print(f"Note: Glassdoor limited to 15 results per search")
                    elif site.lower() == 'zip_recruiter':
                        # ZipRecruiter sometimes needs specific formatting
                        scrape_params['results_wanted'] = min(results_wanted, 20)
                    
                    # Scrape jobs with optimized settings
                    jobs_df = scrape_jobs(**scrape_params)
                    
                    print(f"✓ {site}: Retrieved {len(jobs_df) if jobs_df is not None else 0} jobs")
                    
                    if jobs_df is not None and not jobs_df.empty:
                        # Convert to dict for JSON serialization with proper handling
                        jobs_df = jobs_df.astype(object).where(pd.notnull(jobs_df), None)
                        # Convert datetime objects to strings
                        for col in jobs_df.select_dtypes(include=['datetime64']).columns:
                            jobs_df[col] = jobs_df[col].astype(str)
                        # Convert any enum types to their values (strings)
                        for col in jobs_df.columns:
                            jobs_df[col] = jobs_df[col].apply(
                                lambda x: x.value if hasattr(x, 'value') else (str(x) if x is not None else None)
                            )
                        jobs_list = jobs_df.to_dict('records')
                        
                        # Apply ML-powered relevance filtering with job type
                        job_type_filter = job_types[0] if job_types else None
                        filtered_jobs = matcher.filter_jobs(jobs_list, search_term, threshold=0.5, job_type_filter=job_type_filter)
                        
                        term_jobs.extend(filtered_jobs)
                        
                except Exception as e:
                    print(f"✗ Error scraping {site} for {search_term}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Continue with other sites even if one fails
                    continue
            
            # Store jobs for this search term
            if term_jobs:
                jobs_by_search_term[search_term] = term_jobs
        
        # Combine all jobs for display
        all_jobs = []
        for term_jobs in jobs_by_search_term.values():
            all_jobs.extend(term_jobs)
        
        if not all_jobs:
            return jsonify({'error': 'No relevant jobs found matching your criteria'}), 404
        
        # Save separate CSV for each search term
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_files = {}
        
        for search_term, term_jobs in jobs_by_search_term.items():
            # Create clean filename from search term
            clean_term = re.sub(r'[^a-zA-Z0-9]', '_', search_term).lower()
            filename = f"jobs_{clean_term}_{timestamp}.csv"
            filepath = OUTPUT_DIR / filename
            
            df = pd.DataFrame(term_jobs)
            # Remove description column to reduce file size
            if 'description' in df.columns:
                df = df.drop('description', axis=1)
            df.to_csv(filepath, index=False)
            
            download_files[search_term] = filename
        
        # Also save combined CSV
        combined_filename = f"jobs_all_{timestamp}.csv"
        combined_filepath = OUTPUT_DIR / combined_filename
        df_all = pd.DataFrame(all_jobs)
        if 'description' in df_all.columns:
            df_all = df_all.drop('description', axis=1)
        df_all.to_csv(combined_filepath, index=False)
        
        # Return results
        return jsonify({
            'success': True,
            'jobs_count': len(all_jobs),
            'jobs': all_jobs[:100],  # Return first 100 for display
            'download_url': f'/api/download/{combined_filename}',
            'download_files': download_files,  # Per-term files
            'jobs_by_term': {term: len(jobs) for term, jobs in jobs_by_search_term.items()}
        })
        
    except Exception as e:
        print(f"Error in scrape endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download(filename):
    try:
        filepath = OUTPUT_DIR / filename
        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
