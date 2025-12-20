"""
Advanced Job Matching Engine with NLP
Filters jobs based on relevance to search terms using keyword matching and fuzzy matching
"""

import re
from difflib import SequenceMatcher
from typing import List, Dict, Any

class JobMatcher:
    """Smart job matcher using NLP techniques"""
    
    def __init__(self):
        # Exclusion keywords - filter out these types of postings
        self.exclusion_keywords = [
            'w2', 'c2c', 'c2h', 'corp to corp', 'corp-to-corp',
            '1099', 'contract to hire', 'w-2', 'w 2',
            'third party', '3rd party', 'vendor', 'staffing',
            'no c2c', 'no w2', 'visa sponsor', 'h1b',
            'bench sales', 'recruiter', 'please share resume'
        ]
        
        # Common tech keywords and their variations
        self.tech_keywords = {
            'java': ['java', 'jdk', 'jvm', 'spring', 'hibernate', 'maven', 'gradle'],
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'pytorch'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'typescript'],
            'data': ['data scientist', 'data analyst', 'data engineer', 'analytics', 'ml', 'machine learning'],
            'software': ['software engineer', 'software developer', 'swe', 'backend', 'frontend', 'full stack'],
            'devops': ['devops', 'sre', 'site reliability', 'kubernetes', 'docker', 'aws', 'cloud'],
            'network': ['network engineer', 'network admin', 'cisco', 'routing', 'switching'],
            'security': ['security', 'cybersecurity', 'infosec', 'penetration', 'ethical hacking'],
        }
        
    def extract_keywords(self, text: str) -> set:
        """Extract important keywords from text"""
        if not text:
            return set()
        
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
        words = text.split()
        
        # Include bigrams (two-word phrases)
        keywords = set(words)
        for i in range(len(words) - 1):
            keywords.add(f"{words[i]} {words[i+1]}")
        
        return keywords
    
    def calculate_relevance(self, job_title: str, search_term: str, job_description: str = "") -> float:
        """Calculate relevance score between job and search term"""
        if not job_title or not search_term:
            return 0.0
        
        job_title = job_title.lower()
        search_term = search_term.lower()
        
        # Direct match in title - highest score
        if search_term in job_title:
            return 1.0
        
        # Extract keywords
        job_keywords = self.extract_keywords(job_title)
        search_keywords = self.extract_keywords(search_term)
        
        # Check for keyword overlap
        overlap = job_keywords.intersection(search_keywords)
        if overlap:
            return 0.9
        
        # Check for related tech keywords
        for key, variations in self.tech_keywords.items():
            search_has_key = any(v in search_term for v in variations)
            job_has_key = any(v in job_title for v in variations)
            if search_has_key and job_has_key:
                return 0.8
        
        # Fuzzy matching for similar words
        job_words = job_title.split()
        search_words = search_term.split()
        
        max_similarity = 0.0
        for jw in job_words:
            for sw in search_words:
                if len(jw) > 3 and len(sw) > 3:  # Only compare meaningful words
                    similarity = SequenceMatcher(None, jw, sw).ratio()
                    max_similarity = max(max_similarity, similarity)
        
        if max_similarity > 0.8:
            return 0.7
        
        # Check description if available (lower weight)
        if job_description:
            desc_lower = job_description.lower()
            if search_term in desc_lower:
                return 0.5
        
        return 0.0
    
    def contains_exclusion_keywords(self, text: str) -> bool:
        """Check if text contains any exclusion keywords"""
        if not text:
            return False
        
        text_lower = text.lower()
        for keyword in self.exclusion_keywords:
            if keyword in text_lower:
                return True
        return False
    
    def is_internship_position(self, title: str, description: str = "") -> bool:
        """Check if job is an internship based on title and description"""
        if not title:
            return False
        
        title_lower = title.lower()
        desc_lower = description.lower() if description else ""
        
        # Internship keywords
        internship_keywords = ['intern', 'internship', 'co-op', 'coop', 'student']
        
        # Check if any internship keyword is in title or description
        for keyword in internship_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return True
        
        return False
    
    def is_senior_position(self, title: str) -> bool:
        """Check if job is a senior/experienced position based on title"""
        if not title:
            return False
        
        title_lower = title.lower()
        
        # Senior level keywords that indicate NOT entry-level
        senior_keywords = ['senior', 'sr.', 'lead', 'principal', 'staff', 'architect', 
                          'director', 'manager', 'head of', 'chief', 'vp', 'vice president']
        
        for keyword in senior_keywords:
            if keyword in title_lower:
                return True
        
        return False
    
    def filter_jobs(self, jobs: List[Dict[str, Any]], search_term: str, threshold: float = 0.5, job_type_filter: str = None) -> List[Dict[str, Any]]:
        """Filter jobs based on relevance to search term and job type"""
        filtered_jobs = []
        
        for job in jobs:
            title = job.get('title', '')
            description = job.get('description', '')
            company = job.get('company', '')
            
            # First check: Exclude jobs with unwanted keywords
            combined_text = f"{title} {description} {company}"
            if self.contains_exclusion_keywords(combined_text):
                continue  # Skip this job
            
            # Second check: Job type filtering (if specified)
            if job_type_filter:
                is_internship = self.is_internship_position(title, description)
                is_senior = self.is_senior_position(title)
                
                if job_type_filter == 'internship':
                    # For internship filter: MUST be internship, NO senior positions
                    if not is_internship or is_senior:
                        continue
                elif job_type_filter == 'fulltime':
                    # For full-time filter: NO internships, NO senior positions (unless explicitly searching for senior)
                    if is_internship:
                        continue
                    # Allow senior positions only if search term contains senior keywords
                    if is_senior and 'senior' not in search_term.lower() and 'sr' not in search_term.lower():
                        continue
            
            # Third check: Calculate relevance
            relevance = self.calculate_relevance(title, search_term, description)
            
            if relevance >= threshold:
                job['relevance_score'] = relevance
                filtered_jobs.append(job)
        
        # Sort by relevance score (highest first)
        filtered_jobs.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return filtered_jobs
    
    def map_experience_level(self, years_range: str) -> List[str]:
        """Map years of experience to LinkedIn levels"""
        mapping = {
            'internship': ['internship'],
            '1-3': ['entry_level', 'associate'],
            '3-5': ['associate', 'mid_senior_level'],
            '5-7': ['mid_senior_level'],
            '7+': ['mid_senior_level', 'director', 'executive']
        }
        return mapping.get(years_range, [])
    
    def extract_years_from_description(self, description: str) -> int:
        """Extract required years of experience from job description"""
        if not description:
            return 0
        
        # Patterns to match years of experience
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
            r'experience:\s*(\d+)\+?\s*(?:years?|yrs?)',
            r'minimum\s*(?:of\s*)?(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, description.lower())
            years.extend([int(m) for m in matches])
        
        return max(years) if years else 0
    
    def filter_by_experience(self, jobs: List[Dict[str, Any]], experience_levels: List[str]) -> List[Dict[str, Any]]:
        """Filter jobs by experience level"""
        if not experience_levels:
            return jobs
        
        # Map experience ranges to LinkedIn levels
        linkedin_levels = []
        for exp in experience_levels:
            linkedin_levels.extend(self.map_experience_level(exp))
        
        linkedin_levels = list(set(linkedin_levels))
        
        filtered = []
        for job in jobs:
            job_level = job.get('job_level', '').lower()
            
            # Check if job level matches
            if any(level in job_level for level in linkedin_levels):
                filtered.append(job)
                continue
            
            # Check experience from description
            description = job.get('description', '')
            required_years = self.extract_years_from_description(description)
            
            if required_years == 0:
                # No experience specified, include it
                filtered.append(job)
            else:
                # Check if it matches the experience range
                for exp in experience_levels:
                    if exp == 'internship' and required_years == 0:
                        filtered.append(job)
                        break
                    elif exp == '1-3' and 1 <= required_years <= 3:
                        filtered.append(job)
                        break
                    elif exp == '3-5' and 3 <= required_years <= 5:
                        filtered.append(job)
                        break
                    elif exp == '5-7' and 5 <= required_years <= 7:
                        filtered.append(job)
                        break
                    elif exp == '7+' and required_years >= 7:
                        filtered.append(job)
                        break
        
        return filtered

    def get_exclusion_keywords(self) -> List[str]:
        """Return list of exclusion keywords for reference"""
        return self.exclusion_keywords.copy()
