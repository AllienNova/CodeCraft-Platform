from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

# Serve Next.js static files
@app.route('/')
def index():
    return send_file('.next/server/app/page.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('.next/static', path)
    except:
        try:
            return send_from_directory('public', path)
        except:
            return send_file('.next/server/app/page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
