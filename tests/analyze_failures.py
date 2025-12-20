"""Analyze why specific firms failed scraping"""
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
}

# Test some failed firms to understand why
failed_firms = [
    ("Tower Research", "https://www.tower-research.com/join-us"),
    ("UBS", "https://www.ubs.com/global/en/careers.html"),
    ("Credit Suisse", "https://www.credit-suisse.com/careers"),
    ("Qube Research", "https://www.qube-rt.com/careers"),
    ("Morgan Stanley", "https://www.morganstanley.com/people-opportunities/careers"),
    ("PIMCO", "https://www.pimco.com/en-us/careers"),
]

print("=" * 80)
print("DETAILED FAILURE ANALYSIS")
print("=" * 80)
print()

for name, url in failed_firms:
    print(f"Analyzing: {name}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        if response.status_code == 403:
            print("❌ REASON: 403 FORBIDDEN")
            print("   Explanation: Anti-bot protection (Cloudflare/similar)")
            print("   Detection: Recognized our script as non-browser")
            if 'cloudflare' in response.text.lower():
                print("   Protection: Cloudflare detected")
            if 'captcha' in response.text.lower():
                print("   Protection: CAPTCHA required")
                
        elif response.status_code == 404:
            print("❌ REASON: 404 NOT FOUND")
            print("   Explanation: Page doesn't exist or moved")
            print("   Solution: Need to find correct career page URL")
            
        elif response.status_code == 301 or response.status_code == 302:
            print("⚠️  REASON: REDIRECT")
            print(f"   Redirected to: {response.url}")
            
        elif response.status_code == 200:
            # Check content
            content = response.text.lower()
            
            if len(content) < 1000:
                print("⚠️  REASON: MINIMAL CONTENT")
                print(f"   Page size: {len(content)} bytes (too small)")
                
            if 'workday' in content or 'myworkdayjobs' in content:
                print("⚠️  REASON: WORKDAY REDIRECT")
                print("   Requires: External Workday system (different domain)")
                print("   Solution: Need to follow to workdayjobs.com subdomain")
                
            if 'taleo' in content:
                print("⚠️  REASON: TALEO SYSTEM")
                print("   Requires: Oracle Taleo login/complex navigation")
                
            if 'javascript' in content[:2000]:
                print("⚠️  REASON: JAVASCRIPT REQUIRED")
                print("   Content loaded via JavaScript (not in HTML)")
                
            if 'login' in content[:3000] or 'sign in' in content[:3000]:
                print("⚠️  REASON: LOGIN REQUIRED")
                print("   Page requires authentication")
                
    except requests.exceptions.Timeout:
        print("❌ REASON: TIMEOUT")
        print("   Explanation: Server took >10 seconds to respond")
        print("   Possible: Rate limiting or slow server")
        
    except requests.exceptions.ConnectionError:
        print("❌ REASON: CONNECTION ERROR")
        print("   Explanation: Can't connect to server")
        print("   Possible: DNS issue, server down, or blocking")
        
    except Exception as e:
        print(f"❌ REASON: {type(e).__name__}")
        print(f"   Error: {str(e)[:100]}")
    
    print()
    print("-" * 80)
    print()

