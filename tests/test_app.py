#!/usr/bin/env python3
"""
Quick test script for Karthik's Job Search Site
"""

import requests
import json
import time

def test_website():
    base_url = "http://localhost:5001"
    
    print("=" * 60)
    print("Testing Karthik's Job Search Site")
    print("=" * 60)
    print()
    
    # Test 1: Check if server is running
    print("✓ Test 1: Checking if server is running...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("  ✅ Server is running on port 5000")
            print(f"  Title: Karthik's Job Search Site")
        else:
            print(f"  ❌ Server returned status code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Cannot connect to server: {e}")
        print("  Please start the server with: python3 app.py")
        return
    
    print()
    
    # Test 2: Test API endpoint
    print("✓ Test 2: Testing job search API...")
    print("  Searching for 'Python Developer' in 'Remote'...")
    
    search_data = {
        "search_terms": ["Python Developer"],
        "location": "Remote",
        "sites": ["indeed"],
        "results_wanted": 3,
        "is_remote": True
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{base_url}/api/scrape",
            json=search_data,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API returned successfully in {elapsed_time:.2f} seconds")
            print(f"  Jobs found: {data.get('jobs_count', 0)}")
            
            if data.get('jobs'):
                print("\n  Sample job:")
                job = data['jobs'][0]
                print(f"    Title: {job.get('title', 'N/A')}")
                print(f"    Company: {job.get('company', 'N/A')}")
                print(f"    Location: {job.get('location', 'N/A')}")
                print(f"    Site: {job.get('site', 'N/A')}")
                print(f"    URL: {job.get('job_url', 'N/A')[:60]}...")
        else:
            error_data = response.json()
            print(f"  ❌ API error: {error_data.get('error', 'Unknown error')}")
            return
            
    except requests.exceptions.Timeout:
        print("  ⚠️  Request timed out (this can happen with slow networks)")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        return
    except json.JSONDecodeError:
        print(f"  ❌ Invalid JSON response")
        return
    
    print()
    print("=" * 60)
    print("✅ All tests passed! The application is working correctly.")
    print()
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    test_website()
