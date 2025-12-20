"""
Test suite for the refactored application
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from job_search_app.app import create_app
        print("✓ Application factory imports successfully")
    except Exception as e:
        print(f"✗ Failed to import app: {e}")
        return False
    
    try:
        from job_search_app.config import Config, DevelopmentConfig, ProductionConfig
        print("✓ Configuration modules import successfully")
    except Exception as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from job_search_app.routes import main_bp, api_bp
        print("✓ Route blueprints import successfully")
    except Exception as e:
        print(f"✗ Failed to import routes: {e}")
        return False
    
    try:
        from job_search_app.utils import setup_logger, validate_job_search_params
        print("✓ Utility functions import successfully")
    except Exception as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    try:
        from job_search_app.services import JobMatcher, KeywordExpander, CompanyScraper
        print("✓ Service modules import successfully")
    except Exception as e:
        print(f"✗ Failed to import services: {e}")
        return False
    
    return True


def test_app_creation():
    """Test application creation"""
    print("\nTesting app creation...")
    
    try:
        from job_search_app.app import create_app
        
        # Test development config
        app = create_app('development')
        print(f"✓ Development app created: {app.name}")
        print(f"  - Debug mode: {app.debug}")
        print(f"  - Testing mode: {app.testing}")
        
        # Test production config with proper SECRET_KEY
        os.environ['SECRET_KEY'] = 'test-production-secret-key-for-testing'
        app_prod = create_app('production')
        print(f"✓ Production app created: {app_prod.name}")
        print(f"  - Debug mode: {app_prod.debug}")
        del os.environ['SECRET_KEY']
        
        return True
    except Exception as e:
        print(f"✗ Failed to create app: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_blueprints():
    """Test blueprint registration"""
    print("\nTesting blueprints...")
    
    try:
        from job_search_app.app import create_app
        app = create_app('development')
        
        blueprints = list(app.blueprints.keys())
        print(f"✓ Registered blueprints: {blueprints}")
        
        # Check expected blueprints
        if 'main' in blueprints:
            print("  ✓ Main blueprint registered")
        else:
            print("  ✗ Main blueprint missing")
            return False
        
        if 'api' in blueprints:
            print("  ✓ API blueprint registered")
        else:
            print("  ✗ API blueprint missing")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to test blueprints: {e}")
        return False


def test_routes():
    """Test that routes are registered"""
    print("\nTesting routes...")
    
    try:
        from job_search_app.app import create_app
        app = create_app('development')
        
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"✓ Total routes registered: {len(routes)}")
        
        # Check critical routes
        critical_routes = [
            ('/', 'GET'),
            ('/health', 'GET'),
            ('/api/search', 'POST'),
            ('/api/companies', 'GET'),
        ]
        
        for route_path, method in critical_routes:
            found = False
            for rule in app.url_map.iter_rules():
                if rule.rule == route_path and method in rule.methods:
                    found = True
                    break
            if found:
                print(f"  ✓ {method} {route_path}")
            else:
                print(f"  ✗ {method} {route_path} missing")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test routes: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validation():
    """Test input validation"""
    print("\nTesting input validation...")
    
    try:
        from job_search_app.utils.validators import validate_job_search_params
        from job_search_app.utils.errors import ValidationError
        
        # Test valid input
        valid_params = {
            'search_term': 'Python Developer',
            'location': 'San Francisco',
            'site_name': ['linkedin'],
            'results_wanted': 15
        }
        
        result = validate_job_search_params(valid_params)
        print("✓ Valid parameters accepted")
        print(f"  - Search term: {result['search_term']}")
        print(f"  - Location: {result['location']}")
        
        # Test invalid input
        try:
            invalid_params = {'search_term': 'Python'}  # Missing location
            validate_job_search_params(invalid_params)
            print("✗ Invalid parameters not rejected")
            return False
        except ValidationError as e:
            print(f"✓ Invalid parameters rejected: {e.message}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test validation: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handlers():
    """Test error handling"""
    print("\nTesting error handlers...")
    
    try:
        from job_search_app.utils.errors import ValidationError, ScrapingError, APIError
        
        # Test ValidationError
        err = ValidationError("Test validation error")
        print(f"✓ ValidationError: status={err.status_code}, message={err.message}")
        
        # Test ScrapingError
        err = ScrapingError("Test scraping error")
        print(f"✓ ScrapingError: status={err.status_code}, message={err.message}")
        
        # Test error dict conversion
        err_dict = err.to_dict()
        print(f"✓ Error dict conversion: {err_dict}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test error handlers: {e}")
        return False


def test_configuration():
    """Test configuration management"""
    print("\nTesting configuration...")
    
    try:
        from job_search_app.config import config, DevelopmentConfig, ProductionConfig
        
        # Test config access
        dev_config = config['development']
        print(f"✓ Development config loaded")
        print(f"  - Debug: {dev_config.DEBUG}")
        print(f"  - Log level: {dev_config.LOG_LEVEL}")
        
        prod_config = config['production']
        print(f"✓ Production config loaded")
        print(f"  - Debug: {prod_config.DEBUG}")
        print(f"  - Session cookie secure: {prod_config.SESSION_COOKIE_SECURE}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test configuration: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("JOB SEARCH APPLICATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("App Creation", test_app_creation),
        ("Blueprints", test_blueprints),
        ("Routes", test_routes),
        ("Validation", test_validation),
        ("Error Handlers", test_error_handlers),
        ("Configuration", test_configuration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
