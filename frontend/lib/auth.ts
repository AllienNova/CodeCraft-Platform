import { supabase } from './supabase'
import { Database } from './database.types'

type Profile = Database['public']['Tables']['profiles']['Row']
type Child = Database['public']['Tables']['children']['Row']

export interface AuthUser {
  id: string
  email: string
  profile: Profile | null
  children: Child[]
}

export interface AuthState {
  user: AuthUser | null
  loading: boolean
  error: string | null
}

// Determine tier based on age
export function determineTier(age: number): 'magic_workshop' | 'innovation_lab' | 'professional_studio' {
  if (age <= 7) return 'magic_workshop'
  if (age <= 12) return 'innovation_lab'
  return 'professional_studio'
}

// Get current user with profile and children
export async function getCurrentUser(): Promise<AuthUser | null> {
  try {
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    
    if (authError || !user) {
      return null
    }

    // Get user profile
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single()

    if (profileError) {
      console.error('Error fetching profile:', profileError)
      return null
    }

    // Get children if user is a parent
    let children: Child[] = []
    if (profile?.role === 'parent') {
      const { data: childrenData, error: childrenError } = await supabase
        .from('children')
        .select('*')
        .eq('parent_id', user.id)
        .order('created_at', { ascending: true })

      if (!childrenError && childrenData) {
        children = childrenData
      }
    }

    return {
      id: user.id,
      email: user.email || '',
      profile,
      children
    }
  } catch (error) {
    console.error('Error getting current user:', error)
    return null
  }
}

// Sign up new parent user
export async function signUpParent(email: string, password: string, fullName: string) {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          role: 'parent'
        }
      }
    })

    if (error) {
      throw error
    }

    return { data, error: null }
  } catch (error) {
    console.error('Error signing up parent:', error)
    return { data: null, error }
  }
}

// Sign in user
export async function signIn(email: string, password: string) {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })

    if (error) {
      throw error
    }

    return { data, error: null }
  } catch (error) {
    console.error('Error signing in:', error)
    return { data: null, error }
  }
}

// Sign out user
export async function signOut() {
  try {
    const { error } = await supabase.auth.signOut()
    if (error) {
      throw error
    }
    return { error: null }
  } catch (error) {
    console.error('Error signing out:', error)
    return { error }
  }
}

// Create child profile
export async function createChildProfile(parentId: string, name: string, age: number) {
  try {
    const tier = determineTier(age)
    
    const { data, error } = await supabase
      .from('children')
      .insert({
        parent_id: parentId,
        name,
        age,
        tier
      })
      .select()
      .single()

    if (error) {
      throw error
    }

    return { data, error: null }
  } catch (error) {
    console.error('Error creating child profile:', error)
    return { data: null, error }
  }
}

// Update child profile
export async function updateChildProfile(childId: string, updates: Partial<Pick<Child, 'name' | 'age' | 'avatar_url'>>) {
  try {
    // If age is being updated, recalculate tier
    const updateData = { ...updates }
    if (updates.age) {
      updateData.tier = determineTier(updates.age)
    }

    const { data, error } = await supabase
      .from('children')
      .update(updateData)
      .eq('id', childId)
      .select()
      .single()

    if (error) {
      throw error
    }

    return { data, error: null }
  } catch (error) {
    console.error('Error updating child profile:', error)
    return { data: null, error }
  }
}

// Delete child profile
export async function deleteChildProfile(childId: string) {
  try {
    const { error } = await supabase
      .from('children')
      .delete()
      .eq('id', childId)

    if (error) {
      throw error
    }

    return { error: null }
  } catch (error) {
    console.error('Error deleting child profile:', error)
    return { error }
  }
}

// Get child by ID (with parent verification)
export async function getChildById(childId: string, parentId: string): Promise<Child | null> {
  try {
    const { data, error } = await supabase
      .from('children')
      .select('*')
      .eq('id', childId)
      .eq('parent_id', parentId)
      .single()

    if (error) {
      console.error('Error fetching child:', error)
      return null
    }

    return data
  } catch (error) {
    console.error('Error getting child by ID:', error)
    return null
  }
}

// Reset password
export async function resetPassword(email: string) {
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/reset-password`
    })

    if (error) {
      throw error
    }

    return { error: null }
  } catch (error) {
    console.error('Error resetting password:', error)
    return { error }
  }
}

// Update password
export async function updatePassword(newPassword: string) {
  try {
    const { error } = await supabase.auth.updateUser({
      password: newPassword
    })

    if (error) {
      throw error
    }

    return { error: null }
  } catch (error) {
    console.error('Error updating password:', error)
    return { error }
  }
}

// Social login with Google
export async function signInWithGoogle() {
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    })

    if (error) {
      throw error
    }

    return { error: null }
  } catch (error) {
    console.error('Error signing in with Google:', error)
    return { error }
  }
}

// Check if user has completed onboarding
export async function hasCompletedOnboarding(userId: string): Promise<boolean> {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('onboarding_completed')
      .eq('id', userId)
      .single()

    if (error || !data) {
      return false
    }

    return data.onboarding_completed || false
  } catch (error) {
    console.error('Error checking onboarding status:', error)
    return false
  }
}

// Mark onboarding as completed
export async function completeOnboarding(userId: string) {
  try {
    const { error } = await supabase
      .from('profiles')
      .update({ onboarding_completed: true })
      .eq('id', userId)

    if (error) {
      throw error
    }

    return { error: null }
  } catch (error) {
    console.error('Error completing onboarding:', error)
    return { error }
  }
}

