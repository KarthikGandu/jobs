"""
AI Job Matcher - Calculate match scores between resume and job descriptions
"""
from typing import Dict, List, Optional
import re
from collections import Counter
import math


class JobMatcher:
    """Match jobs to user resume using AI algorithms"""
    
    def __init__(self):
        self.common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def normalize_text(self, text: str) -> List[str]:
        """Normalize and tokenize text"""
        if not text:
            return []
        
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common words and short words
        words = [w for w in words if w not in self.common_words and len(w) > 2]
        
        return words
    
    def calculate_skill_match(self, resume_skills: List[str], job_description: str) -> Dict:
        """Calculate skill matching score"""
        if not resume_skills or not job_description:
            return {'score': 0, 'matched': [], 'missing': []}
        
        job_text_lower = job_description.lower()
        
        matched_skills = []
        for skill in resume_skills:
            # Check if skill appears in job description
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', job_text_lower):
                matched_skills.append(skill)
        
        # Calculate score (percentage of resume skills found in job)
        score = (len(matched_skills) / len(resume_skills)) * 100 if resume_skills else 0
        
        return {
            'score': score,
            'matched': matched_skills,
            'total_resume_skills': len(resume_skills)
        }
    
    def calculate_experience_match(self, user_experience: Optional[int], job_description: str) -> float:
        """Calculate experience matching score"""
        if not job_description:
            return 50
        
        # Extract required years from job description
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'minimum\s+(\d+)\s+years?',
            r'at least\s+(\d+)\s+years?',
        ]
        
        required_years = []
        for pattern in patterns:
            matches = re.findall(pattern, job_description.lower())
            required_years.extend([int(m) for m in matches])
        
        if not required_years:
            return 75
        
        required = max(required_years)
        
        if user_experience is None:
            return 50
        
        if user_experience >= required:
            return 100
        elif user_experience >= required * 0.75:
            return 80
        elif user_experience >= required * 0.5:
            return 60
        else:
            return 40
    
    def calculate_education_match(self, user_degree: Optional[str], job_description: str) -> float:
        """Calculate education matching score"""
        if not job_description:
            return 70
        
        job_lower = job_description.lower()
        
        degree_hierarchy = {
            'phd': 5, 'doctorate': 5,
            'master': 4, 'mba': 4, 'ms': 4, 'ma': 4,
            'bachelor': 3, 'bs': 3, 'ba': 3,
            'associate': 2
        }
        
        degree_required = any(deg in job_lower for deg in ['degree', 'bachelor', 'master', 'phd'])
        
        if not degree_required:
            return 80
        
        if not user_degree:
            return 40
        
        user_level = degree_hierarchy.get(user_degree.lower(), 0)
        
        required_level = 0
        for deg, level in degree_hierarchy.items():
            if deg in job_lower:
                required_level = max(required_level, level)
        
        if required_level == 0:
            return 70
        
        if user_level >= required_level:
            return 100
        elif user_level == required_level - 1:
            return 70
        else:
            return 50
    
    def calculate_keyword_match(self, resume_text: str, job_description: str) -> float:
        """Calculate keyword overlap using TF-IDF-like approach"""
        if not resume_text or not job_description:
            return 0
        
        resume_words = self.normalize_text(resume_text)
        job_words = self.normalize_text(job_description)
        
        if not resume_words or not job_words:
            return 0
        
        resume_counter = Counter(resume_words)
        job_counter = Counter(job_words)
        
        common_words = set(resume_counter.keys()) & set(job_counter.keys())
        
        if not common_words:
            return 0
        
        dot_product = sum(resume_counter[word] * job_counter[word] for word in common_words)
        resume_magnitude = math.sqrt(sum(count ** 2 for count in resume_counter.values()))
        job_magnitude = math.sqrt(sum(count ** 2 for count in job_counter.values()))
        
        if resume_magnitude == 0 or job_magnitude == 0:
            return 0
        
        similarity = dot_product / (resume_magnitude * job_magnitude)
        return similarity * 100
    
    def calculate_overall_match(
        self,
        resume_data: Dict,
        job_description: str,
        job_title: str = ""
    ) -> Dict:
        """
        Calculate overall match score
        
        Args:
            resume_data: Dict with skills, experience, education, raw_text
            job_description: Job description text
            job_title: Job title (optional)
        
        Returns:
            Dict with overall score and breakdown
        """
        # Weight for each component
        weights = {
            'skills': 0.40,
            'experience': 0.25,
            'education': 0.15,
            'keywords': 0.20
        }
        
        # Calculate individual scores
        skills_result = self.calculate_skill_match(
            resume_data.get('skills', []),
            job_description
        )
        
        experience_score = self.calculate_experience_match(
            resume_data.get('years_experience'),
            job_description
        )
        
        education_score = self.calculate_education_match(
            resume_data.get('highest_degree'),
            job_description
        )
        
        keyword_score = self.calculate_keyword_match(
            resume_data.get('raw_text', ''),
            job_description
        )
        
        # Calculate weighted overall score
        overall_score = (
            skills_result['score'] * weights['skills'] +
            experience_score * weights['experience'] +
            education_score * weights['education'] +
            keyword_score * weights['keywords']
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'skills_score': round(skills_result['score'], 1),
            'experience_score': round(experience_score, 1),
            'education_score': round(education_score, 1),
            'keywords_score': round(keyword_score, 1),
            'matched_skills': skills_result['matched'],
            'total_resume_skills': skills_result['total_resume_skills']
        }
