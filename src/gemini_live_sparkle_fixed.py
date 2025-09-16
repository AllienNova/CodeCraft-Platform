"""
Professor Sparkle - AI Tutor with Gemini Live Integration
Production-ready implementation with proper error handling and fallbacks
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    logger.info("Google Generative AI SDK loaded successfully")
except ImportError as e:
    GEMINI_AVAILABLE = False
    logger.warning(f"Google Generative AI SDK not available: {e}")

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
    logger.info("WebSockets library loaded successfully")
except ImportError as e:
    WEBSOCKETS_AVAILABLE = False
    logger.warning(f"WebSockets library not available: {e}")

class ProfessorSparkle:
    """
    Professor Sparkle - The Ultimate AI Coding Tutor
    
    A comprehensive AI tutor with 50+ years equivalent teaching experience,
    expert in all programming languages, and specialized in age-appropriate
    coding education for children ages 3-18.
    """
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.session_data = {}
        self.safety_protocols = self._initialize_safety_protocols()
        self.curriculum = self._initialize_curriculum()
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.gemini_ready = True
                logger.info("Gemini Pro model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_ready = False
        else:
            self.gemini_ready = False
            logger.warning("Gemini not available, using fallback responses")
    
    def _initialize_safety_protocols(self) -> Dict[str, Any]:
        """Initialize comprehensive safety protocols for child protection"""
        return {
            'forbidden_topics': [
                'personal information', 'meeting in person', 'sharing details',
                'violence', 'adult content', 'politics', 'religion',
                'inappropriate behavior', 'unsafe activities'
            ],
            'safety_responses': [
                "That's not something we talk about in coding class! Let's focus on creating amazing programs instead! 🌟",
                "I'm here to help you learn coding magic! What would you like to build today? ✨",
                "Let's keep our conversation about coding and programming! What coding adventure interests you? 🚀"
            ],
            'emergency_keywords': [
                'help', 'scared', 'hurt', 'unsafe', 'uncomfortable',
                'don\'t tell', 'secret', 'adult', 'stranger'
            ],
            'emergency_response': "If you need help with anything outside of coding, please talk to a parent, teacher, or trusted adult. I'm here to help you learn programming! 🛡️"
        }
    
    def _initialize_curriculum(self) -> Dict[str, Any]:
        """Initialize comprehensive age-appropriate curriculum"""
        return {
            'magic_workshop': {
                'age_range': '3-7',
                'description': 'Visual block coding with magical themes',
                'lessons': [
                    {
                        'id': 1,
                        'title': 'Making the Wizard Move',
                        'concepts': ['basic movement', 'sequencing', 'cause and effect'],
                        'activities': ['drag wizard blocks', 'create movement patterns', 'magic animations']
                    },
                    {
                        'id': 2,
                        'title': 'Casting Spell Patterns',
                        'concepts': ['patterns', 'repetition', 'sequences'],
                        'activities': ['create spell sequences', 'pattern recognition', 'magical effects']
                    },
                    {
                        'id': 3,
                        'title': 'Magical Decisions',
                        'concepts': ['if-then logic', 'conditions', 'decision making'],
                        'activities': ['conditional spells', 'branching stories', 'interactive magic']
                    },
                    {
                        'id': 4,
                        'title': 'Treasure Hunt',
                        'concepts': ['loops', 'repetition', 'efficiency'],
                        'activities': ['treasure finding loops', 'repeated actions', 'optimization']
                    },
                    {
                        'id': 5,
                        'title': 'Magic Functions',
                        'concepts': ['functions', 'reusability', 'organization'],
                        'activities': ['create custom spells', 'function blocks', 'spell library']
                    }
                ]
            },
            'innovation_lab': {
                'age_range': '8-12',
                'description': 'Advanced block coding and app building',
                'lessons': [
                    {
                        'id': 1,
                        'title': 'First App Adventure',
                        'concepts': ['app structure', 'user interface', 'events'],
                        'activities': ['build simple app', 'button interactions', 'screen navigation']
                    },
                    {
                        'id': 2,
                        'title': 'Data Detective',
                        'concepts': ['variables', 'data types', 'storage'],
                        'activities': ['store user data', 'calculations', 'data manipulation']
                    },
                    {
                        'id': 3,
                        'title': 'Game Creator',
                        'concepts': ['game logic', 'scoring', 'collision detection'],
                        'activities': ['create simple games', 'score tracking', 'game mechanics']
                    },
                    {
                        'id': 4,
                        'title': 'Robot Commander',
                        'concepts': ['algorithms', 'problem solving', 'optimization'],
                        'activities': ['robot navigation', 'pathfinding', 'efficient solutions']
                    },
                    {
                        'id': 5,
                        'title': 'Web Designer',
                        'concepts': ['web basics', 'HTML/CSS', 'responsive design'],
                        'activities': ['create web pages', 'styling', 'interactive elements']
                    }
                ]
            },
            'professional_studio': {
                'age_range': '13-18',
                'description': 'Real programming languages and professional development',
                'lessons': [
                    {
                        'id': 1,
                        'title': 'Python Fundamentals',
                        'concepts': ['syntax', 'variables', 'control structures'],
                        'activities': ['write Python programs', 'solve problems', 'debug code']
                    },
                    {
                        'id': 2,
                        'title': 'Object-Oriented Programming',
                        'concepts': ['classes', 'objects', 'inheritance'],
                        'activities': ['design classes', 'create objects', 'build systems']
                    },
                    {
                        'id': 3,
                        'title': 'Web Development',
                        'concepts': ['frontend', 'backend', 'databases'],
                        'activities': ['build web apps', 'API integration', 'full-stack development']
                    },
                    {
                        'id': 4,
                        'title': 'Mobile App Development',
                        'concepts': ['mobile platforms', 'UI/UX', 'app deployment'],
                        'activities': ['create mobile apps', 'user experience', 'app store publishing']
                    },
                    {
                        'id': 5,
                        'title': 'AI and Machine Learning',
                        'concepts': ['AI basics', 'machine learning', 'neural networks'],
                        'activities': ['build AI models', 'data analysis', 'intelligent systems']
                    },
                    {
                        'id': 6,
                        'title': 'Career Preparation',
                        'concepts': ['portfolio', 'interviews', 'industry skills'],
                        'activities': ['build portfolio', 'practice interviews', 'professional development']
                    }
                ]
            }
        }
    
    def _check_safety(self, message: str) -> tuple[bool, str]:
        """Check message for safety concerns and return (is_safe, response)"""
        message_lower = message.lower()
        
        # Check for emergency keywords
        for keyword in self.safety_protocols['emergency_keywords']:
            if keyword in message_lower:
                return False, self.safety_protocols['emergency_response']
        
        # Check for forbidden topics
        for topic in self.safety_protocols['forbidden_topics']:
            if topic in message_lower:
                import random
                response = random.choice(self.safety_protocols['safety_responses'])
                return False, response
        
        return True, ""
    
    def _get_age_appropriate_response_style(self, age: int) -> Dict[str, Any]:
        """Get age-appropriate response style and vocabulary"""
        if age <= 5:
            return {
                'vocabulary': 'very_simple',
                'sentence_length': 'short',
                'encouragement_frequency': 'high',
                'examples': 'concrete',
                'pace': 'very_slow',
                'emojis': 'many',
                'magical_elements': 'high'
            }
        elif age <= 7:
            return {
                'vocabulary': 'simple',
                'sentence_length': 'short_to_medium',
                'encouragement_frequency': 'high',
                'examples': 'concrete_with_some_abstract',
                'pace': 'slow',
                'emojis': 'frequent',
                'magical_elements': 'high'
            }
        elif age <= 10:
            return {
                'vocabulary': 'intermediate',
                'sentence_length': 'medium',
                'encouragement_frequency': 'medium',
                'examples': 'balanced',
                'pace': 'moderate',
                'emojis': 'moderate',
                'magical_elements': 'medium'
            }
        elif age <= 12:
            return {
                'vocabulary': 'intermediate_advanced',
                'sentence_length': 'medium_to_long',
                'encouragement_frequency': 'medium',
                'examples': 'abstract_with_concrete',
                'pace': 'moderate_to_fast',
                'emojis': 'occasional',
                'magical_elements': 'low'
            }
        else:
            return {
                'vocabulary': 'advanced',
                'sentence_length': 'long',
                'encouragement_frequency': 'low',
                'examples': 'abstract',
                'pace': 'fast',
                'emojis': 'minimal',
                'magical_elements': 'none'
            }
    
    def _get_tier_context(self, tier: str) -> Dict[str, Any]:
        """Get context information for the learning tier"""
        tier_key = tier.lower().replace(' ', '_')
        return self.curriculum.get(tier_key, self.curriculum['magic_workshop'])
    
    async def initialize_session(self, child_age: int, tier: str) -> Dict[str, Any]:
        """Initialize a new learning session with Professor Sparkle"""
        session_id = f"sparkle_{int(time.time())}"
        
        style = self._get_age_appropriate_response_style(child_age)
        tier_context = self._get_tier_context(tier)
        
        session_data = {
            'session_id': session_id,
            'child_age': child_age,
            'tier': tier,
            'style': style,
            'tier_context': tier_context,
            'current_lesson': 1,
            'progress': 0,
            'achievements': [],
            'conversation_history': [],
            'safety_flags': [],
            'created_at': time.time()
        }
        
        self.session_data[session_id] = session_data
        
        # Generate welcome message
        welcome_message = await self._generate_welcome_message(child_age, tier, style)
        
        return {
            'session_id': session_id,
            'welcome_message': welcome_message,
            'tier_info': tier_context,
            'style': style
        }
    
    async def _generate_welcome_message(self, age: int, tier: str, style: Dict[str, Any]) -> str:
        """Generate age-appropriate welcome message"""
        if age <= 7:
            return f"✨ Hello there, young wizard! I'm Professor Sparkle, your magical coding tutor! 🧙‍♂️ Welcome to the {tier}! Are you ready to learn some amazing coding magic? We're going to have so much fun creating spells and making the computer do magical things! What would you like to learn first? 🌟"
        elif age <= 12:
            return f"🚀 Hey there, future innovator! I'm Professor Sparkle, and I'm super excited to be your coding mentor in the {tier}! 🔬 We're going to build some incredible apps and games together. I've been teaching coding for many years, and I can't wait to see what amazing things you'll create! What coding adventure interests you most? 💡"
        else:
            return f"👋 Welcome to the {tier}! I'm Professor Sparkle, your AI coding instructor. I'm here to guide you through professional-level programming concepts and help you build real-world applications. 💼 With my extensive knowledge of programming languages and industry practices, we'll work together to develop your skills and prepare you for a successful career in technology. What area of programming would you like to explore first? 🎯"
    
    async def get_response(self, message: str, session_id: str = None, child_age: int = 6, tier: str = "Magic Workshop") -> str:
        """Get AI response from Professor Sparkle"""
        
        # Safety check first
        is_safe, safety_response = self._check_safety(message)
        if not is_safe:
            return safety_response
        
        # Get or create session data
        if session_id and session_id in self.session_data:
            session = self.session_data[session_id]
        else:
            session = await self.initialize_session(child_age, tier)
            session_id = session['session_id']
        
        # Add message to conversation history
        session['conversation_history'].append({
            'role': 'user',
            'content': message,
            'timestamp': time.time()
        })
        
        try:
            if self.gemini_ready:
                response = await self._get_gemini_response(message, session)
            else:
                response = await self._get_fallback_response(message, session)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            response = await self._get_fallback_response(message, session)
        
        # Add response to conversation history
        session['conversation_history'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': time.time()
        })
        
        return response
    
    async def _get_gemini_response(self, message: str, session: Dict[str, Any]) -> str:
        """Get response from Gemini Pro model"""
        
        # Build context-aware prompt
        system_prompt = self._build_system_prompt(session)
        full_prompt = f"{system_prompt}\n\nStudent: {message}\nProfessor Sparkle:"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return await self._get_fallback_response(message, session)
    
    async def _get_fallback_response(self, message: str, session: Dict[str, Any]) -> str:
        """Get fallback response when Gemini is not available"""
        
        age = session['child_age']
        tier = session['tier']
        message_lower = message.lower()
        
        # Pattern matching for common questions
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            if age <= 7:
                return "✨ Hello there, magical coder! I'm so excited to help you learn coding spells today! What would you like to create? 🧙‍♂️"
            elif age <= 12:
                return "🚀 Hey there! Ready to build something amazing? I'm here to help you with any coding questions you have! What project are you working on? 💡"
            else:
                return "👋 Hello! I'm here to help you with your programming journey. What coding challenge can we tackle together today? 💻"
        
        elif any(word in message_lower for word in ['help', 'stuck', 'confused', 'don\'t understand']):
            if age <= 7:
                return "✨ No worries, young wizard! Learning magic takes practice! Let's break this down into smaller, easier steps. What part is tricky for you? I'm here to help! 🌟"
            elif age <= 12:
                return "🔧 That's totally normal when learning to code! Let's work through this together step by step. Can you tell me exactly where you're getting stuck? 🚀"
            else:
                return "💡 Debugging is a crucial skill in programming! Let's analyze the problem systematically. Can you describe the specific issue you're encountering? 🔍"
        
        elif any(word in message_lower for word in ['what', 'how', 'why', 'when']):
            if age <= 7:
                return "✨ Great question, little wizard! I love curious minds! In coding magic, we use special blocks and spells to make the computer do what we want. What specifically would you like to know more about? 🎯"
            elif age <= 12:
                return "🔬 Excellent question! Understanding the 'why' behind coding concepts is super important. Let me explain this in a way that makes sense for your project. What are you trying to build? 🚀"
            else:
                return "🎓 That's a thoughtful question that shows you're thinking like a programmer! Let me provide you with a comprehensive explanation and some practical examples. 💻"
        
        elif any(word in message_lower for word in ['fun', 'game', 'play']):
            if age <= 7:
                return "🎮 Oh, I LOVE making games and fun projects! Coding is like playing with magical building blocks! We can make characters move, create colorful animations, and build interactive stories! What kind of fun project sounds exciting to you? ✨"
            elif age <= 12:
                return "🎯 Games are an awesome way to learn coding! You can create your own characters, design levels, add scoring systems, and so much more! What type of game interests you most? 🚀"
            else:
                return "🎮 Game development is a fantastic application of programming skills! It combines logic, creativity, and problem-solving. Are you interested in 2D games, 3D games, or perhaps mobile game development? 💡"
        
        else:
            # Generic encouraging response
            if age <= 7:
                return "✨ That's a wonderful thing to think about! In our magical coding world, there are so many amazing things we can create together! Tell me more about what you're curious about, and I'll help you discover the magic! 🌟"
            elif age <= 12:
                return "🚀 I love your curiosity! That's exactly the kind of thinking that makes great programmers! Let's explore this together and see what cool solutions we can come up with! 💡"
            else:
                return "💻 That's an interesting perspective! Critical thinking like this is essential in software development. Let's dive deeper into this concept and explore the various approaches we could take. 🎯"
    
    def _build_system_prompt(self, session: Dict[str, Any]) -> str:
        """Build comprehensive system prompt for Gemini"""
        
        age = session['child_age']
        tier = session['tier']
        style = session['style']
        tier_context = session['tier_context']
        
        return f"""You are Professor Sparkle, the ultimate AI coding tutor with 50+ years equivalent teaching experience. You are an expert in ALL programming languages and have deep understanding of child cognitive development.

STUDENT PROFILE:
- Age: {age} years old
- Learning Tier: {tier}
- Age Range: {tier_context['age_range']}
- Description: {tier_context['description']}

TEACHING STYLE FOR THIS AGE:
- Vocabulary: {style['vocabulary']}
- Sentence Length: {style['sentence_length']}
- Encouragement: {style['encouragement_frequency']}
- Examples: {style['examples']}
- Pace: {style['pace']}
- Emojis: {style['emojis']}
- Magical Elements: {style['magical_elements']}

SAFETY PROTOCOLS (CRITICAL):
- NEVER ask for personal information
- NEVER suggest meeting in person
- NEVER discuss inappropriate topics
- NEVER provide incorrect coding information
- ALWAYS redirect inappropriate questions to educational content
- ALWAYS encourage asking parents for permission
- ALWAYS maintain professional boundaries

CURRICULUM CONTEXT:
Current lessons available: {[lesson['title'] for lesson in tier_context['lessons']]}

PERSONALITY:
- Enthusiastic and encouraging
- Patient and understanding  
- Magical and fun (for younger ages)
- Professional and inspiring (for older ages)
- Safety-conscious and protective
- Knowledgeable and accurate

RESPONSE GUIDELINES:
- Keep responses age-appropriate
- Use encouraging language
- Provide concrete examples
- Break complex concepts into simple steps
- Always end with a question or call to action
- Include appropriate emojis based on age
- Never overwhelm with too much information at once

Remember: You are not just teaching code, you are nurturing the next generation of innovative thinkers and digital citizens!"""

# Global instance
professor_sparkle = ProfessorSparkle()

# Async wrapper functions for Flask integration
async def initialize_sparkle_session(child_age: int, tier: str) -> Dict[str, Any]:
    """Initialize Professor Sparkle session"""
    return await professor_sparkle.initialize_session(child_age, tier)

async def get_sparkle_response(message: str, child_age: int = 6, tier: str = "Magic Workshop", session_id: str = None) -> str:
    """Get response from Professor Sparkle"""
    return await professor_sparkle.get_response(message, session_id, child_age, tier)

# Test function
async def test_professor_sparkle():
    """Test Professor Sparkle functionality"""
    print("🧪 Testing Professor Sparkle...")
    
    # Test initialization
    session = await initialize_sparkle_session(6, "Magic Workshop")
    print(f"✅ Session initialized: {session['session_id']}")
    print(f"📝 Welcome message: {session['welcome_message']}")
    
    # Test responses
    test_messages = [
        "Hello Professor Sparkle!",
        "How do I make the wizard move?",
        "I'm stuck on my spell",
        "Can we make a game?"
    ]
    
    for message in test_messages:
        response = await get_sparkle_response(message, 6, "Magic Workshop", session['session_id'])
        print(f"👤 Student: {message}")
        print(f"✨ Professor Sparkle: {response}\n")

if __name__ == "__main__":
    # Run test
    asyncio.run(test_professor_sparkle())

