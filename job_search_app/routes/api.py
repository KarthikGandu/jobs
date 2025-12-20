"""
API routes - handles all API requests
"""
from flask import Blueprint, request, jsonify, send_file, current_app
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import io

# Add jobspy2 to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "jobspy2" / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "jobsparser" / "src"))

from jobspy2 import scrape_jobs

from ..services import JobMatcher, KeywordExpander, CompanyScraper
from ..utils import validate_job_search_params, validate_keyword_expansion, validate_company_search
from ..utils.errors import ValidationError, ScrapingError, ResourceNotFoundError

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize services
matcher = JobMatcher()
expander = KeywordExpander()
company_scraper = CompanyScraper()


@api_bp.route('/companies', methods=['GET'])
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
            'status': 'success',
            'total_companies': len(companies),
            'companies': companies,
            'by_category': by_category
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching companies: {str(e)}")
        raise ScrapingError(f"Failed to fetch companies: {str(e)}")


@api_bp.route('/companies/<company_name>/jobs', methods=['POST'])
def scrape_company_jobs(company_name):
    """Scrape jobs from a specific company"""
    try:
        data = request.get_json() or {}
        params = validate_company_search({
            'company': company_name,
            'search_term': data.get('search_term', ''),
            'results_wanted': data.get('results_wanted', 15)
        })
        
        current_app.logger.info(f"Scraping jobs for company: {params['company']}")
        
        # Scrape company jobs
        jobs_df = company_scraper.scrape_company_jobs(
            company=params['company'],
            search_term=params['search_term'],
            results_wanted=params['results_wanted']
        )
        
        if jobs_df is None or len(jobs_df) == 0:
            return jsonify({
                'status': 'success',
                'jobs_found': 0,
                'message': f'No jobs found for {params["company"]}',
                'jobs': []
            })
        
        # Convert to list of dictionaries
        jobs_list = jobs_df.to_dict('records')
        
        # Save to file
        output_dir = Path(current_app.config['OUTPUT_DIR'])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{params['company'].replace(' ', '_')}_{timestamp}.csv"
        filepath = output_dir / filename
        jobs_df.to_csv(filepath, index=False)
        
        return jsonify({
            'status': 'success',
            'jobs_found': len(jobs_list),
            'company': params['company'],
            'jobs': jobs_list,
            'file': filename
        })
        
    except ValidationError as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error scraping company jobs: {str(e)}")
        raise ScrapingError(f"Failed to scrape jobs: {str(e)}")


@api_bp.route('/search', methods=['POST'])
def search_jobs():
    """Search for jobs across multiple sites"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        # Handle both search_term (single) and search_terms (array) from frontend
        search_terms = data.get('search_terms', [])
        if not search_terms:
            search_term = data.get('search_term', '')
            if search_term:
                search_terms = [search_term]
        
        if not search_terms:
            raise ValidationError("search_term or search_terms is required")
        
        # Get parameters from frontend format
        location = data.get('location', '')
        if not location:
            raise ValidationError("location is required")
        
        sites = data.get('sites', ['linkedin', 'indeed'])
        results_wanted = data.get('results_wanted', 20)
        distance = data.get('distance', 50)
        is_remote = data.get('is_remote', False)
        job_types = data.get('job_types', [])
        hours_old = data.get('hours_old')
        
        current_app.logger.info(f"Job search request: {search_terms} in {location}")
        
        # Search for each term and combine results
        all_jobs = []
        jobs_by_term = {}
        
        for term in search_terms:
            try:
                current_app.logger.info(f"Searching for: {term}")
                
                jobs_df = scrape_jobs(
                    site_name=sites,
                    search_term=term,
                    location=location,
                    results_wanted=results_wanted,
                    distance=distance,
                    job_type=job_types[0] if job_types else None,
                    is_remote=is_remote,
                    country_indeed='usa',
                    hours_old=hours_old
                )
                
                if jobs_df is not None and len(jobs_df) > 0:
                    jobs_by_term[term] = len(jobs_df)
                    all_jobs.append(jobs_df)
                else:
                    jobs_by_term[term] = 0
                    
            except Exception as e:
                current_app.logger.error(f"Error searching for {term}: {str(e)}")
                jobs_by_term[term] = 0
        
        # Combine all results
        if all_jobs:
            combined_df = pd.concat(all_jobs, ignore_index=True)
            # Remove duplicates based on job_url
            combined_df = combined_df.drop_duplicates(subset=['job_url'], keep='first')
        else:
            return jsonify({
                'status': 'success',
                'jobs_count': 0,
                'message': 'No jobs found matching your criteria',
                'jobs': [],
                'jobs_by_term': jobs_by_term
            })
        
        # Convert to list of dictionaries
        jobs_list = combined_df.to_dict('records')
        
        # Save to CSV
        output_dir = Path(current_app.config['OUTPUT_DIR'])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jobs_{timestamp}.csv"
        filepath = output_dir / filename
        combined_df.to_csv(filepath, index=False)
        
        return jsonify({
            'status': 'success',
            'jobs_count': len(jobs_list),
            'jobs': jobs_list,
            'jobs_by_term': jobs_by_term,
            'download_url': f'/api/download/{filename}',
            'download_files': {}  # For compatibility with frontend
        })
        
    except ValidationError as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error during job search: {str(e)}")
        raise ScrapingError(f"Job search failed: {str(e)}")


@api_bp.route('/match', methods=['POST'])
def match_jobs():
    """Match and filter jobs based on ML criteria"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        jobs = data.get('jobs')
        preferences = data.get('preferences', {})
        
        if not jobs:
            raise ValidationError("jobs array is required")
        
        current_app.logger.info(f"Matching {len(jobs)} jobs with preferences")
        
        # Convert to DataFrame
        jobs_df = pd.DataFrame(jobs)
        
        # Match jobs
        matched_df = matcher.match_jobs(jobs_df, preferences)
        matched_list = matched_df.to_dict('records')
        
        return jsonify({
            'status': 'success',
            'total_jobs': len(jobs),
            'matched_jobs': len(matched_list),
            'jobs': matched_list
        })
        
    except ValidationError as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error matching jobs: {str(e)}")
        raise ScrapingError(f"Job matching failed: {str(e)}")


@api_bp.route('/expand-keywords', methods=['POST'])
def expand_keywords():
    """Expand search keywords with related terms - FAST VERSION"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        # Handle both single keyword and multiple keywords
        keywords = data.get('keywords', [])
        if not keywords:
            keyword = data.get('keyword', '')
            if not keyword:
                raise ValidationError("keyword or keywords is required")
            keywords = [keyword]
        
        current_app.logger.info(f"Expanding keywords: {keywords}")
        
        # Fast expansion - limit to max 8 variations per keyword
        all_expanded = set()
        for kw in keywords:
            all_expanded.add(kw)  # Keep original
            expanded = expander.expand_keyword(kw, max_expansions=5)  # Reduced from 8 to 5
            all_expanded.update(expanded[:5])  # Take only top 5
            
            # Stop if we have enough terms
            if len(all_expanded) >= 15:
                break
        
        expanded_list = list(all_expanded)[:15]  # Max 15 total terms
        
        return jsonify({
            'success': True,
            'status': 'success',
            'original_keywords': keywords,
            'expanded': expanded_list,
            'count': len(expanded_list)
        })
        
    except ValidationError as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error expanding keywords: {str(e)}")
        raise ScrapingError(f"Keyword expansion failed: {str(e)}")


@api_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a job results CSV file"""
    try:
        output_dir = Path(current_app.config['OUTPUT_DIR'])
        filepath = output_dir / filename
        
        if not filepath.exists():
            raise ResourceNotFoundError(f"File not found: {filename}")
        
        return send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except ResourceNotFoundError as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error downloading file: {str(e)}")
        raise ScrapingError(f"File download failed: {str(e)}")
