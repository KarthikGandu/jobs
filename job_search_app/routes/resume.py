"""
Resume routes - Upload and manage resumes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os

from job_search_app.extensions import db
from job_search_app.models.resume import Resume
from job_search_app.services.resume_parser import ResumeParser

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route('/upload', methods=['POST'])
@login_required
def upload_resume():
    """Upload and parse user resume"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'status': 'error', 'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'status': 'error', 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'error': 'Invalid file type. Please upload PDF or DOCX'}), 400
        
        # Create upload directory
        upload_dir = Path(current_app.root_path).parent / 'uploads' / 'resumes'
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{current_user.id}_{timestamp}_{filename}"
        file_path = upload_dir / filename
        
        # Save file
        file.save(str(file_path))
        
        # Check file size
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            os.remove(file_path)
            return jsonify({'status': 'error', 'error': 'File size exceeds 5MB limit'}), 400
        
        # Parse resume
        parser = ResumeParser()
        try:
            parsed_data = parser.parse_resume(str(file_path))
        except Exception as e:
            os.remove(file_path)
            current_app.logger.error(f"Error parsing resume: {e}")
            return jsonify({'status': 'error', 'error': 'Failed to parse resume. Please check file format.'}), 400
        
        # Delete old resume if exists
        old_resume = Resume.query.filter_by(user_id=current_user.id).first()
        if old_resume and old_resume.file_path:
            old_path = Path(old_resume.file_path)
            if old_path.exists():
                old_path.unlink()
            db.session.delete(old_resume)
        
        # Create new resume record
        resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=os.path.getsize(file_path),
            raw_text=parsed_data['raw_text'],
            skills=parsed_data['skills'],
            education=parsed_data['education'],
            certifications=parsed_data['certifications'],
            years_experience=parsed_data['years_experience'],
            highest_degree=parsed_data['highest_degree']
        )
        
        db.session.add(resume)
        
        # Update user
        current_user.has_resume = True
        current_user.resume_filename = file.filename
        current_user.resume_uploaded_at = datetime.utcnow()
        if parsed_data['years_experience']:
            current_user.years_experience = parsed_data['years_experience']
        
        db.session.commit()
        
        current_app.logger.info(f"Resume uploaded for user {current_user.id}: {filename}")
        
        return jsonify({
            'status': 'success',
            'message': 'Resume uploaded and parsed successfully',
            'resume': resume.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error uploading resume: {e}", exc_info=True)
        return jsonify({'status': 'error', 'error': 'Failed to upload resume'}), 500


@resume_bp.route('/info', methods=['GET'])
@login_required
def get_resume_info():
    """Get current user's resume information"""
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    
    if not resume:
        return jsonify({'status': 'error', 'error': 'No resume found'}), 404
    
    return jsonify({
        'status': 'success',
        'resume': resume.to_dict()
    })


@resume_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_resume():
    """Delete user's resume"""
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    
    if not resume:
        return jsonify({'status': 'error', 'error': 'No resume found'}), 404
    
    # Delete file
    if resume.file_path:
        file_path = Path(resume.file_path)
        if file_path.exists():
            file_path.unlink()
    
    # Delete database record
    db.session.delete(resume)
    
    # Update user
    current_user.has_resume = False
    current_user.resume_filename = None
    current_user.resume_uploaded_at = None
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Resume deleted successfully'
    })
