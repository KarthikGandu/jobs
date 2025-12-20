# Test Suite

This directory contains all tests for the Job Search Application.

## Running Tests

### Run All Tests
```bash
python tests/test_application.py
```

### Individual Test Files
```bash
# Application tests
python tests/test_application.py

# Original tests (archived)
python tests/test_app.py
python tests/test_sites.py
python tests/test_quant_firms.py
```

## Test Structure

- `test_application.py` - Main test suite for refactored application
- `test_app.py` - Original application tests
- `test_sites.py` - Job site scraping tests
- `test_quant_firms.py` - Quantitative firms scraping tests
- `analyze_failures.py` - Failure analysis utility

## Test Coverage

The main test suite (`test_application.py`) covers:

1. **Import Tests** - All modules import correctly
2. **App Creation** - Application factory works
3. **Blueprint Tests** - Blueprints registered properly
4. **Route Tests** - All endpoints exist
5. **Validation Tests** - Input validation works
6. **Error Handler Tests** - Error handling works
7. **Configuration Tests** - Config management works

## Expected Output

```
============================================================
JOB SEARCH APPLICATION TEST SUITE
============================================================

Testing imports...
✓ Application factory imports successfully
✓ Configuration modules import successfully
✓ Route blueprints import successfully
✓ Utility functions import successfully
✓ Service modules import successfully

Testing app creation...
✓ Development app created: job_search_app
  - Debug mode: True
  - Testing mode: False
✓ Production app created: job_search_app
  - Debug mode: False

Testing blueprints...
✓ Registered blueprints: ['main', 'api']
  ✓ Main blueprint registered
  ✓ API blueprint registered

Testing routes...
✓ Total routes registered: 10
  ✓ GET /
  ✓ GET /health
  ✓ POST /api/search
  ✓ GET /api/companies

Testing input validation...
✓ Valid parameters accepted
  - Search term: Python Developer
  - Location: San Francisco
✓ Invalid parameters rejected: location is required

Testing error handlers...
✓ ValidationError: status=400, message=Test validation error
✓ ScrapingError: status=503, message=Test scraping error
✓ Error dict conversion: {'status': 'error', 'error': 'Test scraping error'}

Testing configuration...
✓ Development config loaded
  - Debug: True
  - Log level: DEBUG
✓ Production config loaded
  - Debug: False
  - Session cookie secure: True

============================================================
TEST SUMMARY
============================================================
✓ PASS - Imports
✓ PASS - App Creation
✓ PASS - Blueprints
✓ PASS - Routes
✓ PASS - Validation
✓ PASS - Error Handlers
✓ PASS - Configuration

Results: 7/7 tests passed

🎉 All tests passed! Application is ready.
```

## Adding New Tests

To add new tests, create a new test file following this pattern:

```python
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_your_feature():
    """Test description"""
    from job_search_app import your_module
    
    # Test implementation
    assert condition, "Error message"
    return True

if __name__ == '__main__':
    result = test_your_feature()
    sys.exit(0 if result else 1)
```

## CI/CD Integration

Tests are automatically run in the CI/CD pipeline on every push:

- See `.github/workflows/ci.yml` for configuration
- Tests must pass before deployment
- Coverage reports are generated automatically
