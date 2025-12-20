"""
Smart Keyword Expansion for Job Searches
Automatically expands search terms to include related variations and derivatives
"""

from typing import List, Set

class KeywordExpander:
    """Expands job search keywords to include related terms"""
    
    def __init__(self):
        # Keyword expansion mappings
        self.expansions = {
            'software engineer': [
                'Software Engineer',
                'Software Developer',
                'Backend Engineer',
                'Full Stack Engineer',
                'Frontend Engineer',
                'Application Developer',
                'Backend Software Developer',
                'Full Stack Software Engineer',
            ],
            'backend engineer': [
                'Backend Engineer',
                'Backend Developer',
                'Backend Software Engineer',
                'Server Side Engineer',
                'API Engineer',
            ],
            'frontend engineer': [
                'Frontend Engineer',
                'Frontend Developer',
                'UI Engineer',
                'Web Developer',
                'React Developer',
                'Vue Developer',
                'Angular Developer',
            ],
            'full stack engineer': [
                'Full Stack Engineer',
                'Full Stack Developer',
                'Full-Stack Engineer',
                'Fullstack Engineer',
            ],
            'data scientist': [
                'Data Scientist',
                'Machine Learning Engineer',
                'ML Engineer',
                'Applied Scientist',
                'Research Scientist',
            ],
            'data analyst': [
                'Data Analyst',
                'Business Analyst',
                'Analytics Engineer',
                'Business Intelligence Analyst',
                'BI Analyst',
            ],
            'data engineer': [
                'Data Engineer',
                'ETL Engineer',
                'Data Platform Engineer',
                'Big Data Engineer',
                'Pipeline Engineer',
            ],
            'devops engineer': [
                'DevOps Engineer',
                'Site Reliability Engineer',
                'SRE',
                'Cloud Engineer',
                'Infrastructure Engineer',
                'Platform Engineer',
            ],
            'network engineer': [
                'Network Engineer',
                'Network Administrator',
                'Network Architect',
                'Systems Engineer',
            ],
            'security engineer': [
                'Security Engineer',
                'Cybersecurity Engineer',
                'Information Security Engineer',
                'AppSec Engineer',
                'Security Analyst',
            ],
            'python developer': [
                'Python Developer',
                'Python Engineer',
                'Python Software Engineer',
                'Django Developer',
                'Flask Developer',
            ],
            'java developer': [
                'Java Developer',
                'Java Engineer',
                'Java Software Engineer',
                'Spring Boot Developer',
                'J2EE Developer',
            ],
            'javascript developer': [
                'JavaScript Developer',
                'JS Developer',
                'Node.js Developer',
                'React Developer',
                'Vue.js Developer',
                'Angular Developer',
            ],
            'mobile developer': [
                'Mobile Developer',
                'iOS Developer',
                'Android Developer',
                'React Native Developer',
                'Flutter Developer',
            ],
            'qa engineer': [
                'QA Engineer',
                'Quality Assurance Engineer',
                'Test Engineer',
                'SDET',
                'Automation Engineer',
            ],
            'product manager': [
                'Product Manager',
                'Technical Product Manager',
                'Senior Product Manager',
                'Associate Product Manager',
            ],
            'quant trader': [
                'Quant Trader',
                'Quantitative Trader',
                'Algorithmic Trader',
                'Trading Analyst',
                'Quantitative Analyst',
                'Trader',
                'Trading Associate',
            ],
            'quantitative analyst': [
                'Quantitative Analyst',
                'Quant Analyst',
                'Quantitative Researcher',
                'Quantitative Associate',
                'Risk Analyst',
            ],
            'investment banker': [
                'Investment Banker',
                'Investment Banking Analyst',
                'Investment Banking Associate',
                'IB Analyst',
                'Banking Analyst',
            ],
            'financial analyst': [
                'Financial Analyst',
                'Finance Analyst',
                'Investment Analyst',
                'Equity Analyst',
                'Research Analyst',
            ],
            'accountant': [
                'Accountant',
                'Staff Accountant',
                'Senior Accountant',
                'Accounting Associate',
            ],
            'marketing manager': [
                'Marketing Manager',
                'Digital Marketing Manager',
                'Marketing Lead',
                'Growth Marketing Manager',
            ],
            'sales engineer': [
                'Sales Engineer',
                'Solutions Engineer',
                'Presales Engineer',
                'Technical Sales Engineer',
            ],
        }
        
        # Tech stack specific expansions
        self.tech_expansions = {
            'python': ['Python Developer', 'Python Engineer', 'Django Developer', 'Flask Developer'],
            'java': ['Java Developer', 'Java Engineer', 'Spring Boot Developer'],
            'javascript': ['JavaScript Developer', 'Node.js Developer', 'React Developer', 'Vue Developer'],
            'c++': ['C++ Engineer', 'C++ Developer', 'C++ Software Engineer'],
            'go': ['Go Developer', 'Golang Engineer', 'Go Backend Engineer'],
            'rust': ['Rust Developer', 'Rust Engineer'],
            'react': ['React Developer', 'React Engineer', 'Frontend React Developer'],
            'node': ['Node.js Developer', 'Node Developer', 'Backend Node Engineer'],
        }
    
    def normalize_keyword(self, keyword: str) -> str:
        """Normalize keyword for matching"""
        return keyword.lower().strip()
    
    def generate_smart_variations(self, keyword: str) -> List[str]:
        """Generate intelligent variations for ANY job title"""
        variations = []
        original = keyword.strip()
        
        # Common job title patterns
        title_words = original.split()
        
        # Pattern 1: Role variations (Engineer, Developer, Specialist, etc.)
        role_variants = {
            'engineer': ['Engineer', 'Developer', 'Specialist', 'Architect'],
            'developer': ['Developer', 'Engineer', 'Programmer', 'Specialist'],
            'analyst': ['Analyst', 'Specialist', 'Consultant', 'Associate'],
            'manager': ['Manager', 'Lead', 'Director', 'Head'],
            'scientist': ['Scientist', 'Researcher', 'Analyst', 'Engineer'],
            'trader': ['Trader', 'Associate', 'Analyst', 'Specialist'],
            'consultant': ['Consultant', 'Analyst', 'Advisor', 'Specialist'],
            'designer': ['Designer', 'Specialist', 'Lead', 'Creative'],
            'architect': ['Architect', 'Designer', 'Engineer', 'Lead'],
        }
        
        # Pattern 2: Level/Seniority variations
        levels = ['', 'Junior ', 'Senior ', 'Lead ', 'Staff ', 'Principal ']
        
        # Pattern 3: Area variations (Frontend, Backend, Full Stack, etc.)
        areas = ['', 'Frontend ', 'Backend ', 'Full Stack ', 'Full-Stack ']
        
        # Add original
        variations.append(original)
        
        # Generate variations based on role type
        last_word = title_words[-1].lower() if title_words else ''
        
        if last_word in role_variants:
            # Generate role variations
            base = ' '.join(title_words[:-1]) if len(title_words) > 1 else ''
            for variant in role_variants[last_word]:
                if base:
                    variations.append(f"{base} {variant}".strip())
                else:
                    variations.append(variant)
        
        # Check if it's a tech/domain specific role
        if any(word in original.lower() for word in ['software', 'data', 'machine learning', 'ml', 'ai']):
            # Add common variations
            if 'engineer' in original.lower():
                variations.append(original.replace('Engineer', 'Developer'))
                variations.append(original.replace('engineer', 'developer'))
            if 'developer' in original.lower():
                variations.append(original.replace('Developer', 'Engineer'))
                variations.append(original.replace('developer', 'engineer'))
        
        # Pattern matching for common structures
        if 'engineer' in original.lower() or 'developer' in original.lower():
            # Add area variations
            for area in ['Backend', 'Frontend', 'Full Stack']:
                if area.lower() not in original.lower():
                    variations.append(f"{area} {original}")
        
        # Remove duplicates (case-insensitive)
        seen = set()
        unique_variations = []
        for var in variations:
            var_lower = var.lower()
            if var_lower not in seen:
                seen.add(var_lower)
                unique_variations.append(var)
        
        return unique_variations[:8]  # Return top 8 variations
    
    def expand_keyword(self, keyword: str, max_expansions: int = 8) -> List[str]:
        """Expand a single keyword to related terms"""
        normalized = self.normalize_keyword(keyword)
        
        # Check direct expansions first (predefined)
        if normalized in self.expansions:
            return self.expansions[normalized][:max_expansions]
        
        # Check tech stack expansions
        for tech, expansions in self.tech_expansions.items():
            if tech in normalized:
                return expansions[:max_expansions]
        
        # Check if keyword contains a known pattern
        for key in self.expansions.keys():
            if key in normalized or normalized in key:
                return self.expansions[key][:max_expansions]
        
        # Use smart generation for ANY job title
        return self.generate_smart_variations(keyword)[:max_expansions]
    
    def expand_keywords(self, keywords: List[str], max_total: int = 10) -> List[str]:
        """Expand multiple keywords intelligently"""
        expanded = set()
        
        for keyword in keywords:
            # Add original keyword
            expanded.add(keyword)
            
            # Add expansions
            expansions = self.expand_keyword(keyword)
            for exp in expansions:
                if len(expanded) < max_total:
                    expanded.add(exp)
        
        return list(expanded)
    
    def get_suggested_keywords(self, keyword: str) -> List[str]:
        """Get suggested related keywords for UI display"""
        normalized = self.normalize_keyword(keyword)
        
        suggestions = []
        
        # Get direct expansions
        if normalized in self.expansions:
            suggestions.extend(self.expansions[normalized])
        
        # Check partial matches
        for key, values in self.expansions.items():
            if key in normalized or normalized in key:
                suggestions.extend(values)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for item in suggestions:
            if item.lower() not in seen and item.lower() != normalized:
                seen.add(item.lower())
                unique_suggestions.append(item)
        
        return unique_suggestions[:8]  # Return top 8 suggestions
