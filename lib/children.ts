import { supabase } from './supabase'
import { Database } from './database.types'

type Child = Database['public']['Tables']['children']['Row']
type TierType = Database['public']['Enums']['tier_type']

export interface ChildWithProgress extends Child {
  tier_display_name: string
  tier_description: string
  last_active: string
  progress_summary?: {
    total_lessons: number
    completed_lessons: number
    total_modules: number
    completed_modules: number
    total_time_minutes: number
    achievements_count: number
    projects_count: number
  }
}

export interface TierContent {
  module_id: string
  module_name: string
  module_description: string
  module_order: number
  lesson_count: number
  estimated_hours: number
}

// Get all children for a parent with enhanced data
export async function getParentChildren(parentId: string): Promise<ChildWithProgress[]> {
  try {
    const { data, error } = await supabase.rpc('get_parent_children', {
      parent_user_id: parentId
    })

    if (error) {
      console.error('Error fetching parent children:', error)
      throw error
    }

    return data || []
  } catch (error) {
    console.error('Error in getParentChildren:', error)
    throw error
  }
}

// Get progress summary for a specific child
export async function getChildProgressSummary(childId: string) {
  try {
    const { data, error } = await supabase.rpc('get_child_progress_summary', {
      child_user_id: childId
    })

    if (error) {
      console.error('Error fetching child progress:', error)
      throw error
    }

    return data?.[0] || {
      total_lessons: 0,
      completed_lessons: 0,
      total_modules: 0,
      completed_modules: 0,
      total_time_minutes: 0,
      achievements_count: 0,
      projects_count: 0
    }
  } catch (error) {
    console.error('Error in getChildProgressSummary:', error)
    throw error
  }
}

// Get tier-appropriate content for a child
export async function getTierContent(tier: TierType): Promise<TierContent[]> {
  try {
    const { data, error } = await supabase.rpc('get_tier_content', {
      child_tier: tier
    })

    if (error) {
      console.error('Error fetching tier content:', error)
      throw error
    }

    return data || []
  } catch (error) {
    console.error('Error in getTierContent:', error)
    throw error
  }
}

// Create a new child profile
export async function createChild(parentId: string, name: string, age: number) {
  try {
    const { data, error } = await supabase
      .from('children')
      .insert({
        parent_id: parentId,
        name: name.trim(),
        age: age
        // tier will be automatically set by the database trigger
      })
      .select()
      .single()

    if (error) {
      console.error('Error creating child:', error)
      throw error
    }

    return { data, error: null }
  } catch (error) {
    console.error('Error in createChild:', error)
    return { data: null, error }
  }
}

// Update child profile using the safe database function
export async function updateChild(
  childId: string, 
  parentId: string, 
  updates: {
    name?: string
    age?: number
    avatar_url?: string
  }
) {
  try {
    const { data, error } = await supabase.rpc('update_child_profile', {
      child_user_id: childId,
      parent_user_id: parentId,
      new_name: updates.name || null,
      new_age: updates.age || null,
      new_avatar_url: updates.avatar_url || null
    })

    if (error) {
      console.error('Error updating child:', error)
      throw error
    }

    return { success: data, error: null }
  } catch (error) {
    console.error('Error in updateChild:', error)
    return { success: false, error }
  }
}

// Safely delete a child and all related data
export async function deleteChild(childId: string, parentId: string) {
  try {
    const { data, error } = await supabase.rpc('delete_child_safely', {
      child_user_id: childId,
      parent_user_id: parentId
    })

    if (error) {
      console.error('Error deleting child:', error)
      throw error
    }

    return { success: data, error: null }
  } catch (error) {
    console.error('Error in deleteChild:', error)
    return { success: false, error }
  }
}

// Get a specific child by ID (with parent verification)
export async function getChildById(childId: string, parentId: string): Promise<Child | null> {
  try {
    const { data, error } = await supabase
      .from('children')
      .select('*')
      .eq('id', childId)
      .eq('parent_id', parentId)
      .eq('is_active', true)
      .single()

    if (error) {
      console.error('Error fetching child by ID:', error)
      return null
    }

    return data
  } catch (error) {
    console.error('Error in getChildById:', error)
    return null
  }
}

// Get tier information for display
export function getTierInfo(tier: TierType) {
  switch (tier) {
    case 'magic_workshop':
      return {
        name: 'Magic Workshop',
        description: 'Ages 5-7 • Visual block coding with magical themes',
        color: 'from-pink-500 to-purple-500',
        bgColor: 'bg-pink-50',
        textColor: 'text-pink-700',
        ageRange: '5-7',
        features: [
          'Drag-and-drop visual blocks',
          'Magical characters and stories',
          'Interactive animations',
          'Voice narration',
          'Simple game creation'
        ]
      }
    case 'innovation_lab':
      return {
        name: 'Innovation Lab',
        description: 'Ages 8-12 • Advanced blocks and app building',
        color: 'from-blue-500 to-cyan-500',
        bgColor: 'bg-blue-50',
        textColor: 'text-blue-700',
        ageRange: '8-12',
        features: [
          'Advanced block programming',
          'Logic and conditional statements',
          'Variables and functions',
          'App and game development',
          'Collaborative projects'
        ]
      }
    case 'professional_studio':
      return {
        name: 'Professional Studio',
        description: 'Ages 13+ • Real programming languages and tools',
        color: 'from-green-500 to-emerald-500',
        bgColor: 'bg-green-50',
        textColor: 'text-green-700',
        ageRange: '13+',
        features: [
          'JavaScript, Python, HTML/CSS',
          'Professional development tools',
          'Version control with Git',
          'Full-stack web development',
          'Portfolio building'
        ]
      }
    default:
      return {
        name: 'Unknown Tier',
        description: 'Age-appropriate learning path',
        color: 'from-gray-500 to-gray-600',
        bgColor: 'bg-gray-50',
        textColor: 'text-gray-700',
        ageRange: 'All ages',
        features: []
      }
  }
}

// Determine tier based on age (client-side helper)
export function determineTierFromAge(age: number): TierType {
  if (age <= 7) return 'magic_workshop'
  if (age <= 12) return 'innovation_lab'
  return 'professional_studio'
}

// Validate child data
export function validateChildData(name: string, age: number): string | null {
  if (!name || name.trim().length === 0) {
    return 'Name is required'
  }
  
  if (name.trim().length > 100) {
    return 'Name must be less than 100 characters'
  }
  
  if (age < 3 || age > 18) {
    return 'Age must be between 3 and 18'
  }
  
  return null
}

// Format learning time for display
export function formatLearningTime(minutes: number): string {
  if (minutes < 60) {
    return `${minutes}m`
  }
  
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  
  if (remainingMinutes === 0) {
    return `${hours}h`
  }
  
  return `${hours}h ${remainingMinutes}m`
}

// Calculate progress percentage
export function calculateProgressPercentage(completed: number, total: number): number {
  if (total === 0) return 0
  return Math.round((completed / total) * 100)
}

// Get achievement level based on progress
export function getAchievementLevel(achievementsCount: number): {
  level: string
  color: string
  nextMilestone: number
} {
  if (achievementsCount >= 50) {
    return { level: 'Master Coder', color: 'text-purple-600', nextMilestone: 100 }
  } else if (achievementsCount >= 25) {
    return { level: 'Expert Builder', color: 'text-blue-600', nextMilestone: 50 }
  } else if (achievementsCount >= 10) {
    return { level: 'Creative Developer', color: 'text-green-600', nextMilestone: 25 }
  } else if (achievementsCount >= 5) {
    return { level: 'Rising Star', color: 'text-yellow-600', nextMilestone: 10 }
  } else {
    return { level: 'Beginner', color: 'text-gray-600', nextMilestone: 5 }
  }
}

