import os
import sys
from datetime import datetime, timedelta
import bcrypt
import json

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'codecraft-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'codecraft.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='parent')  # 'parent' or 'child'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    children = db.relationship('ChildProfile', backref='parent', lazy=True)

class ChildProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tier = db.Column(db.String(20), nullable=False)  # 'explorer', 'creator', 'innovator'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', backref='child', lazy=True)
    progress = db.relationship('Progress', backref='child', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(db.String(50), nullable=False)  # 'story', 'game', 'app', etc.
    content = db.Column(db.Text)  # JSON content of the project
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_shared = db.Column(db.Boolean, default=False)
    share_code = db.Column(db.String(10), unique=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    module_id = db.Column(db.String(50), nullable=False)
    lesson_id = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)  # in minutes
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def determine_tier(age):
    if age <= 7:
        return 'explorer'
    elif age <= 9:
        return 'creator'
    else:
        return 'innovator'

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CodeCraft API is running'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if data.get('role') == 'parent':
            # Parent registration
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'error': 'Email and password required'}), 400
            
            # Check if user exists
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'User already exists'}), 400
            
            # Create parent user
            user = User(
                email=email,
                password_hash=hash_password(password),
                role='parent'
            )
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=7)
            )
            
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role
                }
            }), 201
            
        elif data.get('role') == 'child':
            # Child profile creation
            parent_email = data.get('parent_email')
            child_name = data.get('child_name')
            child_age = data.get('child_age')
            
            if not all([parent_email, child_name, child_age]):
                return jsonify({'error': 'All fields required'}), 400
            
            # Find or create parent
            parent = User.query.filter_by(email=parent_email, role='parent').first()
            if not parent:
                # Create a temporary parent account for demo purposes
                parent = User(
                    email=parent_email,
                    password_hash=hash_password('temp-password'),
                    role='parent'
                )
                db.session.add(parent)
                db.session.flush()
            
            # Create child profile
            child = ChildProfile(
                name=child_name,
                age=int(child_age),
                parent_id=parent.id,
                tier=determine_tier(int(child_age))
            )
            db.session.add(child)
            db.session.commit()
            
            # Create access token for child session
            access_token = create_access_token(
                identity=f"child_{child.id}",
                expires_delta=timedelta(hours=8)
            )
            
            return jsonify({
                'access_token': access_token,
                'child': {
                    'id': child.id,
                    'name': child.name,
                    'age': child.age,
                    'tier': child.tier,
                    'parent_id': child.parent_id
                }
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/children', methods=['GET'])
@jwt_required()
def get_children():
    try:
        user_id = get_jwt_identity()
        
        # Handle child sessions
        if isinstance(user_id, str) and user_id.startswith('child_'):
            child_id = int(user_id.split('_')[1])
            child = ChildProfile.query.get(child_id)
            if child:
                return jsonify({
                    'current_child': {
                        'id': child.id,
                        'name': child.name,
                        'age': child.age,
                        'tier': child.tier,
                        'last_active': child.last_active.isoformat() if child.last_active else None,
                        'created_at': child.created_at.isoformat()
                    }
                })
        
        # Handle parent sessions
        user = User.query.get(user_id)
        if not user or user.role != 'parent':
            return jsonify({'error': 'Unauthorized'}), 403
        
        children = ChildProfile.query.filter_by(parent_id=user_id).all()
        
        return jsonify({
            'children': [{
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'tier': child.tier,
                'last_active': child.last_active.isoformat() if child.last_active else None,
                'created_at': child.created_at.isoformat()
            } for child in children]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tiers/<tier_name>/content', methods=['GET'])
def get_tier_content(tier_name):
    """Get curriculum content for a specific tier"""
    try:
        # Mock curriculum data - in production this would come from database
        curriculum = {
            'explorer': {
                'modules': [
                    {
                        'id': 'getting_started',
                        'title': 'Getting Started with Magic',
                        'description': 'Learn the basics of coding with Sparkle the Unicorn',
                        'lessons': [
                            {'id': 'meet_sparkle', 'title': 'Meet Sparkle the Unicorn', 'completed': True},
                            {'id': 'first_blocks', 'title': 'Your First Magic Blocks', 'completed': True},
                            {'id': 'make_sparkle_move', 'title': 'Make Sparkle Move', 'completed': False}
                        ]
                    },
                    {
                        'id': 'story_building',
                        'title': 'Building Magical Stories',
                        'description': 'Create interactive stories with characters and scenes',
                        'lessons': [
                            {'id': 'story_characters', 'title': 'Choose Your Characters', 'completed': False},
                            {'id': 'story_scenes', 'title': 'Create Beautiful Scenes', 'completed': False},
                            {'id': 'story_actions', 'title': 'Add Actions and Movement', 'completed': False}
                        ]
                    }
                ]
            },
            'creator': {
                'modules': [
                    {
                        'id': 'advanced_blocks',
                        'title': 'Advanced Block Programming',
                        'description': 'Master logic, loops, and variables',
                        'lessons': [
                            {'id': 'logic_blocks', 'title': 'If-Then-Else Logic', 'completed': True},
                            {'id': 'loops', 'title': 'Repeat and Loop Blocks', 'completed': True},
                            {'id': 'variables', 'title': 'Variables and Data', 'completed': False}
                        ]
                    },
                    {
                        'id': 'app_building',
                        'title': 'Building Real Apps',
                        'description': 'Create Progressive Web Apps that work on any device',
                        'lessons': [
                            {'id': 'app_design', 'title': 'Designing Your App', 'completed': False},
                            {'id': 'user_interface', 'title': 'Creating User Interfaces', 'completed': False},
                            {'id': 'app_logic', 'title': 'Adding App Logic', 'completed': False}
                        ]
                    }
                ]
            },
            'innovator': {
                'modules': [
                    {
                        'id': 'professional_coding',
                        'title': 'Professional Coding Skills',
                        'description': 'Learn real programming languages and tools',
                        'lessons': [
                            {'id': 'javascript_basics', 'title': 'JavaScript Fundamentals', 'completed': True},
                            {'id': 'html_css', 'title': 'HTML and CSS Mastery', 'completed': True},
                            {'id': 'react_intro', 'title': 'Introduction to React', 'completed': True}
                        ]
                    },
                    {
                        'id': 'full_stack',
                        'title': 'Full-Stack Development',
                        'description': 'Build complete web applications with backend and database',
                        'lessons': [
                            {'id': 'backend_basics', 'title': 'Backend Development', 'completed': False},
                            {'id': 'databases', 'title': 'Working with Databases', 'completed': False},
                            {'id': 'deployment', 'title': 'Deploying Your Apps', 'completed': False}
                        ]
                    }
                ]
            }
        }
        
        if tier_name not in curriculum:
            return jsonify({'error': 'Tier not found'}), 404
        
        return jsonify(curriculum[tier_name])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Handle child sessions
        if isinstance(user_id, str) and user_id.startswith('child_'):
            child_id = int(user_id.split('_')[1])
        else:
            child_id = data.get('child_id')
            # Verify child belongs to user for parent sessions
            child = ChildProfile.query.get(child_id)
            if not child or child.parent_id != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
        
        title = data.get('title')
        description = data.get('description', '')
        project_type = data.get('project_type')
        content = data.get('content', '{}')
        
        project = Project(
            title=title,
            description=description,
            project_type=project_type,
            content=content,
            child_id=child_id
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'project': {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'project_type': project.project_type,
                'created_at': project.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Static file serving for frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({'message': 'CodeCraft API is running', 'frontend': 'Not deployed yet'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

