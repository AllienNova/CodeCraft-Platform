import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Types for our database
export type Database = {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          email: string
          full_name: string | null
          avatar_url: string | null
          role: 'parent' | 'teacher' | 'admin'
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          email: string
          full_name?: string | null
          avatar_url?: string | null
          role?: 'parent' | 'teacher' | 'admin'
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          email?: string
          full_name?: string | null
          avatar_url?: string | null
          role?: 'parent' | 'teacher' | 'admin'
          created_at?: string
          updated_at?: string
        }
      }
      children: {
        Row: {
          id: string
          parent_id: string
          name: string
          age: number
          tier: 'magic_workshop' | 'innovation_lab' | 'professional_studio'
          avatar_url: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          parent_id: string
          name: string
          age: number
          tier?: 'magic_workshop' | 'innovation_lab' | 'professional_studio'
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          parent_id?: string
          name?: string
          age?: number
          tier?: 'magic_workshop' | 'innovation_lab' | 'professional_studio'
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}

