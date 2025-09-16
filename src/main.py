from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('../.next/server/app/index.html')

@app.route('/auth/signin')
def signin():
    return send_file('../.next/server/app/auth/signin/index.html')

@app.route('/auth/signup') 
def signup():
    return send_file('../.next/server/app/auth/signup/index.html')

@app.route('/dashboard')
def dashboard():
    return send_file('../.next/server/app/dashboard.html')

@app.route('/_next/<path:path>')
def serve_next(path):
    return send_from_directory('../.next', path)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../public', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
