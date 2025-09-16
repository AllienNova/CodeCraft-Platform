import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import About from './pages/About';
import Features from './pages/Features';
import Pricing from './pages/Pricing';
import Curriculum from './pages/Curriculum';
import './App.css';

// Enhanced Home Page with Micro-animations and Psychological Marketing
const HomePage = () => {
  const [email, setEmail] = useState('')
  const [childAge, setChildAge] = useState('')
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [urgencyCount, setUrgencyCount] = useState(127)
  const [socialProofCount, setSocialProofCount] = useState(2847)
  const [isVisible, setIsVisible] = useState(false)

  // Micro-animation: Counter animations
  useEffect(() => {
    setIsVisible(true)
    
    // Urgency counter animation (decreasing)
    const urgencyTimer = setInterval(() => {
      setUrgencyCount(prev => Math.max(prev - Math.floor(Math.random() * 3), 95))
    }, 30000) // Every 30 seconds

    // Social proof counter animation (increasing)
    const socialTimer = setInterval(() => {
      setSocialProofCount(prev => prev + Math.floor(Math.random() * 5))
    }, 45000) // Every 45 seconds

    return () => {
      clearInterval(urgencyTimer)
      clearInterval(socialTimer)
    }
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    setIsSubmitted(true)
    console.log('Beta signup:', { email, childAge })
    
    // Psychological trigger: Immediate gratification
    setTimeout(() => {
      setUrgencyCount(prev => prev - 1)
    }, 1000)
  }

  return (
    <>
      {/* SEO Optimization */}
      <Helmet>
        <title>CodeCraft - #1 Coding Platform for Kids Ages 5-15 | Learn Programming Through Play</title>
        <meta name="description" content="Transform your child into a confident programmer with CodeCraft's magical coding adventures. Age-appropriate learning for kids 5-15. Join 2,847+ families. Start free trial today!" />
        <meta name="keywords" content="kids coding, children programming, learn to code, coding for kids, programming education, STEM learning, coding games, kids apps" />
        <meta property="og:title" content="CodeCraft - Where Young Minds Learn to Code" />
        <meta property="og:description" content="Magical coding adventures that transform children into confident programmers. Ages 5-15. Safe, educational, irresistibly fun." />
        <meta property="og:image" content="/og-image.jpg" />
        <meta property="og:url" content="https://codecraft.com" />
        <meta name="twitter:card" content="summary_large_image" />
        <link rel="canonical" href="https://codecraft.com" />
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "EducationalOrganization",
            "name": "CodeCraft",
            "description": "Coding education platform for children ages 5-15",
            "url": "https://codecraft.com",
            "logo": "https://codecraft.com/logo.png",
            "contactPoint": {
              "@type": "ContactPoint",
              "telephone": "+1-555-CODECRAFT",
              "contactType": "customer service"
            }
          })}
        </script>
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
        {/* Hero Section with Enhanced Psychological Triggers */}
        <section className="relative overflow-hidden py-20 lg:py-32">
          {/* Animated Background Elements */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-blue-600/10 to-pink-600/10"></div>
          <div className="absolute top-10 left-10 w-20 h-20 bg-purple-300/20 rounded-full animate-bounce delay-1000"></div>
          <div className="absolute top-32 right-20 w-16 h-16 bg-blue-300/20 rounded-full animate-pulse delay-2000"></div>
          <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-pink-300/20 rounded-full animate-ping delay-3000"></div>
          
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className={`space-y-8 transform transition-all duration-1000 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
                {/* Enhanced Urgency Badge with Pulsing Animation */}
                <div className="inline-flex items-center bg-gradient-to-r from-orange-400 to-red-500 text-white px-6 py-3 rounded-full text-sm font-bold shadow-lg animate-pulse hover:animate-bounce transition-all duration-300">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                  <span className="relative">🔥 URGENT: Only {urgencyCount} Beta Spots Left - Filling Fast!</span>
                </div>
                
                {/* Emotional Hook with Gradient Text Animation */}
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  <span className="text-gray-900 block animate-fadeInUp">Your Child's</span>
                  <span className="bg-gradient-to-r from-purple-600 via-blue-600 to-pink-600 bg-clip-text text-transparent block animate-fadeInUp delay-200 bg-size-200 animate-gradient">
                    Coding Adventure
                  </span>
                  <span className="text-gray-900 block animate-fadeInUp delay-400">Starts Here</span>
                </h1>

                {/* Enhanced Value Proposition with Psychological Triggers */}
                <div className="space-y-4 animate-fadeInUp delay-600">
                  <p className="text-xl text-gray-600 leading-relaxed">
                    <span className="font-semibold text-purple-600">Don't let your child fall behind</span> in the digital revolution. 
                    Transform them into a confident programmer through magical adventures, 
                    real app building, and professional development skills.
                  </p>
                  <p className="text-lg text-gray-700 font-medium">
                    <span className="bg-yellow-200 px-2 py-1 rounded">Ages 5-15</span> • 
                    <span className="bg-green-200 px-2 py-1 rounded ml-2">100% Safe</span> • 
                    <span className="bg-blue-200 px-2 py-1 rounded ml-2">Irresistibly Fun</span>
                  </p>
                </div>

                {/* Enhanced Social Proof with Live Counters */}
                <div className="flex items-center space-x-8 animate-fadeInUp delay-800">
                  <div className="flex items-center space-x-3">
                    <div className="flex -space-x-2">
                      {[1,2,3,4,5].map(i => (
                        <div key={i} className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-400 to-blue-400 border-3 border-white shadow-lg animate-pulse" style={{animationDelay: `${i * 200}ms`}}></div>
                      ))}
                    </div>
                    <div className="text-sm">
                      <div className="font-bold text-gray-900 animate-countUp">{socialProofCount.toLocaleString()}+ families joined</div>
                      <div className="text-gray-500">This month alone!</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {[1,2,3,4,5].map(i => (
                      <span key={i} className="text-yellow-400 text-xl animate-bounce" style={{animationDelay: `${i * 100}ms`}}>⭐</span>
                    ))}
                    <div className="text-sm ml-2">
                      <div className="font-bold text-gray-900">4.9/5 rating</div>
                      <div className="text-gray-500">From real parents</div>
                    </div>
                  </div>
                </div>

                {/* Enhanced Trust Indicators with Icons */}
                <div className="flex items-center space-x-6 text-sm text-gray-600 animate-fadeInUp delay-1000">
                  <span className="flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-full">
                    <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
                    <span className="font-medium">COPPA+ Compliant</span>
                  </span>
                  <span className="flex items-center space-x-2 bg-blue-50 px-3 py-2 rounded-full">
                    <span className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></span>
                    <span className="font-medium">No Credit Card Required</span>
                  </span>
                  <span className="flex items-center space-x-2 bg-purple-50 px-3 py-2 rounded-full">
                    <span className="w-3 h-3 bg-purple-500 rounded-full animate-pulse"></span>
                    <span className="font-medium">Parent Approved</span>
                  </span>
                </div>

                {/* Fear of Missing Out (FOMO) Trigger */}
                <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg animate-fadeInUp delay-1200">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <span className="text-red-400 text-xl">⚠️</span>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-red-700">
                        <span className="font-medium">Warning:</span> Software developer salaries average $107,000+. 
                        Children who start coding early have a <span className="font-bold">300% advantage</span> in future earnings.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Enhanced Beta Signup Form with Micro-interactions */}
              <div className={`lg:pl-8 transform transition-all duration-1000 delay-500 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
                <div className="bg-white/95 backdrop-blur-sm border-0 shadow-2xl rounded-3xl p-8 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
                  <div className="text-center pb-6">
                    <div className="mx-auto w-20 h-20 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mb-4 animate-bounce">
                      <span className="text-3xl text-white">🚀</span>
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900 mb-2 animate-pulse">
                      Join the Beta Revolution
                    </h2>
                    <p className="text-gray-600 mb-4">
                      Be among the first {urgencyCount} families to experience the future of coding education
                    </p>
                    
                    {/* Real-time Social Proof */}
                    <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium inline-block animate-pulse">
                      <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-green-400 opacity-75"></span>
                      <span className="relative ml-3">🔴 LIVE: 23 parents signed up in the last hour</span>
                    </div>
                  </div>
                  
                  {!isSubmitted ? (
                    <form onSubmit={handleSubmit} className="space-y-6">
                      <div className="transform transition-all duration-300 hover:scale-105">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Parent Email Address
                        </label>
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="your.email@example.com"
                          required
                          className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 hover:border-purple-300"
                        />
                      </div>
                      
                      <div className="transform transition-all duration-300 hover:scale-105">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Child's Age (This determines their learning tier)
                        </label>
                        <select 
                          value={childAge}
                          onChange={(e) => setChildAge(e.target.value)}
                          required
                          className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 hover:border-purple-300"
                        >
                          <option value="">Select age to unlock their perfect tier...</option>
                          <option value="5">5 years old → 🦄 Magic Workshop</option>
                          <option value="6">6 years old → 🦄 Magic Workshop</option>
                          <option value="7">7 years old → 🦄 Magic Workshop</option>
                          <option value="8">8 years old → 🚀 Innovation Lab</option>
                          <option value="9">9 years old → 🚀 Innovation Lab</option>
                          <option value="10">10 years old → 💻 Professional Studio</option>
                          <option value="11">11 years old → 💻 Professional Studio</option>
                          <option value="12">12 years old → 💻 Professional Studio</option>
                          <option value="13">13 years old → 💻 Professional Studio</option>
                          <option value="14">14 years old → 💻 Professional Studio</option>
                          <option value="15">15 years old → 💻 Professional Studio</option>
                        </select>
                      </div>

                      {/* Enhanced CTA Button with Multiple Psychological Triggers */}
                      <button 
                        type="submit" 
                        className="w-full bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 hover:from-green-600 hover:via-blue-600 hover:to-purple-600 text-white text-xl py-4 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 font-bold transform hover:scale-105 animate-pulse hover:animate-none relative overflow-hidden"
                      >
                        <span className="relative z-10">⚡ SECURE MY CHILD'S FUTURE - FREE TRIAL</span>
                        <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-orange-500 opacity-0 hover:opacity-20 transition-opacity duration-300"></div>
                      </button>

                      {/* Risk Reversal and Trust Signals */}
                      <div className="text-center space-y-2">
                        <p className="text-xs text-gray-500 flex items-center justify-center space-x-2">
                          <span>🔒</span>
                          <span>Your information is encrypted and will never be shared</span>
                        </p>
                        <div className="flex items-center justify-center space-x-4 text-xs text-gray-600">
                          <span className="flex items-center space-x-1">
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                            <span>Instant Access</span>
                          </span>
                          <span className="flex items-center space-x-1">
                            <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                            <span>No Commitment</span>
                          </span>
                          <span className="flex items-center space-x-1">
                            <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                            <span>Cancel Anytime</span>
                          </span>
                        </div>
                      </div>
                    </form>
                  ) : (
                    <div className="text-center py-8 animate-fadeIn">
                      <div className="mx-auto w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-4 animate-bounce">
                        <span className="text-3xl text-green-600">✓</span>
                      </div>
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">🎉 Welcome to the Beta Revolution!</h3>
                      <p className="text-gray-600 mb-4">
                        Check your email for exclusive access instructions and your child's personalized learning roadmap.
                      </p>
                      <div className="bg-gradient-to-r from-green-400 to-blue-500 text-white px-6 py-3 rounded-full inline-block font-bold animate-pulse">
                        Beta Access Confirmed ✓
                      </div>
                      <p className="text-sm text-gray-500 mt-4">
                        You're now part of an exclusive group of forward-thinking parents!
                      </p>
                    </div>
                  )}
                </div>

                {/* Enhanced Urgency Counter with Live Updates */}
                <div className="mt-6 text-center">
                  <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-full inline-block shadow-lg animate-pulse hover:animate-bounce transition-all duration-300">
                    <span className="text-sm font-bold flex items-center space-x-2">
                      <span className="animate-ping inline-flex h-2 w-2 rounded-full bg-white opacity-75"></span>
                      <span>⏰ URGENT: Only {urgencyCount} Beta Spots Remaining</span>
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-2 animate-pulse">
                    ⚠️ Spots are filling every few minutes - Don't wait!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Enhanced Three Tiers Section with Hover Animations */}
        <section className="py-20 bg-white relative overflow-hidden">
          {/* Animated Background Elements */}
          <div className="absolute top-0 left-0 w-full h-full opacity-5">
            <div className="absolute top-10 left-10 w-32 h-32 bg-purple-300 rounded-full animate-float"></div>
            <div className="absolute top-32 right-20 w-24 h-24 bg-blue-300 rounded-full animate-float delay-1000"></div>
            <div className="absolute bottom-20 left-1/3 w-20 h-20 bg-pink-300 rounded-full animate-float delay-2000"></div>
          </div>

          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div className="text-center mb-16 animate-fadeInUp">
              <h2 className="text-5xl font-bold text-gray-900 mb-6">
                Three Magical Tiers That <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Grow With Your Child</span>
              </h2>
              <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
                From magical adventures to professional development, each tier is scientifically designed for your child's cognitive development stage
              </p>
              
              {/* Social Proof for Tiers */}
              <div className="mt-8 flex items-center justify-center space-x-8 text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-purple-500 rounded-full animate-pulse"></span>
                  <span>1,247 kids in Magic Workshop</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></span>
                  <span>892 kids building real apps</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-indigo-500 rounded-full animate-pulse"></span>
                  <span>708 kids coding professionally</span>
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Magic Workshop - Enhanced with Micro-animations */}
              <div className="group relative overflow-hidden border-0 shadow-xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 hover:-rotate-1 bg-white rounded-3xl p-8 cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-pink-500/10 group-hover:from-purple-500/20 group-hover:to-pink-500/20 transition-all duration-500"></div>
                
                {/* Floating Animation Elements */}
                <div className="absolute top-4 right-4 w-6 h-6 bg-purple-300/30 rounded-full animate-float"></div>
                <div className="absolute bottom-8 left-4 w-4 h-4 bg-pink-300/30 rounded-full animate-float delay-1000"></div>
                
                <div className="relative text-center pb-6">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-4 group-hover:animate-bounce transition-all duration-300">
                    <span className="text-3xl text-white">🦄</span>
                  </div>
                  <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-bold mb-3 inline-block group-hover:bg-purple-200 transition-all duration-300">Ages 5-7</div>
                  <h3 className="text-3xl font-bold text-gray-900 mb-3 group-hover:text-purple-600 transition-all duration-300">Magic Workshop</h3>
                  <p className="text-gray-600 group-hover:text-gray-700 transition-all duration-300">
                    Where coding feels like casting spells with Sparkle the Unicorn
                  </p>
                </div>
                
                <div className="relative">
                  <ul className="space-y-4">
                    {[
                      'Drag-and-drop "spell blocks"',
                      'Animated stories & characters', 
                      'No reading required',
                      '10 magical adventures'
                    ].map((item, index) => (
                      <li key={index} className="flex items-center space-x-3 group-hover:translate-x-2 transition-all duration-300" style={{transitionDelay: `${index * 100}ms`}}>
                        <span className="w-6 h-6 text-green-500 font-bold">✓</span>
                        <span className="group-hover:font-medium transition-all duration-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                  
                  {/* Success Story */}
                  <div className="mt-6 bg-purple-50 p-4 rounded-xl group-hover:bg-purple-100 transition-all duration-300">
                    <p className="text-sm text-purple-700 italic">
                      "My 5-year-old thinks she's a real wizard now!" - Sarah M.
                    </p>
                  </div>
                </div>
              </div>

              {/* Innovation Lab - Most Popular with Enhanced Effects */}
              <div className="group relative overflow-hidden border-0 shadow-xl hover:shadow-3xl transition-all duration-500 transform hover:scale-110 ring-4 ring-blue-500 bg-white rounded-3xl p-8 cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-green-500/10 group-hover:from-blue-500/20 group-hover:to-green-500/20 transition-all duration-500"></div>
                
                {/* Most Popular Badge with Animation */}
                <div className="absolute -top-3 -right-3">
                  <div className="bg-gradient-to-r from-blue-500 to-green-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg animate-pulse group-hover:animate-bounce">
                    🏆 Most Popular
                  </div>
                </div>
                
                {/* Floating Animation Elements */}
                <div className="absolute top-6 right-8 w-5 h-5 bg-blue-300/30 rounded-full animate-float delay-500"></div>
                <div className="absolute bottom-12 left-6 w-3 h-3 bg-green-300/30 rounded-full animate-float delay-1500"></div>
                
                <div className="relative text-center pb-6">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-blue-500 to-green-500 rounded-full flex items-center justify-center mb-4 group-hover:animate-spin transition-all duration-1000">
                    <span className="text-3xl text-white">🚀</span>
                  </div>
                  <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-bold mb-3 inline-block group-hover:bg-blue-200 transition-all duration-300">Ages 8-9</div>
                  <h3 className="text-3xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-all duration-300">Innovation Lab</h3>
                  <p className="text-gray-600 group-hover:text-gray-700 transition-all duration-300">
                    Build real apps and games with Robo the Robot
                  </p>
                </div>
                
                <div className="relative">
                  <ul className="space-y-4">
                    {[
                      'Visual programming blocks',
                      'Real app development',
                      'Database integration', 
                      'App store publishing'
                    ].map((item, index) => (
                      <li key={index} className="flex items-center space-x-3 group-hover:translate-x-2 transition-all duration-300" style={{transitionDelay: `${index * 100}ms`}}>
                        <span className="w-6 h-6 text-green-500 font-bold">✓</span>
                        <span className="group-hover:font-medium transition-all duration-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                  
                  {/* Success Story */}
                  <div className="mt-6 bg-blue-50 p-4 rounded-xl group-hover:bg-blue-100 transition-all duration-300">
                    <p className="text-sm text-blue-700 italic">
                      "My 9-year-old built an app that's on the app store!" - Mike T.
                    </p>
                  </div>
                </div>
              </div>

              {/* Professional Studio - Enhanced with Professional Feel */}
              <div className="group relative overflow-hidden border-0 shadow-xl hover:shadow-3xl transition-all duration-500 transform hover:scale-105 hover:rotate-1 bg-white rounded-3xl p-8 cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 group-hover:from-indigo-500/20 group-hover:to-purple-500/20 transition-all duration-500"></div>
                
                {/* Floating Animation Elements */}
                <div className="absolute top-5 right-6 w-4 h-4 bg-indigo-300/30 rounded-full animate-float delay-700"></div>
                <div className="absolute bottom-10 left-5 w-6 h-6 bg-purple-300/30 rounded-full animate-float delay-1200"></div>
                
                <div className="relative text-center pb-6">
                  <div className="mx-auto w-20 h-20 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center mb-4 group-hover:animate-pulse transition-all duration-300">
                    <span className="text-3xl text-white">💻</span>
                  </div>
                  <div className="bg-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-sm font-bold mb-3 inline-block group-hover:bg-indigo-200 transition-all duration-300">Ages 10+</div>
                  <h3 className="text-3xl font-bold text-gray-900 mb-3 group-hover:text-indigo-600 transition-all duration-300">Professional Studio</h3>
                  <p className="text-gray-600 group-hover:text-gray-700 transition-all duration-300">
                    Real coding languages and professional tools
                  </p>
                </div>
                
                <div className="relative">
                  <ul className="space-y-4">
                    {[
                      'Python, JavaScript, HTML/CSS',
                      'Professional IDE',
                      'Cloud deployment',
                      'Industry certifications'
                    ].map((item, index) => (
                      <li key={index} className="flex items-center space-x-3 group-hover:translate-x-2 transition-all duration-300" style={{transitionDelay: `${index * 100}ms`}}>
                        <span className="w-6 h-6 text-green-500 font-bold">✓</span>
                        <span className="group-hover:font-medium transition-all duration-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                  
                  {/* Success Story */}
                  <div className="mt-6 bg-indigo-50 p-4 rounded-xl group-hover:bg-indigo-100 transition-all duration-300">
                    <p className="text-sm text-indigo-700 italic">
                      "My 12-year-old got a coding internship!" - Lisa R.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Enhanced Tier Comparison CTA */}
            <div className="text-center mt-16 animate-fadeInUp delay-1000">
              <div className="bg-gradient-to-r from-purple-100 to-blue-100 p-8 rounded-3xl">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Not sure which tier is perfect for your child?
                </h3>
                <p className="text-gray-600 mb-6">
                  Our smart assessment will recommend the ideal learning path based on your child's age and interests.
                </p>
                <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all duration-300">
                  🎯 Find My Child's Perfect Tier
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Enhanced Final CTA with Maximum Psychological Impact */}
        <section className="py-20 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 relative overflow-hidden">
          {/* Animated Background Elements */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-10 left-10 w-40 h-40 bg-white rounded-full animate-pulse"></div>
            <div className="absolute top-32 right-20 w-32 h-32 bg-white rounded-full animate-pulse delay-1000"></div>
            <div className="absolute bottom-20 left-1/4 w-24 h-24 bg-white rounded-full animate-pulse delay-2000"></div>
          </div>

          <div className="max-w-5xl mx-auto text-center px-4 relative">
            <div className="animate-fadeInUp">
              <h2 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                Don't Let Your Child Fall Behind in the 
                <span className="block bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent animate-pulse">
                  Digital Revolution
                </span>
              </h2>
              
              <p className="text-xl text-purple-100 mb-4">
                Join {socialProofCount.toLocaleString()}+ families who've already given their children the ultimate advantage
              </p>
              
              {/* Enhanced Fear of Missing Out */}
              <div className="bg-red-500/20 border border-red-300 rounded-xl p-4 mb-8 backdrop-blur-sm">
                <p className="text-white font-medium">
                  ⚠️ <span className="font-bold">REALITY CHECK:</span> By 2030, 85% of jobs will require coding skills. 
                  Children who start now will earn <span className="font-bold text-yellow-300">$50,000+ more annually</span> than their peers.
                </p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-8 animate-fadeInUp delay-500">
              <button className="group bg-white text-purple-600 px-10 py-5 rounded-full text-xl font-bold hover:shadow-2xl transition-all transform hover:scale-110 relative overflow-hidden">
                <span className="relative z-10 flex items-center space-x-2">
                  <span>🚀</span>
                  <span>START FREE TRIAL NOW</span>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-orange-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
              
              <div className="text-purple-200 text-lg font-medium animate-pulse">
                <div className="flex items-center space-x-2">
                  <span className="animate-ping inline-flex h-3 w-3 rounded-full bg-red-400 opacity-75"></span>
                  <span>⏰ Only {urgencyCount} beta spots remaining</span>
                </div>
              </div>
            </div>

            {/* Enhanced Trust Signals */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-purple-200 animate-fadeInUp delay-700">
              <div className="flex items-center justify-center space-x-2">
                <span className="text-2xl">✓</span>
                <span className="font-medium">No Credit Card Required</span>
              </div>
              <div className="flex items-center justify-center space-x-2">
                <span className="text-2xl">✓</span>
                <span className="font-medium">COPPA+ Compliant</span>
              </div>
              <div className="flex items-center justify-center space-x-2">
                <span className="text-2xl">✓</span>
                <span className="font-medium">Cancel Anytime</span>
              </div>
            </div>

            {/* Final Urgency Push */}
            <div className="mt-8 animate-fadeInUp delay-1000">
              <p className="text-purple-200 text-lg">
                <span className="font-bold text-yellow-300">Limited Time:</span> First 500 beta families get 
                <span className="font-bold text-yellow-300"> lifetime 50% discount</span> when we launch publicly.
              </p>
            </div>
          </div>
        </section>
      </div>

      {/* Custom CSS for Animations */}
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }

        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        @keyframes countUp {
          from { transform: scale(0.8); }
          to { transform: scale(1); }
        }

        .animate-fadeInUp { animation: fadeInUp 0.8s ease-out forwards; }
        .animate-fadeIn { animation: fadeIn 0.8s ease-out forwards; }
        .animate-float { animation: float 3s ease-in-out infinite; }
        .animate-gradient { animation: gradient 3s ease infinite; }
        .animate-countUp { animation: countUp 0.5s ease-out; }
        .bg-size-200 { background-size: 200% 200%; }

        .delay-200 { animation-delay: 200ms; }
        .delay-400 { animation-delay: 400ms; }
        .delay-500 { animation-delay: 500ms; }
        .delay-600 { animation-delay: 600ms; }
        .delay-700 { animation-delay: 700ms; }
        .delay-800 { animation-delay: 800ms; }
        .delay-1000 { animation-delay: 1000ms; }
        .delay-1200 { animation-delay: 1200ms; }
        .delay-1500 { animation-delay: 1500ms; }
        .delay-2000 { animation-delay: 2000ms; }
        .delay-3000 { animation-delay: 3000ms; }

        .shadow-3xl {
          box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
        }
      `}</style>
    </>
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<About />} />
            <Route path="/features" element={<Features />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/curriculum" element={<Curriculum />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;

