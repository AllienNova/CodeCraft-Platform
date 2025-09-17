from flask import Flask, request, jsonify, redirect, make_response
from flask_socketio import SocketIO, emit
import hashlib
import jwt
from datetime import datetime, timedelta
import os
import asyncio
import json
from gemini_live_sparkle import professor_sparkle, initialize_sparkle_session, get_sparkle_response

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory user storage (replace with database in production)
users = []

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Codopia - Where Code Becomes Craft</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            @keyframes pulse-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
                50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
            }
            .float { animation: float 6s ease-in-out infinite; }
            .pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
        </style>
    </head>
    <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <!-- Navigation -->
        <nav class="bg-white/90 backdrop-blur-md shadow-lg sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center space-x-2">
                        <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                            <span class="text-white text-xl font-bold">C</span>
                        </div>
                        <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Codopia</span>
                    </div>
                    <div class="hidden md:flex items-center space-x-8">
                        <a href="#" class="text-gray-700 hover:text-purple-600 font-medium">Home</a>
                        <a href="#features" class="text-gray-700 hover:text-purple-600 font-medium">Features</a>
                        <a href="#tiers" class="text-gray-700 hover:text-purple-600 font-medium">Learning Tiers</a>
                        <a href="#about" class="text-gray-700 hover:text-purple-600 font-medium">About</a>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/signin" class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full hover:from-purple-600 hover:to-pink-600 transition-all">Sign In</a>
                        <a href="/signup" class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-full hover:from-blue-600 hover:to-purple-600 transition-all">Start Free Trial</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="relative py-20 overflow-hidden">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="space-y-8">
                        <div class="inline-block bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-semibold">
                            🚨 URGENT: Only 91 Beta Spots Left - Filling Fast!
                        </div>
                        
                        <h1 class="text-5xl lg:text-6xl font-bold leading-tight">
                            Your Child's <br>
                            <span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Coding Adventure</span> <br>
                            Starts Here
                        </h1>
                        
                        <p class="text-xl text-gray-600 leading-relaxed">
                            <span class="text-purple-600 font-semibold">Don't let your child fall behind</span> in the digital revolution. Transform 
                            them into a confident programmer through magical adventures, real 
                            app building, and professional development skills.
                        </p>
                        
                        <div class="flex items-center space-x-6">
                            <div class="flex items-center space-x-2">
                                <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">Ages 5-15</span>
                                <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">100% Safe</span>
                                <span class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">Irresistibly Fun</span>
                            </div>
                        </div>
                        
                        <div class="flex items-center space-x-4">
                            <div class="flex -space-x-2">
                                <div class="w-10 h-10 bg-purple-400 rounded-full border-2 border-white"></div>
                                <div class="w-10 h-10 bg-pink-400 rounded-full border-2 border-white"></div>
                                <div class="w-10 h-10 bg-blue-400 rounded-full border-2 border-white"></div>
                                <div class="w-10 h-10 bg-green-400 rounded-full border-2 border-white"></div>
                                <div class="w-10 h-10 bg-yellow-400 rounded-full border-2 border-white"></div>
                            </div>
                            <div>
                                <div class="flex items-center space-x-1">
                                    <span class="text-yellow-400">⭐⭐⭐⭐⭐</span>
                                    <span class="font-semibold">4.9/5 rating</span>
                                </div>
                                <p class="text-sm text-gray-600">From real parents</p>
                            </div>
                        </div>
                        
                        <div class="bg-orange-50 border-l-4 border-orange-400 p-4 rounded-lg">
                            <div class="flex items-center">
                                <div class="flex-shrink-0">
                                    <span class="text-orange-400 text-xl">⚠️</span>
                                </div>
                                <div class="ml-3">
                                    <p class="text-orange-800">
                                        <strong>Warning:</strong> Software developer salaries average $107,000+. Children who start coding 
                                        early have a <strong>300% advantage</strong> in future earnings.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="relative">
                        <div class="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-8 text-white pulse-glow">
                            <div class="text-center mb-6">
                                <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4">
                                    <span class="text-purple-500 text-2xl">✨</span>
                                </div>
                                <h3 class="text-2xl font-bold mb-2">Join Codopia NOW</h3>
                                <p class="text-purple-100">Be among the first 99 families to experience the future of coding education by 
                                Requesting Early Access Now. DON'T LET YOUR CHILD FALL BEHIND</p>
                                <div class="mt-4 bg-purple-600 text-white px-4 py-2 rounded-lg inline-block">
                                    🔥 LIVE: Join the first wave of beta testers!
                                </div>
                            </div>
                            
                            <form action="/signup" method="GET" class="space-y-4">
                                <div>
                                    <label class="block text-purple-100 text-sm font-medium mb-2">Parent Email Address</label>
                                    <input type="email" name="email" placeholder="your.email@example.com" 
                                           class="w-full px-4 py-3 rounded-lg text-gray-900 focus:ring-2 focus:ring-white focus:outline-none">
                                </div>
                                
                                <div>
                                    <label class="block text-purple-100 text-sm font-medium mb-2">Child's Age (This determines their learning tier)</label>
                                    <select name="age" class="w-full px-4 py-3 rounded-lg text-gray-900 focus:ring-2 focus:ring-white focus:outline-none">
                                        <option>Select age to unlock their perfect tier...</option>
                                        <option value="5">5 years old → Magic Workshop</option>
                                        <option value="6">6 years old → Magic Workshop</option>
                                        <option value="7">7 years old → Magic Workshop</option>
                                        <option value="8">8 years old → Innovation Lab</option>
                                        <option value="9">9 years old → Innovation Lab</option>
                                        <option value="10">10 years old → Innovation Lab</option>
                                        <option value="11">11 years old → Innovation Lab</option>
                                        <option value="12">12 years old → Innovation Lab</option>
                                        <option value="13">13 years old → Professional Studio</option>
                                        <option value="14">14 years old → Professional Studio</option>
                                        <option value="15">15 years old → Professional Studio</option>
                                    </select>
                                </div>
                                
                                <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-6 rounded-lg transition-all text-lg">
                                    🔒 SECURE MY CHILD'S FUTURE - FREE TRIAL
                                </button>
                                
                                <div class="text-center text-purple-100 text-sm space-y-1">
                                    <div class="flex items-center justify-center space-x-4">
                                        <span>🛡️ Your information is encrypted and will never be shared</span>
                                    </div>
                                    <div class="flex items-center justify-center space-x-4">
                                        <span>⚡ Instant Access</span>
                                        <span>🚫 No Commitment</span>
                                        <span>❌ Cancel Anytime</span>
                                    </div>
                                </div>
                            </form>
                        </div>
                        
                        <div class="mt-6 bg-gradient-to-r from-orange-500 to-red-500 text-white p-4 rounded-xl text-center">
                            <div class="flex items-center justify-center space-x-2">
                                <span class="text-xl">🚨</span>
                                <span class="font-bold">URGENT: Only 91 Beta Spots Remaining</span>
                            </div>
                            <p class="text-sm mt-1">⚠️ Spots are filling every few minutes - Don't wait!</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Three Tiers Section -->
        <section id="tiers" class="py-20 bg-white/50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-16">
                    <h2 class="text-4xl font-bold text-gray-900 mb-4">
                        Three Magical Tiers That <span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Grow With Your Child</span>
                    </h2>
                    <p class="text-xl text-gray-600 max-w-3xl mx-auto">
                        From magical adventures to professional development, each tier is scientifically 
                        designed for your child's cognitive development stage
                    </p>
                </div>
                
                <div class="grid md:grid-cols-3 gap-8">
                    <!-- Magic Workshop -->
                    <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 border border-purple-200 hover:shadow-xl transition-all">
                        <div class="text-center mb-6">
                            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-white text-2xl">🎨</span>
                            </div>
                            <h3 class="text-2xl font-bold text-purple-700 mb-2">Magic Workshop</h3>
                            <p class="text-purple-600 font-semibold">Ages 5-7 • Visual Block Coding</p>
                        </div>
                        
                        <div class="space-y-4">
                            <div class="flex items-center space-x-3">
                                <span class="text-purple-500">🧙‍♂️</span>
                                <span>Ready for Magic Workshop</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-purple-500">✨</span>
                                <span>Drag-and-drop spell blocks</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-purple-500">🎭</span>
                                <span>Interactive storytelling</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-purple-500">🏆</span>
                                <span>Achievement badges</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Innovation Lab -->
                    <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 border border-blue-200 hover:shadow-xl transition-all">
                        <div class="text-center mb-6">
                            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-white text-2xl">🔬</span>
                            </div>
                            <h3 class="text-2xl font-bold text-blue-700 mb-2">Innovation Lab</h3>
                            <p class="text-blue-600 font-semibold">Ages 8-12 • Advanced Blocks</p>
                        </div>
                        
                        <div class="space-y-4">
                            <div class="flex items-center space-x-3">
                                <span class="text-blue-500">🚀</span>
                                <span>Ready for Innovation Lab</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-blue-500">📱</span>
                                <span>Build real mobile apps</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-blue-500">🎮</span>
                                <span>Create interactive games</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-blue-500">🏆</span>
                                <span>Advanced achievements</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Professional Studio -->
                    <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 border border-green-200 hover:shadow-xl transition-all">
                        <div class="text-center mb-6">
                            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-white text-2xl">💼</span>
                            </div>
                            <h3 class="text-2xl font-bold text-green-700 mb-2">Professional Studio</h3>
                            <p class="text-green-600 font-semibold">Ages 13+ • Real Programming</p>
                        </div>
                        
                        <div class="space-y-4">
                            <div class="flex items-center space-x-3">
                                <span class="text-green-500">💻</span>
                                <span>Ready for Professional Studio</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-green-500">🌐</span>
                                <span>Full-stack web development</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-green-500">🤖</span>
                                <span>AI and machine learning</span>
                            </div>
                            <div class="flex items-center space-x-3">
                                <span class="text-green-500">🎓</span>
                                <span>Career preparation</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </body>
    </html>
    '''

# Authentication routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Start Free Trial - Codopia</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
            <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div class="max-w-md w-full space-y-8">
                    <div class="text-center">
                        <a href="/" class="inline-flex items-center text-purple-600 hover:text-purple-800 mb-8">
                            ← Back to Home
                        </a>
                        <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Start Your Free Trial</h2>
                        <p class="mt-2 text-gray-600">Create your account and add your child's profile</p>
                    </div>
                    
                    <form action="/signup" method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="parent_name" class="block text-sm font-medium text-gray-700">Parent Full Name</label>
                            <input id="parent_name" name="parent_name" type="text" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="John Smith">
                        </div>
                        
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="parent@example.com">
                        </div>
                        
                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                            <input id="password" name="password" type="password" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="Create a secure password">
                        </div>
                        
                        <div>
                            <label for="child_name" class="block text-sm font-medium text-gray-700">Child's Name</label>
                            <input id="child_name" name="child_name" type="text" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="Emma Smith">
                        </div>
                        
                        <div>
                            <label for="child_age" class="block text-sm font-medium text-gray-700">Child's Age (This determines their learning tier)</label>
                            <select id="child_age" name="child_age" required 
                                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                                <option value="">Select age to unlock their perfect tier...</option>
                                <option value="3">3 years old → Magic Workshop</option>
                                <option value="4">4 years old → Magic Workshop</option>
                                <option value="5">5 years old → Magic Workshop</option>
                                <option value="6">6 years old → Magic Workshop</option>
                                <option value="7">7 years old → Magic Workshop</option>
                                <option value="8">8 years old → Innovation Lab</option>
                                <option value="9">9 years old → Innovation Lab</option>
                                <option value="10">10 years old → Innovation Lab</option>
                                <option value="11">11 years old → Innovation Lab</option>
                                <option value="12">12 years old → Innovation Lab</option>
                                <option value="13">13 years old → Professional Studio</option>
                                <option value="14">14 years old → Professional Studio</option>
                                <option value="15">15 years old → Professional Studio</option>
                                <option value="16">16 years old → Professional Studio</option>
                                <option value="17">17 years old → Professional Studio</option>
                                <option value="18">18 years old → Professional Studio</option>
                            </select>
                        </div>
                        
                        <button type="submit" 
                                class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                            🔒 SECURE MY CHILD'S FUTURE - FREE TRIAL
                        </button>
                        
                        <div class="text-center text-sm text-gray-600 space-y-2">
                            <div>🛡️ Your information is encrypted and will never be shared</div>
                            <div class="flex justify-center space-x-4">
                                <span>⚡ Instant Access</span>
                                <span>🚫 No Commitment</span>
                                <span>❌ Cancel Anytime</span>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <span class="text-sm text-gray-600">Already have an account? </span>
                            <a href="/signin" class="text-sm text-purple-600 hover:text-purple-800">Sign In</a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # Handle POST request
    data = request.form
    parent_name = data.get('parent_name')
    email = data.get('email')
    password = data.get('password')
    child_name = data.get('child_name')
    child_age = int(data.get('child_age'))
    
    # Determine tier based on age
    if child_age <= 7:
        tier = 'Magic Workshop'
    elif child_age <= 12:
        tier = 'Innovation Lab'
    else:
        tier = 'Professional Studio'
    
    # Hash password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Create user
    user = {
        'id': len(users) + 1,
        'parent_name': parent_name,
        'email': email,
        'password_hash': password_hash,
        'children': [{
            'name': child_name,
            'age': child_age,
            'tier': tier,
            'progress': 0,
            'achievements': 0
        }],
        'created_at': datetime.now().isoformat()
    }
    
    users.append(user)
    
    # Create JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.secret_key, algorithm='HS256')
    
    # Create response and set cookie
    response = make_response(redirect('/dashboard'))
    response.set_cookie('auth_token', token, max_age=30*24*60*60, httponly=True)
    
    return response

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sign In - Codopia</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
            <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div class="max-w-md w-full space-y-8">
                    <div class="text-center">
                        <a href="/" class="inline-flex items-center text-purple-600 hover:text-purple-800 mb-8">
                            ← Back to Home
                        </a>
                        <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Welcome Back</h2>
                        <p class="mt-2 text-gray-600">Sign in to your Codopia account</p>
                    </div>
                    
                    <form action="/signin" method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="your.email@example.com">
                        </div>
                        
                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                            <input id="password" name="password" type="password" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="Enter your password">
                        </div>
                        
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <input id="remember_me" name="remember_me" type="checkbox" 
                                       class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded">
                                <label for="remember_me" class="ml-2 block text-sm text-gray-900">Remember me</label>
                            </div>
                            <div class="text-sm">
                                <a href="/forgot-password" class="text-purple-600 hover:text-purple-800">Forgot your password?</a>
                            </div>
                        </div>
                        
                        <button type="submit" 
                                class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                            Sign In
                        </button>
                        
                        <div class="text-center">
                            <span class="text-sm text-gray-600">Don't have an account? </span>
                            <a href="/signup" class="text-sm text-purple-600 hover:text-purple-800">Create Account</a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # Handle POST request
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    # Hash password for comparison
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Find user
    user = next((u for u in users if u['email'] == email and u['password_hash'] == password_hash), None)
    
    if user:
        # Create JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.secret_key, algorithm='HS256')
        
        # Create response and set cookie
        response = make_response(redirect('/dashboard'))
        response.set_cookie('auth_token', token, max_age=30*24*60*60, httponly=True)
        
        return response
    else:
        return redirect('/signin?error=invalid_credentials')

@app.route('/dashboard')
def dashboard():
    # Get user from token
    token = request.cookies.get('auth_token')
    if not token:
        return redirect('/signin')
    
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user = next((u for u in users if u['id'] == payload['user_id']), None)
        if not user:
            return redirect('/signin')
    except:
        return redirect('/signin')
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Codopia</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <!-- Navigation -->
        <nav class="bg-white/90 backdrop-blur-md shadow-lg">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center space-x-2">
                        <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                            <span class="text-white text-xl font-bold">C</span>
                        </div>
                        <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Codopia</span>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-gray-700">Welcome, {user['parent_name']}</span>
                        <a href="/signout" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600">Sign Out</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-2">Your Children's Learning Dashboard</h1>
            <p class="text-gray-600 mb-8">Track progress, manage profiles, and access learning environments</p>
            
            <div class="grid lg:grid-cols-3 gap-8">
                <!-- Children Cards -->
                <div class="lg:col-span-2 space-y-6">
                    {generate_children_cards(user['children'])}
                    
                    <!-- Add Another Child -->
                    <div class="bg-white rounded-xl p-6 border-2 border-dashed border-purple-300 hover:border-purple-500 transition-all cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span class="text-purple-500 text-2xl">+</span>
                            </div>
                            <h3 class="text-xl font-semibold text-purple-700 mb-2">Add Another Child</h3>
                            <p class="text-gray-600">Create a profile for another child to start their coding journey</p>
                        </div>
                    </div>
                </div>
                
                <!-- Stats Sidebar -->
                <div class="space-y-6">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-white rounded-xl p-6 text-center">
                            <div class="text-3xl font-bold text-purple-600">{len(user['children'])}</div>
                            <div class="text-gray-600">Active Children</div>
                        </div>
                        <div class="bg-white rounded-xl p-6 text-center">
                            <div class="text-3xl font-bold text-blue-600">{sum(child.get('achievements', 0) for child in user['children'])}</div>
                            <div class="text-gray-600">Total Achievements</div>
                        </div>
                        <div class="bg-white rounded-xl p-6 text-center">
                            <div class="text-3xl font-bold text-green-600">{sum(child.get('progress', 0) for child in user['children']) // len(user['children']) if user['children'] else 0}%</div>
                            <div class="text-gray-600">Average Progress</div>
                        </div>
                        <div class="bg-white rounded-xl p-6 text-center">
                            <div class="text-3xl font-bold text-pink-600">7</div>
                            <div class="text-gray-600">Days Active</div>
                        </div>
                    </div>
                    
                    <!-- Recent Activity -->
                    <div class="bg-white rounded-xl p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
                        <div class="space-y-3">
                            <div class="flex items-center space-x-3">
                                <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                                    <span class="text-purple-600 text-sm">🎉</span>
                                </div>
                                <div>
                                    <p class="text-sm font-medium">Welcome to Codopia!</p>
                                    <p class="text-xs text-gray-500">Your coding adventure begins now. Start with your first lesson!</p>
                                    <p class="text-xs text-gray-400">Just now</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

def generate_children_cards(children):
    cards = []
    for child in children:
        tier_colors = {
            'Magic Workshop': 'from-purple-500 to-pink-500',
            'Innovation Lab': 'from-blue-500 to-indigo-500',
            'Professional Studio': 'from-green-500 to-emerald-500'
        }
        
        tier_icons = {
            'Magic Workshop': '🎨',
            'Innovation Lab': '🔬',
            'Professional Studio': '💼'
        }
        
        color = tier_colors.get(child['tier'], 'from-gray-500 to-gray-600')
        icon = tier_icons.get(child['tier'], '🎓')
        
        card = f'''
        <div class="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                    <div class="w-12 h-12 bg-gradient-to-r {color} rounded-full flex items-center justify-center">
                        <span class="text-white text-xl">{icon}</span>
                    </div>
                    <div>
                        <h3 class="text-xl font-semibold text-gray-900">{child['name']}</h3>
                        <p class="text-gray-600">Age {child['age']} • {child['tier']}</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-2xl font-bold text-purple-600">{child.get('progress', 0)}%</div>
                    <div class="text-sm text-gray-600">Progress</div>
                </div>
            </div>
            
            <div class="mb-4">
                <div class="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Learning Progress</span>
                    <span>{child.get('progress', 0)}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-gradient-to-r {color} h-2 rounded-full" style="width: {child.get('progress', 0)}%"></div>
                </div>
            </div>
            
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-4">
                    <div class="text-center">
                        <div class="text-lg font-semibold text-yellow-600">{child.get('achievements', 0)}</div>
                        <div class="text-xs text-gray-600">achievements</div>
                    </div>
                    <div class="text-center">
                        <div class="text-lg font-semibold text-blue-600">Level</div>
                        <div class="text-xs text-gray-600">1</div>
                    </div>
                </div>
                <a href="/learning/{child['tier'].lower().replace(' ', '-')}" 
                   class="bg-gradient-to-r {color} text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all">
                    Start Learning
                </a>
            </div>
        </div>
        '''
        cards.append(card)
    
    return '\n'.join(cards)

# Learning Environment Routes
@app.route('/learning/magic-workshop')
def magic_workshop():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Magic Workshop - Codopia</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <style>
            .draggable {
                cursor: move;
                transition: transform 0.2s;
            }
            .draggable:hover {
                transform: scale(1.05);
            }
            .drop-zone {
                min-height: 200px;
                border: 2px dashed #d1d5db;
                transition: all 0.3s;
            }
            .drop-zone.drag-over {
                border-color: #8b5cf6;
                background-color: #f3f4f6;
            }
        </style>
    </head>
    <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <!-- Navigation -->
        <nav class="bg-white/90 backdrop-blur-md shadow-lg">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center space-x-4">
                        <a href="/dashboard" class="text-green-600 hover:text-green-800 font-medium">← Back to Dashboard</a>
                        <div class="flex items-center space-x-2">
                            <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                                <span class="text-white text-sm">🎨</span>
                            </div>
                            <span class="text-xl font-bold text-purple-600">Magic Workshop</span>
                        </div>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-gray-700">Alex Johnson • Age 6</span>
                        <button id="sparkle-btn" class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full hover:from-purple-600 hover:to-pink-600 transition-all">
                            ✨ Ask Professor Sparkle
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="grid lg:grid-cols-4 gap-8">
                <!-- Magic Lessons -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-center space-x-2 mb-6">
                        <span class="text-2xl">🧙‍♂️</span>
                        <h2 class="text-xl font-bold text-purple-700">Magic Lessons</h2>
                    </div>
                    
                    <div class="space-y-4">
                        <div class="bg-purple-100 rounded-lg p-4 border-l-4 border-purple-500">
                            <h3 class="font-semibold text-purple-800 mb-1">Lesson 1: Making the Wizard Move</h3>
                            <p class="text-sm text-purple-600 mb-2">Learn basic movement spells</p>
                            <div class="flex items-center space-x-2">
                                <span class="text-purple-500">🧙‍♂️</span>
                                <div class="flex-1 bg-purple-200 rounded-full h-2">
                                    <div class="bg-purple-500 h-2 rounded-full w-1/5"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="font-semibold text-gray-600 mb-1">Lesson 2: Casting Spell Patterns</h3>
                            <p class="text-sm text-gray-500 mb-2">Create magical sequences</p>
                            <div class="flex items-center space-x-2">
                                <span class="text-gray-400">🔮</span>
                                <span class="text-sm text-gray-500">Complete Lesson 1 to unlock</span>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="font-semibold text-gray-600 mb-1">Lesson 3: Magical Decisions</h3>
                            <p class="text-sm text-gray-500 mb-2">If-then magic spells</p>
                            <div class="flex items-center space-x-2">
                                <span class="text-gray-400">⚡</span>
                                <span class="text-sm text-gray-500">Complete Lesson 2 to unlock</span>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="font-semibold text-gray-600 mb-1">Lesson 4: Treasure Hunt</h3>
                            <p class="text-sm text-gray-500 mb-2">Loops and repetition</p>
                            <div class="flex items-center space-x-2">
                                <span class="text-gray-400">💎</span>
                                <span class="text-sm text-gray-500">Complete Lesson 3 to unlock</span>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="font-semibold text-gray-600 mb-1">Lesson 5: Magic Functions</h3>
                            <p class="text-sm text-gray-500 mb-2">Create your own spells</p>
                            <div class="flex items-center space-x-2">
                                <span class="text-gray-400">🌟</span>
                                <span class="text-sm text-gray-500">Complete Lesson 4 to unlock</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-6 text-center">
                        <div class="text-sm text-gray-600 mb-2">Progress</div>
                        <div class="text-lg font-bold text-purple-600">1/5</div>
                    </div>
                </div>
                
                <!-- Magic Spell Blocks -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-center space-x-2 mb-6">
                        <span class="text-2xl">🪄</span>
                        <h2 class="text-xl font-bold text-purple-700">Magic Spell Blocks</h2>
                    </div>
                    
                    <div class="space-y-4">
                        <div>
                            <h3 class="font-semibold text-purple-600 mb-3">Movement Spells</h3>
                            <div class="space-y-2">
                                <div class="draggable bg-blue-500 text-white p-3 rounded-lg cursor-move hover:bg-blue-600 transition-all" draggable="true" data-spell="move-right">
                                    ➡️ Move Right
                                </div>
                                <div class="draggable bg-blue-500 text-white p-3 rounded-lg cursor-move hover:bg-blue-600 transition-all" draggable="true" data-spell="move-left">
                                    ⬅️ Move Left
                                </div>
                                <div class="draggable bg-blue-500 text-white p-3 rounded-lg cursor-move hover:bg-blue-600 transition-all" draggable="true" data-spell="move-up">
                                    ⬆️ Move Up
                                </div>
                                <div class="draggable bg-blue-500 text-white p-3 rounded-lg cursor-move hover:bg-blue-600 transition-all" draggable="true" data-spell="move-down">
                                    ⬇️ Move Down
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="font-semibold text-green-600 mb-3">Action Spells</h3>
                            <div class="space-y-2">
                                <div class="draggable bg-green-500 text-white p-3 rounded-lg cursor-move hover:bg-green-600 transition-all" draggable="true" data-spell="cast-sparkle">
                                    ✨ Cast Sparkle
                                </div>
                                <div class="draggable bg-green-500 text-white p-3 rounded-lg cursor-move hover:bg-green-600 transition-all" draggable="true" data-spell="magic-orb">
                                    🔮 Magic Orb
                                </div>
                                <div class="draggable bg-green-500 text-white p-3 rounded-lg cursor-move hover:bg-green-600 transition-all" draggable="true" data-spell="star-burst">
                                    🌟 Star Burst
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="font-semibold text-orange-600 mb-3">Control Spells</h3>
                            <div class="space-y-2">
                                <div class="draggable bg-orange-500 text-white p-3 rounded-lg cursor-move hover:bg-orange-600 transition-all" draggable="true" data-spell="repeat">
                                    🔄 Repeat 3 times
                                </div>
                                <div class="draggable bg-orange-500 text-white p-3 rounded-lg cursor-move hover:bg-orange-600 transition-all" draggable="true" data-spell="wait">
                                    ⏱️ Wait 1 second
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Spell Canvas -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-center space-x-2 mb-6">
                        <span class="text-2xl">🧙‍♂️</span>
                        <h2 class="text-xl font-bold text-purple-700">Spell Canvas</h2>
                    </div>
                    
                    <div class="mb-4 flex space-x-2">
                        <button id="cast-spell" class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-all">
                            ▶️ Cast Spell
                        </button>
                        <button id="clear-canvas" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-all">
                            🗑️ Clear
                        </button>
                    </div>
                    
                    <div id="spell-canvas" class="drop-zone bg-purple-50 rounded-lg p-4 min-h-[300px] border-2 border-dashed border-purple-300">
                        <div class="text-center text-purple-400 mt-20">
                            <div class="text-4xl mb-4">🎯</div>
                            <p>Drag spell blocks here to create your magic!</p>
                            <p class="text-sm mt-2">Start with a movement spell to make the wizard move</p>
                        </div>
                    </div>
                </div>
                
                <!-- Magic Stage -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-center space-x-2 mb-6">
                        <span class="text-2xl">🎭</span>
                        <h2 class="text-xl font-bold text-purple-700">Magic Stage</h2>
                    </div>
                    
                    <div id="magic-stage" class="bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg p-4 h-64 relative overflow-hidden">
                        <div id="wizard" class="absolute text-4xl transition-all duration-500" style="top: 50%; left: 50%; transform: translate(-50%, -50%);">
                            🧙‍♂️
                        </div>
                        
                        <!-- Magic effects container -->
                        <div id="magic-effects" class="absolute inset-0 pointer-events-none"></div>
                    </div>
                    
                    <div class="mt-4 flex justify-between items-center">
                        <button id="reset-stage" class="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600 transition-all">
                            🔄 Reset
                        </button>
                        <div class="text-right">
                            <div class="text-sm text-gray-600">⭐ Magic Points: <span id="magic-points">0</span></div>
                            <div class="text-sm text-gray-600">🏆 Achievements: <span id="achievements">0</span></div>
                        </div>
                    </div>
                    
                    <div class="mt-4 text-center text-sm text-purple-600">
                        Complete the lesson to unlock the next magical adventure!
                    </div>
                </div>
            </div>
        </div>

        <!-- Professor Sparkle Modal -->
        <div id="sparkle-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50">
            <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
                <div class="flex items-center space-x-3 mb-6">
                    <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                        <span class="text-white text-xl">✨</span>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold text-purple-700">Professor Sparkle</h3>
                        <p class="text-purple-600">Your Magical Coding Tutor</p>
                    </div>
                    <button id="close-sparkle" class="ml-auto text-gray-400 hover:text-gray-600">
                        <span class="text-2xl">×</span>
                    </button>
                </div>
                
                <div id="sparkle-chat" class="bg-purple-50 rounded-lg p-4 h-64 overflow-y-auto mb-4">
                    <div class="text-purple-600 mb-4">
                        ✨ Hello there, young wizard! I'm Professor Sparkle, and I'm here to help you learn the magical art of coding! What would you like to know about today's lesson?
                    </div>
                </div>
                
                <div class="flex space-x-2">
                    <input id="sparkle-input" type="text" placeholder="Ask Professor Sparkle anything..." 
                           class="flex-1 px-3 py-2 border border-purple-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
                    <button id="send-sparkle" class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-lg hover:from-purple-600 hover:to-pink-600">
                        Send ✨
                    </button>
                </div>
                
                <div class="mt-4 text-center">
                    <button id="voice-sparkle" class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-full hover:from-blue-600 hover:to-purple-600 transition-all">
                        🎤 Talk to Professor Sparkle
                    </button>
                </div>
            </div>
        </div>

        <script>
            // Initialize Socket.IO for real-time communication with Professor Sparkle
            const socket = io();
            
            // Drag and Drop functionality
            let draggedElement = null;
            let spellSequence = [];
            
            // Make spell blocks draggable
            document.querySelectorAll('.draggable').forEach(element => {
                element.addEventListener('dragstart', (e) => {
                    draggedElement = e.target;
                    e.dataTransfer.effectAllowed = 'move';
                });
            });
            
            // Set up drop zone
            const spellCanvas = document.getElementById('spell-canvas');
            
            spellCanvas.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                spellCanvas.classList.add('drag-over');
            });
            
            spellCanvas.addEventListener('dragleave', () => {
                spellCanvas.classList.remove('drag-over');
            });
            
            spellCanvas.addEventListener('drop', (e) => {
                e.preventDefault();
                spellCanvas.classList.remove('drag-over');
                
                if (draggedElement) {
                    // Clear the placeholder if this is the first spell
                    if (spellSequence.length === 0) {
                        spellCanvas.innerHTML = '';
                    }
                    
                    // Create a copy of the dragged element
                    const spellBlock = document.createElement('div');
                    spellBlock.className = 'bg-gradient-to-r from-purple-500 to-pink-500 text-white p-3 rounded-lg mb-2 flex items-center justify-between';
                    spellBlock.innerHTML = `
                        <span>${draggedElement.textContent}</span>
                        <button class="text-white hover:text-red-200 ml-2" onclick="removeSpell(this)">×</button>
                    `;
                    
                    spellCanvas.appendChild(spellBlock);
                    
                    // Add to spell sequence
                    spellSequence.push({
                        type: draggedElement.dataset.spell,
                        text: draggedElement.textContent
                    });
                    
                    draggedElement = null;
                }
            });
            
            // Remove spell function
            function removeSpell(button) {
                const spellBlock = button.parentElement;
                const index = Array.from(spellCanvas.children).indexOf(spellBlock);
                spellSequence.splice(index, 1);
                spellBlock.remove();
                
                // Show placeholder if no spells
                if (spellSequence.length === 0) {
                    spellCanvas.innerHTML = `
                        <div class="text-center text-purple-400 mt-20">
                            <div class="text-4xl mb-4">🎯</div>
                            <p>Drag spell blocks here to create your magic!</p>
                            <p class="text-sm mt-2">Start with a movement spell to make the wizard move</p>
                        </div>
                    `;
                }
            }
            
            // Cast spell functionality
            document.getElementById('cast-spell').addEventListener('click', () => {
                if (spellSequence.length === 0) {
                    alert('Add some spell blocks first! 🪄');
                    return;
                }
                
                executeSpellSequence();
            });
            
            // Clear canvas
            document.getElementById('clear-canvas').addEventListener('click', () => {
                spellSequence = [];
                spellCanvas.innerHTML = `
                    <div class="text-center text-purple-400 mt-20">
                        <div class="text-4xl mb-4">🎯</div>
                        <p>Drag spell blocks here to create your magic!</p>
                        <p class="text-sm mt-2">Start with a movement spell to make the wizard move</p>
                    </div>
                `;
            });
            
            // Execute spell sequence
            async function executeSpellSequence() {
                const wizard = document.getElementById('wizard');
                const magicEffects = document.getElementById('magic-effects');
                
                for (let i = 0; i < spellSequence.length; i++) {
                    const spell = spellSequence[i];
                    
                    switch (spell.type) {
                        case 'move-right':
                            moveWizard(wizard, 50, 0);
                            break;
                        case 'move-left':
                            moveWizard(wizard, -50, 0);
                            break;
                        case 'move-up':
                            moveWizard(wizard, 0, -50);
                            break;
                        case 'move-down':
                            moveWizard(wizard, 0, 50);
                            break;
                        case 'cast-sparkle':
                            createMagicEffect(magicEffects, '✨', wizard);
                            break;
                        case 'magic-orb':
                            createMagicEffect(magicEffects, '🔮', wizard);
                            break;
                        case 'star-burst':
                            createMagicEffect(magicEffects, '🌟', wizard);
                            break;
                        case 'wait':
                            await sleep(1000);
                            break;
                    }
                    
                    await sleep(500); // Pause between spells
                }
                
                // Award magic points
                const points = spellSequence.length * 10;
                updateMagicPoints(points);
            }
            
            function moveWizard(wizard, deltaX, deltaY) {
                const rect = wizard.parentElement.getBoundingClientRect();
                const wizardRect = wizard.getBoundingClientRect();
                
                const currentX = wizardRect.left - rect.left;
                const currentY = wizardRect.top - rect.top;
                
                const newX = Math.max(0, Math.min(rect.width - 50, currentX + deltaX));
                const newY = Math.max(0, Math.min(rect.height - 50, currentY + deltaY));
                
                wizard.style.left = newX + 'px';
                wizard.style.top = newY + 'px';
                wizard.style.transform = 'none';
            }
            
            function createMagicEffect(container, effect, wizard) {
                const effectElement = document.createElement('div');
                effectElement.textContent = effect;
                effectElement.className = 'absolute text-2xl animate-ping';
                effectElement.style.left = wizard.style.left;
                effectElement.style.top = wizard.style.top;
                
                container.appendChild(effectElement);
                
                setTimeout(() => {
                    effectElement.remove();
                }, 1000);
            }
            
            function updateMagicPoints(points) {
                const currentPoints = parseInt(document.getElementById('magic-points').textContent);
                document.getElementById('magic-points').textContent = currentPoints + points;
            }
            
            function sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
            
            // Reset stage
            document.getElementById('reset-stage').addEventListener('click', () => {
                const wizard = document.getElementById('wizard');
                wizard.style.left = '';
                wizard.style.top = '';
                wizard.style.transform = 'translate(-50%, -50%)';
                
                document.getElementById('magic-effects').innerHTML = '';
            });
            
            // Professor Sparkle Modal
            const sparkleBtn = document.getElementById('sparkle-btn');
            const sparkleModal = document.getElementById('sparkle-modal');
            const closeSparkle = document.getElementById('close-sparkle');
            const sparkleInput = document.getElementById('sparkle-input');
            const sendSparkle = document.getElementById('send-sparkle');
            const sparkleChat = document.getElementById('sparkle-chat');
            const voiceSparkle = document.getElementById('voice-sparkle');
            
            sparkleBtn.addEventListener('click', () => {
                sparkleModal.classList.remove('hidden');
                sparkleModal.classList.add('flex');
                sparkleInput.focus();
            });
            
            closeSparkle.addEventListener('click', () => {
                sparkleModal.classList.add('hidden');
                sparkleModal.classList.remove('flex');
            });
            
            // Send message to Professor Sparkle
            sendSparkle.addEventListener('click', sendMessageToSparkle);
            sparkleInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessageToSparkle();
                }
            });
            
            function sendMessageToSparkle() {
                const message = sparkleInput.value.trim();
                if (!message) return;
                
                // Add user message to chat
                const userMessage = document.createElement('div');
                userMessage.className = 'bg-white rounded-lg p-3 mb-3 ml-8';
                userMessage.innerHTML = `<strong>You:</strong> ${message}`;
                sparkleChat.appendChild(userMessage);
                
                // Clear input
                sparkleInput.value = '';
                
                // Send to Professor Sparkle via Socket.IO
                socket.emit('sparkle_message', {
                    message: message,
                    child_age: 6,
                    tier: 'Magic Workshop'
                });
                
                // Scroll to bottom
                sparkleChat.scrollTop = sparkleChat.scrollHeight;
            }
            
            // Receive response from Professor Sparkle
            socket.on('sparkle_response', (data) => {
                const sparkleMessage = document.createElement('div');
                sparkleMessage.className = 'bg-purple-100 rounded-lg p-3 mb-3 mr-8';
                sparkleMessage.innerHTML = `<strong>Professor Sparkle:</strong> ${data.response}`;
                sparkleChat.appendChild(sparkleMessage);
                
                // Scroll to bottom
                sparkleChat.scrollTop = sparkleChat.scrollHeight;
            });
            
            // Voice interaction (placeholder)
            voiceSparkle.addEventListener('click', () => {
                alert('🎤 Voice interaction with Professor Sparkle coming soon! For now, you can type your questions. ✨');
            });
            
            // Initialize Professor Sparkle session
            socket.emit('init_sparkle', {
                child_age: 6,
                tier: 'Magic Workshop'
            });
        </script>
    </body>
    </html>
    '''

# Professor Sparkle Socket.IO Events
@socketio.on('init_sparkle')
def handle_init_sparkle(data):
    child_age = data.get('child_age', 6)
    tier = data.get('tier', 'Magic Workshop')
    
    # Initialize Professor Sparkle session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        session_data = loop.run_until_complete(initialize_sparkle_session(child_age, tier))
        emit('sparkle_ready', session_data)
    except Exception as e:
        emit('sparkle_error', {'message': str(e)})
    finally:
        loop.close()

@socketio.on('sparkle_message')
def handle_sparkle_message(data):
    message = data.get('message', '')
    child_age = data.get('child_age', 6)
    tier = data.get('tier', 'Magic Workshop')
    
    # Get response from Professor Sparkle
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        response = loop.run_until_complete(get_sparkle_response(message, child_age, tier))
        emit('sparkle_response', {'response': response})
    except Exception as e:
        emit('sparkle_response', {'response': '✨ *magical sparkles* Oh my! My magic wand seems to be having technical difficulties. Let me try that spell again! What would you like to learn about coding magic? 🪄'})
    finally:
        loop.close()

# Other routes
@app.route('/signout')
def signout():
    response = make_response(redirect('/'))
    response.set_cookie('auth_token', '', expires=0)
    return response

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Forgot Password - Codopia</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
            <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div class="max-w-md w-full space-y-8">
                    <div class="text-center">
                        <a href="/signin" class="inline-flex items-center text-purple-600 hover:text-purple-800 mb-8">
                            ← Back to Sign In
                        </a>
                        <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Reset Your Password</h2>
                        <p class="mt-2 text-gray-600">Enter your email address and we'll send you a reset link</p>
                    </div>
                    
                    <form action="/forgot-password" method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                                   placeholder="your.email@example.com">
                        </div>
                        
                        <button type="submit" 
                                class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                            Send Reset Link
                        </button>
                        
                        <div class="text-center">
                            <span class="text-sm text-gray-600">Remember your password? </span>
                            <a href="/signin" class="text-sm text-purple-600 hover:text-purple-800">Sign In</a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # Handle POST request
    email = request.form.get('email')
    
    # In production, you would send an actual email
    # For now, we'll just simulate the process
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Link Sent - Codopia</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div class="max-w-md w-full space-y-8 text-center">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-white text-2xl">✓</span>
                </div>
                <h2 class="text-3xl font-bold text-gray-900">Check Your Email</h2>
                <p class="text-gray-600">We've sent a password reset link to your email address. Please check your inbox and follow the instructions.</p>
                <a href="/signin" class="inline-block bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all">
                    Back to Sign In
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

