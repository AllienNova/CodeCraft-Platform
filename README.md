# 🚀 Codopia - Where Code Becomes Craft

A comprehensive coding education platform for children ages 3-18, featuring AI-powered tutoring, interactive learning environments, and tier-based curriculum progression.

## 🌟 Overview

Codopia transforms coding education through:
- **🧙‍♂️ Professor Sparkle**: AI tutor with Gemini Live voice interaction
- **🎨 Three Learning Tiers**: Age-appropriate progression from visual blocks to professional programming
- **🔒 Enterprise Security**: Supabase authentication with Row Level Security
- **📱 Modern Stack**: Next.js 15, TypeScript, Tailwind CSS, Flask backend

## 🎯 Learning Tiers

### 🎨 Magic Workshop (Ages 3-7)
- Visual block coding with magical themes
- Story-based learning adventures
- Basic programming concepts through play
- **Lessons**: Wizard Movement, Spell Patterns, Magical Decisions, Treasure Hunt, Magic Functions

### 🔬 Innovation Lab (Ages 8-12)
- Advanced block coding and app development
- Real-world problem solving
- Collaborative projects and creativity
- **Lessons**: First App, Data Detective, Game Creator, Robot Commander, Web Designer

### 💼 Professional Studio (Ages 13-18)
- Real programming languages (Python, JavaScript, etc.)
- Software engineering principles
- Career preparation and industry practices
- **Lessons**: Python Fundamentals, OOP, Web Development, Mobile Apps, AI/ML, Career Prep

## 🏗️ Repository Structure

```
codopia-platform/
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore                # Comprehensive ignore rules
├── requirements.txt          # Python dependencies
├── package.json             # Node.js dependencies
│
├── backend/                 # Flask Backend
│   ├── main.py             # Main Flask application
│   ├── auth_service.py     # Authentication service
│   ├── supabase_client.py  # Database client
│   ├── professor_sparkle.py # AI integration
│   ├── gemini_live_sparkle.py # Gemini Live API
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Homepage
│   │   ├── about.html      # About page
│   │   ├── features.html   # Features page
│   │   ├── pricing.html    # Pricing page
│   │   ├── academy.html    # Academy page
│   │   ├── magazine.html   # Magazine page
│   │   └── learning/       # Learning modules
│   │       └── magic_workshop.html
│   └── static/             # Static assets
│       ├── css/
│       ├── js/
│       └── images/
│
├── frontend/               # React/Next.js Frontend
│   ├── components/         # React components
│   │   ├── About.jsx
│   │   ├── Features.jsx
│   │   ├── Pricing.jsx
│   │   ├── Navigation.jsx
│   │   └── Footer.jsx
│   ├── app/               # Next.js app directory
│   ├── lib/               # Utility libraries
│   ├── contexts/          # React contexts
│   └── public/            # Public assets
│
├── docs/                  # Documentation
│   ├── content/           # Content documentation
│   │   ├── about-page-content.md
│   │   ├── features-content.md
│   │   ├── magazine-content.md
│   │   └── academy-content.md
│   ├── deployment/        # Deployment guides
│   ├── api/              # API documentation
│   └── user-guides/      # User guides
│
├── scripts/              # Utility scripts
│   └── create_tables.py  # Database setup
│
└── .archive/             # Archived files
    ├── .gitkeep
    └── old_versions/
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Supabase account
- Gemini API key (for Professor Sparkle)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AllienNova/Codopia.git
cd Codopia
```

2. **Install frontend dependencies**
```bash
npm install
```

3. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
# Copy environment template
cp .env.local.example .env.local

# Configure your environment variables
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key
```

5. **Database setup**
```bash
# Run Supabase migrations
npx supabase db push
```

6. **Start development servers**
```bash
# Backend (Flask)
cd backend && python main.py

# Frontend (Next.js) - in a new terminal
cd frontend && npm run dev
```

## 🧙‍♂️ Professor Sparkle AI Tutor

### Features
- **Real-time voice interaction** using Gemini Live API
- **Age-appropriate teaching** with developmental stage awareness
- **Comprehensive safety protocols** for child protection
- **Interactive learning support** with visual aids and progress tracking

### Voice Interaction
```javascript
// Initialize Professor Sparkle
const sparkle = new ProfessorSparkleVoice();
await sparkle.connectToSparkle(childProfile);

// Voice interaction automatically handles:
// - Speech recognition and processing
// - Real-time AI response generation
// - Visual feedback synchronization
// - Progress tracking and assessment
```

### Safety Safeguards
- ✅ Never requests personal information
- ✅ Redirects inappropriate topics to educational content
- ✅ Maintains professional boundaries
- ✅ Provides accurate coding information only
- ✅ Adapts to child's developmental stage

## 🔒 Security & Authentication

### Supabase Integration
- **Row Level Security (RLS)** for data protection
- **Parent-child relationship management**
- **Automatic tier assignment** based on age
- **Session management** with secure tokens

### Authentication Flow
1. Parent creates account with email/password
2. Child profile created with age-based tier assignment
3. Secure session established with JWT tokens
4. Access control enforced through RLS policies

## 🎨 Learning Environment

### Interactive Features
- **Drag-and-drop coding blocks** for visual programming
- **Real-time code execution** with immediate feedback
- **Progress tracking** with achievement system
- **Collaborative features** for peer learning

### Curriculum Integration
- **Structured lesson progression** with prerequisites
- **Assessment criteria** for each learning objective
- **Cross-curricular connections** to math, science, and art
- **Portfolio development** for showcasing projects

## 📊 Technology Stack

### Frontend
- **Next.js 15** - React framework with app router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Supabase Client** - Database and auth integration

### Backend
- **Flask** - Python web framework
- **Supabase** - PostgreSQL database with real-time features
- **Gemini Live API** - AI voice interaction
- **WebSockets** - Real-time communication

### Infrastructure
- **Vercel** - Frontend deployment
- **Manus Cloud** - Backend hosting
- **Supabase** - Database and authentication
- **GitHub Actions** - CI/CD pipeline

## 🚀 Deployment

### Production URLs
- **Frontend**: Deployed on Vercel
- **Backend**: https://0vhlizcg6ze5.manus.space
- **Database**: Supabase cloud instance

### Environment Configuration
```bash
# Production environment variables
SUPABASE_URL=https://ylymepybqcykyomsmxwk.supabase.co
SUPABASE_ANON_KEY=your_production_key
GEMINI_API_KEY=your_production_gemini_key
FLASK_SECRET_KEY=your_secure_secret_key
```

## 📚 Documentation

- **[Architecture Overview](docs/architecture/)** - System design and migration strategies
- **[API Documentation](docs/api/)** - Gemini Live integration and endpoints
- **[Deployment Guide](docs/deployment/)** - Production deployment instructions
- **[Curriculum Guide](docs/curriculum/)** - Educational content and lesson plans

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Maintain comprehensive test coverage
- Document all new features
- Ensure child safety in all implementations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Supabase** for providing the backend infrastructure
- **Google Gemini** for AI capabilities
- **Next.js team** for the excellent React framework
- **Open source community** for the amazing tools and libraries

## 📞 Support

For support, email support@codopia.com or join our community Discord.

---

**Built with ❤️ for the next generation of coders**

*Codopia - Where Code Becomes Craft*
