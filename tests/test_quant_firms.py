"""Test scraping quant trading firm career pages"""
import requests
from bs4 import BeautifulSoup
import json

firms = [
    ("Hudson River Trading", "https://www.hudsonrivertrading.com/careers/"),
    ("Jump Trading", "https://www.jumptrading.com/careers"),
    ("Virtu Financial", "https://www.virtu.com/careers/"),
    ("Tower Research Capital", "https://www.tower-research.com/join-us"),
    ("HAP Capital", "https://haptrading.com/join-us/"),
    ("QuantLab Financial", "https://www.quantlab.com/careers"),
    ("Headlands Technologies", "https://www.headlandstech.com/careers"),
    ("Jane Street", "https://www.janestreet.com/join-jane-street/open-roles/"),
    ("Citadel Securities", "https://www.citadelsecurities.com/careers/open-opportunities/"),
    ("IMC Trading", "https://www.imc.com/us/careers"),
    ("Optiver", "https://www.optiver.com/careers"),
    ("Akuna Capital", "https://akunacapital.com/careers"),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

print("=" * 80)
print("TESTING QUANT TRADING FIRM CAREER PAGES")
print("=" * 80)
print()

results = []

for name, url in firms:
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for common ATS systems
            content = response.text.lower()
            
            ats_detected = None
            if 'greenhouse' in content:
                ats_detected = "Greenhouse"
            elif 'lever' in content:
                ats_detected = "Lever"
            elif 'workday' in content:
                ats_detected = "Workday"
            elif 'taleo' in content:
                ats_detected = "Oracle Taleo"
            elif 'icims' in content:
                ats_detected = "iCIMS"
            elif 'jobvite' in content:
                ats_detected = "Jobvite"
            
            # Check for job listings
            job_keywords = ['position', 'role', 'opening', 'opportunity', 'job']
            has_jobs = any(keyword in content for keyword in job_keywords)
            
            # Check if heavily JavaScript dependent
            js_heavy = 'data-react' in content or 'data-ng' in content or '__NEXT_DATA__' in content
            
            # Try to find job elements
            job_elements = []
            for selector in ['job', 'role', 'position', 'opening', 'opportunity']:
                job_elements.extend(soup.find_all(class_=lambda x: x and selector in x.lower()))
            
            result = {
                'name': name,
                'url': url,
                'status': 'SUCCESS',
                'ats': ats_detected,
                'js_heavy': js_heavy,
                'has_jobs': has_jobs,
                'job_elements_found': len(job_elements),
                'scrapable': not js_heavy and has_jobs
            }
            
            print(f"  ATS: {ats_detected or 'Custom/Unknown'}")
            print(f"  JavaScript Heavy: {'Yes' if js_heavy else 'No'}")
            print(f"  Job Listings Found: {len(job_elements)} elements")
            
            if result['scrapable']:
                print(f"  ✅ LIKELY SCRAPABLE")
            elif js_heavy:
                print(f"  ⚠️  NEEDS SELENIUM (JavaScript-heavy)")
            else:
                print(f"  ❌ DIFFICULT TO SCRAPE")
            
        else:
            result = {
                'name': name,
                'url': url,
                'status': f'FAILED ({response.status_code})',
                'scrapable': False
            }
            print(f"  ❌ Failed with status {response.status_code}")
        
        results.append(result)
        
    except Exception as e:
        result = {
            'name': name,
            'url': url,
            'status': f'ERROR: {str(e)[:50]}',
            'scrapable': False
        }
        results.append(result)
        print(f"  ❌ Error: {str(e)[:80]}")
    
    print()

# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

scrapable = [r for r in results if r.get('scrapable', False)]
needs_selenium = [r for r in results if r.get('js_heavy', False)]
failed = [r for r in results if r['status'] != 'SUCCESS']

print(f"Total Firms: {len(firms)}")
print(f"✅ Likely Scrapable (Simple): {len(scrapable)}")
print(f"⚠️  Needs Selenium (JS-heavy): {len(needs_selenium)}")
print(f"❌ Failed/Difficult: {len(failed)}")
print()

if scrapable:
    print("✅ SCRAPABLE:")
    for r in scrapable:
        print(f"  • {r['name']}")
    print()

if needs_selenium:
    print("⚠️  NEEDS SELENIUM:")
    for r in needs_selenium:
        print(f"  • {r['name']} (ATS: {r.get('ats', 'Unknown')})")
    print()

# ATS Statistics
ats_counts = {}
for r in results:
    if r.get('ats'):
        ats_counts[r['ats']] = ats_counts.get(r['ats'], 0) + 1

if ats_counts:
    print("ATS Systems Detected:")
    for ats, count in ats_counts.items():
        print(f"  • {ats}: {count} firms")
    print()

print("=" * 80)
print("RECOMMENDATION")
print("=" * 80)
if len(scrapable) >= 6:
    print("✅ GOOD NEWS: Many firms use simple career pages")
    print("   Can build basic scraper for these")
elif len(needs_selenium) >= 6:
    print("⚠️  MIXED: Most firms need Selenium")
    print("   Need browser automation for reliable scraping")
else:
    print("❌ CHALLENGING: Most firms use complex ATS systems")
    print("   Better to use LinkedIn/Indeed with company filters")

print("=" * 80)

