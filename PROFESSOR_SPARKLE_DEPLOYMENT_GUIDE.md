# 🧙‍♂️ Professor Sparkle Deployment Guide with Gemini Live API

Complete step-by-step instructions for deploying Professor Sparkle AI tutor with real-time voice interaction capabilities.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Google AI API Setup](#google-ai-api-setup)
3. [Environment Configuration](#environment-configuration)
4. [Local Development Setup](#local-development-setup)
5. [Production Deployment](#production-deployment)
6. [Voice Integration Testing](#voice-integration-testing)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.11+ (required for Google AI SDK compatibility)
- **Node.js**: 18+ (for frontend components)
- **Memory**: Minimum 2GB RAM (4GB+ recommended for production)
- **Storage**: 1GB+ available space
- **Network**: Stable internet connection for API calls

### Required Accounts
- **Google AI Studio Account** (for Gemini API access)
- **Supabase Account** (for database and authentication)
- **Deployment Platform** (Vercel, Railway, or similar)

## 🔑 Google AI API Setup

### Step 1: Create Google AI Studio Account

1. **Visit Google AI Studio**
   ```
   https://aistudio.google.com/
   ```

2. **Sign in with Google Account**
   - Use your Google account or create a new one
   - Accept the terms of service

3. **Create New Project**
   - Click "Create Project" or use existing project
   - Note your project ID for later use

### Step 2: Generate API Key

1. **Navigate to API Keys**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **Create API Key**
   - Click "Create API Key"
   - Select your project
   - Copy the generated API key (starts with `AIza...`)
   - **⚠️ IMPORTANT**: Store this key securely - it won't be shown again

3. **Enable Required APIs**
   - Generative Language API
   - AI Platform API (if using advanced features)

### Step 3: Configure API Quotas

1. **Check Quotas**
   ```
   https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
   ```

2. **Recommended Settings for Production**
   - **Requests per minute**: 60+ (adjust based on expected users)
   - **Requests per day**: 1000+ (scale according to usage)
   - **Concurrent requests**: 10+ (for multiple simultaneous users)

## ⚙️ Environment Configuration

### Step 1: Clone Repository

```bash
git clone https://github.com/AllienNova/Codopia.git
cd Codopia
```

### Step 2: Create Environment Files

#### Production Environment (`.env.production`)
```bash
# Google AI Configuration
GOOGLE_AI_API_KEY=AIza_your_actual_api_key_here
GOOGLE_AI_MODEL=gemini-pro
GOOGLE_AI_VOICE_MODEL=gemini-live

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Flask Configuration
FLASK_SECRET_KEY=your_super_secure_secret_key_here
FLASK_ENV=production
FLASK_DEBUG=false

# Security Settings
JWT_SECRET_KEY=your_jwt_secret_key
CORS_ORIGINS=https://your-frontend-domain.com

# Voice Configuration
VOICE_ENABLED=true
VOICE_LANGUAGE=en-US
VOICE_SPEED=1.0
VOICE_PITCH=0.0

# Safety Configuration
SAFETY_LEVEL=strict
CONTENT_FILTERING=enabled
PARENTAL_CONTROLS=enabled

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/professor-sparkle.log
```

#### Development Environment (`.env.local`)
```bash
# Google AI Configuration
GOOGLE_AI_API_KEY=AIza_your_development_api_key_here
GOOGLE_AI_MODEL=gemini-pro

# Supabase Configuration (Development)
SUPABASE_URL=https://your-dev-project.supabase.co
SUPABASE_ANON_KEY=your_dev_supabase_anon_key

# Flask Configuration
FLASK_SECRET_KEY=dev_secret_key
FLASK_ENV=development
FLASK_DEBUG=true

# Voice Configuration
VOICE_ENABLED=true
VOICE_LANGUAGE=en-US

# Safety Configuration
SAFETY_LEVEL=strict
CONTENT_FILTERING=enabled

# Logging
LOG_LEVEL=DEBUG
```

### Step 3: Secure Environment Variables

#### For Production Servers
```bash
# Set environment variables securely
export GOOGLE_AI_API_KEY="your_api_key_here"
export SUPABASE_URL="your_supabase_url"
export FLASK_SECRET_KEY="your_secret_key"

# Or use a secure environment file
sudo nano /etc/environment
# Add your variables there
```

#### For Docker Deployment
```dockerfile
# Dockerfile environment setup
ENV GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}
ENV SUPABASE_URL=${SUPABASE_URL}
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
```

## 🛠️ Local Development Setup

### Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install additional dependencies for Gemini Live
pip install google-generativeai==0.8.3
pip install flask-socketio==5.3.6
pip install websockets==12.0
```

### Step 2: Install Frontend Dependencies

```bash
# Install Node.js dependencies
npm install

# Install additional packages for voice features
npm install @google/generative-ai
npm install socket.io-client
npm install web-speech-api
```

### Step 3: Database Setup

```bash
# Initialize Supabase
npx supabase init
npx supabase start

# Run migrations
npx supabase db push

# Seed initial data (optional)
npx supabase db seed
```

### Step 4: Start Development Servers

```bash
# Terminal 1: Start Flask backend
cd backend
source ../venv/bin/activate
python main.py

# Terminal 2: Start Next.js frontend
npm run dev

# Terminal 3: Start Supabase (if local)
npx supabase start
```

### Step 5: Test Professor Sparkle

```bash
# Run Professor Sparkle test
cd backend
python -c "
import asyncio
from gemini_live_sparkle_fixed import professor_sparkle

async def test():
    session = await professor_sparkle.initialize_session(6, 'Magic Workshop')
    response = await professor_sparkle.get_response('Hello!', session['session_id'])
    print(f'Professor Sparkle: {response}')

asyncio.run(test())
"
```

## 🚀 Production Deployment

### Option 1: Vercel + Railway Deployment

#### Frontend (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
vercel --prod

# Set environment variables in Vercel dashboard
# - NEXT_PUBLIC_SUPABASE_URL
# - NEXT_PUBLIC_SUPABASE_ANON_KEY
```

#### Backend (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables in Railway dashboard
# - GOOGLE_AI_API_KEY
# - SUPABASE_URL
# - FLASK_SECRET_KEY
```

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Run application
CMD ["python", "main.py"]
```

#### Docker Compose Setup
```yaml
version: '3.8'

services:
  professor-sparkle:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
    volumes:
      - ./logs:/var/log
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - professor-sparkle
    restart: unless-stopped
```

#### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f professor-sparkle

# Scale if needed
docker-compose up -d --scale professor-sparkle=3
```

### Option 3: Cloud Platform Deployment

#### Google Cloud Platform
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Initialize and deploy
gcloud init
gcloud app deploy

# Set environment variables
gcloud app versions set-env-vars \
  GOOGLE_AI_API_KEY="your_api_key" \
  SUPABASE_URL="your_supabase_url"
```

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create production
eb deploy

# Set environment variables
eb setenv GOOGLE_AI_API_KEY="your_api_key"
eb setenv SUPABASE_URL="your_supabase_url"
```

## 🎙️ Voice Integration Testing

### Step 1: Test Basic Voice Recognition

```javascript
// Frontend voice test
const testVoiceRecognition = () => {
  if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onresult = (event) => {
      const transcript = event.results[event.results.length - 1][0].transcript;
      console.log('Voice input:', transcript);
    };
    
    recognition.start();
  }
};
```

### Step 2: Test Gemini Live Integration

```python
# Backend Gemini Live test
import asyncio
from gemini_live_sparkle_fixed import professor_sparkle

async def test_gemini_live():
    # Test with real API key
    session = await professor_sparkle.initialize_session(8, 'Innovation Lab')
    
    # Test various inputs
    test_inputs = [
        "Hello Professor Sparkle!",
        "Can you help me build an app?",
        "What is a variable?",
        "I'm stuck on my code"
    ]
    
    for input_text in test_inputs:
        response = await professor_sparkle.get_response(
            input_text, 
            session['session_id'], 
            8, 
            'Innovation Lab'
        )
        print(f"Input: {input_text}")
        print(f"Response: {response}\n")

# Run test
asyncio.run(test_gemini_live())
```

### Step 3: Test WebSocket Communication

```javascript
// Test real-time communication
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to Professor Sparkle');
  
  // Test voice message
  socket.emit('voice_message', {
    message: 'Hello Professor Sparkle!',
    child_age: 6,
    tier: 'Magic Workshop'
  });
});

socket.on('sparkle_response', (data) => {
  console.log('Professor Sparkle says:', data.response);
  // Convert to speech
  const utterance = new SpeechSynthesisUtterance(data.response);
  speechSynthesis.speak(utterance);
});
```

## 📊 Monitoring & Maintenance

### Step 1: Set Up Logging

```python
# Enhanced logging configuration
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        RotatingFileHandler('professor_sparkle.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('professor_sparkle')
```

### Step 2: Health Check Endpoints

```python
# Add to Flask app
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': time.time(),
        'gemini_status': 'connected' if professor_sparkle.gemini_ready else 'fallback',
        'version': '1.0.0'
    }

@app.route('/metrics')
def metrics():
    return {
        'active_sessions': len(professor_sparkle.session_data),
        'total_responses': professor_sparkle.total_responses,
        'safety_triggers': professor_sparkle.safety_triggers,
        'uptime': time.time() - start_time
    }
```

### Step 3: Performance Monitoring

```python
# Add performance tracking
import time
from functools import wraps

def track_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

# Apply to Professor Sparkle methods
@track_performance
async def get_response(self, message, session_id=None, child_age=6, tier="Magic Workshop"):
    # ... existing code
```

### Step 4: Error Alerting

```python
# Set up error notifications
import smtplib
from email.mime.text import MIMEText

def send_alert(error_message):
    msg = MIMEText(f"Professor Sparkle Error: {error_message}")
    msg['Subject'] = 'Professor Sparkle Alert'
    msg['From'] = 'alerts@codopia.com'
    msg['To'] = 'admin@codopia.com'
    
    # Send email (configure SMTP settings)
    # smtp_server.send_message(msg)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Gemini API Key Issues
```bash
# Symptoms: "API key not valid" errors
# Solutions:
- Verify API key is correct and active
- Check API quotas in Google Cloud Console
- Ensure billing is enabled for the project
- Test with curl:
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

#### 2. WebSocket Connection Issues
```javascript
// Symptoms: Voice interaction not working
// Solutions:
- Check CORS settings in Flask app
- Verify WebSocket port is open
- Test connection manually:
const socket = io('http://localhost:5000', {
  transports: ['websocket', 'polling']
});
```

#### 3. Voice Recognition Problems
```javascript
// Symptoms: Speech not being recognized
// Solutions:
- Check browser permissions for microphone
- Test in HTTPS environment (required for production)
- Verify browser compatibility:
if (!('webkitSpeechRecognition' in window)) {
  console.error('Speech recognition not supported');
}
```

#### 4. Performance Issues
```python
# Symptoms: Slow response times
# Solutions:
- Implement response caching
- Use connection pooling for database
- Add request rate limiting:
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)
```

#### 5. Memory Issues
```bash
# Symptoms: High memory usage
# Solutions:
- Implement session cleanup
- Use memory profiling:
pip install memory-profiler
python -m memory_profiler main.py

# Add session cleanup
def cleanup_old_sessions():
    current_time = time.time()
    for session_id, session in list(professor_sparkle.session_data.items()):
        if current_time - session['created_at'] > 3600:  # 1 hour
            del professor_sparkle.session_data[session_id]
```

### Debug Mode Setup

```python
# Enable debug mode for troubleshooting
import os
os.environ['FLASK_DEBUG'] = 'true'
os.environ['LOG_LEVEL'] = 'DEBUG'

# Add debug endpoints
@app.route('/debug/sessions')
def debug_sessions():
    return {
        'active_sessions': list(professor_sparkle.session_data.keys()),
        'session_count': len(professor_sparkle.session_data)
    }

@app.route('/debug/test-gemini')
async def debug_gemini():
    try:
        response = await professor_sparkle.get_response("Test message", None, 6, "Magic Workshop")
        return {'status': 'success', 'response': response}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
```

## 🎯 Production Checklist

### Pre-Deployment
- [ ] Google AI API key configured and tested
- [ ] Supabase database set up with proper RLS policies
- [ ] Environment variables securely configured
- [ ] SSL certificates installed (for HTTPS)
- [ ] CORS settings configured for production domains
- [ ] Rate limiting implemented
- [ ] Logging and monitoring set up
- [ ] Error alerting configured
- [ ] Backup strategy implemented

### Post-Deployment
- [ ] Health check endpoints responding
- [ ] Voice recognition working in production
- [ ] WebSocket connections stable
- [ ] Professor Sparkle responses appropriate
- [ ] Safety protocols functioning
- [ ] Performance metrics within acceptable ranges
- [ ] Error rates below threshold
- [ ] User authentication working
- [ ] Database connections stable
- [ ] SSL certificates valid

### Ongoing Maintenance
- [ ] Monitor API usage and costs
- [ ] Review safety logs regularly
- [ ] Update dependencies monthly
- [ ] Backup database weekly
- [ ] Review performance metrics
- [ ] Update content and responses
- [ ] Test disaster recovery procedures
- [ ] Monitor user feedback

## 📞 Support and Resources

### Documentation
- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/rest)
- [Supabase Documentation](https://supabase.com/docs)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)

### Community Support
- [Codopia GitHub Issues](https://github.com/AllienNova/Codopia/issues)
- [Google AI Developer Community](https://developers.googleblog.com/2023/12/how-its-made-gemini-multimodal-prompting.html)
- [Supabase Discord](https://discord.supabase.com/)

### Professional Support
- Email: support@codopia.com
- Documentation: https://docs.codopia.com
- Status Page: https://status.codopia.com

---

**🎉 Congratulations!** You now have Professor Sparkle deployed with full Gemini Live API integration, providing children with an interactive, safe, and educational AI coding tutor experience!

*Built with ❤️ for the next generation of coders*

