import React, { useState } from 'react';

const Features = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const features = {
    overview: [
      {
        icon: '🦄',
        title: 'Age-Appropriate Learning',
        description: 'Three distinct tiers designed specifically for different developmental stages, ensuring optimal challenge and engagement.',
        details: ['Magic Workshop (Ages 5-7)', 'Innovation Lab (Ages 8-9)', 'Professional Studio (Ages 10+)']
      },
      {
        icon: '🎮',
        title: 'Gamified Experience',
        description: 'Learning feels like playing with achievement systems, progress tracking, and celebration moments.',
        details: ['Badge collection system', 'Progress visualization', 'Celebration animations', 'Peer sharing']
      },
      {
        icon: '🔒',
        title: 'Safety & Privacy',
        description: 'COPPA+ compliant platform with comprehensive parental controls and child-safe interactions.',
        details: ['COPPA compliance', 'Parental dashboard', 'Content moderation', 'Secure data handling']
      },
      {
        icon: '🚀',
        title: 'Real-World Skills',
        description: 'From visual blocks to professional coding languages, children learn skills used by industry professionals.',
        details: ['Visual programming', 'Text-based coding', 'Professional tools', 'Industry practices']
      }
    ],
    magic: [
      {
        icon: '✨',
        title: 'Sparkle the Unicorn Guide',
        description: 'Magical mascot provides encouragement, guidance, and celebrates every achievement.',
        details: ['Interactive character', 'Encouraging messages', 'Progress celebrations', 'Emotional support']
      },
      {
        icon: '🎭',
        title: 'Spell-Casting Interface',
        description: 'Drag-and-drop "magic blocks" that feel like casting spells but teach real programming concepts.',
        details: ['Visual block programming', 'Drag-and-drop interface', 'Immediate feedback', 'No reading required']
      },
      {
        icon: '🌈',
        title: 'Animated Characters',
        description: 'Lovable characters like Benny Bunny and Freddy Frog respond to code and bring stories to life.',
        details: ['Character animations', 'Interactive responses', 'Story creation', 'Emotional engagement']
      },
      {
        icon: '🎪',
        title: 'Magical Adventures',
        description: '10 progressive adventures that teach fundamental programming concepts through magical storytelling.',
        details: ['Progressive difficulty', 'Story-based learning', 'Concept reinforcement', 'Creative expression']
      }
    ],
    innovation: [
      {
        icon: '🤖',
        title: 'Robo the Robot Mentor',
        description: 'Tech-savvy guide that introduces advanced concepts and celebrates innovation.',
        details: ['Advanced guidance', 'Technical explanations', 'Innovation encouragement', 'Problem-solving tips']
      },
      {
        icon: '📱',
        title: 'Real App Development',
        description: 'Build actual mobile apps with databases, APIs, and user interfaces that work in the real world.',
        details: ['Mobile app creation', 'Database integration', 'API connections', 'User interface design']
      },
      {
        icon: '🔧',
        title: 'Visual Programming Plus',
        description: 'Advanced visual blocks with real code generation, bridging visual and text-based programming.',
        details: ['Advanced block types', 'Code generation', 'Logic structures', 'Data manipulation']
      },
      {
        icon: '🌐',
        title: 'Internet Integration',
        description: 'Connect apps to real web services, APIs, and cloud platforms for authentic development experience.',
        details: ['Web service integration', 'Cloud deployment', 'API usage', 'Real-world connections']
      }
    ],
    professional: [
      {
        icon: '🧠',
        title: 'CodeMentor AI Assistant',
        description: 'Intelligent AI guide that provides real-time code suggestions, debugging help, and best practices.',
        details: ['Code suggestions', 'Error detection', 'Best practices', 'Performance optimization']
      },
      {
        icon: '💻',
        title: 'Professional IDE',
        description: 'Full-featured development environment with syntax highlighting, debugging, and version control.',
        details: ['Syntax highlighting', 'Debugging tools', 'Version control', 'Multi-language support']
      },
      {
        icon: '☁️',
        title: 'Cloud Deployment',
        description: 'Deploy real applications to professional cloud platforms like Vercel, Netlify, and Heroku.',
        details: ['Multiple cloud platforms', 'One-click deployment', 'Custom domains', 'Production environments']
      },
      {
        icon: '🔬',
        title: 'Testing & DevOps',
        description: 'Learn industry-standard practices including testing, CI/CD, and professional development workflows.',
        details: ['Automated testing', 'CI/CD pipelines', 'Code quality', 'Professional workflows']
      }
    ]
  };

  const tabs = [
    { id: 'overview', label: 'Platform Overview', icon: '🌟' },
    { id: 'magic', label: 'Magic Workshop', icon: '🦄' },
    { id: 'innovation', label: 'Innovation Lab', icon: '🚀' },
    { id: 'professional', label: 'Professional Studio', icon: '💻' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Platform Features
            </span>
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed">
            Discover the comprehensive features that make CodeCraft the most effective 
            and engaging coding education platform for children.
          </p>
        </div>
      </section>

      {/* Feature Tabs */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Tab Navigation */}
          <div className="flex flex-wrap justify-center mb-12 bg-white rounded-2xl p-2 shadow-lg">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                    : 'text-gray-600 hover:text-purple-600'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Feature Grid */}
          <div className="grid md:grid-cols-2 gap-8">
            {features[activeTab].map((feature, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all">
                <div className="flex items-start mb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center mr-6 flex-shrink-0">
                    <span className="text-2xl">{feature.icon}</span>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-3">{feature.title}</h3>
                    <p className="text-gray-600 leading-relaxed mb-4">{feature.description}</p>
                  </div>
                </div>
                <ul className="space-y-2">
                  {feature.details.map((detail, idx) => (
                    <li key={idx} className="flex items-center text-gray-700">
                      <span className="w-2 h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mr-3"></span>
                      {detail}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technical Specifications */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Technical Specifications
            </span>
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Platform Requirements */}
            <div className="bg-gray-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Platform Requirements</h3>
              <ul className="space-y-3 text-gray-700">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Modern web browser (Chrome, Firefox, Safari, Edge)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Stable internet connection
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Tablet or desktop recommended
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  No software installation required
                </li>
              </ul>
            </div>

            {/* Supported Languages */}
            <div className="bg-gray-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Programming Languages</h3>
              <ul className="space-y-3 text-gray-700">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Visual Block Programming (Scratch-like)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Python (Professional Studio)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  JavaScript (Professional Studio)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  HTML/CSS (Professional Studio)
                </li>
              </ul>
            </div>

            {/* Security Features */}
            <div className="bg-gray-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Security & Privacy</h3>
              <ul className="space-y-3 text-gray-700">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  COPPA+ compliant
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  End-to-end encryption
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  Comprehensive parental controls
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  Content moderation
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Integration Capabilities */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Integration & Deployment
            </span>
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Cloud Platforms */}
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Supported Cloud Platforms</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">☁️</span>
                  <span className="font-semibold">Vercel</span>
                </div>
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">🌐</span>
                  <span className="font-semibold">Netlify</span>
                </div>
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">🚀</span>
                  <span className="font-semibold">Heroku</span>
                </div>
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">📄</span>
                  <span className="font-semibold">GitHub Pages</span>
                </div>
              </div>
            </div>

            {/* Development Tools */}
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">Professional Development Tools</h3>
              <div className="space-y-4">
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">🔧</span>
                  <div>
                    <div className="font-semibold">Git Version Control</div>
                    <div className="text-sm text-gray-600">Professional source code management</div>
                  </div>
                </div>
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">🧪</span>
                  <div>
                    <div className="font-semibold">Automated Testing</div>
                    <div className="text-sm text-gray-600">Unit and integration testing frameworks</div>
                  </div>
                </div>
                <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">🔄</span>
                  <div>
                    <div className="font-semibold">CI/CD Pipelines</div>
                    <div className="text-sm text-gray-600">Continuous integration and deployment</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Experience All Features with Your Free Trial
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Discover how CodeCraft's comprehensive feature set transforms children into confident programmers.
          </p>
          <button className="bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105">
            Start FREE 7-Day Trial
          </button>
          <p className="text-purple-200 mt-4">No credit card required • COPPA compliant • Cancel anytime</p>
        </div>
      </section>
    </div>
  );
};

export default Features;

