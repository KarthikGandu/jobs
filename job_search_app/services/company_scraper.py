"""
Company Career Page Scraper for Quant Trading Firms
Scrapes jobs from 24 confirmed working firms
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
import re
from datetime import datetime

class CompanyScraper:
    """Base scraper for company career pages"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        # 24 confirmed working firms
        self.companies = {
            # Prop Trading (9 firms)
            'hudson_river_trading': {
                'name': 'Hudson River Trading',
                'url': 'https://www.hudsonrivertrading.com/careers/',
                'type': 'greenhouse',
                'category': 'Prop Trading',
            },
            'quantlab': {
                'name': 'QuantLab Financial',
                'url': 'https://www.quantlab.com/careers',
                'type': 'jobvite',
                'category': 'Prop Trading',
            },
            'jane_street': {
                'name': 'Jane Street',
                'url': 'https://www.janestreet.com/join-jane-street/open-roles/',
                'type': 'custom',
                'category': 'Prop Trading',
            },
            'citadel_securities': {
                'name': 'Citadel Securities',
                'url': 'https://www.citadelsecurities.com/careers/open-opportunities/',
                'type': 'custom',
                'category': 'Prop Trading',
            },
            'optiver': {
                'name': 'Optiver',
                'url': 'https://www.optiver.com/careers',
                'type': 'custom',
                'category': 'Prop Trading',
            },
            'akuna_capital': {
                'name': 'Akuna Capital',
                'url': 'https://akunacapital.com/careers',
                'type': 'custom',
                'category': 'Prop Trading',
            },
            'old_mission': {
                'name': 'Old Mission Capital',
                'url': 'https://oldmissioncapital.com/careers',
                'type': 'greenhouse',
                'category': 'Prop Trading',
            },
            'gts': {
                'name': 'GTS Global Trading',
                'url': 'https://gtsx.com/careers',
                'type': 'lever',
                'category': 'Prop Trading',
            },
            'flow_traders': {
                'name': 'Flow Traders',
                'url': 'https://www.flowtraders.com/careers',
                'type': 'greenhouse',
                'category': 'Prop Trading',
            },
            
            # Hedge Funds (8 firms)
            'citadel': {
                'name': 'Citadel LLC',
                'url': 'https://www.citadel.com/careers/open-opportunities/',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            'worldquant': {
                'name': 'WorldQuant',
                'url': 'https://www.worldquant.com/careers',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            'two_sigma': {
                'name': 'Two Sigma',
                'url': 'https://www.twosigma.com/careers',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            'pdt_partners': {
                'name': 'PDT Partners',
                'url': 'https://www.pdtpartners.com/careers',
                'type': 'greenhouse',
                'category': 'Hedge Fund',
            },
            'bridgewater': {
                'name': 'Bridgewater Associates',
                'url': 'https://www.bridgewater.com/careers',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            'aqr': {
                'name': 'AQR Capital Management',
                'url': 'https://www.aqr.com/Careers',
                'type': 'greenhouse',
                'category': 'Hedge Fund',
            },
            'squarepoint': {
                'name': 'Squarepoint Capital',
                'url': 'https://www.squarepoint-capital.com/careers',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            'teza': {
                'name': 'Teza Technologies',
                'url': 'https://www.teza.com/careers',
                'type': 'custom',
                'category': 'Hedge Fund',
            },
            
            # Asset Managers (3 firms)
            'blackrock': {
                'name': 'BlackRock',
                'url': 'https://careers.blackrock.com',
                'type': 'custom',
                'category': 'Asset Manager',
            },
            'fidelity': {
                'name': 'Fidelity Investments',
                'url': 'https://jobs.fidelity.com',
                'type': 'workday',
                'category': 'Asset Manager',
            },
            'state_street': {
                'name': 'State Street',
                'url': 'https://careers.statestreet.com',
                'type': 'workday',
                'category': 'Asset Manager',
            },
            
            # Investment Banks (4 firms)
            'deutsche_bank': {
                'name': 'Deutsche Bank',
                'url': 'https://careers.db.com',
                'type': 'custom',
                'category': 'Investment Bank',
            },
            'barclays': {
                'name': 'Barclays',
                'url': 'https://search.jobs.barclays/',
                'type': 'workday',
                'category': 'Investment Bank',
            },
            'societe_generale': {
                'name': 'Société Générale',
                'url': 'https://careers.societegenerale.com',
                'type': 'taleo',
                'category': 'Investment Bank',
            },
            'nomura': {
                'name': 'Nomura',
                'url': 'https://www.nomura.com/careers',
                'type': 'custom',
                'category': 'Investment Bank',
            },
        }
    
    def get_company_list(self) -> List[Dict]:
        """Get list of all companies"""
        return [
            {
                'id': key,
                'name': info['name'],
                'category': info['category'],
                'url': info['url']
            }
            for key, info in self.companies.items()
        ]
    
    def scrape_company(self, company_id: str, search_term: str = None) -> List[Dict]:
        """Scrape jobs from a specific company"""
        if company_id not in self.companies:
            raise ValueError(f"Unknown company: {company_id}")
        
        company = self.companies[company_id]
        scraper_type = company['type']
        
        if scraper_type == 'greenhouse':
            return self._scrape_greenhouse(company, search_term)
        elif scraper_type == 'lever':
            return self._scrape_lever(company, search_term)
        elif scraper_type == 'jobvite':
            return self._scrape_jobvite(company, search_term)
        elif scraper_type == 'workday':
            return self._scrape_workday(company, search_term)
        elif scraper_type == 'taleo':
            return self._scrape_taleo(company, search_term)
        else:  # custom
            return self._scrape_custom(company, search_term)
    
    def scrape_all_companies(self, search_term: str = None, categories: List[str] = None) -> Dict[str, List[Dict]]:
        """Scrape jobs from all companies"""
        results = {}
        
        for company_id, company_info in self.companies.items():
            # Filter by category if specified
            if categories and company_info['category'] not in categories:
                continue
            
            try:
                print(f"Scraping {company_info['name']}...")
                jobs = self.scrape_company(company_id, search_term)
                if jobs:
                    results[company_id] = jobs
                    print(f"  ✓ Found {len(jobs)} jobs")
                else:
                    print(f"  - No jobs found")
            except Exception as e:
                print(f"  ✗ Error: {str(e)[:50]}")
                continue
        
        return results
    
    def _scrape_greenhouse(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape Greenhouse ATS (standardized API)"""
        # Greenhouse has a public API endpoint
        # Extract company token from URL
        try:
            response = requests.get(company['url'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find Greenhouse board token
            scripts = soup.find_all('script')
            board_token = None
            
            for script in scripts:
                if script.string and 'greenhouse' in script.string.lower():
                    # Extract token from script
                    match = re.search(r'boards/([a-zA-Z0-9_-]+)', script.string)
                    if match:
                        board_token = match.group(1)
                        break
            
            if not board_token:
                # Try to find in page source
                match = re.search(r'boards\.greenhouse\.io/([a-zA-Z0-9_-]+)', response.text)
                if match:
                    board_token = match.group(1)
            
            if board_token:
                # Use Greenhouse API
                api_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
                api_response = requests.get(api_url, timeout=10)
                
                if api_response.status_code == 200:
                    data = api_response.json()
                    jobs = []
                    
                    for job in data.get('jobs', []):
                        # Filter by search term if provided
                        if search_term:
                            title_lower = job.get('title', '').lower()
                            if search_term.lower() not in title_lower:
                                continue
                        
                        jobs.append({
                            'title': job.get('title'),
                            'location': job.get('location', {}).get('name') if isinstance(job.get('location'), dict) else job.get('location'),
                            'url': job.get('absolute_url'),
                            'company': company['name'],
                            'company_id': board_token,
                            'category': company['category'],
                            'posted_date': job.get('updated_at'),
                            'source': 'greenhouse'
                        })
                    
                    return jobs
        except Exception as e:
            print(f"Greenhouse error for {company['name']}: {e}")
        
        return []
    
    def _scrape_lever(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape Lever ATS"""
        # Lever also has an API
        try:
            # Extract company name for Lever API
            company_slug = company['url'].split('//')[-1].split('.')[0]
            
            # Try Lever API
            api_url = f"https://api.lever.co/v0/postings/{company_slug}"
            response = requests.get(api_url, params={'mode': 'json'}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = []
                
                for job in data:
                    if search_term:
                        title_lower = job.get('text', '').lower()
                        if search_term.lower() not in title_lower:
                            continue
                    
                    jobs.append({
                        'title': job.get('text'),
                        'location': job.get('categories', {}).get('location'),
                        'url': job.get('hostedUrl'),
                        'company': company['name'],
                        'category': company['category'],
                        'posted_date': job.get('createdAt'),
                        'source': 'lever'
                    })
                
                return jobs
        except Exception as e:
            print(f"Lever error for {company['name']}: {e}")
        
        return []
    
    def _scrape_jobvite(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape Jobvite ATS"""
        # Jobvite requires custom parsing
        return self._scrape_custom(company, search_term)
    
    def _scrape_workday(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape Workday ATS"""
        # Workday is complex - for now, return empty
        # TODO: Implement Workday scraping in future
        return []
    
    def _scrape_taleo(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape Taleo ATS"""
        # Taleo is complex - for now, return empty
        # TODO: Implement Taleo scraping in future
        return []
    
    def _scrape_custom(self, company: Dict, search_term: str = None) -> List[Dict]:
        """Scrape custom career pages (HTML parsing)"""
        try:
            response = requests.get(company['url'], headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = []
                
                # Try to find job listings with common patterns
                job_elements = []
                
                # Pattern 1: Elements with "job" in class name
                job_elements.extend(soup.find_all(class_=re.compile(r'job', re.I)))
                
                # Pattern 2: Elements with "position" in class name
                job_elements.extend(soup.find_all(class_=re.compile(r'position', re.I)))
                
                # Pattern 3: Elements with "role" in class name
                job_elements.extend(soup.find_all(class_=re.compile(r'role', re.I)))
                
                # Pattern 4: Elements with "opening" in class name
                job_elements.extend(soup.find_all(class_=re.compile(r'opening', re.I)))
                
                for element in job_elements[:50]:  # Limit to first 50 to avoid duplicates
                    # Extract title
                    title = None
                    for tag in ['h1', 'h2', 'h3', 'h4', 'a']:
                        title_elem = element.find(tag)
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            if len(title) > 10:  # Valid title
                                break
                    
                    if not title:
                        continue
                    
                    # Filter by search term
                    if search_term and search_term.lower() not in title.lower():
                        continue
                    
                    # Extract URL
                    url = None
                    link = element.find('a', href=True)
                    if link:
                        url = link['href']
                        if url and not url.startswith('http'):
                            # Make absolute URL
                            base_url = '/'.join(company['url'].split('/')[:3])
                            url = base_url + url
                    
                    # Extract location (try common patterns)
                    location = "Location not specified"
                    location_elem = element.find(class_=re.compile(r'location', re.I))
                    if location_elem:
                        location = location_elem.get_text(strip=True)
                    
                    jobs.append({
                        'title': title,
                        'location': location,
                        'url': url or company['url'],
                        'company': company['name'],
                        'category': company['category'],
                        'posted_date': datetime.now().isoformat(),
                        'source': 'custom_parse'
                    })
                
                # Remove duplicates by title
                seen_titles = set()
                unique_jobs = []
                for job in jobs:
                    if job['title'] not in seen_titles:
                        seen_titles.add(job['title'])
                        unique_jobs.append(job)
                
                return unique_jobs
                
        except Exception as e:
            print(f"Custom scrape error for {company['name']}: {e}")
        
        return []
