from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

def find_file(relative_path):
    """Find file in multiple possible locations"""
    possible_paths = [
        relative_path,
        os.path.join('/src', relative_path),
        os.path.join(os.getcwd(), relative_path),
        os.path.join(os.path.dirname(__file__), relative_path)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

@app.route('/')
def index():
    file_path = find_file('.next/server/app/index.html')
    if file_path:
        return send_file(file_path)
    return f"File not found. Checked paths: {['.next/server/app/index.html', '/src/.next/server/app/index.html']}", 404

@app.route('/auth/signin')
def signin():
    file_path = find_file('.next/server/app/auth/signin/index.html')
    if file_path:
        return send_file(file_path)
    return "Signin page not found", 404

@app.route('/auth/signup') 
def signup():
    file_path = find_file('.next/server/app/auth/signup/index.html')
    if file_path:
        return send_file(file_path)
    return "Signup page not found", 404

@app.route('/dashboard')
def dashboard():
    file_path = find_file('.next/server/app/dashboard.html')
    if file_path:
        return send_file(file_path)
    return "Dashboard page not found", 404

@app.route('/_next/<path:path>')
def serve_next(path):
    next_dir = find_file('.next')
    if next_dir and os.path.isdir(next_dir):
        return send_from_directory(next_dir, path)
    return "Next.js assets not found", 404

@app.route('/static/<path:path>')
def serve_static(path):
    public_dir = find_file('public')
    if public_dir and os.path.isdir(public_dir):
        return send_from_directory(public_dir, path)
    return "Static assets not found", 404

@app.route('/debug')
def debug():
    """Debug endpoint to check file locations"""
    cwd = os.getcwd()
    files_info = {
        'current_directory': cwd,
        'files_in_cwd': os.listdir(cwd) if os.path.exists(cwd) else [],
        'src_exists': os.path.exists('/src'),
        'next_exists': os.path.exists('.next'),
        'index_html_path': find_file('.next/server/app/index.html')
    }
    return files_info

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
