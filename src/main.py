from flask import Flask, send_from_directory, send_file, jsonify
import os

app = Flask(__name__)

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

@app.route('/')
def index():
    file_path = find_file('.next/server/app/index.html')
    if file_path:
        return send_file(file_path)
    
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
            .btn { background: white; color: #667eea; padding: 15px 30px; border: none; border-radius: 25px; font-size: 1.1em; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Codopia</h1>
            <p>Where Code Becomes Craft</p>
            <p>A comprehensive coding education platform for children ages 5-10.</p>
            <a href="/auth/signin" class="btn">Get Started</a>
            <p style="margin-top: 40px; font-size: 0.9em; opacity: 0.8;">
                Platform is loading... If you see this page, the deployment is working but Next.js files are still being processed.
            </p>
        </div>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/auth/signin')
def signin():
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
            input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
            .btn { background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
            .btn:hover { background: #5a6fd8; }
            .back-link { text-align: center; margin-top: 20px; }
            .back-link a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Welcome Back to Codopia</h2>
            <form>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" placeholder="parent@example.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" placeholder="Enter your password" required>
                </div>
                <button type="submit" class="btn">Sign In</button>
            </form>
            <div class="back-link">
                <a href="/">← Back to Home</a> | 
                <a href="/auth/signup">Create Account</a>
            </div>
        </div>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/auth/signup') 
def signup():
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
            input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
            .btn { background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
            .btn:hover { background: #5a6fd8; }
            .back-link { text-align: center; margin-top: 20px; }
            .back-link a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Join Codopia Today</h2>
            <form>
                <div class="form-group">
                    <label>Parent Email</label>
                    <input type="email" placeholder="your.email@example.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" placeholder="Create a secure password" required>
                </div>
                <div class="form-group">
                    <label>Child's Name</label>
                    <input type="text" placeholder="Your child's name" required>
                </div>
                <div class="form-group">
                    <label>Child's Age</label>
                    <select required>
                        <option value="">Select age</option>
                        <option value="5">5 years old</option>
                        <option value="6">6 years old</option>
                        <option value="7">7 years old</option>
                        <option value="8">8 years old</option>
                        <option value="9">9 years old</option>
                        <option value="10">10 years old</option>
                    </select>
                </div>
                <button type="submit" class="btn">Start Free Trial</button>
            </form>
            <div class="back-link">
                <a href="/">← Back to Home</a> | 
                <a href="/auth/signin">Already have an account?</a>
            </div>
        </div>
    </body>
    </html>
    ''', 200, {'Content-Type': 'text/html'}

@app.route('/dashboard')
def dashboard():
    file_path = find_file('.next/server/app/dashboard.html')
    if file_path:
        return send_file(file_path)
    return "Dashboard page - Coming soon!", 200

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
    """Debug endpoint to check file locations"""
    cwd = os.getcwd()
    script_dir = os.path.dirname(__file__)
    
    files_info = {
        'current_directory': cwd,
        'script_directory': script_dir,
        'files_in_cwd': os.listdir(cwd) if os.path.exists(cwd) else [],
        'files_in_script_dir': os.listdir(script_dir) if os.path.exists(script_dir) else [],
        'src_exists': os.path.exists('/src'),
        'next_exists_cwd': os.path.exists(os.path.join(cwd, '.next')),
        'next_exists_src': os.path.exists('/src/.next'),
        'index_html_path': find_file('.next/server/app/index.html'),
        'next_directory_path': find_directory('.next')
    }
    return jsonify(files_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
