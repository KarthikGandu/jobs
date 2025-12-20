"""Test scraping from different sites"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "jobspy2" / "src"))

from jobspy2 import scrape_jobs

sites_to_test = [
    ('indeed', 'Indeed'),
    ('linkedin', 'LinkedIn'),
    ('glassdoor', 'Glassdoor'),
    ('zip_recruiter', 'ZipRecruiter'),
    ('google', 'Google Jobs'),
]

print("=" * 60)
print("Testing Job Site Scrapers")
print("=" * 60)
print()

for site_code, site_name in sites_to_test:
    print(f"Testing {site_name}...")
    try:
        if site_code == 'google':
            result = scrape_jobs(
                site_name=site_code,
                google_search_term="Software Engineer",
                location="San Francisco",
                results_wanted=5,
            )
        else:
            result = scrape_jobs(
                site_name=site_code,
                search_term="Software Engineer",
                location="San Francisco",
                results_wanted=5,
                country_indeed='USA',
            )
        
        if result is not None and not result.empty:
            print(f"  ✅ SUCCESS - {len(result)} jobs found")
            print(f"     Sample: {result.iloc[0]['title'] if 'title' in result.columns else 'N/A'}")
        else:
            print(f"  ⚠️  WARNING - No results returned (may be rate limited or blocked)")
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"  ❌ ERROR - {error_msg}")
        
        # Provide specific guidance
        if 'glassdoor' in site_code.lower():
            print(f"     Note: Glassdoor requires authentication or may be blocking automated requests")
        elif 'ziprecruiter' in site_code.lower():
            print(f"     Note: ZipRecruiter may require specific user agents or cookies")
        elif 'google' in site_code.lower():
            print(f"     Note: Google Jobs has strict rate limiting")
    
    print()

print("=" * 60)
print("Summary:")
print("  ✅ = Working perfectly")
print("  ⚠️  = May work but currently no results")
print("  ❌ = Blocked or requires fixes")
print()
print("Recommendation: Focus on Indeed and LinkedIn for best results")
print("=" * 60)
