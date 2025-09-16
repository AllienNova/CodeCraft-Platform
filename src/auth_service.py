import os
import hashlib
import secrets
from datetime import datetime, timedelta
import json

class SupabaseAuthService:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL', 'https://ylymepybqcykyomsmxwk.supabase.co')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY', '')
        self.service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
        self.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
        
        # Simple in-memory storage for demo (replace with actual Supabase calls)
        self.users = {}
        self.children = {}
    
    def hash_password(self, password: str) -> str:
        """Simple password hashing"""
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            hash_part, salt = hashed.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
        except:
            return False
    
    def determine_tier(self, age: int) -> str:
        """Determine learning tier based on age"""
        if age <= 7:
            return 'magic_workshop'
        elif age <= 12:
            return 'innovation_lab'
        else:
            return 'professional_studio'
    
    def create_user_account(self, email: str, password: str, full_name: str) -> dict:
        """Create a new user account"""
        try:
            if email in self.users:
                return {
                    "success": False,
                    "error": "User already exists"
                }
            
            user_id = secrets.token_hex(16)
            hashed_password = self.hash_password(password)
            
            user_data = {
                "id": user_id,
                "email": email,
                "password": hashed_password,
                "full_name": full_name,
                "role": "parent",
                "created_at": datetime.utcnow().isoformat()
            }
            
            self.users[email] = user_data
            
            return {
                "success": True,
                "user": {"id": user_id, "email": email},
                "message": "Account created successfully"
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def sign_in_user(self, email: str, password: str) -> dict:
        """Sign in user with email and password"""
        try:
            if email not in self.users:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
            
            user = self.users[email]
            if not self.verify_password(password, user['password']):
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
            
            # Get user's children
            user_children = [child for child in self.children.values() if child['parent_id'] == user['id']]
            
            return {
                "success": True,
                "user": {"id": user['id'], "email": user['email']},
                "session": {"access_token": "demo_token"},
                "profile": user,
                "children": user_children,
                "message": "Signed in successfully"
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
            child_id = secrets.token_hex(16)
            
            child_data = {
                "id": child_id,
                "parent_id": parent_id,
                "name": name,
                "age": age,
                "tier": tier,
                "created_at": datetime.utcnow().isoformat()
            }
            
            self.children[child_id] = child_data
            
            return {
                "success": True,
                "child": child_data,
                "message": f"Child profile created successfully in {tier.replace('_', ' ').title()}"
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_with_children(self, user_id: str) -> dict:
        """Get user profile with children"""
        try:
            # Find user by ID
            user = None
            for u in self.users.values():
                if u['id'] == user_id:
                    user = u
                    break
            
            if not user:
                return {
                    "success": False,
                    "error": "User not found"
                }
            
            # Get user's children
            user_children = [child for child in self.children.values() if child['parent_id'] == user_id]
            
            return {
                "success": True,
                "profile": user,
                "children": user_children
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_session_token(self, user_id: str) -> str:
        """Create a simple session token"""
        return f"session_{user_id}_{secrets.token_hex(16)}"
    
    def verify_session_token(self, token: str) -> dict:
        """Verify session token"""
        try:
            if token.startswith('session_'):
                parts = token.split('_')
                if len(parts) >= 3:
                    user_id = parts[1]
                    return {
                        "success": True,
                        "user_id": user_id
                    }
            
            return {
                "success": False,
                "error": "Invalid token"
            }
        except:
            return {
                "success": False,
                "error": "Invalid token"
            }
    
    def sign_out_user(self) -> dict:
        """Sign out current user"""
        return {
            "success": True,
            "message": "Signed out successfully"
        }
