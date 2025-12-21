"""
Resume Parser - Extract information from PDF/DOCX resumes
"""
import re
from pathlib import Path
import PyPDF2
import docx
from typing import Dict, List, Optional


class ResumeParser:
    """Parse resumes and extract skills, experience, education"""
    
    # Common skills to look for
    TECHNICAL_SKILLS = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
        'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
        'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
        'data science', 'analytics', 'tableau', 'power bi', 'excel',
        'agile', 'scrum', 'jira', 'rest api', 'graphql', 'microservices'
    }
    
    DEGREES = ['phd', 'doctorate', 'master', 'mba', 'bachelor', 'associate', 'bs', 'ba', 'ms', 'ma']
    
    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
    
    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""
    
    def parse_file(self, file_path: str) -> str:
        """Parse resume file and extract text"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return self.parse_pdf(str(file_path))
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return self.parse_docx(str(file_path))
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.TECHNICAL_SKILLS:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def extract_years_experience(self, text: str) -> Optional[int]:
        """Extract years of experience"""
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+in'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        return max(years) if years else None
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        text_lower = text.lower()
        
        for degree in self.DEGREES:
            if degree in text_lower:
                # Try to find the university/college
                pattern = rf'{degree}[^\n]*(?:from|at)?\s+([A-Z][^\n,]+(?:University|College|Institute))'
                match = re.search(pattern, text, re.IGNORECASE)
                
                if match:
                    education.append({
                        'degree': degree.title(),
                        'institution': match.group(1).strip()
                    })
                else:
                    education.append({
                        'degree': degree.title(),
                        'institution': 'Unknown'
                    })
        
        return education
    
    def determine_highest_degree(self, education: List[Dict[str, str]]) -> Optional[str]:
        """Determine highest degree level"""
        degree_hierarchy = {
            'phd': 5, 'doctorate': 5,
            'master': 4, 'mba': 4, 'ms': 4, 'ma': 4,
            'bachelor': 3, 'bs': 3, 'ba': 3,
            'associate': 2
        }
        
        if not education:
            return None
        
        max_level = 0
        highest = None
        
        for edu in education:
            degree = edu['degree'].lower()
            level = degree_hierarchy.get(degree, 0)
            if level > max_level:
                max_level = level
                highest = edu['degree']
        
        return highest
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_patterns = [
            r'certified\s+([A-Z][^\n,]+)',
            r'certification[:\s]+([A-Z][^\n,]+)',
            r'(AWS|Azure|GCP)\s+([A-Z][^\n,]+)\s+Certified',
            r'(PMP|CISSP|CPA|CFA|Six Sigma)',
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                cert = match if isinstance(match, str) else ' '.join(match)
                certifications.append(cert.strip())
        
        return list(set(certifications))
    
    def parse_resume(self, file_path: str) -> Dict:
        """
        Parse resume and extract all information
        
        Returns:
            Dictionary with extracted information
        """
        # Extract text
        text = self.parse_file(file_path)
        
        if not text:
            raise ValueError("Could not extract text from resume")
        
        # Extract all information
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        years_experience = self.extract_years_experience(text)
        certifications = self.extract_certifications(text)
        highest_degree = self.determine_highest_degree(education)
        
        return {
            'raw_text': text,
            'skills': skills,
            'education': education,
            'years_experience': years_experience,
            'certifications': certifications,
            'highest_degree': highest_degree,
            'email': self.extract_email(text),
            'phone': self.extract_phone(text)
        }
