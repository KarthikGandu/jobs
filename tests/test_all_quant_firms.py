"""Test scraping ALL quant trading firms, hedge funds, and financial institutions"""
import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

print("=" * 100)
print("TESTING ALL QUANT TRADING FIRMS, HEDGE FUNDS & FINANCIAL INSTITUTIONS")
print("=" * 100)
print()

# Read firms from CSV
firms = []
with open('quant_firms_full_list.csv', 'r') as f:
    reader = csv.DictReader(f)
    firms = list(reader)

results = []
categories_stats = {}

for i, firm in enumerate(firms, 1):
    name = firm['Company Name']
    url = firm['Career URL']
    category = firm['Category']
    
    print(f"[{i}/{len(firms)}] Testing: {name}")
    print(f"     URL: {url[:70]}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = response.text.lower()
            
            # Detect ATS
            ats = None
            if 'greenhouse' in content or 'boards-api.greenhouse.io' in content:
                ats = "Greenhouse"
            elif 'lever.co' in content or 'lever' in content:
                ats = "Lever"
            elif 'myworkdayjobs.com' in content or 'workday' in content:
                ats = "Workday"
            elif 'taleo' in content:
                ats = "Taleo"
            elif 'icims' in content:
                ats = "iCIMS"
            elif 'jobvite' in content:
                ats = "Jobvite"
            elif 'smartrecruiters' in content:
                ats = "SmartRecruiters"
            
            # Check for JavaScript frameworks
            js_heavy = any(x in content for x in ['data-react', '__next_data__', 'ng-app', 'vue.js'])
            
            # Try to find job elements
            job_count = 0
            for selector in ['job', 'role', 'position', 'opening', 'career', 'opportunity']:
                job_count += len(soup.find_all(class_=lambda x: x and selector in str(x).lower()))
            
            scrapable = not js_heavy and job_count > 0
            
            result = {
                'name': name,
                'category': category,
                'url': url,
                'status': '✅ SUCCESS',
                'http_code': response.status_code,
                'ats': ats or 'Custom',
                'js_heavy': js_heavy,
                'job_elements': job_count,
                'scrapable': 'YES' if scrapable else ('SELENIUM' if js_heavy else 'MAYBE')
            }
            
            symbol = '✅' if scrapable else ('⚠️' if js_heavy else '🔍')
            print(f"     {symbol} Status: {response.status_code} | ATS: {ats or 'Custom'} | Jobs: {job_count} | Scrapable: {result['scrapable']}")
            
        else:
            result = {
                'name': name,
                'category': category,
                'url': url,
                'status': f'❌ HTTP {response.status_code}',
                'http_code': response.status_code,
                'scrapable': 'NO'
            }
            print(f"     ❌ Failed: HTTP {response.status_code}")
        
    except requests.exceptions.Timeout:
        result = {
            'name': name,
            'category': category,
            'url': url,
            'status': '⏱️ TIMEOUT',
            'scrapable': 'NO'
        }
        print(f"     ⏱️ Timeout")
    except Exception as e:
        result = {
            'name': name,
            'category': category,
            'url': url,
            'status': f'❌ ERROR',
            'error': str(e)[:50],
            'scrapable': 'NO'
        }
        print(f"     ❌ Error: {str(e)[:60]}")
    
    results.append(result)
    
    # Track by category
    if category not in categories_stats:
        categories_stats[category] = {'total': 0, 'scrapable': 0}
    categories_stats[category]['total'] += 1
    if result.get('scrapable') == 'YES':
        categories_stats[category]['scrapable'] += 1
    
    time.sleep(0.5)  # Be polite
    print()

# Summary
print("\n" + "=" * 100)
print("OVERALL SUMMARY")
print("=" * 100)

total = len(results)
scrapable = len([r for r in results if r.get('scrapable') == 'YES'])
needs_selenium = len([r for r in results if r.get('scrapable') == 'SELENIUM'])
maybe = len([r for r in results if r.get('scrapable') == 'MAYBE'])
failed = len([r for r in results if r.get('scrapable') == 'NO'])

print(f"\nTotal Firms Tested: {total}")
print(f"✅ Easily Scrapable: {scrapable} ({scrapable*100//total}%)")
print(f"⚠️  Needs Selenium: {needs_selenium} ({needs_selenium*100//total}%)")
print(f"🔍 Maybe Scrapable: {maybe} ({maybe*100//total}%)")
print(f"❌ Not Scrapable: {failed} ({failed*100//total}%)")

print(f"\n{'='*100}")
print("BY CATEGORY")
print("=" * 100)
for cat, stats in sorted(categories_stats.items()):
    pct = int(stats['scrapable'] * 100 / stats['total']) if stats['total'] > 0 else 0
    print(f"{cat:20s}: {stats['scrapable']:2d}/{stats['total']:2d} scrapable ({pct:3d}%)")

# ATS breakdown
ats_count = {}
for r in results:
    if 'ats' in r:
        ats = r['ats']
        ats_count[ats] = ats_count.get(ats, 0) + 1

print(f"\n{'='*100}")
print("ATS SYSTEMS DETECTED")
print("=" * 100)
for ats, count in sorted(ats_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{ats:20s}: {count} firms")

# Top scrapable firms
print(f"\n{'='*100}")
print("✅ EASILY SCRAPABLE FIRMS (Top 20)")
print("=" * 100)
scrapable_firms = [r for r in results if r.get('scrapable') == 'YES']
for i, r in enumerate(scrapable_firms[:20], 1):
    print(f"{i:2d}. {r['name']:40s} ({r.get('ats', 'Custom')})")

if len(scrapable_firms) > 20:
    print(f"... and {len(scrapable_firms) - 20} more")

# Save results to CSV
with open('scraping_test_results.csv', 'w', newline='') as f:
    if results:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print(f"\n{'='*100}")
print("RECOMMENDATION")
print("=" * 100)

if scrapable >= 30:
    print("✅ EXCELLENT: 30+ firms easily scrapable")
    print("   Definitely worth building a custom scraper!")
elif scrapable >= 15:
    print("✅ GOOD: 15+ firms easily scrapable")
    print("   Worth building for targeted quant/hedge fund search")
elif scrapable >= 5:
    print("⚠️  MODERATE: 5-15 firms scrapable")
    print("   Could be useful for specific firms, limited coverage")
else:
    print("❌ DIFFICULT: Most firms have complex systems")
    print("   Better to use LinkedIn/Indeed with company filters")

print("\nResults saved to: scraping_test_results.csv")
print("=" * 100)

