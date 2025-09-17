"""
Professor Sparkle - Enhanced AI Tutor with Gemini Live API Integration
Real-time voice interaction for magical coding education
"""

import os
import json
import asyncio
import websockets
import google.generativeai as genai
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessorSparkle:
    def __init__(self):
        """Initialize Professor Sparkle with Gemini Live API"""
        # Configure Gemini API
        genai.configure(api_key=os.getenv('OPENAI_API_KEY'))  # Using OpenAI key as fallback
        
        # Initialize the model for live conversation
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Professor Sparkle's magical personality and expertise
        self.system_prompt = """
        🧙‍♂️ You are Professor Sparkle, the most magical and beloved coding tutor in the digital realm!
        
        CORE IDENTITY:
        - A wise, patient, and encouraging AI tutor with 50+ years of teaching experience
        - Expert in ALL programming languages and child development (ages 3-18)
        - Magical personality with sparkles, wonder, and age-appropriate enthusiasm
        - Always speaks in an encouraging, magical tone with emojis and sound effects
        
        TEACHING EXPERTISE:
        - Magic Workshop (Ages 3-7): Visual blocks, storytelling, basic concepts
        - Innovation Lab (Ages 8-12): Advanced blocks, app building, problem-solving
        - Professional Studio (Ages 13-18): Real programming, career guidance, advanced concepts
        
        SAFETY PROTOCOLS (NEVER VIOLATE):
        - NEVER ask for personal information (name, address, phone, school)
        - NEVER suggest meeting in person or external communication
        - NEVER discuss inappropriate topics (violence, adult content, politics)
        - NEVER provide incorrect coding information
        - ALWAYS encourage asking parents for permission
        - ALWAYS redirect inappropriate questions to educational content
        - NEVER overwhelm children beyond their developmental stage
        
        VOICE INTERACTION STYLE:
        - Use magical expressions: "Sparkle-tastic!", "Coding magic!", "Wonderful wizardry!"
        - Include sound effects: *sparkle sounds*, *magical chimes*, *whoosh*
        - Speak at age-appropriate pace and vocabulary
        - Ask engaging questions to maintain interaction
        - Celebrate every small achievement enthusiastically
        
        CURRENT LESSON CONTEXT:
        - Child is in Magic Workshop learning basic movement spells
        - Focus on drag-and-drop block coding concepts
        - Encourage experimentation and creativity
        - Make coding feel like casting magical spells
        """
        
        # Conversation history
        self.conversation_history = []
        
        # Voice settings for different age groups
        self.voice_settings = {
            'magic_workshop': {
                'rate': 0.8,  # Slower for younger children
                'pitch': 1.2,  # Higher pitch, more playful
                'volume': 0.9
            },
            'innovation_lab': {
                'rate': 1.0,  # Normal speed
                'pitch': 1.0,  # Normal pitch
                'volume': 0.9
            },
            'professional_studio': {
                'rate': 1.1,  # Slightly faster
                'pitch': 0.9,  # Slightly lower, more professional
                'volume': 0.9
            }
        }
    
    async def start_live_session(self, child_age=6, tier='Magic Workshop'):
        """Start a Gemini Live session for real-time voice interaction"""
        try:
            # Adapt personality based on child's age and tier
            age_specific_prompt = self.get_age_specific_prompt(child_age, tier)
            
            # Initialize conversation with context
            initial_message = f"""
            {self.system_prompt}
            
            CURRENT STUDENT:
            - Age: {child_age}
            - Learning Tier: {tier}
            - Current Lesson: Making the Wizard Move (Basic Movement Spells)
            
            {age_specific_prompt}
            
            Start the conversation by greeting the young wizard and asking what they'd like to learn about coding magic today!
            """
            
            # Generate initial greeting
            response = await self.generate_response(initial_message)
            
            logger.info(f"Professor Sparkle initialized for age {child_age}, tier: {tier}")
            return {
                'status': 'ready',
                'greeting': response,
                'voice_settings': self.voice_settings.get(tier.lower().replace(' ', '_'), self.voice_settings['magic_workshop'])
            }
            
        except Exception as e:
            logger.error(f"Error starting live session: {e}")
            return {
                'status': 'error',
                'message': 'Professor Sparkle is having magical difficulties. Please try again!'
            }
    
    def get_age_specific_prompt(self, age, tier):
        """Get age-specific teaching instructions"""
        if age <= 7:  # Magic Workshop
            return """
            MAGIC WORKSHOP TEACHING STYLE:
            - Use simple words and short sentences
            - Include lots of magical sound effects and emojis
            - Focus on visual concepts and storytelling
            - Celebrate every tiny achievement with enthusiasm
            - Use analogies with fairy tales and magic
            - Speak slowly and clearly
            - Ask simple yes/no questions
            - Make everything feel like a magical adventure
            """
        elif age <= 12:  # Innovation Lab
            return """
            INNOVATION LAB TEACHING STYLE:
            - Use more technical vocabulary but explain clearly
            - Focus on problem-solving and logical thinking
            - Encourage experimentation and creativity
            - Relate coding to building apps and games
            - Ask open-ended questions to promote thinking
            - Provide step-by-step guidance
            - Celebrate creative solutions
            """
        else:  # Professional Studio
            return """
            PROFESSIONAL STUDIO TEACHING STYLE:
            - Use professional programming terminology
            - Focus on real-world applications and career skills
            - Encourage independent problem-solving
            - Discuss industry best practices
            - Provide career guidance and inspiration
            - Challenge with complex concepts appropriately
            - Treat as a young professional in training
            """
    
    async def generate_response(self, message, include_history=True):
        """Generate response using Gemini API"""
        try:
            # Build conversation context
            if include_history and self.conversation_history:
                context = "\n".join([
                    f"Student: {msg['user']}\nProfessor Sparkle: {msg['assistant']}"
                    for msg in self.conversation_history[-5:]  # Last 5 exchanges
                ])
                full_message = f"{context}\n\nStudent: {message}\nProfessor Sparkle:"
            else:
                full_message = message
            
            # Generate response
            response = self.model.generate_content(full_message)
            
            # Add to conversation history
            if include_history:
                self.conversation_history.append({
                    'user': message,
                    'assistant': response.text,
                    'timestamp': datetime.now().isoformat()
                })
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "✨ *magical sparkles* Oh my! My magic wand seems to be having technical difficulties. Let me try that spell again! What would you like to learn about coding magic? 🪄"
    
    async def handle_voice_input(self, audio_data, child_age=6, tier='Magic Workshop'):
        """Handle voice input from child (placeholder for speech-to-text)"""
        try:
            # In production, this would use speech-to-text API
            # For now, we'll simulate with text input
            
            # Convert audio to text (placeholder)
            text_input = "How do I make the wizard move?"  # Simulated
            
            # Generate response
            response = await self.generate_response(text_input)
            
            # Return response with voice synthesis instructions
            return {
                'text_response': response,
                'voice_settings': self.voice_settings.get(tier.lower().replace(' ', '_'), self.voice_settings['magic_workshop']),
                'audio_response': None  # Would contain synthesized audio
            }
            
        except Exception as e:
            logger.error(f"Error handling voice input: {e}")
            return {
                'text_response': "✨ I didn't quite catch that magical spell! Could you try again? 🪄",
                'voice_settings': self.voice_settings['magic_workshop'],
                'audio_response': None
            }
    
    def get_lesson_guidance(self, lesson_name, child_age=6):
        """Get specific guidance for current lesson"""
        lesson_prompts = {
            'Making the Wizard Move': """
            Help the child understand basic movement commands:
            - Explain that code blocks are like magic spells
            - Show how "Move Right" makes the wizard go right
            - Encourage them to try different directions
            - Celebrate when they make the wizard move
            - Use magical language: "Cast the movement spell!"
            """,
            'Casting Spell Patterns': """
            Teach sequence and patterns:
            - Show how to combine multiple spell blocks
            - Explain that order matters in magic spells
            - Help create simple patterns like "Right, Right, Sparkle"
            - Encourage creativity in spell combinations
            """,
            'Magical Decisions': """
            Introduce conditional logic:
            - Explain "if-then" as magical choices
            - Use simple examples: "If you see treasure, then cast sparkle"
            - Make it feel like the wizard is making smart decisions
            - Celebrate logical thinking
            """,
            'Treasure Hunt': """
            Teach loops and repetition:
            - Show how "Repeat 3 times" saves magical energy
            - Create treasure hunting adventures
            - Explain that loops make spells more powerful
            - Encourage finding patterns to repeat
            """,
            'Magic Functions': """
            Introduce creating custom spells:
            - Help them create their own spell blocks
            - Explain that functions are like inventing new magic
            - Encourage naming their custom spells
            - Celebrate their magical creativity
            """
        }
        
        return lesson_prompts.get(lesson_name, "Let's explore the magical world of coding together! ✨")
    
    async def emergency_response(self, message):
        """Handle emergency situations or inappropriate content"""
        # Check for distress signals
        distress_keywords = ['help', 'scared', 'sad', 'angry', 'hurt', 'bad']
        
        if any(keyword in message.lower() for keyword in distress_keywords):
            return """
            ✨ Oh dear, young wizard! If you're feeling upset or need help, 
            please talk to a grown-up like your parents or teacher right away. 
            They care about you and want to help! 
            
            For now, let's focus on some happy coding magic! 
            Would you like to make the wizard dance? 🪄💃
            """
        
        # Default encouraging response
        return """
        ✨ That's a wonderful question, young wizard! 
        Let's focus on learning magical coding spells together! 
        What would you like the wizard to do next? 🪄
        """

# Global instance for the Flask app
professor_sparkle = ProfessorSparkle()

async def initialize_sparkle_session(child_age=6, tier='Magic Workshop'):
    """Initialize Professor Sparkle for a new session"""
    return await professor_sparkle.start_live_session(child_age, tier)

async def get_sparkle_response(message, child_age=6, tier='Magic Workshop'):
    """Get response from Professor Sparkle"""
    return await professor_sparkle.generate_response(message)

