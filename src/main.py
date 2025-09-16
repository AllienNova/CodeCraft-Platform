from flask import Flask, send_from_directory, send_file, jsonify, request, make_response, redirect, url_for
import os
from auth_service import SupabaseAuthService
from professor_sparkle import ProfessorSparkle, create_sparkle_routes

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Initialize Supabase Auth Service
auth_service = SupabaseAuthService()

def find_file(relative_path):
    """Find file in multiple possible locations with detailed logging"""
    possible_paths = [
        relative_path,
        os.path.join('src', relative_path),
        os.path.join('/src', relative_path),
        os.path.join(os.getcwd(), relative_path),
        os.path.join(os.path.dirname(__file__), relative_path),
        os.path.join(os.path.dirname(__file__), '..', relative_path)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def find_directory(relative_path):
    """Find directory in multiple possible locations"""
    possible_paths = [
        relative_path,
        os.path.join('src', relative_path),
        os.path.join('/src', relative_path),
        os.path.join(os.getcwd(), relative_path),
        os.path.join(os.path.dirname(__file__), relative_path),
        os.path.join(os.path.dirname(__file__), '..', relative_path)
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            return path
    return None

def get_current_user():
    """Get current user from session token"""
    token = request.cookies.get('session_token')
    if not token:
        return None
    
    result = auth_service.verify_session_token(token)
    if result['success']:
        user_data = auth_service.get_user_with_children(result['user_id'])
        if user_data['success']:
            return {
                'id': result['user_id'],
                'profile': user_data['profile'],
                'children': user_data['children']
            }
    return None

@app.route('/')
def index():
    file_path = find_file('.next/server/app/index.html')
    if file_path:
        return send_file(file_path)
    
    # Check if user is logged in
    user = get_current_user()
    if user:
        return redirect('/dashboard')
    
    # Fallback: serve a basic HTML page if Next.js files not found
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Codopia - Code Your Future, Change Your World</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { text-align: center; max-width: 600px; }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; margin-bottom: 30px; }
            .btn { background: white; color: #667eea; padding: 15px 30px; border: none; border-radius: 25px; font-size: 1.1em; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
            .features { margin-top: 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .feature { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Codopia</h1>
            <p>Where Code Becomes Craft</p>
            <p>A comprehensive coding education platform for children ages 5-10.</p>
            <div>
                <a href="/auth/signin" class="btn">Sign In</a>
                <a href="/auth/signup" class="btn">Start Free Trial</a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🎨 Magic Workshop</h3>
                    <p>Ages 5-7: Visual block coding with magical themes</p>
                </div>
                <div class="feature">
                    <h3>🔬 Innovation Lab</h3>
                    <p>Ages 8-12: Advanced blocks and app building</p>
                </div>
                <div class="feature">
                    <h3>💼 Professional Studio</h3>
                    <p>Ages 13+: Real programming languages</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/auth/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password are required"}), 400
        
        result = auth_service.sign_in_user(email, password)
        
        if result['success']:
            # Create session token
            token = auth_service.create_session_token(result['user'].id)
            
            response = make_response(jsonify({
                "success": True,
                "message": "Signed in successfully",
                "redirect": "/dashboard"
            }))
            response.set_cookie('session_token', token, max_age=7*24*60*60, httponly=True, secure=True)
            return response
        else:
            return jsonify(result), 401
    
    # GET request - show signin form
    file_path = find_file('.next/server/app/auth/signin/index.html')
    if file_path:
        return send_file(file_path)
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign In - Codopia</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }
            h2 { text-align: center; color: #333; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; }
            input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }
            .btn { background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
            .btn:hover { background: #5a6fd8; }
            .btn:disabled { background: #ccc; cursor: not-allowed; }
            .back-link { text-align: center; margin-top: 20px; }
            .back-link a { color: #667eea; text-decoration: none; }
            .error { color: #e74c3c; margin-top: 10px; text-align: center; }
            .success { color: #27ae60; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Welcome Back to Codopia</h2>
            <form id="signinForm">
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" id="email" name="email" placeholder="parent@example.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit" class="btn" id="submitBtn">Sign In</button>
                <div id="message"></div>
            </form>
            <div class="back-link">
                <a href="/">← Back to Home</a> | 
                <a href="/auth/signup">Create Account</a>
            </div>
        </div>
        
        <script>
            document.getElementById('signinForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const messageDiv = document.getElementById('message');
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing In...';
                messageDiv.innerHTML = '';
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                try {
                    const response = await fetch('/auth/signin', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        messageDiv.innerHTML = '<div class="success">' + result.message + '</div>';
                        setTimeout(() => {
                            window.location.href = result.redirect;
                        }, 1000);
                    } else {
                        messageDiv.innerHTML = '<div class="error">' + result.error + '</div>';
                    }
                } catch (error) {
                    messageDiv.innerHTML = '<div class="error">An error occurred. Please try again.</div>';
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Sign In';
                }
            });
        </script>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        child_name = data.get('child_name')
        child_age = data.get('child_age')
        
        if not all([email, password, full_name, child_name, child_age]):
            return jsonify({"success": False, "error": "All fields are required"}), 400
        
        try:
            child_age = int(child_age)
        except ValueError:
            return jsonify({"success": False, "error": "Invalid age"}), 400
        
        # Create user account
        user_result = auth_service.create_user_account(email, password, full_name)
        
        if user_result['success']:
            # Create child profile
            child_result = auth_service.create_child_profile(
                user_result['user'].id, 
                child_name, 
                child_age
            )
            
            if child_result['success']:
                # Create session token
                token = auth_service.create_session_token(user_result['user'].id)
                
                response = make_response(jsonify({
                    "success": True,
                    "message": f"Account created successfully! {child_name} has been enrolled in {child_result['child']['tier'].replace('_', ' ').title()}.",
                    "redirect": "/dashboard"
                }))
                response.set_cookie('session_token', token, max_age=7*24*60*60, httponly=True, secure=True)
                return response
            else:
                return jsonify({
                    "success": False,
                    "error": f"Account created but failed to create child profile: {child_result['error']}"
                }), 500
        else:
            return jsonify(user_result), 400
    
    # GET request - show signup form
    file_path = find_file('.next/server/app/auth/signup/index.html')
    if file_path:
        return send_file(file_path)
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign Up - Codopia</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .form-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }
            h2 { text-align: center; color: #333; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; }
            input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; box-sizing: border-box; }
            .btn { background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
            .btn:hover { background: #5a6fd8; }
            .btn:disabled { background: #ccc; cursor: not-allowed; }
            .back-link { text-align: center; margin-top: 20px; }
            .back-link a { color: #667eea; text-decoration: none; }
            .error { color: #e74c3c; margin-top: 10px; text-align: center; }
            .success { color: #27ae60; margin-top: 10px; text-align: center; }
            .tier-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #667eea; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Join Codopia Today</h2>
            <form id="signupForm">
                <div class="form-group">
                    <label>Your Full Name</label>
                    <input type="text" id="full_name" name="full_name" placeholder="Your full name" required>
                </div>
                <div class="form-group">
                    <label>Parent Email</label>
                    <input type="email" id="email" name="email" placeholder="your.email@example.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="password" name="password" placeholder="Create a secure password" required>
                </div>
                <div class="form-group">
                    <label>Child's Name</label>
                    <input type="text" id="child_name" name="child_name" placeholder="Your child's name" required>
                </div>
                <div class="form-group">
                    <label>Child's Age</label>
                    <select id="child_age" name="child_age" required onchange="updateTierInfo()">
                        <option value="">Select age</option>
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
                    </select>
                </div>
                <div id="tierInfo" class="tier-info" style="display: none;">
                    <strong>Learning Tier: </strong><span id="tierName"></span><br>
                    <small id="tierDescription"></small>
                </div>
                <button type="submit" class="btn" id="submitBtn">Start Free Trial</button>
                <div id="message"></div>
            </form>
            <div class="back-link">
                <a href="/">← Back to Home</a> | 
                <a href="/auth/signin">Already have an account?</a>
            </div>
        </div>
        
        <script>
            function updateTierInfo() {
                const age = parseInt(document.getElementById('child_age').value);
                const tierInfo = document.getElementById('tierInfo');
                const tierName = document.getElementById('tierName');
                const tierDescription = document.getElementById('tierDescription');
                
                if (age) {
                    let tier, description;
                    if (age <= 7) {
                        tier = 'Magic Workshop';
                        description = 'Visual block coding with magical themes and storytelling';
                    } else if (age <= 12) {
                        tier = 'Innovation Lab';
                        description = 'Advanced blocks, app building, and creative projects';
                    } else {
                        tier = 'Professional Studio';
                        description = 'Real programming languages and professional development tools';
                    }
                    
                    tierName.textContent = tier;
                    tierDescription.textContent = description;
                    tierInfo.style.display = 'block';
                } else {
                    tierInfo.style.display = 'none';
                }
            }
            
            document.getElementById('signupForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const messageDiv = document.getElementById('message');
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating Account...';
                messageDiv.innerHTML = '';
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                try {
                    const response = await fetch('/auth/signup', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        messageDiv.innerHTML = '<div class="success">' + result.message + '</div>';
                        setTimeout(() => {
                            window.location.href = result.redirect;
                        }, 2000);
                    } else {
                        messageDiv.innerHTML = '<div class="error">' + result.error + '</div>';
                    }
                } catch (error) {
                    messageDiv.innerHTML = '<div class="error">An error occurred. Please try again.</div>';
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Start Free Trial';
                }
            });
        </script>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect('/auth/signin')
    
    file_path = find_file('.next/server/app/dashboard.html')
    if file_path:
        return send_file(file_path)
    
    # Generate dashboard HTML with user data
    children_html = ""
    if user['children']:
        for child in user['children']:
            tier_info = {
                'magic_workshop': {'name': 'Magic Workshop', 'color': '#e91e63', 'description': 'Ages 5-7 • Visual block coding'},
                'innovation_lab': {'name': 'Innovation Lab', 'color': '#2196f3', 'description': 'Ages 8-12 • Advanced blocks'},
                'professional_studio': {'name': 'Professional Studio', 'color': '#4caf50', 'description': 'Ages 13+ • Real programming'}
            }.get(child['tier'], {'name': 'Unknown', 'color': '#666', 'description': ''})
            
            children_html += f'''
            <div class="child-card" style="border-left: 4px solid {tier_info['color']};">
                <h3>{child['name']} (Age {child['age']})</h3>
                <p><strong>{tier_info['name']}</strong></p>
                <p>{tier_info['description']}</p>
                <button class="btn-small">Continue Learning</button>
            </div>
            '''
    else:
        children_html = '''
        <div class="empty-state">
            <h3>No children added yet</h3>
            <p>Add your first child to get started with their coding journey</p>
            <button class="btn" onclick="showAddChildForm()">Add Child</button>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Codopia</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f5f5; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }}
            .header h1 {{ margin: 0; }}
            .header p {{ margin: 5px 0 0 0; opacity: 0.9; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .children-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
            .child-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .child-card h3 {{ margin: 0 0 10px 0; color: #333; }}
            .child-card p {{ margin: 5px 0; color: #666; }}
            .btn {{ background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
            .btn:hover {{ background: #5a6fd8; }}
            .btn-small {{ background: #667eea; color: white; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }}
            .btn-small:hover {{ background: #5a6fd8; }}
            .empty-state {{ text-align: center; padding: 40px; background: white; border-radius: 10px; }}
            .nav {{ background: white; padding: 15px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .nav a {{ color: #667eea; text-decoration: none; margin-right: 20px; }}
            .nav a:hover {{ text-decoration: underline; }}
            .logout {{ float: right; }}
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/dashboard">Dashboard</a>
            <a href="/profile">Profile</a>
            <a href="/auth/signout" class="logout">Sign Out</a>
        </div>
        
        <div class="header">
            <h1>Welcome back, {user['profile']['full_name'] if user['profile'] else 'Parent'}!</h1>
            <p>Manage your children's coding journey</p>
        </div>
        
        <div class="container">
            <h2>Your Children</h2>
            <div class="children-grid">
                {children_html}
            </div>
        </div>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/auth/signout')
def signout():
    response = make_response(redirect('/'))
    response.set_cookie('session_token', '', expires=0)
    return response

@app.route('/api/add-child', methods=['POST'])
def add_child():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    
    if not name or not age:
        return jsonify({"success": False, "error": "Name and age are required"}), 400
    
    try:
        age = int(age)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid age"}), 400
    
    result = auth_service.create_child_profile(user['id'], name, age)
    return jsonify(result)

@app.route('/_next/<path:path>')
def serve_next(path):
    next_dir = find_directory('.next')
    if next_dir:
        try:
            return send_from_directory(next_dir, path)
        except:
            pass
    return "Asset not found", 404

@app.route('/static/<path:path>')
def serve_static(path):
    public_dir = find_directory('public')
    if public_dir:
        try:
            return send_from_directory(public_dir, path)
        except:
            pass
    return "Static file not found", 404

@app.route('/debug')
def debug():
    """Debug endpoint to check file locations and auth status"""
    cwd = os.getcwd()
    script_dir = os.path.dirname(__file__)
    user = get_current_user()
    
    files_info = {
        'current_directory': cwd,
        'script_directory': script_dir,
        'files_in_cwd': os.listdir(cwd) if os.path.exists(cwd) else [],
        'files_in_script_dir': os.listdir(script_dir) if os.path.exists(script_dir) else [],
        'src_exists': os.path.exists('/src'),
        'next_exists_cwd': os.path.exists(os.path.join(cwd, '.next')),
        'next_exists_src': os.path.exists('/src/.next'),
        'index_html_path': find_file('.next/server/app/index.html'),
        'next_directory_path': find_directory('.next'),
        'authenticated_user': user is not None,
        'user_id': user['id'] if user else None,
        'children_count': len(user['children']) if user else 0
    }
    return jsonify(files_info)

# Add learning environment routes
@app.route('/learning/magic-workshop')
def magic_workshop():
    user = get_current_user()
    if not user:
        return redirect('/auth/signin')
    
    # Find a child in Magic Workshop tier
    magic_child = None
    for child in user['children']:
        if child['tier'] == 'magic_workshop':
            magic_child = child
            break
    
    if not magic_child:
        return redirect('/dashboard?error=no_magic_workshop_child')
    
    # Serve the Magic Workshop learning environment
    template_path = find_file('templates/learning/magic_workshop.html')
    if template_path:
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Replace child name in template
        content = content.replace('Emma', magic_child['name'])
        return content, 200, {'Content-Type': 'text/html'}
    
    return "Magic Workshop not found", 404

@app.route('/learning/innovation-lab')
def innovation_lab():
    user = get_current_user()
    if not user:
        return redirect('/auth/signin')
    
    return "Innovation Lab coming soon!", 200

@app.route('/learning/professional-studio')
def professional_studio():
    user = get_current_user()
    if not user:
        return redirect('/auth/signin')
    
    return "Professional Studio coming soon!", 200

# Serve static files for learning environment
@app.route('/static/<path:filename>')
def serve_learning_static(filename):
    static_dir = find_directory('static')
    if static_dir:
        return send_from_directory(static_dir, filename)
    return "File not found", 404

# Initialize Professor Sparkle routes
professor_sparkle = ProfessorSparkle()
create_sparkle_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
