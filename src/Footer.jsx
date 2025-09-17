import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center mb-4">
              <span className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                CodeCraft
              </span>
            </div>
            <p className="text-gray-300 mb-6 max-w-md">
              Transforming children into confident programmers through magical, age-appropriate 
              learning experiences. Where coding feels like play, but builds real skills.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">Facebook</span>
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">Twitter</span>
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">LinkedIn</span>
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">YouTube</span>
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/features" className="text-gray-300 hover:text-white transition-colors">Features</a></li>
              <li><a href="/curriculum" className="text-gray-300 hover:text-white transition-colors">Curriculum</a></li>
              <li><a href="/pricing" className="text-gray-300 hover:text-white transition-colors">Pricing</a></li>
              <li><a href="/about" className="text-gray-300 hover:text-white transition-colors">About Us</a></li>
              <li><a href="/demo" className="text-gray-300 hover:text-white transition-colors">Live Demo</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li><a href="/help" className="text-gray-300 hover:text-white transition-colors">Help Center</a></li>
              <li><a href="/contact" className="text-gray-300 hover:text-white transition-colors">Contact Us</a></li>
              <li><a href="/community" className="text-gray-300 hover:text-white transition-colors">Community</a></li>
              <li><a href="/tutorials" className="text-gray-300 hover:text-white transition-colors">Tutorials</a></li>
              <li><a href="/status" className="text-gray-300 hover:text-white transition-colors">System Status</a></li>
            </ul>
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-12 pt-8 border-t border-gray-800">
          <div className="flex flex-wrap justify-center items-center space-x-8 mb-8">
            <div className="flex items-center space-x-2 text-gray-300">
              <span className="text-green-400">🔒</span>
              <span className="text-sm">COPPA Compliant</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-300">
              <span className="text-blue-400">🛡️</span>
              <span className="text-sm">Privacy Protected</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-300">
              <span className="text-yellow-400">⭐</span>
              <span className="text-sm">4.9/5 Parent Rating</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-300">
              <span className="text-purple-400">👨‍👩‍👧‍👦</span>
              <span className="text-sm">2,847+ Families</span>
            </div>
          </div>
        </div>

        {/* Newsletter Signup */}
        <div className="mt-8 pt-8 border-t border-gray-800">
          <div className="max-w-md mx-auto text-center">
            <h3 className="text-lg font-semibold mb-4">Stay Updated</h3>
            <p className="text-gray-300 mb-4">Get the latest updates on new features and coding tips for kids.</p>
            <div className="flex">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-2 rounded-l-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:border-purple-500"
              />
              <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-r-lg hover:shadow-lg transition-all">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
          <div className="text-gray-400 text-sm mb-4 md:mb-0">
            © 2024 CodeCraft. All rights reserved.
          </div>
          <div className="flex space-x-6 text-sm">
            <a href="/privacy" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</a>
            <a href="/terms" className="text-gray-400 hover:text-white transition-colors">Terms of Service</a>
            <a href="/cookies" className="text-gray-400 hover:text-white transition-colors">Cookie Policy</a>
            <a href="/accessibility" className="text-gray-400 hover:text-white transition-colors">Accessibility</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

