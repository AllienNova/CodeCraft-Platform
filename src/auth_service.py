import os
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt
from datetime import datetime, timedelta
import jwt

# Load environment variables
load_dotenv()

class SupabaseAuthService:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.secret_key = os.getenv('FLASK_SECRET_KEY')
        
        # Create Supabase clients
        self.supabase: Client = create_client(self.url, self.anon_key)
        self.admin_supabase: Client = create_client(self.url, self.service_key)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def determine_tier(self, age: int) -> str:
        """Determine learning tier based on age"""
        if age <= 7:
            return 'magic_workshop'
        elif age <= 12:
            return 'innovation_lab'
        else:
            return 'professional_studio'
    
    def create_user_account(self, email: str, password: str, full_name: str) -> dict:
        """Create a new user account using Supabase Auth"""
        try:
            # Create user with Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name,
                        "role": "parent"
                    }
                }
            })
            
            if auth_response.user:
                # Create profile in our custom table
                profile_data = {
                    "id": auth_response.user.id,
                    "email": email,
                    "full_name": full_name,
                    "role": "parent",
                    "created_at": datetime.utcnow().isoformat()
                }
                
                profile_response = self.admin_supabase.table('profiles').insert(profile_data).execute()
                
                return {
                    "success": True,
                    "user": auth_response.user,
                    "profile": profile_response.data[0] if profile_response.data else None,
                    "message": "Account created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create user account"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def sign_in_user(self, email: str, password: str) -> dict:
        """Sign in user with email and password"""
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Get user profile
                profile_response = self.supabase.table('profiles').select('*').eq('id', auth_response.user.id).execute()
                
                # Get user's children
                children_response = self.supabase.table('children').select('*').eq('parent_id', auth_response.user.id).execute()
                
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session,
                    "profile": profile_response.data[0] if profile_response.data else None,
                    "children": children_response.data if children_response.data else [],
                    "message": "Signed in successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_child_profile(self, parent_id: str, name: str, age: int) -> dict:
        """Create a child profile"""
        try:
            tier = self.determine_tier(age)
            
            child_data = {
                "parent_id": parent_id,
                "name": name,
                "age": age,
                "tier": tier,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.admin_supabase.table('children').insert(child_data).execute()
            
            if response.data:
                return {
                    "success": True,
                    "child": response.data[0],
                    "message": f"Child profile created successfully in {tier.replace('_', ' ').title()}"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create child profile"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_with_children(self, user_id: str) -> dict:
        """Get user profile with children"""
        try:
            # Get user profile
            profile_response = self.supabase.table('profiles').select('*').eq('id', user_id).execute()
            
            # Get user's children
            children_response = self.supabase.table('children').select('*').eq('parent_id', user_id).execute()
            
            return {
                "success": True,
                "profile": profile_response.data[0] if profile_response.data else None,
                "children": children_response.data if children_response.data else []
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_session_token(self, user_id: str) -> str:
        """Create a JWT session token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_session_token(self, token: str) -> dict:
        """Verify JWT session token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {
                "success": True,
                "user_id": payload['user_id']
            }
        except jwt.ExpiredSignatureError:
            return {
                "success": False,
                "error": "Token has expired"
            }
        except jwt.InvalidTokenError:
            return {
                "success": False,
                "error": "Invalid token"
            }
    
    def sign_out_user(self) -> dict:
        """Sign out current user"""
        try:
            self.supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Signed out successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
