"""
Supabase Client for Codopia Flask Backend
Handles database operations for user management, progress tracking, and learning analytics
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client with environment variables"""
        self.url = os.environ.get('SUPABASE_URL', 'https://ylymepybqcykyomsmxwk.supabase.co')
        self.key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlseW1lcHlicWN5a3lvbXNteHdrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODAxNjU1NSwiZXhwIjoyMDczNTkyNTU1fQ.kIyPRDJFy5g3ovXhK96mxgckeNFQwzxPaEsjCY52cfI')
        
        try:
            self.client: Client = create_client(self.url, self.key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise

    # USER MANAGEMENT OPERATIONS
    
    def create_user(self, email: str, password_hash: str, full_name: str, role: str = 'parent') -> Dict[str, Any]:
        """Create a new user in the database with fallback to in-memory storage"""
        try:
            # Try Supabase first
            import uuid
            user_id = str(uuid.uuid4())
            profile_data = {
                'id': user_id,
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name,
                'role': role,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            try:
                result = self.client.table('users').insert(profile_data).execute()
                if result.data:
                    logger.info(f"User created in Supabase: {email}")
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase user creation failed, using fallback: {e}")
            
            # Fallback: store in memory (for development)
            if not hasattr(self, '_fallback_users'):
                self._fallback_users = {}
            
            self._fallback_users[user_id] = profile_data
            logger.info(f"User created with fallback method: {email}")
            return profile_data
                
        except Exception as e:
            logger.error(f"Error creating user {email}: {e}")
            raise

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by email address with fallback"""
        try:
            # Try Supabase first
            try:
                result = self.client.table('users').select('*').eq('email', email).execute()
                if result.data:
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase query failed, using fallback: {e}")
            
            # Fallback: check in-memory storage
            if hasattr(self, '_fallback_users'):
                for user in self._fallback_users.values():
                    if user['email'] == email:
                        return user
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving user {email}: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by ID with fallback"""
        try:
            # Try Supabase first
            try:
                result = self.client.table('users').select('*').eq('id', user_id).execute()
                if result.data:
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase query failed, using fallback: {e}")
            
            # Fallback: check in-memory storage
            if hasattr(self, '_fallback_users') and user_id in self._fallback_users:
                return self._fallback_users[user_id]
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            return None

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user information with fallback"""
        try:
            updates['updated_at'] = datetime.utcnow().isoformat()
            
            # Try Supabase first
            try:
                result = self.client.table('users').update(updates).eq('id', user_id).execute()
                if result.data:
                    logger.info(f"User updated in Supabase: {user_id}")
                    return True
            except Exception as e:
                logger.warning(f"Supabase update failed, using fallback: {e}")
            
            # Fallback: update in-memory storage
            if hasattr(self, '_fallback_users') and user_id in self._fallback_users:
                self._fallback_users[user_id].update(updates)
                logger.info(f"User updated with fallback method: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return False

    # CHILD PROFILE OPERATIONS
    
    def create_child_profile(self, parent_id: str, name: str, age: int, tier: str) -> Dict[str, Any]:
        """Create a child profile linked to parent with fallback"""
        try:
            import uuid
            child_id = str(uuid.uuid4())
            child_data = {
                'id': child_id,
                'parent_id': parent_id,
                'name': name,
                'age': age,
                'tier': tier,
                'magic_points': 0,
                'achievements': [],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            # Try Supabase first
            try:
                result = self.client.table('children').insert(child_data).execute()
                if result.data:
                    logger.info(f"Child profile created in Supabase: {name}")
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase child creation failed, using fallback: {e}")
            
            # Fallback: store in memory
            if not hasattr(self, '_fallback_children'):
                self._fallback_children = {}
            
            self._fallback_children[child_id] = child_data
            logger.info(f"Child profile created with fallback method: {name}")
            return child_data
            
        except Exception as e:
            logger.error(f"Error creating child profile {name}: {e}")
            raise

    def get_children_by_parent(self, parent_id: str) -> List[Dict[str, Any]]:
        """Get all children for a parent with fallback"""
        try:
            children = []
            
            # Try Supabase first
            try:
                result = self.client.table('children').select('*').eq('parent_id', parent_id).execute()
                if result.data:
                    children.extend(result.data)
            except Exception as e:
                logger.warning(f"Supabase children query failed, using fallback: {e}")
            
            # Fallback: check in-memory storage
            if hasattr(self, '_fallback_children'):
                for child in self._fallback_children.values():
                    if child['parent_id'] == parent_id:
                        children.append(child)
            
            return children
            
        except Exception as e:
            logger.error(f"Error retrieving children for parent {parent_id}: {e}")
            return []

    def get_child_by_id(self, child_id: str) -> Optional[Dict[str, Any]]:
        """Get child profile by ID with fallback"""
        try:
            # Try Supabase first
            try:
                result = self.client.table('children').select('*').eq('id', child_id).execute()
                if result.data:
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase child query failed, using fallback: {e}")
            
            # Fallback: check in-memory storage
            if hasattr(self, '_fallback_children') and child_id in self._fallback_children:
                return self._fallback_children[child_id]
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving child {child_id}: {e}")
            return None

    def update_child_profile(self, child_id: str, updates: Dict[str, Any]) -> bool:
        """Update child profile with fallback"""
        try:
            updates['updated_at'] = datetime.utcnow().isoformat()
            
            # Try Supabase first
            try:
                result = self.client.table('children').update(updates).eq('id', child_id).execute()
                if result.data:
                    logger.info(f"Child profile updated in Supabase: {child_id}")
                    return True
            except Exception as e:
                logger.warning(f"Supabase child update failed, using fallback: {e}")
            
            # Fallback: update in-memory storage
            if hasattr(self, '_fallback_children') and child_id in self._fallback_children:
                self._fallback_children[child_id].update(updates)
                logger.info(f"Child profile updated with fallback method: {child_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating child {child_id}: {e}")
            return False

    # PROGRESS TRACKING OPERATIONS
    
    def save_lesson_progress(self, child_id: str, lesson_id: str, progress_data: Dict[str, Any]) -> bool:
        """Save lesson progress for a child"""
        try:
            progress_entry = {
                'child_id': child_id,
                'lesson_id': lesson_id,
                'progress_data': json.dumps(progress_data),
                'completed': progress_data.get('completed', False),
                'score': progress_data.get('score', 0),
                'time_spent': progress_data.get('time_spent', 0),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            # Check if progress already exists
            existing = self.client.table('lesson_progress').select('*').eq('child_id', child_id).eq('lesson_id', lesson_id).execute()
            
            if existing.data:
                # Update existing progress
                result = self.client.table('lesson_progress').update(progress_entry).eq('child_id', child_id).eq('lesson_id', lesson_id).execute()
            else:
                # Create new progress entry
                result = self.client.table('lesson_progress').insert(progress_entry).execute()
            
            if result.data:
                logger.info(f"Progress saved for child {child_id}, lesson {lesson_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error saving progress for child {child_id}, lesson {lesson_id}: {e}")
            return False

    def get_child_progress(self, child_id: str) -> List[Dict[str, Any]]:
        """Get all progress for a child"""
        try:
            result = self.client.table('lesson_progress').select('*').eq('child_id', child_id).execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error retrieving progress for child {child_id}: {e}")
            return []

    def get_lesson_progress(self, child_id: str, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Get specific lesson progress"""
        try:
            result = self.client.table('lesson_progress').select('*').eq('child_id', child_id).eq('lesson_id', lesson_id).execute()
            
            if result.data:
                progress = result.data[0]
                # Parse JSON progress data
                if progress.get('progress_data'):
                    progress['progress_data'] = json.loads(progress['progress_data'])
                return progress
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving lesson progress for child {child_id}, lesson {lesson_id}: {e}")
            return None

    # ACHIEVEMENT OPERATIONS
    
    def award_achievement(self, child_id: str, achievement_id: str, achievement_data: Dict[str, Any]) -> bool:
        """Award an achievement to a child"""
        try:
            achievement_entry = {
                'child_id': child_id,
                'achievement_id': achievement_id,
                'achievement_data': json.dumps(achievement_data),
                'earned_at': datetime.utcnow().isoformat()
            }
            
            result = self.client.table('achievements').insert(achievement_entry).execute()
            
            if result.data:
                logger.info(f"Achievement {achievement_id} awarded to child {child_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error awarding achievement {achievement_id} to child {child_id}: {e}")
            return False

    def get_child_achievements(self, child_id: str) -> List[Dict[str, Any]]:
        """Get all achievements for a child"""
        try:
            result = self.client.table('achievements').select('*').eq('child_id', child_id).execute()
            
            achievements = result.data if result.data else []
            
            # Parse JSON achievement data
            for achievement in achievements:
                if achievement.get('achievement_data'):
                    achievement['achievement_data'] = json.loads(achievement['achievement_data'])
            
            return achievements
            
        except Exception as e:
            logger.error(f"Error retrieving achievements for child {child_id}: {e}")
            return []

    # ANALYTICS OPERATIONS
    
    def get_parent_analytics(self, parent_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a parent's children"""
        try:
            children = self.get_children_by_parent(parent_id)
            analytics = {
                'total_children': len(children),
                'children_data': []
            }
            
            for child in children:
                child_id = child['id']
                progress = self.get_child_progress(child_id)
                achievements = self.get_child_achievements(child_id)
                
                child_analytics = {
                    'child_info': child,
                    'total_lessons': len(progress),
                    'completed_lessons': len([p for p in progress if p.get('completed')]),
                    'total_achievements': len(achievements),
                    'magic_points': child.get('magic_points', 0),
                    'recent_progress': sorted(progress, key=lambda x: x['updated_at'], reverse=True)[:5]
                }
                
                analytics['children_data'].append(child_analytics)
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error retrieving analytics for parent {parent_id}: {e}")
            return {}

    # UTILITY OPERATIONS
    
    def health_check(self) -> bool:
        """Check if Supabase connection is healthy"""
        try:
            result = self.client.table('profiles').select('count').execute()
            return True
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return False

# Global Supabase client instance
supabase_client = SupabaseClient()

