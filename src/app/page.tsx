'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuth } from '@/components/providers'

// Floating Sparkles Animation Component
function FloatingSparkles() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(20)].map((_, i) => (
        <div
          key={i}
          className="absolute w-2 h-2 bg-yellow-300 rounded-full animate-pulse"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            animationDuration: `${2 + Math.random() * 2}s`
          }}
        />
      ))}
    </div>
  )
}

export default function LandingPage() {
  const { user, loading } = useAuth()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    )
  }

  // If user is logged in, redirect to dashboard
  if (user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50">
        <div className="container mx-auto px-4 py-16 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">
            Welcome back to Codopia!
          </h1>
          <div className="space-x-4">
            <Link href="/dashboard">
              <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                Go to Dashboard
              </Button>
            </Link>
            <Button variant="outline" onClick={() => window.location.reload()}>
              Sign Out
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 relative overflow-hidden">
      <FloatingSparkles />
      
      {/* Navigation */}
      <nav className="relative z-10 bg-white/80 backdrop-blur-sm border-b border-purple-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">C</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                Codopia
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link href="/auth/signin">
                <Button variant="outline">Sign In</Button>
              </Link>
              <Link href="/auth/signup">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-5xl lg:text-6xl font-bold leading-tight mb-8">
            Your Child&apos;s{' '}
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Coding Adventure
            </span>{' '}
            Starts Here
          </h1>
          
          <p className="text-xl text-gray-600 leading-relaxed mb-12 max-w-3xl mx-auto">
            Transform children into confident programmers through magical adventures, 
            real app building, and professional development skills.
          </p>
          
          <div className="flex flex-wrap justify-center items-center gap-6 mb-12">
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full font-medium">Ages 5-15</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full font-medium">No Experience Needed</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full font-medium">Parent Dashboard</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signup">
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-lg px-8 py-4">
                Start Free Trial
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="text-lg px-8 py-4">
              Watch Demo
            </Button>
          </div>
        </div>
      </div>

      {/* Learning Tiers */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Age-Perfect Learning Paths
          </h2>
          <p className="text-xl text-gray-600">
            Every child learns differently. Our three tiers ensure the perfect fit.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Magic Workshop */}
          <Card className="relative overflow-hidden border-2 border-pink-200 hover:border-pink-300 transition-colors">
            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-pink-500 to-purple-500"></div>
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">✨</span>
              </div>
              <CardTitle className="text-2xl text-pink-700">Magic Workshop</CardTitle>
              <CardDescription className="text-pink-600 font-medium">Ages 5-7</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-gray-600 mb-6">
                Visual block coding with magical themes. Children create their first programs 
                while developing logical thinking skills.
              </p>
              <ul className="text-sm text-gray-600 space-y-2 mb-6">
                <li>• Drag-and-drop visual blocks</li>
                <li>• Magical characters and stories</li>
                <li>• Interactive animations</li>
                <li>• Voice narration</li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600">
                Explore Magic
              </Button>
            </CardContent>
          </Card>

          {/* Innovation Lab */}
          <Card className="relative overflow-hidden border-2 border-blue-200 hover:border-blue-300 transition-colors">
            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-cyan-500"></div>
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">🚀</span>
              </div>
              <CardTitle className="text-2xl text-blue-700">Innovation Lab</CardTitle>
              <CardDescription className="text-blue-600 font-medium">Ages 8-12</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-gray-600 mb-6">
                Advanced block programming with logic and app building. 
                Students create real applications and games.
              </p>
              <ul className="text-sm text-gray-600 space-y-2 mb-6">
                <li>• Advanced block programming</li>
                <li>• Logic and conditional statements</li>
                <li>• Variables and functions</li>
                <li>• App and game development</li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600">
                Build Apps
              </Button>
            </CardContent>
          </Card>

          {/* Professional Studio */}
          <Card className="relative overflow-hidden border-2 border-green-200 hover:border-green-300 transition-colors">
            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-green-500 to-emerald-500"></div>
            <CardHeader className="text-center pb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">💻</span>
              </div>
              <CardTitle className="text-2xl text-green-700">Professional Studio</CardTitle>
              <CardDescription className="text-green-600 font-medium">Ages 13+</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-gray-600 mb-6">
                Real programming languages and professional tools. 
                Students build portfolios and prepare for tech careers.
              </p>
              <ul className="text-sm text-gray-600 space-y-2 mb-6">
                <li>• JavaScript, Python, HTML/CSS</li>
                <li>• Professional development tools</li>
                <li>• Version control with Git</li>
                <li>• Portfolio building</li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600">
                Code Professionally
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* CTA Section */}
      <div className="relative z-10 bg-gradient-to-r from-purple-600 to-blue-600 py-16">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Start Your Child&apos;s Coding Journey?
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Join thousands of families already building the future together.
          </p>
          <Link href="/auth/signup">
            <Button size="lg" className="bg-white text-purple-600 hover:bg-gray-100 text-lg px-8 py-4">
              Start Free Trial Today
            </Button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative z-10 bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">C</span>
              </div>
              <span className="text-xl font-bold">Codopia</span>
            </div>
            <p className="text-gray-400 mb-4">
              Empowering the next generation of innovators through code.
            </p>
            <p className="text-gray-500 text-sm">
              © 2025 Codopia. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
