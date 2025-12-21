"""
Resume model for storing parsed resume data
"""
from datetime import datetime
from job_search_app.extensions import db


class Resume(db.Model):
    """Resume data model"""
    
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # File info
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.Integer)
    
    # Parsed content
    raw_text = db.Column(db.Text)
    
    # Extracted information
    skills = db.Column(db.JSON)  # List of skills
    education = db.Column(db.JSON)  # List of education entries
    experience = db.Column(db.JSON)  # List of work experience
    certifications = db.Column(db.JSON)  # List of certifications
    
    # Metadata
    years_experience = db.Column(db.Integer)
    highest_degree = db.Column(db.String(100))
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert resume to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'skills': self.skills or [],
            'education': self.education or [],
            'experience': self.experience or [],
            'certifications': self.certifications or [],
            'years_experience': self.years_experience,
            'highest_degree': self.highest_degree,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    def __repr__(self):
        return f'<Resume {self.filename}>'
