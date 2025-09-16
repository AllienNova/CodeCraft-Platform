from flask import Flask, request, jsonify, redirect, make_response
import hashlib
import jwt
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

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
                                <span class="text-blue-500">👥</span>
                                <span>Collaborative projects</span>
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
                                <span>Career pathway guidance</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="bg-gray-900 text-white py-12">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <div class="flex items-center justify-center space-x-2 mb-4">
                        <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                            <span class="text-white text-xl font-bold">C</span>
                        </div>
                        <span class="text-2xl font-bold">Codopia</span>
                    </div>
                    <p class="text-gray-400 mb-8">Where Code Becomes Craft</p>
                    
                    <div class="flex items-center justify-center space-x-8 mb-8">
                        <span class="flex items-center space-x-2">
                            <span class="text-green-400">✓</span>
                            <span>COPPA+ Compliant</span>
                        </span>
                        <span class="flex items-center space-x-2">
                            <span class="text-blue-400">🔒</span>
                            <span>No Credit Card Required</span>
                        </span>
                        <span class="flex items-center space-x-2">
                            <span class="text-purple-400">👨‍👩‍👧‍👦</span>
                            <span>Parent Approved</span>
                        </span>
                    </div>
                    
                    <p class="text-gray-500 text-sm">
                        © 2024 Codopia. All rights reserved. | Privacy Policy | Terms of Service
                    </p>
                </div>
            </div>
        </footer>
    </body>
    </html>
    '''

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
                        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Welcome back to Codopia</h2>
                        <p class="mt-2 text-gray-600">Sign in to continue your child's coding journey</p>
                    </div>
                    
                    <form method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Enter your email">
                        </div>
                        
                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                            <input id="password" name="password" type="password" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Enter your password">
                        </div>
                        
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <input id="remember-me" name="remember-me" type="checkbox" 
                                       class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded">
                                <label for="remember-me" class="ml-2 block text-sm text-gray-700">Remember me</label>
                            </div>
                            <a href="/forgot-password" class="text-sm text-purple-600 hover:text-purple-800">Forgot password?</a>
                        </div>
                        
                        <button type="submit" 
                                class="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-4 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all font-semibold">
                            Sign In
                        </button>
                        
                        <div class="text-center">
                            <span class="text-gray-600">Don't have an account? </span>
                            <a href="/signup" class="text-purple-600 hover:text-purple-800 font-medium">Create Account</a>
                        </div>
                        
                        <div class="mt-6">
                            <div class="relative">
                                <div class="absolute inset-0 flex items-center">
                                    <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center text-sm">
                                    <span class="px-2 bg-gray-50 text-gray-500">Or continue with</span>
                                </div>
                            </div>
                            
                            <div class="mt-6">
                                <button type="button" 
                                        class="w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-50 transition-all font-semibold flex items-center justify-center space-x-2">
                                    <span>🔍</span>
                                    <span>Continue with Google</span>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Find user
    user = None
    for u in users:
        if u['email'] == email and u['password'] == password_hash:
            user = u
            break
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.secret_key, algorithm='HS256')
    
    # Set cookie and redirect to dashboard
    response = make_response(redirect('/dashboard'))
    response.set_cookie('token', token, max_age=7*24*60*60, httponly=True)
    return response

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
                        <a href="/" class="inline-flex items-center text-purple-600 hover:text-purple-800 mb-4">
                            <span>←</span>
                            <span class="ml-2">Back to Home</span>
                        </a>
                        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Start Your Free Trial</h2>
                        <p class="mt-2 text-gray-600">Create your account and add your child's profile</p>
                    </div>
                    
                    <form method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Parent Full Name</label>
                            <input id="name" name="name" type="text" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="John Smith">
                        </div>
                        
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="parent@example.com">
                        </div>
                        
                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                            <input id="password" name="password" type="password" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Create a secure password">
                        </div>
                        
                        <div>
                            <label for="child_name" class="block text-sm font-medium text-gray-700 mb-2">Child's Name</label>
                            <input id="child_name" name="child_name" type="text" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Emma Smith">
                        </div>
                        
                        <div>
                            <label for="child_age" class="block text-sm font-medium text-gray-700 mb-2">Child's Age (This determines their learning tier)</label>
                            <select id="child_age" name="child_age" required 
                                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
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
                                class="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg hover:from-green-600 hover:to-green-700 transition-all font-semibold">
                            🔒 SECURE MY CHILD'S FUTURE - FREE TRIAL
                        </button>
                        
                        <div class="text-center text-sm text-gray-600 space-y-1">
                            <div class="flex items-center justify-center space-x-4">
                                <span>🛡️ Your information is encrypted and will never be shared</span>
                            </div>
                            <div class="flex items-center justify-center space-x-4">
                                <span>⚡ Instant Access</span>
                                <span>🚫 No Commitment</span>
                                <span>❌ Cancel Anytime</span>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <span class="text-gray-600">Already have an account? </span>
                            <a href="/signin" class="text-purple-600 hover:text-purple-800 font-medium">Sign In</a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # Handle POST request
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    child_name = request.form.get('child_name')
    child_age = request.form.get('child_age')
    
    if not all([name, email, password, child_name, child_age]):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Check if user already exists
    for user in users:
        if user['email'] == email:
            return jsonify({'error': 'User with this email already exists'}), 400
    
    # Determine tier based on age
    age = int(child_age)
    if age <= 7:
        tier = 'Magic Workshop'
    elif age <= 12:
        tier = 'Innovation Lab'
    else:
        tier = 'Professional Studio'
    
    # Create new user
    user_id = len(users) + 1
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    new_user = {
        'id': user_id,
        'name': name,
        'email': email,
        'password': password_hash,
        'children': [{
            'name': child_name,
            'age': age,
            'tier': tier,
            'progress': 0,
            'achievements': []
        }],
        'created_at': datetime.utcnow().isoformat()
    }
    
    users.append(new_user)
    
    # Create JWT token
    token = jwt.encode({
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.secret_key, algorithm='HS256')
    
    # Set cookie and redirect to dashboard
    response = make_response(redirect('/dashboard'))
    response.set_cookie('token', token, max_age=7*24*60*60, httponly=True)
    return response

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return redirect('/signin')
    
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Get user data
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return redirect('/signin')
        
        children_cards = ""
        for child in user['children']:
            tier_color = {
                'Magic Workshop': 'from-purple-500 to-pink-500',
                'Innovation Lab': 'from-blue-500 to-indigo-500',
                'Professional Studio': 'from-green-500 to-emerald-500'
            }.get(child['tier'], 'from-gray-500 to-gray-600')
            
            tier_icon = {
                'Magic Workshop': '🎨',
                'Innovation Lab': '🔬',
                'Professional Studio': '💼'
            }.get(child['tier'], '📚')
            
            learning_url = {
                'Magic Workshop': '/learning/magic-workshop',
                'Innovation Lab': '/learning/innovation-lab',
                'Professional Studio': '/learning/professional-studio'
            }.get(child['tier'], '/learning/magic-workshop')
            
            children_cards += f'''
            <div class="bg-white rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-3">
                        <div class="w-12 h-12 bg-gradient-to-r {tier_color} rounded-full flex items-center justify-center">
                            <span class="text-white text-xl">{tier_icon}</span>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">{child['name']}</h3>
                            <p class="text-gray-600">Age {child['age']} • {child['tier']}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-2xl font-bold text-purple-600">{child['progress']}%</div>
                        <div class="text-sm text-gray-500">Progress</div>
                    </div>
                </div>
                
                <div class="mb-4">
                    <div class="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Learning Progress</span>
                        <span>{child['progress']}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-gradient-to-r {tier_color} h-2 rounded-full" style="width: {child['progress']}%"></div>
                    </div>
                </div>
                
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <div class="flex items-center space-x-1">
                            <span class="text-yellow-500">🏆</span>
                            <span class="text-sm text-gray-600">{len(child['achievements'])} achievements</span>
                        </div>
                        <div class="flex items-center space-x-1">
                            <span class="text-purple-500">⭐</span>
                            <span class="text-sm text-gray-600">Level {child['progress'] // 20 + 1}</span>
                        </div>
                    </div>
                    <a href="{learning_url}" class="bg-gradient-to-r {tier_color} text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all">
                        Start Learning
                    </a>
                </div>
            </div>
            '''
        
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
            <nav class="bg-white/90 backdrop-blur-md shadow-lg sticky top-0 z-50">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center py-4">
                        <div class="flex items-center space-x-2">
                            <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                                <span class="text-white text-xl font-bold">C</span>
                            </div>
                            <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Codopia</span>
                        </div>
                        <div class="flex items-center space-x-4">
                            <span class="text-gray-700">Welcome, {user['name']}</span>
                            <a href="/logout" class="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-lg hover:from-red-600 hover:to-red-700 transition-all">
                                Sign Out
                            </a>
                        </div>
                    </div>
                </div>
            </nav>

            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <!-- Header -->
                <div class="mb-8">
                    <h1 class="text-4xl font-bold text-gray-900 mb-2">Your Children's Learning Dashboard</h1>
                    <p class="text-xl text-gray-600">Track progress, manage profiles, and access learning environments</p>
                </div>

                <!-- Children Cards -->
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    {children_cards}
                    
                    <!-- Add Child Card -->
                    <div class="bg-white/50 border-2 border-dashed border-purple-300 rounded-2xl p-6 flex flex-col items-center justify-center hover:border-purple-500 transition-all cursor-pointer">
                        <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                            <span class="text-purple-600 text-2xl">+</span>
                        </div>
                        <h3 class="text-lg font-semibold text-purple-700 mb-2">Add Another Child</h3>
                        <p class="text-purple-600 text-center text-sm">Create a profile for another child to start their coding journey</p>
                    </div>
                </div>

                <!-- Quick Stats -->
                <div class="grid md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                        <div class="text-3xl font-bold text-purple-600 mb-2">{len(user['children'])}</div>
                        <div class="text-gray-600">Active Children</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                        <div class="text-3xl font-bold text-blue-600 mb-2">{sum(len(child['achievements']) for child in user['children'])}</div>
                        <div class="text-gray-600">Total Achievements</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                        <div class="text-3xl font-bold text-green-600 mb-2">{sum(child['progress'] for child in user['children']) // len(user['children']) if user['children'] else 0}%</div>
                        <div class="text-gray-600">Average Progress</div>
                    </div>
                    <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                        <div class="text-3xl font-bold text-pink-600 mb-2">7</div>
                        <div class="text-gray-600">Days Active</div>
                    </div>
                </div>

                <!-- Recent Activity -->
                <div class="bg-white rounded-2xl shadow-xl p-6">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Recent Activity</h2>
                    <div class="space-y-4">
                        <div class="flex items-center space-x-4 p-4 bg-purple-50 rounded-lg">
                            <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center">
                                <span class="text-white">🎉</span>
                            </div>
                            <div class="flex-1">
                                <p class="font-semibold text-gray-900">Welcome to Codopia!</p>
                                <p class="text-gray-600 text-sm">Your coding adventure begins now. Start with your first lesson!</p>
                            </div>
                            <div class="text-sm text-gray-500">Just now</div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        
    except jwt.InvalidTokenError:
        return redirect('/signin')

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('token', '', expires=0)
    return response

# Forgot Password functionality
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Password - Codopia</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
            <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div class="max-w-md w-full space-y-8">
                    <div class="text-center">
                        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Reset Your Password</h2>
                        <p class="mt-2 text-gray-600">Enter your email address and we'll send you a reset link</p>
                    </div>
                    
                    <form method="POST" class="mt-8 space-y-6">
                        <div>
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                            <input id="email" name="email" type="email" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Enter your email address">
                        </div>
                        
                        <button type="submit" 
                                class="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-4 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all font-semibold">
                            Send Reset Link
                        </button>
                        
                        <div class="text-center">
                            <a href="/signin" class="text-purple-600 hover:text-purple-800 font-medium">
                                ← Back to Sign In
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if user exists
    user_found = False
    for user in users:
        if user['email'] == email:
            user_found = True
            break
    
    if not user_found:
        return jsonify({'error': 'No account found with this email address'}), 404
    
    # Generate reset token (in production, this would be stored in database with expiration)
    reset_token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }, app.secret_key, algorithm='HS256')
    
    # In production, you would send this via email
    # For demo purposes, we'll return it directly
    return jsonify({
        'message': 'Password reset link sent to your email',
        'reset_link': f'/reset-password?token={reset_token}',
        'note': 'In production, this would be sent via email'
    })

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token')
        if not token:
            return redirect('/forgot-password')
        
        try:
            # Verify token
            payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            email = payload['email']
        except jwt.ExpiredSignatureError:
            return '''
            <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
                <div class="text-center">
                    <h2 class="text-2xl font-bold text-red-600 mb-4">Reset Link Expired</h2>
                    <p class="text-gray-600 mb-4">This password reset link has expired. Please request a new one.</p>
                    <a href="/forgot-password" class="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600">Request New Link</a>
                </div>
            </div>
            '''
        except jwt.InvalidTokenError:
            return '''
            <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
                <div class="text-center">
                    <h2 class="text-2xl font-bold text-red-600 mb-4">Invalid Reset Link</h2>
                    <p class="text-gray-600 mb-4">This password reset link is invalid. Please request a new one.</p>
                    <a href="/forgot-password" class="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600">Request New Link</a>
                </div>
            </div>
            '''
        
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Set New Password - Codopia</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
            <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div class="max-w-md w-full space-y-8">
                    <div class="text-center">
                        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4">
                            <span class="text-white text-2xl font-bold">C</span>
                        </div>
                        <h2 class="text-3xl font-bold text-gray-900">Set New Password</h2>
                        <p class="mt-2 text-gray-600">Enter your new password for {email}</p>
                    </div>
                    
                    <form method="POST" class="mt-8 space-y-6">
                        <input type="hidden" name="token" value="{token}">
                        
                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                            <input id="password" name="password" type="password" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Enter your new password">
                        </div>
                        
                        <div>
                            <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                            <input id="confirm_password" name="confirm_password" type="password" required 
                                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                   placeholder="Confirm your new password">
                        </div>
                        
                        <button type="submit" 
                                class="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-4 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all font-semibold">
                            Update Password
                        </button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    # Handle POST request
    token = request.form.get('token')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([token, password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    try:
        # Verify token
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        email = payload['email']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Reset link has expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid reset link'}), 400
    
    # Update user password
    for user in users:
        if user['email'] == email:
            user['password'] = hashlib.sha256(password.encode()).hexdigest()
            break
    
    return '''
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <div class="text-center">
            <div class="mx-auto h-16 w-16 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center mb-4">
                <span class="text-white text-2xl">✓</span>
            </div>
            <h2 class="text-2xl font-bold text-green-600 mb-4">Password Updated Successfully!</h2>
            <p class="text-gray-600 mb-4">Your password has been updated. You can now sign in with your new password.</p>
            <a href="/signin" class="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600">Sign In</a>
        </div>
    </div>
    '''

# Learning Environment Routes
@app.route('/learning/magic-workshop')
def magic_workshop():
    token = request.cookies.get('token')
    if not token:
        return redirect('/signin')
    
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Get user and child info
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return redirect('/signin')
        
        # Get child info (for demo, use first child)
        child = user['children'][0] if user['children'] else {'name': 'Young Wizard', 'age': 6}
        
        # Read the Magic Workshop template
        with open('src/templates/learning/magic_workshop.html', 'r') as f:
            template = f.read()
        
        # Replace template variables
        template = template.replace('{{ child_name }}', child['name'])
        template = template.replace('{{ child_age }}', str(child['age']))
        
        return template
        
    except jwt.InvalidTokenError:
        return redirect('/signin')

@app.route('/learning/innovation-lab')
def innovation_lab():
    token = request.cookies.get('token')
    if not token:
        return redirect('/signin')
    
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        # For now, redirect to Magic Workshop as placeholder
        return redirect('/learning/magic-workshop')
        
    except jwt.InvalidTokenError:
        return redirect('/signin')

@app.route('/learning/professional-studio')
def professional_studio():
    token = request.cookies.get('token')
    if not token:
        return redirect('/signin')
    
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        # For now, redirect to Magic Workshop as placeholder
        return redirect('/learning/magic-workshop')
        
    except jwt.InvalidTokenError:
        return redirect('/signin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
