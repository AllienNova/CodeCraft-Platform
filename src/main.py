from flask import Flask, request, jsonify, render_template_string, render_template, session, redirect, url_for, make_response
from flask_socketio import SocketIO, emit
import hashlib
import jwt
from datetime import datetime, timedelta
import os
import asyncio
import json
from gemini_live_sparkle_fixed import professor_sparkle, initialize_sparkle_session, get_sparkle_response

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Supabase client
try:
    from supabase_client import SupabaseClient
    db = SupabaseClient()
    print("✅ Supabase database client initialized successfully")
except Exception as e:
    print(f"⚠️ Supabase initialization failed, using fallback: {e}")
    db = None

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*")

# Get port from environment (Railway sets this)
port = int(os.environ.get('PORT', 5000))

# In-memory user storage (replace with database in production)
users = []

@app.route('/')
def home():
    return render_template('index.html')

# Authentication routes

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template_string(signup_html)
    
    try:
        # Get form data
        parent_name = request.form.get('parent_name')
        email = request.form.get('email')
        password = request.form.get('password')
        child_name = request.form.get('child_name')
        child_age = request.form.get('child_age')
        
        # Validate required fields
        if not all([parent_name, email, password, child_name, child_age]):
            return "All fields are required", 400
        
        # Check if user already exists
        if any(u['email'] == email for u in users):
            return "Email already registered", 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Determine tier based on age
        age = int(child_age)
        if age <= 7:
            tier = "Magic Workshop"
        elif age <= 12:
            tier = "Innovation Lab"
        else:
            tier = "Professional Studio"
        
        # Create user
        user = {
            'id': len(users) + 1,
            'parent_name': parent_name,
            'email': email,
            'password_hash': password_hash,
            'children': [{
                'name': child_name,
                'age': age,
                'tier': tier,
                'progress': 0
            }]
        }
        
        users.append(user)
        
        # Create JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': email,
            'exp': datetime.now() + timedelta(days=30)
        }, app.secret_key, algorithm='HS256')
        
        # Create response and set cookie
        response = make_response(redirect('/dashboard'))
        response.set_cookie('auth_token', token, max_age=30*24*60*60, httponly=True)
        return response
        
    except Exception as e:
        print(f"Signup error: {e}")
        return f"Signup failed: {str(e)}", 500

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
                    <div>
                        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                            Sign in to your account
                        </h2>
                    </div>
                    <form class="mt-8 space-y-6" method="POST">
                        <div class="rounded-md shadow-sm -space-y-px">
                            <div>
                                <input name="email" type="email" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm" placeholder="Email address">
                            </div>
                            <div>
                                <input name="password" type="password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm" placeholder="Password">
                            </div>
                        </div>
                        <div>
                            <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                                Sign in
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        '''
    
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return "Email and password required", 400
        
        # Find user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = next((u for u in users if u['email'] == email and u['password_hash'] == password_hash), None)
        
        if not user:
            return "Invalid credentials", 401
        
        # Create JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': email,
            'exp': datetime.now() + timedelta(days=30)
        }, app.secret_key, algorithm='HS256')
        
        # Create response and set cookie
        response = make_response(redirect('/dashboard'))
        response.set_cookie('auth_token', token, max_age=30*24*60*60, httponly=True)
        return response
        
    except Exception as e:
        print(f"Signin error: {e}")
        return f"Signin failed: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Codopia</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
        <div class="min-h-screen">
            <nav class="bg-white shadow-lg">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between h-16">
                        <div class="flex items-center">
                            <span class="text-2xl font-bold text-purple-600">Codopia Dashboard</span>
                        </div>
                        <div class="flex items-center space-x-4">
                            <a href="/learning/magic-workshop" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">Start Learning</a>
                            <a href="/logout" class="text-gray-600 hover:text-gray-900">Logout</a>
                        </div>
                    </div>
                </div>
            </nav>
            
            <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div class="px-4 py-6 sm:px-0">
                    <div class="border-4 border-dashed border-gray-200 rounded-lg p-8">
                        <h1 class="text-3xl font-bold text-gray-900 mb-4">Welcome to Codopia!</h1>
                        <p class="text-gray-600 mb-6">Ready to start your magical coding adventure?</p>
                        
                        <div class="grid md:grid-cols-3 gap-6">
                            <div class="bg-purple-100 p-6 rounded-lg">
                                <h3 class="text-xl font-bold text-purple-800 mb-2">Magic Workshop</h3>
                                <p class="text-purple-600 mb-4">Ages 5-7 • Visual Block Coding</p>
                                <a href="/learning/magic-workshop" class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Start Adventure</a>
                            </div>
                            
                            <div class="bg-blue-100 p-6 rounded-lg">
                                <h3 class="text-xl font-bold text-blue-800 mb-2">Innovation Lab</h3>
                                <p class="text-blue-600 mb-4">Ages 8-12 • Advanced Blocks</p>
                                <button class="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed">Coming Soon</button>
                            </div>
                            
                            <div class="bg-green-100 p-6 rounded-lg">
                                <h3 class="text-xl font-bold text-green-800 mb-2">Professional Studio</h3>
                                <p class="text-green-600 mb-4">Ages 13+ • Real Programming</p>
                                <button class="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed">Coming Soon</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/learning/magic-workshop')
def magic_workshop():
    return render_template('learning/magic_workshop.html')

# Socket.IO events for Professor Sparkle
@socketio.on('init_sparkle')
def handle_init_sparkle():
    """Initialize Professor Sparkle session"""
    try:
        session_id = initialize_sparkle_session()
        emit('sparkle_ready', {'session_id': session_id})
        print(f"✨ Professor Sparkle session initialized: {session_id}")
    except Exception as e:
        print(f"❌ Error initializing Sparkle: {e}")
        emit('sparkle_error', {'error': str(e)})

@socketio.on('sparkle_message')
def handle_sparkle_message(data):
    """Handle messages to Professor Sparkle"""
    try:
        message = data.get('message', '')
        session_id = data.get('session_id', '')
        
        if not message:
            emit('sparkle_error', {'error': 'No message provided'})
            return
        
        print(f"🎭 Sparkle received: {message}")
        
        # Get response from Professor Sparkle
        response = get_sparkle_response(message, session_id)
        
        emit('sparkle_response', {
            'message': response,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"✨ Sparkle responded: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ Error in Sparkle message: {e}")
        emit('sparkle_error', {'error': str(e)})

if __name__ == '__main__':
    print(f"🚀 Starting Codopia Platform on port {port}")
    print(f"🎭 Professor Sparkle AI: Ready")
    print(f"💾 Database: {'Supabase' if db else 'Fallback'}")
    print(f"🌐 Access at: http://localhost:{port}")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

# Signup HTML template
signup_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up - Codopia</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Create your account
                </h2>
            </div>
            <form class="mt-8 space-y-6" method="POST">
                <div class="space-y-4">
                    <input name="parent_name" type="text" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="Parent Name">
                    <input name="email" type="email" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="Email address">
                    <input name="password" type="password" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="Password">
                    <input name="child_name" type="text" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="Child's Name">
                    <input name="child_age" type="number" min="5" max="18" required class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm" placeholder="Child's Age">
                </div>
                <div>
                    <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                        Create Account
                    </button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
'''

