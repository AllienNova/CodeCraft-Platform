'use client'

import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { createChildProfile } from '@/lib/auth'
import { 
  Plus, 
  Settings, 
  BookOpen, 
  Trophy, 
  Clock, 
  Star,
  Edit,
  Trash2,
  Play
} from 'lucide-react'

export default function DashboardPage() {
  const { user, loading, refreshUser } = useAuth()
  const [showAddChild, setShowAddChild] = useState(false)
  const [newChildName, setNewChildName] = useState('')
  const [newChildAge, setNewChildAge] = useState(6)
  const [addingChild, setAddingChild] = useState(false)
  const [error, setError] = useState('')

  const handleAddChild = async (e: React.FormEvent) => {
    e.preventDefault()
    setAddingChild(true)
    setError('')

    try {
      if (!user?.id) {
        throw new Error('User not authenticated')
      }

      const { error } = await createChildProfile(user.id, newChildName.trim(), newChildAge)
      
      if (error) {
        throw error
      }

      // Refresh user data to show new child
      await refreshUser()
      
      // Reset form
      setNewChildName('')
      setNewChildAge(6)
      setShowAddChild(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add child')
    } finally {
      setAddingChild(false)
    }
  }

  const getTierInfo = (tier: string) => {
    switch (tier) {
      case 'magic_workshop':
        return {
          name: 'Magic Workshop',
          description: 'Ages 5-7 • Visual block coding with magical themes',
          color: 'from-pink-500 to-purple-500',
          bgColor: 'bg-pink-50',
          textColor: 'text-pink-700'
        }
      case 'innovation_lab':
        return {
          name: 'Innovation Lab',
          description: 'Ages 8-12 • Advanced blocks and app building',
          color: 'from-blue-500 to-cyan-500',
          bgColor: 'bg-blue-50',
          textColor: 'text-blue-700'
        }
      case 'professional_studio':
        return {
          name: 'Professional Studio',
          description: 'Ages 13+ • Real programming languages and tools',
          color: 'from-green-500 to-emerald-500',
          bgColor: 'bg-green-50',
          textColor: 'text-green-700'
        }
      default:
        return {
          name: 'Unknown Tier',
          description: '',
          color: 'from-gray-500 to-gray-600',
          bgColor: 'bg-gray-50',
          textColor: 'text-gray-700'
        }
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h1>
          <p className="text-gray-600">Please sign in to access your dashboard.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Welcome back, {user.profile?.full_name || 'Parent'}!
              </h1>
              <p className="text-gray-600 mt-1">
                Manage your children&apos;s coding journey
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" className="flex items-center">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Children Overview */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Children</h2>
            <Button 
              onClick={() => setShowAddChild(true)}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Child
            </Button>
          </div>

          {user.children.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Plus className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No children added yet</h3>
                <p className="text-gray-600 mb-4">
                  Add your first child to get started with their coding journey
                </p>
                <Button 
                  onClick={() => setShowAddChild(true)}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  Add Your First Child
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {user.children.map((child) => {
                const tierInfo = getTierInfo(child.tier)
                return (
                  <Card key={child.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader className="pb-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`w-12 h-12 bg-gradient-to-r ${tierInfo.color} rounded-full flex items-center justify-center text-white font-bold text-lg`}>
                            {child.name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <CardTitle className="text-lg">{child.name}</CardTitle>
                            <CardDescription>Age {child.age}</CardDescription>
                          </div>
                        </div>
                        <div className="flex space-x-1">
                          <Button variant="ghost" size="sm">
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className={`p-3 rounded-lg ${tierInfo.bgColor}`}>
                        <h4 className={`font-semibold ${tierInfo.textColor}`}>
                          {tierInfo.name}
                        </h4>
                        <p className={`text-sm ${tierInfo.textColor} opacity-80`}>
                          {tierInfo.description}
                        </p>
                      </div>

                      {/* Progress Stats */}
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center">
                          <div className="flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full mx-auto mb-1">
                            <BookOpen className="w-4 h-4 text-blue-600" />
                          </div>
                          <p className="text-sm font-semibold text-gray-900">12</p>
                          <p className="text-xs text-gray-600">Lessons</p>
                        </div>
                        <div className="text-center">
                          <div className="flex items-center justify-center w-8 h-8 bg-yellow-100 rounded-full mx-auto mb-1">
                            <Trophy className="w-4 h-4 text-yellow-600" />
                          </div>
                          <p className="text-sm font-semibold text-gray-900">5</p>
                          <p className="text-xs text-gray-600">Badges</p>
                        </div>
                      </div>

                      <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                        <Play className="w-4 h-4 mr-2" />
                        Continue Learning
                      </Button>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Learning Time</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">24h 32m</div>
              <p className="text-xs text-muted-foreground">
                +2h from last week
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Projects Created</CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">8</div>
              <p className="text-xs text-muted-foreground">
                +3 from last week
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Achievements</CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">15</div>
              <p className="text-xs text-muted-foreground">
                +5 from last week
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Add Child Modal */}
      {showAddChild && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Add New Child</CardTitle>
              <CardDescription>
                Create a profile for your child to start their coding journey
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAddChild} className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    value={newChildName}
                    onChange={(e) => setNewChildName(e.target.value)}
                    placeholder="Child's name"
                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700">Age</label>
                  <select
                    value={newChildAge}
                    onChange={(e) => setNewChildAge(parseInt(e.target.value))}
                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    required
                  >
                    {Array.from({ length: 16 }, (_, i) => i + 3).map(age => (
                      <option key={age} value={age}>{age} years old</option>
                    ))}
                  </select>
                </div>

                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="text-sm text-purple-700 font-medium">
                    Learning Tier: {getTierInfo(
                      newChildAge <= 7 ? 'magic_workshop' : 
                      newChildAge <= 12 ? 'innovation_lab' : 
                      'professional_studio'
                    ).name}
                  </p>
                </div>

                <div className="flex space-x-3">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowAddChild(false)}
                    className="flex-1"
                    disabled={addingChild}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    disabled={addingChild}
                  >
                    {addingChild ? 'Adding...' : 'Add Child'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

