"""
Input validation utilities
"""
from typing import Dict, Any, List
from .errors import ValidationError


def validate_job_search_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize job search parameters
    
    Args:
        params: Dictionary of search parameters
        
    Returns:
        Validated and sanitized parameters
        
    Raises:
        ValidationError: If validation fails
    """
    validated = {}
    
    # Required fields
    if not params.get('search_term'):
        raise ValidationError("search_term is required")
    validated['search_term'] = str(params['search_term']).strip()
    
    if not params.get('location'):
        raise ValidationError("location is required")
    validated['location'] = str(params['location']).strip()
    
    # Optional fields with defaults
    validated['site_name'] = params.get('site_name', ['linkedin'])
    if isinstance(validated['site_name'], str):
        validated['site_name'] = [validated['site_name']]
    
    # Validate site names
    valid_sites = ['linkedin', 'indeed', 'glassdoor', 'google', 'ziprecruiter']
    for site in validated['site_name']:
        if site not in valid_sites:
            raise ValidationError(f"Invalid site: {site}. Must be one of {valid_sites}")
    
    # Numeric validations
    try:
        validated['results_wanted'] = int(params.get('results_wanted', 15))
        if validated['results_wanted'] < 1 or validated['results_wanted'] > 100:
            raise ValidationError("results_wanted must be between 1 and 100")
    except (ValueError, TypeError):
        raise ValidationError("results_wanted must be a valid integer")
    
    try:
        validated['distance'] = int(params.get('distance', 50))
        if validated['distance'] < 0:
            raise ValidationError("distance must be non-negative")
    except (ValueError, TypeError):
        raise ValidationError("distance must be a valid integer")
    
    # Optional fields
    validated['job_type'] = params.get('job_type')
    validated['is_remote'] = params.get('is_remote', False)
    validated['country_indeed'] = params.get('country_indeed', 'usa')
    validated['hours_old'] = params.get('hours_old')
    
    # Boolean conversions
    if isinstance(validated['is_remote'], str):
        validated['is_remote'] = validated['is_remote'].lower() in ('true', '1', 'yes')
    
    return validated


def validate_keyword_expansion(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate keyword expansion parameters
    
    Args:
        params: Dictionary with keyword and optional parameters
        
    Returns:
        Validated parameters
        
    Raises:
        ValidationError: If validation fails
    """
    validated = {}
    
    if not params.get('keyword'):
        raise ValidationError("keyword is required")
    validated['keyword'] = str(params['keyword']).strip()
    
    validated['include_related'] = params.get('include_related', True)
    if isinstance(validated['include_related'], str):
        validated['include_related'] = validated['include_related'].lower() in ('true', '1', 'yes')
    
    return validated


def validate_company_search(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate company search parameters
    
    Args:
        params: Dictionary with company search parameters
        
    Returns:
        Validated parameters
        
    Raises:
        ValidationError: If validation fails
    """
    validated = {}
    
    if not params.get('company'):
        raise ValidationError("company is required")
    validated['company'] = str(params['company']).strip()
    
    validated['search_term'] = params.get('search_term', '')
    if validated['search_term']:
        validated['search_term'] = str(validated['search_term']).strip()
    
    try:
        validated['results_wanted'] = int(params.get('results_wanted', 15))
        if validated['results_wanted'] < 1 or validated['results_wanted'] > 100:
            raise ValidationError("results_wanted must be between 1 and 100")
    except (ValueError, TypeError):
        raise ValidationError("results_wanted must be a valid integer")
    
    return validated
