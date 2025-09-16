import os
import json
import asyncio
import websockets
from datetime import datetime
import logging

class ProfessorSparkle:
    """
    Professor Sparkle - AI Coding Tutor with Gemini Live Integration
    
    An experienced, patient, and encouraging AI tutor that helps children
    learn coding through interactive voice conversations, personalized guidance,
    and adaptive curriculum delivery.
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.session_id = None
        self.child_profile = {}
        self.current_lesson = {}
        self.conversation_history = []
        self.learning_progress = {}
        
        # Professor Sparkle's personality traits
        self.personality = {
            "name": "Professor Sparkle",
            "role": "Magical Coding Tutor",
            "personality": "Patient, encouraging, magical, wise, and child-friendly",
            "teaching_style": "Interactive, story-based, hands-on learning",
            "voice_tone": "Warm, enthusiastic, and supportive",
            "expertise": "Visual programming, block coding, computational thinking"
        }
        
        # Curriculum structure for different tiers
        self.curriculum = {
            "magic_workshop": {
                "age_range": "5-7",
                "focus": "Visual block coding with magical themes",
                "lessons": [
                    {
                        "id": "mw_001",
                        "title": "Making the Wizard Move",
                        "concepts": ["sequence", "movement", "basic commands"],
                        "story": "Help the wizard find the magical crystal by moving through the enchanted forest"
                    },
                    {
                        "id": "mw_002", 
                        "title": "Casting Spell Patterns",
                        "concepts": ["repetition", "loops", "patterns"],
                        "story": "Learn to cast repeating spells to create magical patterns"
                    },
                    {
                        "id": "mw_003",
                        "title": "Magical Decisions",
                        "concepts": ["conditionals", "if-then", "decision making"],
                        "story": "Help the wizard make smart choices on the magical adventure"
                    }
                ]
            },
            "innovation_lab": {
                "age_range": "8-12",
                "focus": "Advanced blocks and app building",
                "lessons": [
                    {
                        "id": "il_001",
                        "title": "Building Your First App",
                        "concepts": ["functions", "variables", "user interface"],
                        "story": "Create an app that helps solve real-world problems"
                    }
                ]
            },
            "professional_studio": {
                "age_range": "13+",
                "focus": "Real programming languages",
                "lessons": [
                    {
                        "id": "ps_001",
                        "title": "Python Fundamentals",
                        "concepts": ["syntax", "variables", "functions"],
                        "story": "Start your journey as a professional programmer"
                    }
                ]
            }
        }
    
    def get_system_prompt(self, child_profile, current_lesson):
        """Generate system prompt for Professor Sparkle based on child's profile and current lesson"""
        
        tier = child_profile.get('tier', 'magic_workshop')
        age = child_profile.get('age', 6)
        name = child_profile.get('name', 'Young Coder')
        
        base_prompt = f"""
You are Professor Sparkle, a magical and wise coding tutor who specializes in teaching children how to code.

CHILD PROFILE:
- Name: {name}
- Age: {age} years old
- Learning Tier: {tier.replace('_', ' ').title()}
- Current Lesson: {current_lesson.get('title', 'Introduction')}

YOUR PERSONALITY:
- Magical, wise, and incredibly patient
- Always encouraging and positive
- Use age-appropriate language and concepts
- Incorporate magical themes and storytelling
- Celebrate every small success
- Make coding feel like an adventure

TEACHING APPROACH:
- Break down complex concepts into simple, digestible steps
- Use analogies and stories that relate to magic and adventure
- Encourage experimentation and learning from mistakes
- Ask guiding questions rather than giving direct answers
- Adapt explanations based on the child's responses and understanding

CURRENT LESSON CONTEXT:
- Title: {current_lesson.get('title', 'Getting Started')}
- Concepts: {', '.join(current_lesson.get('concepts', []))}
- Story Context: {current_lesson.get('story', 'Beginning the magical coding journey')}

VOICE INTERACTION GUIDELINES:
- Keep responses conversational and natural for voice
- Use pauses and emphasis to maintain engagement
- Ask questions to check understanding
- Provide clear, step-by-step instructions
- Use sound effects and magical expressions (like "Abracadabra!" or "Sparkle time!")

SAFETY AND APPROPRIATENESS:
- Always maintain child-safe content
- Be patient with repetitive questions
- Encourage breaks if the child seems frustrated
- Celebrate effort over perfection
- Never use complex technical jargon without explanation

Remember: You're not just teaching code, you're inspiring a lifelong love of learning and problem-solving!
"""
        
        if tier == 'magic_workshop':
            base_prompt += """
MAGIC WORKSHOP SPECIFIC:
- Focus on visual drag-and-drop blocks
- Use magical creatures and spells as examples
- Emphasize storytelling and adventure
- Keep concepts very simple and visual
- Use lots of encouragement and celebration
"""
        elif tier == 'innovation_lab':
            base_prompt += """
INNOVATION LAB SPECIFIC:
- Introduce more complex logical thinking
- Focus on building real applications
- Encourage creative problem-solving
- Introduce basic programming concepts
- Connect coding to real-world applications
"""
        elif tier == 'professional_studio':
            base_prompt += """
PROFESSIONAL STUDIO SPECIFIC:
- Introduce actual programming languages
- Focus on industry best practices
- Encourage professional development mindset
- Provide career guidance and inspiration
- Balance challenge with support
"""
        
        return base_prompt
    
    async def initialize_session(self, child_profile, lesson_id=None):
        """Initialize a new learning session with Professor Sparkle"""
        
        self.child_profile = child_profile
        tier = child_profile.get('tier', 'magic_workshop')
        
        # Get current lesson
        if lesson_id:
            self.current_lesson = self.find_lesson_by_id(lesson_id)
        else:
            # Start with first lesson of the tier
            self.current_lesson = self.curriculum[tier]['lessons'][0]
        
        # Generate session ID
        self.session_id = f"sparkle_{child_profile.get('id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize conversation
        welcome_message = self.generate_welcome_message()
        
        return {
            "session_id": self.session_id,
            "professor": self.personality,
            "current_lesson": self.current_lesson,
            "welcome_message": welcome_message,
            "system_prompt": self.get_system_prompt(child_profile, self.current_lesson)
        }
    
    def generate_welcome_message(self):
        """Generate a personalized welcome message"""
        
        name = self.child_profile.get('name', 'Young Coder')
        tier = self.child_profile.get('tier', 'magic_workshop')
        lesson_title = self.current_lesson.get('title', 'Our Adventure')
        
        if tier == 'magic_workshop':
            return f"""
            ✨ *Sparkles appear in the air* ✨
            
            Hello there, {name}! I'm Professor Sparkle, your magical coding tutor! 
            
            I'm absolutely delighted to meet you! Today, we're going on an amazing adventure 
            called "{lesson_title}". Are you ready to learn some magical coding spells?
            
            Remember, in my classroom, there are no mistakes - only magical discoveries! 
            Every time you try something new, you're becoming a more powerful young wizard!
            
            Shall we begin our coding adventure? Just speak to me anytime you have questions 
            or need help! I'm here to guide you every step of the way! 🪄
            """
        elif tier == 'innovation_lab':
            return f"""
            🔬 *Laboratory lights up with innovation* 🔬
            
            Greetings, {name}! I'm Professor Sparkle, and welcome to the Innovation Lab!
            
            You're about to embark on an exciting journey where we'll build amazing apps 
            and solve real-world problems with code! Today's mission: "{lesson_title}".
            
            In this lab, creativity meets technology, and every idea you have could become 
            the next big innovation! Are you ready to become a young inventor?
            
            Let's start building something incredible together! 🚀
            """
        else:  # professional_studio
            return f"""
            💼 *Professional development environment activates* 💼
            
            Welcome, {name}! I'm Professor Sparkle, your guide to professional programming!
            
            You've reached the Professional Studio - where real programmers are made! 
            Today we're diving into "{lesson_title}".
            
            Here, we'll learn the same tools and languages that professional developers 
            use every day. You're taking your first steps toward a potential career in tech!
            
            Ready to code like a pro? Let's make it happen! 💻
            """
    
    def find_lesson_by_id(self, lesson_id):
        """Find a lesson by its ID across all tiers"""
        for tier_name, tier_data in self.curriculum.items():
            for lesson in tier_data['lessons']:
                if lesson['id'] == lesson_id:
                    return lesson
        return self.curriculum['magic_workshop']['lessons'][0]  # Default fallback
    
    async def process_voice_input(self, audio_data, session_context):
        """Process voice input from the child and generate appropriate response"""
        
        # This would integrate with Gemini Live API
        # For now, we'll simulate the processing
        
        try:
            # Simulate Gemini Live API call
            response = await self.call_gemini_live_api(audio_data, session_context)
            
            # Process the response and add teaching context
            enhanced_response = self.enhance_response_with_teaching_context(response)
            
            # Log the interaction for progress tracking
            self.log_interaction(audio_data, enhanced_response)
            
            return enhanced_response
            
        except Exception as e:
            logging.error(f"Error processing voice input: {e}")
            return self.generate_fallback_response()
    
    async def call_gemini_live_api(self, audio_data, session_context):
        """Call Gemini Live API for real-time voice interaction"""
        
        # This is where we'd implement the actual Gemini Live API integration
        # Based on: https://ai.google.dev/gemini-api/docs/live
        
        api_endpoint = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare the request payload
        request_payload = {
            "model": "models/gemini-2.0-flash-exp",
            "generation_config": {
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": "Puck"  # Playful voice for Professor Sparkle
                        }
                    }
                }
            },
            "system_instruction": {
                "parts": [{"text": session_context.get('system_prompt', '')}]
            }
        }
        
        # For demo purposes, return a simulated response
        # In production, this would be the actual API call
        return {
            "audio_response": "simulated_audio_data",
            "text_response": "Great question! Let me help you with that coding concept...",
            "teaching_suggestions": ["Encourage experimentation", "Break down the problem", "Celebrate progress"]
        }
    
    def enhance_response_with_teaching_context(self, api_response):
        """Enhance the API response with additional teaching context and guidance"""
        
        enhanced_response = {
            "audio": api_response.get("audio_response"),
            "text": api_response.get("text_response"),
            "teaching_context": {
                "current_concept": self.current_lesson.get('concepts', []),
                "next_steps": self.generate_next_steps(),
                "encouragement": self.generate_encouragement(),
                "visual_aids": self.suggest_visual_aids()
            },
            "progress_update": self.calculate_progress_update()
        }
        
        return enhanced_response
    
    def generate_next_steps(self):
        """Generate suggested next steps based on current lesson progress"""
        return [
            "Try dragging another spell block",
            "Experiment with different combinations",
            "Ask Professor Sparkle any questions you have"
        ]
    
    def generate_encouragement(self):
        """Generate age-appropriate encouragement"""
        encouragements = [
            "You're doing fantastic! Keep up the magical work! ✨",
            "What a brilliant young coder you are! 🌟",
            "I'm so proud of how you're thinking through this problem! 🎉",
            "Your coding spells are getting stronger every day! 🪄"
        ]
        
        import random
        return random.choice(encouragements)
    
    def suggest_visual_aids(self):
        """Suggest visual aids to help with learning"""
        return {
            "highlight_blocks": ["move-forward", "repeat"],
            "show_animation": "wizard_walking",
            "display_hint": "Try connecting the blocks in order!"
        }
    
    def calculate_progress_update(self):
        """Calculate and return progress update"""
        return {
            "lesson_progress": 45,  # percentage
            "concepts_mastered": ["sequence", "basic_movement"],
            "next_milestone": "Complete 3 successful spell sequences"
        }
    
    def generate_fallback_response(self):
        """Generate a fallback response when API calls fail"""
        return {
            "audio": None,
            "text": "Oops! Professor Sparkle's magic crystal is flickering! Can you try asking your question again? I'm here to help! ✨",
            "teaching_context": {
                "current_concept": self.current_lesson.get('concepts', []),
                "encouragement": "Don't worry, even the best wizards have technical difficulties sometimes! 🪄"
            }
        }
    
    def log_interaction(self, input_data, response_data):
        """Log the interaction for progress tracking and improvement"""
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "child_id": self.child_profile.get('id'),
            "lesson_id": self.current_lesson.get('id'),
            "input_type": "voice",
            "response_type": "voice_and_visual",
            "concepts_discussed": self.current_lesson.get('concepts', [])
        }
        
        self.conversation_history.append(interaction)
        
        # In production, this would save to database
        logging.info(f"Professor Sparkle interaction logged: {interaction}")
    
    def get_lesson_curriculum(self, tier, lesson_id=None):
        """Get structured curriculum for a specific lesson"""
        
        tier_curriculum = self.curriculum.get(tier, self.curriculum['magic_workshop'])
        
        if lesson_id:
            lesson = self.find_lesson_by_id(lesson_id)
        else:
            lesson = tier_curriculum['lessons'][0]
        
        return {
            "tier_info": {
                "name": tier.replace('_', ' ').title(),
                "age_range": tier_curriculum['age_range'],
                "focus": tier_curriculum['focus']
            },
            "lesson": lesson,
            "teaching_approach": self.get_teaching_approach_for_tier(tier),
            "assessment_criteria": self.get_assessment_criteria(lesson)
        }
    
    def get_teaching_approach_for_tier(self, tier):
        """Get specific teaching approach for each tier"""
        
        approaches = {
            "magic_workshop": {
                "method": "Story-based visual learning",
                "interaction_style": "Playful and magical",
                "complexity_level": "Very simple, one concept at a time",
                "feedback_style": "Lots of celebration and encouragement"
            },
            "innovation_lab": {
                "method": "Project-based learning",
                "interaction_style": "Collaborative and exploratory", 
                "complexity_level": "Moderate, building on previous concepts",
                "feedback_style": "Constructive with focus on improvement"
            },
            "professional_studio": {
                "method": "Industry-standard practices",
                "interaction_style": "Mentorship and guidance",
                "complexity_level": "Advanced, real-world applications",
                "feedback_style": "Professional development focused"
            }
        }
        
        return approaches.get(tier, approaches['magic_workshop'])
    
    def get_assessment_criteria(self, lesson):
        """Get assessment criteria for a specific lesson"""
        
        return {
            "understanding_indicators": [
                "Can explain the concept in their own words",
                "Successfully completes hands-on activities", 
                "Asks relevant follow-up questions",
                "Shows creativity in applying the concept"
            ],
            "mastery_indicators": [
                "Can teach the concept to someone else",
                "Applies concept in new situations",
                "Combines with other concepts creatively",
                "Shows confidence in using the concept"
            ],
            "support_needed_indicators": [
                "Struggles with basic concept explanation",
                "Needs repeated guidance for activities",
                "Shows frustration or disengagement",
                "Asks for help frequently"
            ]
        }

# WebSocket handler for real-time voice interaction
class SparkleWebSocketHandler:
    """Handle WebSocket connections for real-time voice interaction with Professor Sparkle"""
    
    def __init__(self):
        self.active_sessions = {}
        self.professor = ProfessorSparkle()
    
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        
        session_id = None
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data['type'] == 'initialize':
                    # Initialize new session
                    child_profile = data['child_profile']
                    lesson_id = data.get('lesson_id')
                    
                    session_data = await self.professor.initialize_session(child_profile, lesson_id)
                    session_id = session_data['session_id']
                    self.active_sessions[session_id] = {
                        'websocket': websocket,
                        'professor': self.professor,
                        'child_profile': child_profile
                    }
                    
                    await websocket.send(json.dumps({
                        'type': 'session_initialized',
                        'data': session_data
                    }))
                
                elif data['type'] == 'voice_input':
                    # Process voice input
                    session_id = data['session_id']
                    audio_data = data['audio_data']
                    
                    if session_id in self.active_sessions:
                        session_context = self.active_sessions[session_id]
                        response = await self.professor.process_voice_input(audio_data, session_context)
                        
                        await websocket.send(json.dumps({
                            'type': 'voice_response',
                            'data': response
                        }))
                
                elif data['type'] == 'progress_update':
                    # Update learning progress
                    session_id = data['session_id']
                    progress_data = data['progress_data']
                    
                    # Process progress update
                    # This would update the child's learning progress in the database
                    
                    await websocket.send(json.dumps({
                        'type': 'progress_updated',
                        'data': {'status': 'success'}
                    }))
        
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
        finally:
            # Clean up session
            if session_id and session_id in self.active_sessions:
                del self.active_sessions[session_id]

# Flask integration
def create_sparkle_routes(app):
    """Create Flask routes for Professor Sparkle integration"""
    
    from flask import request, jsonify
    
    professor = ProfessorSparkle()
    
    @app.route('/api/sparkle/initialize', methods=['POST'])
    def initialize_sparkle_session():
        """Initialize a new Professor Sparkle session"""
        
        data = request.get_json()
        child_profile = data.get('child_profile', {})
        lesson_id = data.get('lesson_id')
        
        try:
            # This would be async in a real implementation
            import asyncio
            session_data = asyncio.run(professor.initialize_session(child_profile, lesson_id))
            
            return jsonify({
                'success': True,
                'data': session_data
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/sparkle/curriculum/<tier>')
    def get_curriculum(tier):
        """Get curriculum information for a specific tier"""
        
        try:
            curriculum_data = professor.get_lesson_curriculum(tier)
            
            return jsonify({
                'success': True,
                'data': curriculum_data
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/sparkle/lesson/<lesson_id>')
    def get_lesson_details(lesson_id):
        """Get detailed information about a specific lesson"""
        
        try:
            lesson = professor.find_lesson_by_id(lesson_id)
            
            return jsonify({
                'success': True,
                'data': lesson
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

# Usage example
if __name__ == "__main__":
    # Example of how to use Professor Sparkle
    
    async def demo_session():
        professor = ProfessorSparkle()
        
        # Sample child profile
        child_profile = {
            'id': 'child_123',
            'name': 'Emma',
            'age': 6,
            'tier': 'magic_workshop'
        }
        
        # Initialize session
        session_data = await professor.initialize_session(child_profile)
        print("Session initialized:", session_data['welcome_message'])
        
        # Get curriculum
        curriculum = professor.get_lesson_curriculum('magic_workshop')
        print("Curriculum:", curriculum)
    
    # Run demo
    # asyncio.run(demo_session())

