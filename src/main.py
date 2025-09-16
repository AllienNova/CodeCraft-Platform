from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, send_file
import os
import json
from datetime import datetime, timedelta
import jwt
import bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')

# In-memory user storage (replace with database in production)
users_db = {}
children_db = {}

def get_file_path(relative_path):
    """Find file in multiple possible locations"""
    possible_paths = [
        relative_path,
        os.path.join('.next', 'server', 'app', relative_path),
        os.path.join('src', '.next', 'server', 'app', relative_path),
        os.path.join('/src', '.next', 'server', 'app', relative_path),
        os.path.join(os.getcwd(), '.next', 'server', 'app', relative_path)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def create_jwt_token(user_id):
    """Create JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.secret_key, algorithm='HS256')

def verify_jwt_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_tier_from_age(age):
    """Determine learning tier based on age"""
    if age <= 7:
        return "Magic Workshop"
    elif age <= 12:
        return "Innovation Lab"
    else:
        return "Professional Studio"

@app.route('/')
def index():
    """Landing page with beautiful design"""
    return render_template_string('''
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
        .float { animation: float 6s ease-in-out infinite; }
        .sparkle {
            animation: sparkle 2s linear infinite;
        }
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body class="bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-2">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                        <span class="text-white font-bold text-xl">C</span>
                    </div>
                    <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Codopia</span>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#features" class="text-gray-700 hover:text-purple-600 transition-colors">Features</a>
                    <a href="#tiers" class="text-gray-700 hover:text-purple-600 transition-colors">Learning Tiers</a>
                    <a href="#about" class="text-gray-700 hover:text-purple-600 transition-colors">About</a>
                    <a href="/signin" class="text-purple-600 hover:text-purple-700 font-semibold">Sign In</a>
                    <a href="/signup" class="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-full hover:from-purple-700 hover:to-blue-700 transition-all">Start Free Trial</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative overflow-hidden py-20">
        <!-- Floating Sparkles -->
        <div class="absolute inset-0 pointer-events-none">
            <div class="sparkle absolute top-20 left-10 w-4 h-4 bg-purple-400 rounded-full"></div>
            <div class="sparkle absolute top-40 right-20 w-3 h-3 bg-blue-400 rounded-full" style="animation-delay: 0.5s;"></div>
            <div class="sparkle absolute bottom-40 left-20 w-2 h-2 bg-pink-400 rounded-full" style="animation-delay: 1s;"></div>
            <div class="sparkle absolute bottom-20 right-10 w-3 h-3 bg-cyan-400 rounded-full" style="animation-delay: 1.5s;"></div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid lg:grid-cols-2 gap-12 items-center">
                <div class="space-y-8">
                    <div class="inline-block bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-semibold">
                        🔥 URGENT: Only 91 Beta Spots Left - Filling Fast!
                    </div>
                    
                    <h1 class="text-5xl lg:text-6xl font-bold leading-tight">
                        Your Child's
                        <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent block">
                            Coding Adventure
                        </span>
                        Starts Here
                    </h1>
                    
                    <p class="text-xl text-gray-600 leading-relaxed">
                        <span class="text-purple-600 font-semibold">Don't let your child fall behind</span> in the digital revolution. Transform 
                        them into a confident programmer through magical adventures, real 
                        app building, and professional development skills.
                    </p>

                    <div class="flex flex-wrap gap-4 text-sm">
                        <div class="flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-full">
                            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span class="text-green-700 font-medium">Ages 3-18</span>
                        </div>
                        <div class="flex items-center space-x-2 bg-blue-50 px-3 py-2 rounded-full">
                            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                            <span class="text-blue-700 font-medium">100% Safe</span>
                        </div>
                        <div class="flex items-center space-x-2 bg-purple-50 px-3 py-2 rounded-full">
                            <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                            <span class="text-purple-700 font-medium">Irresistibly Fun</span>
                        </div>
                    </div>

                    <div class="flex items-center space-x-4">
                        <div class="flex -space-x-2">
                            <div class="w-10 h-10 bg-purple-400 rounded-full border-2 border-white"></div>
                            <div class="w-10 h-10 bg-blue-400 rounded-full border-2 border-white"></div>
                            <div class="w-10 h-10 bg-pink-400 rounded-full border-2 border-white"></div>
                            <div class="w-10 h-10 bg-cyan-400 rounded-full border-2 border-white"></div>
                            <div class="w-10 h-10 bg-green-400 rounded-full border-2 border-white"></div>
                        </div>
                        <div>
                            <div class="flex items-center space-x-1">
                                <span class="text-yellow-400">★★★★★</span>
                                <span class="font-semibold">4.9/5 rating</span>
                            </div>
                            <p class="text-sm text-gray-600">From real parents</p>
                        </div>
                    </div>
                </div>

                <div class="relative">
                    <div class="bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl p-8 text-white float">
                        <div class="text-center space-y-6">
                            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto">
                                <span class="text-3xl">✨</span>
                            </div>
                            <h3 class="text-2xl font-bold">Join Codopia NOW</h3>
                            <p class="text-purple-100">Be among the first 99 families to experience the future of coding education by Requesting Early Access Now. DON'T LET YOUR CHILD FALL BEHIND</p>
                            
                            <div class="bg-white/10 rounded-lg p-4 text-center">
                                <p class="text-sm text-purple-200 mb-2">🔴 LIVE: Join the first wave of beta testers!</p>
                                <div class="text-3xl font-bold">91</div>
                                <p class="text-sm">Beta spots remaining</p>
                            </div>

                            <form class="space-y-4" action="/signup" method="GET">
                                <input 
                                    type="email" 
                                    placeholder="Parent Email Address"
                                    class="w-full px-4 py-3 rounded-lg text-gray-800 placeholder-gray-500"
                                    required
                                />
                                <select class="w-full px-4 py-3 rounded-lg text-gray-800">
                                    <option>Select age to unlock their perfect tier...</option>
                                    <option value="3">3 years old</option>
                                    <option value="4">4 years old</option>
                                    <option value="5">5 years old</option>
                                    <option value="6">6 years old</option>
                                    <option value="7">7 years old</option>
                                    <option value="8">8 years old</option>
                                    <option value="9">9 years old</option>
                                    <option value="10">10 years old</option>
                                    <option value="11">11 years old</option>
                                    <option value="12">12 years old</option>
                                    <option value="13">13 years old</option>
                                    <option value="14">14 years old</option>
                                    <option value="15">15 years old</option>
                                    <option value="16">16 years old</option>
                                    <option value="17">17 years old</option>
                                    <option value="18">18 years old</option>
                                </select>
                                <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-4 rounded-lg transition-colors">
                                    🔒 SECURE MY CHILD'S FUTURE - FREE TRIAL
                                </button>
                            </form>

                            <div class="flex items-center justify-center space-x-4 text-xs text-purple-200">
                                <span>🔒 Your information is encrypted and will never be shared</span>
                            </div>
                            <div class="flex items-center justify-center space-x-4 text-xs text-purple-200">
                                <span>⚡ Instant Access</span>
                                <span>🚫 No Commitment</span>
                                <span>❌ Cancel Anytime</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Three Tiers Section -->
    <section id="tiers" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl font-bold mb-4">Three Magical Tiers That <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Grow With Your Child</span></h2>
                <p class="text-xl text-gray-600">From magical adventures to professional development, each tier is scientifically designed for your child's cognitive development stage</p>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <!-- Magic Workshop -->
                <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 border border-purple-200">
                    <div class="text-center mb-6">
                        <div class="w-16 h-16 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl">🎨</span>
                        </div>
                        <h3 class="text-2xl font-bold text-purple-700">Magic Workshop</h3>
                        <p class="text-purple-600">Ages 3-7 • Ready for Magic Workshop</p>
                    </div>
                    <ul class="space-y-3 text-gray-700">
                        <li class="flex items-center"><span class="text-purple-500 mr-2">✨</span> Visual drag-and-drop coding</li>
                        <li class="flex items-center"><span class="text-purple-500 mr-2">🧙‍♂️</span> Magical story adventures</li>
                        <li class="flex items-center"><span class="text-purple-500 mr-2">🎮</span> Interactive spell casting</li>
                        <li class="flex items-center"><span class="text-purple-500 mr-2">🏆</span> Achievement badges</li>
                    </ul>
                </div>

                <!-- Innovation Lab -->
                <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-8 border border-blue-200">
                    <div class="text-center mb-6">
                        <div class="w-16 h-16 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl">🔬</span>
                        </div>
                        <h3 class="text-2xl font-bold text-blue-700">Innovation Lab</h3>
                        <p class="text-blue-600">Ages 8-12 • Ready for Innovation Lab</p>
                    </div>
                    <ul class="space-y-3 text-gray-700">
                        <li class="flex items-center"><span class="text-blue-500 mr-2">📱</span> Real app development</li>
                        <li class="flex items-center"><span class="text-blue-500 mr-2">🤖</span> Robot programming</li>
                        <li class="flex items-center"><span class="text-blue-500 mr-2">🎯</span> Problem-solving challenges</li>
                        <li class="flex items-center"><span class="text-blue-500 mr-2">👥</span> Collaborative projects</li>
                    </ul>
                </div>

                <!-- Professional Studio -->
                <div class="bg-gradient-to-br from-gray-50 to-slate-50 rounded-2xl p-8 border border-gray-200">
                    <div class="text-center mb-6">
                        <div class="w-16 h-16 bg-gradient-to-r from-gray-600 to-slate-600 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span class="text-white text-2xl">💼</span>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-700">Professional Studio</h3>
                        <p class="text-gray-600">Ages 13-18 • Ready for Professional Studio</p>
                    </div>
                    <ul class="space-y-3 text-gray-700">
                        <li class="flex items-center"><span class="text-gray-500 mr-2">💻</span> Real programming languages</li>
                        <li class="flex items-center"><span class="text-gray-500 mr-2">🌐</span> Web development</li>
                        <li class="flex items-center"><span class="text-gray-500 mr-2">🤖</span> AI & Machine Learning</li>
                        <li class="flex items-center"><span class="text-gray-500 mr-2">🚀</span> Career preparation</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Warning Section -->
    <section class="py-16 bg-gradient-to-r from-orange-500 to-red-500 text-white">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="mb-6">
                <span class="text-6xl">⚠️</span>
            </div>
            <h2 class="text-3xl font-bold mb-4">Warning: Software developer salaries average $107,000+. Children who start coding early have a 300% advantage in future earnings.</h2>
            <div class="bg-red-600 rounded-lg p-6 mt-8">
                <p class="text-xl font-semibold">⏰ URGENT: Only 91 Beta Spots Remaining</p>
                <p class="text-red-200 mt-2">⚠️ Spots are filling every few minutes - Don't wait!</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <div class="flex items-center justify-center space-x-2 mb-4">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                        <span class="text-white font-bold text-xl">C</span>
                    </div>
                    <span class="text-2xl font-bold">Codopia</span>
                </div>
                <p class="text-gray-400 mb-6">Where Code Becomes Craft</p>
                <div class="flex items-center justify-center space-x-6 text-sm text-gray-400">
                    <span>🔒 COPPA+ Compliant</span>
                    <span>🛡️ No Credit Card Required</span>
                    <span>🔐 Parent Approved</span>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
    ''')

@app.route('/signin')
def signin():
    """Sign in page"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In - Codopia</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
        <a href="/" class="inline-flex items-center text-gray-600 hover:text-purple-600 mb-6 transition-colors">
            ← Back to Home
        </a>

        <div class="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
            <div class="text-center mb-8">
                <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-white text-2xl font-bold">C</span>
                </div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                    Welcome Back to Codopia
                </h1>
                <p class="text-gray-600 mt-2">Sign in to continue your child's coding adventure</p>
            </div>

            <div id="error-message" class="hidden bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
                <p class="text-red-700 text-sm"></p>
            </div>

            <form id="signin-form" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                    <input 
                        type="email" 
                        id="email"
                        placeholder="parent@example.com"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input 
                        type="password" 
                        id="password"
                        placeholder="Enter your password"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div class="flex items-center justify-between">
                    <label class="flex items-center">
                        <input type="checkbox" class="rounded border-gray-300 text-purple-600 focus:ring-purple-500" />
                        <span class="ml-2 text-sm text-gray-600">Remember me</span>
                    </label>
                    <a href="#" class="text-sm text-purple-600 hover:text-purple-700">Forgot password?</a>
                </div>

                <button 
                    type="submit" 
                    id="signin-btn"
                    class="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold rounded-lg transition-all"
                >
                    Sign In
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-sm text-gray-600">
                    Don't have an account? 
                    <a href="/signup" class="text-purple-600 hover:text-purple-700 font-semibold">Start Free Trial</a>
                </p>
            </div>

            <div class="flex items-center justify-center space-x-6 pt-6 border-t border-gray-100 mt-6">
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>COPPA Compliant</span>
                </div>
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                    <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span>256-bit SSL</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('signin-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const btn = document.getElementById('signin-btn');
            const errorDiv = document.getElementById('error-message');
            
            btn.textContent = 'Signing In...';
            btn.disabled = true;
            errorDiv.classList.add('hidden');
            
            try {
                const response = await fetch('/api/signin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    errorDiv.querySelector('p').textContent = data.error || 'Invalid email or password';
                    errorDiv.classList.remove('hidden');
                }
            } catch (error) {
                errorDiv.querySelector('p').textContent = 'An error occurred. Please try again.';
                errorDiv.classList.remove('hidden');
            } finally {
                btn.textContent = 'Sign In';
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/signup')
def signup():
    """Sign up page"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Start Free Trial - Codopia</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
        <a href="/" class="inline-flex items-center text-gray-600 hover:text-purple-600 mb-6 transition-colors">
            ← Back to Home
        </a>

        <div class="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
            <div class="text-center mb-8">
                <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-white text-2xl font-bold">C</span>
                </div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                    Start Your Free Trial
                </h1>
                <p class="text-gray-600 mt-2">Create your account and add your child's profile</p>
            </div>

            <div id="error-message" class="hidden bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
                <p class="text-red-700 text-sm"></p>
            </div>

            <form id="signup-form" class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Parent Full Name</label>
                    <input 
                        type="text" 
                        id="parent-name"
                        placeholder="John Smith"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                    <input 
                        type="email" 
                        id="email"
                        placeholder="parent@example.com"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input 
                        type="password" 
                        id="password"
                        placeholder="Create a secure password"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Child's Name</label>
                    <input 
                        type="text" 
                        id="child-name"
                        placeholder="Emma Smith"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Child's Age (This determines their learning tier)</label>
                    <select 
                        id="child-age"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        required
                    >
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

                <button 
                    type="submit" 
                    id="signup-btn"
                    class="w-full py-4 bg-green-500 hover:bg-green-600 text-white font-bold rounded-lg transition-all"
                >
                    🔒 SECURE MY CHILD'S FUTURE - FREE TRIAL
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-sm text-gray-600">
                    Already have an account? 
                    <a href="/signin" class="text-purple-600 hover:text-purple-700 font-semibold">Sign In</a>
                </p>
            </div>

            <div class="flex items-center justify-center space-x-4 text-xs text-gray-500 mt-6">
                <span>🔒 Your information is encrypted and will never be shared</span>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('signup-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const parentName = document.getElementById('parent-name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const childName = document.getElementById('child-name').value;
            const childAge = parseInt(document.getElementById('child-age').value);
            const btn = document.getElementById('signup-btn');
            const errorDiv = document.getElementById('error-message');
            
            btn.textContent = 'Creating Account...';
            btn.disabled = true;
            errorDiv.classList.add('hidden');
            
            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        parent_name: parentName,
                        email, 
                        password,
                        child_name: childName,
                        child_age: childAge
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    errorDiv.querySelector('p').textContent = data.error || 'An error occurred during signup';
                    errorDiv.classList.remove('hidden');
                }
            } catch (error) {
                errorDiv.querySelector('p').textContent = 'An error occurred. Please try again.';
                errorDiv.classList.remove('hidden');
            } finally {
                btn.textContent = '🔒 SECURE MY CHILD\'S FUTURE - FREE TRIAL';
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/dashboard')
def dashboard():
    """Dashboard page - requires authentication"""
    token = session.get('token')
    if not token:
        return redirect('/signin')
    
    user_id = verify_jwt_token(token)
    if not user_id:
        session.pop('token', None)
        return redirect('/signin')
    
    user = users_db.get(user_id)
    if not user:
        return redirect('/signin')
    
    # Get user's children
    user_children = [child for child in children_db.values() if child['parent_id'] == user_id]
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Codopia</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50">
    <!-- Navigation -->
    <nav class="bg-white/80 backdrop-blur-md shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-2">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                        <span class="text-white font-bold text-xl">C</span>
                    </div>
                    <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Codopia</span>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-gray-700">Welcome, {{ user.name }}!</span>
                    <a href="/logout" class="text-purple-600 hover:text-purple-700">Sign Out</a>
                </div>
            </div>
        </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Welcome Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Welcome to Your Family Dashboard</h1>
            <p class="text-gray-600">Manage your children's coding journey and track their progress</p>
        </div>

        <!-- Children Cards -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {% for child in children %}
            <div class="bg-white rounded-2xl shadow-lg p-6 border-l-4 
                {% if child.tier == 'Magic Workshop' %}border-purple-500{% endif %}
                {% if child.tier == 'Innovation Lab' %}border-blue-500{% endif %}
                {% if child.tier == 'Professional Studio' %}border-gray-500{% endif %}
            ">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-gray-900">{{ child.name }}</h3>
                        <p class="text-gray-600">Age {{ child.age }} • {{ child.tier }}</p>
                    </div>
                    <div class="w-12 h-12 
                        {% if child.tier == 'Magic Workshop' %}bg-gradient-to-r from-purple-400 to-pink-400{% endif %}
                        {% if child.tier == 'Innovation Lab' %}bg-gradient-to-r from-blue-400 to-cyan-400{% endif %}
                        {% if child.tier == 'Professional Studio' %}bg-gradient-to-r from-gray-600 to-slate-600{% endif %}
                        rounded-full flex items-center justify-center
                    ">
                        {% if child.tier == 'Magic Workshop' %}<span class="text-white text-xl">🎨</span>{% endif %}
                        {% if child.tier == 'Innovation Lab' %}<span class="text-white text-xl">🔬</span>{% endif %}
                        {% if child.tier == 'Professional Studio' %}<span class="text-white text-xl">💼</span>{% endif %}
                    </div>
                </div>
                
                <div class="space-y-3">
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-600">Progress</span>
                        <span class="text-sm font-semibold text-gray-900">{{ child.progress }}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="
                            {% if child.tier == 'Magic Workshop' %}bg-gradient-to-r from-purple-500 to-pink-500{% endif %}
                            {% if child.tier == 'Innovation Lab' %}bg-gradient-to-r from-blue-500 to-cyan-500{% endif %}
                            {% if child.tier == 'Professional Studio' %}bg-gradient-to-r from-gray-600 to-slate-600{% endif %}
                            h-2 rounded-full
                        " style="width: {{ child.progress }}%"></div>
                    </div>
                    
                    <div class="flex justify-between items-center pt-2">
                        <span class="text-sm text-gray-600">Lessons: {{ child.completed_lessons }}/{{ child.total_lessons }}</span>
                        <span class="text-sm text-gray-600">{{ child.hours_coded }}h coded</span>
                    </div>
                </div>
                
                <div class="mt-6 space-y-2">
                    <a href="/learning/{{ child.tier.lower().replace(' ', '-') }}?child={{ child.id }}" 
                       class="w-full bg-gradient-to-r 
                            {% if child.tier == 'Magic Workshop' %}from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700{% endif %}
                            {% if child.tier == 'Innovation Lab' %}from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700{% endif %}
                            {% if child.tier == 'Professional Studio' %}from-gray-600 to-slate-600 hover:from-gray-700 hover:to-slate-700{% endif %}
                            text-white py-3 px-4 rounded-lg font-semibold text-center block transition-all
                       ">
                        Continue Learning
                    </a>
                    <button class="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-all">
                        View Progress Report
                    </button>
                </div>
            </div>
            {% endfor %}
            
            <!-- Add Child Card -->
            <div class="bg-white rounded-2xl shadow-lg p-6 border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-center min-h-[300px]">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <span class="text-gray-400 text-2xl">+</span>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">Add Another Child</h3>
                <p class="text-gray-600 mb-6">Create a profile for another child to start their coding journey</p>
                <button onclick="showAddChildModal()" class="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all">
                    Add Child Profile
                </button>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="grid md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <div class="text-3xl font-bold text-purple-600 mb-2">{{ total_children }}</div>
                <div class="text-gray-600">Active Learners</div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <div class="text-3xl font-bold text-blue-600 mb-2">{{ total_hours }}</div>
                <div class="text-gray-600">Hours Coded</div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <div class="text-3xl font-bold text-green-600 mb-2">{{ total_lessons }}</div>
                <div class="text-gray-600">Lessons Completed</div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                <div class="text-3xl font-bold text-orange-600 mb-2">{{ total_achievements }}</div>
                <div class="text-gray-600">Achievements</div>
            </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Recent Activity</h2>
            <div class="space-y-4">
                {% for activity in recent_activities %}
                <div class="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                        <span class="text-white text-sm">{{ activity.child_initial }}</span>
                    </div>
                    <div class="flex-1">
                        <p class="text-gray-900 font-medium">{{ activity.description }}</p>
                        <p class="text-gray-600 text-sm">{{ activity.time_ago }}</p>
                    </div>
                    <div class="text-{{ activity.color }}-500">
                        {{ activity.icon }}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <!-- Add Child Modal -->
    <div id="add-child-modal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Add Child Profile</h2>
            
            <form id="add-child-form" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Child's Name</label>
                    <input 
                        type="text" 
                        id="new-child-name"
                        placeholder="Enter child's name"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        required
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Child's Age</label>
                    <select 
                        id="new-child-age"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        required
                    >
                        <option value="">Select age...</option>
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
                
                <div class="flex space-x-4 pt-4">
                    <button 
                        type="button" 
                        onclick="hideAddChildModal()"
                        class="flex-1 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all"
                    >
                        Cancel
                    </button>
                    <button 
                        type="submit"
                        class="flex-1 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all"
                    >
                        Add Child
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
        function showAddChildModal() {
            document.getElementById('add-child-modal').classList.remove('hidden');
        }
        
        function hideAddChildModal() {
            document.getElementById('add-child-modal').classList.add('hidden');
        }
        
        document.getElementById('add-child-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.getElementById('new-child-name').value;
            const age = parseInt(document.getElementById('new-child-age').value);
            
            try {
                const response = await fetch('/api/add-child', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, age })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error adding child: ' + data.error);
                }
            } catch (error) {
                alert('An error occurred. Please try again.');
            }
        });
    </script>
</body>
</html>
    ''', user=user, children=user_children, 
         total_children=len(user_children),
         total_hours=sum(child.get('hours_coded', 0) for child in user_children),
         total_lessons=sum(child.get('completed_lessons', 0) for child in user_children),
         total_achievements=sum(child.get('achievements', 0) for child in user_children),
         recent_activities=[
             {
                 'child_initial': child['name'][0] if user_children else 'C',
                 'description': f"{child['name']} completed a lesson in {child['tier']}" if user_children else "Welcome to Codopia!",
                 'time_ago': '2 hours ago' if user_children else 'Just now',
                 'color': 'green',
                 'icon': '🎉'
             } for child in user_children[:3]
         ] if user_children else [
             {
                 'child_initial': 'C',
                 'description': 'Welcome to Codopia! Add your first child to get started.',
                 'time_ago': 'Just now',
                 'color': 'blue',
                 'icon': '👋'
             }
         ])

# API Routes
@app.route('/api/signin', methods=['POST'])
def api_signin():
    """Handle sign in API"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Find user by email
    user = None
    for uid, u in users_db.items():
        if u['email'] == email:
            user = u
            user['id'] = uid
            break
    
    if not user:
        return jsonify({'success': False, 'error': 'Invalid email or password'})
    
    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return jsonify({'success': False, 'error': 'Invalid email or password'})
    
    # Create session
    token = create_jwt_token(user['id'])
    session['token'] = token
    
    return jsonify({'success': True})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Handle sign up API"""
    data = request.get_json()
    parent_name = data.get('parent_name')
    email = data.get('email')
    password = data.get('password')
    child_name = data.get('child_name')
    child_age = data.get('child_age')
    
    # Check if email already exists
    for user in users_db.values():
        if user['email'] == email:
            return jsonify({'success': False, 'error': 'Email already registered'})
    
    # Create user
    user_id = f"user_{len(users_db) + 1}"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    users_db[user_id] = {
        'name': parent_name,
        'email': email,
        'password_hash': password_hash,
        'created_at': datetime.utcnow().isoformat()
    }
    
    # Create child profile
    child_id = f"child_{len(children_db) + 1}"
    tier = get_tier_from_age(child_age)
    
    children_db[child_id] = {
        'id': child_id,
        'parent_id': user_id,
        'name': child_name,
        'age': child_age,
        'tier': tier,
        'progress': 0,
        'completed_lessons': 0,
        'total_lessons': 5 if tier == 'Magic Workshop' else 5 if tier == 'Innovation Lab' else 6,
        'hours_coded': 0,
        'achievements': 0,
        'created_at': datetime.utcnow().isoformat()
    }
    
    # Create session
    token = create_jwt_token(user_id)
    session['token'] = token
    
    return jsonify({'success': True})

@app.route('/api/add-child', methods=['POST'])
def api_add_child():
    """Add child profile API"""
    token = session.get('token')
    if not token:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    user_id = verify_jwt_token(token)
    if not user_id:
        return jsonify({'success': False, 'error': 'Invalid session'})
    
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    
    # Create child profile
    child_id = f"child_{len(children_db) + 1}"
    tier = get_tier_from_age(age)
    
    children_db[child_id] = {
        'id': child_id,
        'parent_id': user_id,
        'name': name,
        'age': age,
        'tier': tier,
        'progress': 0,
        'completed_lessons': 0,
        'total_lessons': 5 if tier == 'Magic Workshop' else 5 if tier == 'Innovation Lab' else 6,
        'hours_coded': 0,
        'achievements': 0,
        'created_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    """Sign out user"""
    session.pop('token', None)
    return redirect('/')

@app.route('/learning/magic-workshop')
def magic_workshop():
    """Magic Workshop learning environment"""
    token = session.get('token')
    if not token:
        return redirect('/signin')
    
    user_id = verify_jwt_token(token)
    if not user_id:
        return redirect('/signin')
    
    child_id = request.args.get('child')
    child = children_db.get(child_id)
    
    if not child or child['parent_id'] != user_id:
        return redirect('/dashboard')
    
    # Serve the Magic Workshop learning environment
    file_path = get_file_path('templates/learning/magic_workshop.html')
    if file_path:
        return send_file(file_path)
    else:
        return "Magic Workshop learning environment coming soon!", 200

@app.route('/debug')
def debug():
    """Debug endpoint to check file paths"""
    return jsonify({
        'current_directory': os.getcwd(),
        'files_in_cwd': os.listdir('.'),
        'index_html_path': get_file_path('index.html'),
        'next_exists': os.path.exists('.next'),
        'src_exists': os.path.exists('src'),
        'users_count': len(users_db),
        'children_count': len(children_db)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
