'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  ChildWithProgress, 
  getTierInfo, 
  getChildProgressSummary, 
  formatLearningTime,
  calculateProgressPercentage,
  getAchievementLevel
} from '@/lib/children'
import { 
  Play, 
  Edit, 
  Trash2, 
  BookOpen, 
  Trophy, 
  Clock, 
  Star,
  TrendingUp,
  Award
} from 'lucide-react'

interface ChildCardProps {
  child: ChildWithProgress
  onEdit?: (child: ChildWithProgress) => void
  onDelete?: (child: ChildWithProgress) => void
  onStartLearning?: (child: ChildWithProgress) => void
  showActions?: boolean
  compact?: boolean
}

export default function ChildCard({ 
  child, 
  onEdit, 
  onDelete, 
  onStartLearning,
  showActions = true,
  compact = false
}: ChildCardProps) {
  const [progressSummary, setProgressSummary] = useState(child.progress_summary)
  const [loading, setLoading] = useState(!child.progress_summary)

  const tierInfo = getTierInfo(child.tier)

  useEffect(() => {
    if (!child.progress_summary) {
      loadProgressSummary()
    }
  }, [child.id])

  const loadProgressSummary = async () => {
    try {
      setLoading(true)
      const summary = await getChildProgressSummary(child.id)
      setProgressSummary(summary)
    } catch (error) {
      console.error('Error loading progress summary:', error)
    } finally {
      setLoading(false)
    }
  }

  const progressPercentage = progressSummary 
    ? calculateProgressPercentage(progressSummary.completed_lessons, progressSummary.total_lessons)
    : 0

  const achievementLevel = progressSummary 
    ? getAchievementLevel(progressSummary.achievements_count)
    : { level: 'Beginner', color: 'text-gray-600', nextMilestone: 5 }

  const formattedLearningTime = progressSummary 
    ? formatLearningTime(progressSummary.total_time_minutes)
    : '0m'

  if (compact) {
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardContent className="p-4">
          <div className="flex items-center space-x-3">
            <div className={`w-10 h-10 bg-gradient-to-r ${tierInfo.color} rounded-full flex items-center justify-center text-white font-bold`}>
              {child.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-gray-900 truncate">{child.name}</h3>
              <p className="text-sm text-gray-600">Age {child.age} • {tierInfo.name}</p>
            </div>
            {onStartLearning && (
              <Button 
                size="sm"
                onClick={() => onStartLearning(child)}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                <Play className="w-4 h-4" />
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="hover:shadow-lg transition-shadow">
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
          {showActions && (
            <div className="flex space-x-1">
              {onEdit && (
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => onEdit(child)}
                >
                  <Edit className="w-4 h-4" />
                </Button>
              )}
              {onDelete && (
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="text-red-600 hover:text-red-700"
                  onClick={() => onDelete(child)}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              )}
            </div>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Tier Information */}
        <div className={`p-3 rounded-lg ${tierInfo.bgColor}`}>
          <h4 className={`font-semibold ${tierInfo.textColor}`}>
            {tierInfo.name}
          </h4>
          <p className={`text-sm ${tierInfo.textColor} opacity-80`}>
            {tierInfo.description}
          </p>
        </div>

        {/* Achievement Level */}
        {progressSummary && (
          <div className="flex items-center justify-between p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <Award className="w-5 h-5 text-yellow-600" />
              <div>
                <p className={`font-semibold ${achievementLevel.color}`}>
                  {achievementLevel.level}
                </p>
                <p className="text-xs text-gray-600">
                  {progressSummary.achievements_count} achievements
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-600">Next milestone</p>
              <p className="font-semibold text-gray-900">
                {achievementLevel.nextMilestone}
              </p>
            </div>
          </div>
        )}

        {/* Progress Stats */}
        {loading ? (
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="text-center">
                <div className="w-8 h-8 bg-gray-200 rounded-full mx-auto mb-1 animate-pulse"></div>
                <div className="h-4 bg-gray-200 rounded mb-1 animate-pulse"></div>
                <div className="h-3 bg-gray-200 rounded animate-pulse"></div>
              </div>
            ))}
          </div>
        ) : progressSummary ? (
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full mx-auto mb-1">
                <BookOpen className="w-4 h-4 text-blue-600" />
              </div>
              <p className="text-sm font-semibold text-gray-900">
                {progressSummary.completed_lessons}
              </p>
              <p className="text-xs text-gray-600">Lessons</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center w-8 h-8 bg-yellow-100 rounded-full mx-auto mb-1">
                <Trophy className="w-4 h-4 text-yellow-600" />
              </div>
              <p className="text-sm font-semibold text-gray-900">
                {progressSummary.achievements_count}
              </p>
              <p className="text-xs text-gray-600">Badges</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center w-8 h-8 bg-green-100 rounded-full mx-auto mb-1">
                <Clock className="w-4 h-4 text-green-600" />
              </div>
              <p className="text-sm font-semibold text-gray-900">
                {formattedLearningTime}
              </p>
              <p className="text-xs text-gray-600">Time</p>
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <p className="text-gray-500">No progress data available</p>
          </div>
        )}

        {/* Progress Bar */}
        {progressSummary && progressSummary.total_lessons > 0 && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Progress</span>
              <span className="font-semibold text-gray-900">{progressPercentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`bg-gradient-to-r ${tierInfo.color} h-2 rounded-full transition-all duration-300`}
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Recent Activity */}
        {child.last_active && (
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <TrendingUp className="w-4 h-4" />
            <span>
              Last active: {new Date(child.last_active).toLocaleDateString()}
            </span>
          </div>
        )}

        {/* Action Button */}
        {onStartLearning && (
          <Button 
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            onClick={() => onStartLearning(child)}
          >
            <Play className="w-4 h-4 mr-2" />
            Continue Learning
          </Button>
        )}
      </CardContent>
    </Card>
  )
}

