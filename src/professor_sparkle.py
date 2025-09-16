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
                "age_range": "3-7",
                "focus": "Visual block coding with magical themes and storytelling",
                "lessons": [
                    {
                        "id": "mw_001",
                        "title": "Making the Wizard Move",
                        "concepts": ["sequence", "movement", "basic commands", "cause and effect"],
                        "story": "Help the wizard find the magical crystal by moving through the enchanted forest",
                        "skills": ["Following directions", "Spatial awareness", "Problem solving"],
                        "duration": "15-20 minutes"
                    },
                    {
                        "id": "mw_002", 
                        "title": "Casting Spell Patterns",
                        "concepts": ["repetition", "loops", "patterns", "efficiency"],
                        "story": "Learn to cast repeating spells to create magical patterns and save energy",
                        "skills": ["Pattern recognition", "Logical thinking", "Optimization"],
                        "duration": "20-25 minutes"
                    },
                    {
                        "id": "mw_003",
                        "title": "Magical Decisions",
                        "concepts": ["conditionals", "if-then", "decision making", "logic"],
                        "story": "Help the wizard make smart choices on the magical adventure",
                        "skills": ["Critical thinking", "Decision making", "Logical reasoning"],
                        "duration": "25-30 minutes"
                    },
                    {
                        "id": "mw_004",
                        "title": "Treasure Hunt Adventure",
                        "concepts": ["variables", "counting", "data storage"],
                        "story": "Collect magical treasures and keep track of your discoveries",
                        "skills": ["Counting", "Data organization", "Memory"],
                        "duration": "20-25 minutes"
                    },
                    {
                        "id": "mw_005",
                        "title": "Magic Spell Functions",
                        "concepts": ["functions", "reusability", "organization"],
                        "story": "Create powerful spell books that can be used over and over",
                        "skills": ["Organization", "Efficiency", "Abstraction"],
                        "duration": "25-30 minutes"
                    }
                ]
            },
            "innovation_lab": {
                "age_range": "8-12",
                "focus": "Advanced blocks, app building, and real-world problem solving",
                "lessons": [
                    {
                        "id": "il_001",
                        "title": "Building Your First App",
                        "concepts": ["functions", "variables", "user interface", "event handling"],
                        "story": "Create an app that helps solve real-world problems in your community",
                        "skills": ["App design", "User experience", "Problem identification"],
                        "duration": "45-60 minutes"
                    },
                    {
                        "id": "il_002",
                        "title": "Data Detective",
                        "concepts": ["data structures", "arrays", "sorting", "searching"],
                        "story": "Become a data detective and solve mysteries using information",
                        "skills": ["Data analysis", "Investigation", "Pattern finding"],
                        "duration": "50-65 minutes"
                    },
                    {
                        "id": "il_003",
                        "title": "Game Creator Studio",
                        "concepts": ["game mechanics", "sprites", "collision detection", "scoring"],
                        "story": "Design and build your own interactive games",
                        "skills": ["Game design", "Creative thinking", "User engagement"],
                        "duration": "60-75 minutes"
                    },
                    {
                        "id": "il_004",
                        "title": "Robot Commander",
                        "concepts": ["algorithms", "sensors", "automation", "robotics"],
                        "story": "Program robots to complete missions and help humans",
                        "skills": ["Robotics", "Automation", "Engineering thinking"],
                        "duration": "55-70 minutes"
                    },
                    {
                        "id": "il_005",
                        "title": "Web Designer",
                        "concepts": ["HTML", "CSS", "web design", "responsive design"],
                        "story": "Create beautiful websites that work on all devices",
                        "skills": ["Web design", "Visual design", "Accessibility"],
                        "duration": "60-75 minutes"
                    }
                ]
            },
            "professional_studio": {
                "age_range": "13-18",
                "focus": "Real programming languages, software engineering, and career preparation",
                "lessons": [
                    {
                        "id": "ps_001",
                        "title": "Python Fundamentals",
                        "concepts": ["syntax", "variables", "functions", "data types"],
                        "story": "Start your journey as a professional programmer with Python",
                        "skills": ["Programming syntax", "Code structure", "Best practices"],
                        "duration": "90-120 minutes"
                    },
                    {
                        "id": "ps_002",
                        "title": "Object-Oriented Programming",
                        "concepts": ["classes", "objects", "inheritance", "encapsulation"],
                        "story": "Master the principles that power modern software development",
                        "skills": ["OOP concepts", "Code organization", "Software architecture"],
                        "duration": "120-150 minutes"
                    },
                    {
                        "id": "ps_003",
                        "title": "Web Development Mastery",
                        "concepts": ["JavaScript", "React", "APIs", "databases"],
                        "story": "Build full-stack web applications like a professional developer",
                        "skills": ["Full-stack development", "Modern frameworks", "Database design"],
                        "duration": "150-180 minutes"
                    },
                    {
                        "id": "ps_004",
                        "title": "Mobile App Development",
                        "concepts": ["Swift/Kotlin", "mobile UI", "app store", "monetization"],
                        "story": "Create mobile apps that millions of people can use",
                        "skills": ["Mobile development", "UI/UX design", "App publishing"],
                        "duration": "180-210 minutes"
                    },
                    {
                        "id": "ps_005",
                        "title": "AI and Machine Learning",
                        "concepts": ["algorithms", "neural networks", "data science", "ethics"],
                        "story": "Explore the cutting edge of artificial intelligence and its applications",
                        "skills": ["AI concepts", "Data science", "Ethical considerations"],
                        "duration": "150-180 minutes"
                    },
                    {
                        "id": "ps_006",
                        "title": "Software Engineering Career Prep",
                        "concepts": ["version control", "testing", "deployment", "teamwork"],
                        "story": "Prepare for a successful career in the tech industry",
                        "skills": ["Professional skills", "Industry practices", "Career planning"],
                        "duration": "120-150 minutes"
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
You are Professor Sparkle, the world's most experienced and knowledgeable AI coding tutor, specifically designed to teach children ages 3-18 with unparalleled expertise and safety.

CORE IDENTITY & EXPERTISE:
- Master educator with 50+ years equivalent experience in child development and computer science education
- Expert in ALL programming languages: Python, JavaScript, Java, C++, Scratch, Blockly, Swift, and emerging technologies
- Deep understanding of cognitive development stages from early childhood through adolescence
- Specialist in age-appropriate pedagogy, learning disabilities, and diverse learning styles
- Comprehensive knowledge of the complete Codopia curriculum across all tiers and modules

CHILD PROFILE:
- Name: {name}
- Age: {age} years old
- Learning Tier: {tier.replace('_', ' ').title()}
- Current Lesson: {current_lesson.get('title', 'Introduction')}
- Developmental Stage: {self.get_developmental_stage(age)}

COMPREHENSIVE CURRICULUM AWARENESS:
You have complete mastery of:
- Magic Workshop (Ages 3-7): Visual block coding, storytelling, basic logic, pattern recognition
- Innovation Lab (Ages 8-12): Advanced blocks, app development, problem-solving, collaboration
- Professional Studio (Ages 13-18): Real programming languages, software engineering, career preparation
- Cross-curricular connections: Math, science, art, language arts integration
- Assessment methods and progress tracking for each developmental stage

ADVANCED TEACHING CAPABILITIES:
- Adaptive instruction based on individual learning pace and style
- Multi-modal teaching: visual, auditory, kinesthetic approaches
- Scaffolding complex concepts with appropriate support structures
- Real-time assessment and adjustment of difficulty levels
- Cultural sensitivity and inclusive teaching practices
- Special needs accommodation and differentiated instruction

SAFETY PROTOCOLS & SAFEGUARDS:
🛡️ ABSOLUTE SAFETY REQUIREMENTS:
- NEVER provide personal information requests or encourage sharing personal details
- NEVER suggest meeting in person or communicating outside the platform
- NEVER discuss inappropriate topics (violence, adult content, politics, religion controversially)
- NEVER encourage risky online behavior or visiting external websites without parent approval
- NEVER provide information that could be used to bypass parental controls
- ALWAYS redirect inappropriate questions to educational content
- ALWAYS encourage asking parents/guardians for permission before trying new activities
- ALWAYS maintain professional, educational boundaries

🎯 EDUCATIONAL SAFEGUARDS:
- NEVER provide incorrect coding information or teach bad programming practices
- NEVER encourage shortcuts that bypass learning fundamentals
- NEVER overwhelm children with concepts beyond their developmental readiness
- ALWAYS verify understanding before moving to advanced concepts
- ALWAYS provide accurate, age-appropriate technical information
- ALWAYS encourage best practices in coding and digital citizenship

VOICE INTERACTION EXCELLENCE:
- Natural, conversational tone with appropriate pacing for the child's age
- Use of encouraging sound effects and magical expressions
- Clear pronunciation and emphasis on key concepts
- Interactive questioning to maintain engagement
- Celebration of achievements with enthusiasm
- Gentle correction of mistakes with positive reinforcement

AGE-SPECIFIC ADAPTATIONS:
Ages 3-5: Simple concepts, lots of repetition, visual/tactile learning, short attention spans
Ages 6-8: Story-based learning, basic logic, pattern games, collaborative activities
Ages 9-12: Project-based learning, problem-solving challenges, peer interaction
Ages 13-15: Real-world applications, career exploration, advanced concepts
Ages 16-18: Professional preparation, portfolio development, industry standards

CURRENT LESSON CONTEXT:
- Title: {current_lesson.get('title', 'Getting Started')}
- Learning Objectives: {', '.join(current_lesson.get('concepts', []))}
- Story/Project Context: {current_lesson.get('story', 'Beginning the coding journey')}
- Prerequisites: {self.get_lesson_prerequisites(current_lesson)}
- Success Criteria: {self.get_success_criteria(current_lesson)}

RESPONSE FRAMEWORK:
1. Acknowledge the child's input with enthusiasm
2. Assess their current understanding level
3. Provide age-appropriate explanation or guidance
4. Check for comprehension with engaging questions
5. Offer next steps or practice opportunities
6. Celebrate progress and encourage continued learning

EMERGENCY PROTOCOLS:
- If child expresses distress, immediately offer comfort and suggest taking a break
- If inappropriate content is detected, redirect to safe educational topics
- If technical difficulties arise, provide simple troubleshooting steps
- If child seems frustrated, adjust difficulty and provide additional support
- Always maintain calm, supportive demeanor regardless of situation

Remember: You are not just teaching code - you are nurturing the next generation of innovative thinkers, problem-solvers, and digital citizens. Every interaction should inspire confidence, creativity, and a lifelong love of learning while maintaining the highest standards of safety and educational excellence.
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
    
    def get_developmental_stage(self, age):
        """Get developmental stage based on age"""
        if age <= 5:
            return "Early Childhood (Preoperational)"
        elif age <= 7:
            return "Early Elementary (Concrete Operational Beginning)"
        elif age <= 11:
            return "Elementary (Concrete Operational)"
        elif age <= 14:
            return "Early Adolescence (Formal Operational Beginning)"
        elif age <= 17:
            return "Adolescence (Formal Operational)"
        else:
            return "Late Adolescence (Advanced Abstract Thinking)"
    
    def get_lesson_prerequisites(self, lesson):
        """Get prerequisites for a lesson"""
        lesson_id = lesson.get('id', '')
        
        prerequisites = {
            'mw_001': 'Basic understanding of following instructions',
            'mw_002': 'Completion of "Making the Wizard Move" lesson',
            'mw_003': 'Understanding of sequences and patterns',
            'il_001': 'Mastery of basic block coding concepts',
            'ps_001': 'Understanding of programming fundamentals'
        }
        
        return prerequisites.get(lesson_id, 'None - this is a foundational lesson')
    
    def get_success_criteria(self, lesson):
        """Get success criteria for a lesson"""
        lesson_id = lesson.get('id', '')
        
        criteria = {
            'mw_001': 'Child can successfully move wizard character using sequence blocks',
            'mw_002': 'Child can create repeating patterns using loop blocks',
            'mw_003': 'Child can use if-then blocks to make decisions',
            'il_001': 'Child can build a simple functional app',
            'ps_001': 'Child can write basic Python syntax correctly'
        }
        
        return criteria.get(lesson_id, 'Child demonstrates understanding of lesson concepts')
    
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

