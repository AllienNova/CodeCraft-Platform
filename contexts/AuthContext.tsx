'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import { AuthUser, AuthState, getCurrentUser } from '@/lib/auth'

interface AuthContextType extends AuthState {
  signOut: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: React.ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshUser = async () => {
    try {
      setError(null)
      const currentUser = await getCurrentUser()
      setUser(currentUser)
    } catch (err) {
      console.error('Error refreshing user:', err)
      setError('Failed to refresh user data')
      setUser(null)
    }
  }

  const signOut = async () => {
    try {
      setError(null)
      const { error } = await supabase.auth.signOut()
      if (error) {
        throw error
      }
      setUser(null)
    } catch (err) {
      console.error('Error signing out:', err)
      setError('Failed to sign out')
    }
  }

  useEffect(() => {
    // Get initial session
    const getInitialSession = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession()
        
        if (error) {
          console.error('Error getting session:', error)
          setError('Failed to get session')
        } else if (session?.user) {
          await refreshUser()
        }
      } catch (err) {
        console.error('Error in getInitialSession:', err)
        setError('Failed to initialize session')
      } finally {
        setLoading(false)
      }
    }

    getInitialSession()

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth state changed:', event, session?.user?.email)
        
        try {
          setError(null)
          
          if (event === 'SIGNED_IN' && session?.user) {
            await refreshUser()
          } else if (event === 'SIGNED_OUT') {
            setUser(null)
          } else if (event === 'TOKEN_REFRESHED' && session?.user) {
            await refreshUser()
          }
        } catch (err) {
          console.error('Error handling auth state change:', err)
          setError('Authentication error occurred')
        } finally {
          setLoading(false)
        }
      }
    )

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  const value: AuthContextType = {
    user,
    loading,
    error,
    signOut,
    refreshUser
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook for checking if user is authenticated
export function useRequireAuth() {
  const { user, loading } = useAuth()
  
  useEffect(() => {
    if (!loading && !user) {
      // Redirect to login if not authenticated
      window.location.href = '/auth/signin'
    }
  }, [user, loading])

  return { user, loading }
}

// Hook for checking if user is a parent
export function useRequireParent() {
  const { user, loading } = useAuth()
  
  useEffect(() => {
    if (!loading) {
      if (!user) {
        window.location.href = '/auth/signin'
      } else if (user.profile?.role !== 'parent') {
        window.location.href = '/unauthorized'
      }
    }
  }, [user, loading])

  return { user, loading }
}

// Hook for getting current child context
export function useChildContext(childId?: string) {
  const { user } = useAuth()
  const [currentChild, setCurrentChild] = useState<Database['public']['Tables']['children']['Row'] | null>(null)

  useEffect(() => {
    if (user && childId) {
      const child = user.children.find(c => c.id === childId)
      setCurrentChild(child || null)
    }
  }, [user, childId])

  return currentChild
}

