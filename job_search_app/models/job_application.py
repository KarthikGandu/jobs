"""
Job Application model for tracking applied jobs and match scores
"""
from datetime import datetime
from job_search_app.extensions import db


class JobApplication(db.Model):
    """Job application tracking model"""
    
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Job details
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    job_url = db.Column(db.String(500))
    job_description = db.Column(db.Text)
    
    # Match score
    match_percentage = db.Column(db.Float)
    skills_match = db.Column(db.Float)
    experience_match = db.Column(db.Float)
    education_match = db.Column(db.Float)
    keywords_match = db.Column(db.Float)
    
    # Match details
    matched_skills = db.Column(db.JSON)  # Skills that match
    missing_skills = db.Column(db.JSON)  # Skills required but missing
    
    # Status
    status = db.Column(db.String(50), default='saved')  # saved, applied, rejected, interview
    is_favorited = db.Column(db.Boolean, default=False)
    
    # Timestamps
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    applied_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert job application to dictionary"""
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company': self.company,
            'location': self.location,
            'job_url': self.job_url,
            'match_percentage': round(self.match_percentage, 1) if self.match_percentage else 0,
            'skills_match': round(self.skills_match, 1) if self.skills_match else 0,
            'experience_match': round(self.experience_match, 1) if self.experience_match else 0,
            'education_match': round(self.education_match, 1) if self.education_match else 0,
            'matched_skills': self.matched_skills or [],
            'missing_skills': self.missing_skills or [],
            'status': self.status,
            'is_favorited': self.is_favorited,
            'saved_at': self.saved_at.isoformat() if self.saved_at else None
        }
    
    def __repr__(self):
        return f'<JobApplication {self.job_title} at {self.company}>'
