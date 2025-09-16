import { supabase } from './supabase'

// Rate limiting configuration
export const RATE_LIMITS = {
  // Authentication actions
  LOGIN_ATTEMPTS: { max: 5, windowMinutes: 15 },
  SIGNUP_ATTEMPTS: { max: 3, windowMinutes: 60 },
  PASSWORD_RESET: { max: 3, windowMinutes: 60 },
  
  // Child management actions
  CREATE_CHILD: { max: 10, windowMinutes: 60 },
  UPDATE_CHILD: { max: 20, windowMinutes: 60 },
  DELETE_CHILD: { max: 5, windowMinutes: 60 },
  
  // Project actions
  CREATE_PROJECT: { max: 50, windowMinutes: 60 },
  UPDATE_PROJECT: { max: 100, windowMinutes: 60 },
  
  // Message actions
  SEND_MESSAGE: { max: 30, windowMinutes: 60 },
  
  // General API calls
  API_CALLS: { max: 1000, windowMinutes: 60 }
} as const

export type RateLimitAction = keyof typeof RATE_LIMITS

// Check if action is within rate limits
export async function checkRateLimit(action: RateLimitAction): Promise<boolean> {
  try {
    const config = RATE_LIMITS[action]
    
    const { data, error } = await supabase.rpc('check_rate_limit', {
      action_name: action,
      max_requests: config.max,
      window_minutes: config.windowMinutes
    })

    if (error) {
      console.error('Rate limit check error:', error)
      // Fail open - allow the action if we can't check the rate limit
      return true
    }

    return data === true
  } catch (error) {
    console.error('Rate limit check failed:', error)
    // Fail open - allow the action if we can't check the rate limit
    return true
  }
}

// Wrapper function to enforce rate limits on actions
export async function withRateLimit<T>(
  action: RateLimitAction,
  fn: () => Promise<T>
): Promise<T> {
  const allowed = await checkRateLimit(action)
  
  if (!allowed) {
    const config = RATE_LIMITS[action]
    throw new Error(
      `Rate limit exceeded. Maximum ${config.max} ${action} actions allowed per ${config.windowMinutes} minutes.`
    )
  }
  
  return fn()
}

// Security validation functions
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export function validatePassword(password: string): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long')
  }
  
  if (password.length > 128) {
    errors.push('Password must be less than 128 characters')
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }
  
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number')
  }
  
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    errors.push('Password must contain at least one special character')
  }
  
  // Check for common weak passwords
  const commonPasswords = [
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password123', 'admin', 'letmein', 'welcome', 'monkey'
  ]
  
  if (commonPasswords.includes(password.toLowerCase())) {
    errors.push('Password is too common. Please choose a more secure password')
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

export function validateChildName(name: string): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (!name || name.trim().length === 0) {
    errors.push('Name is required')
  }
  
  if (name.trim().length > 100) {
    errors.push('Name must be less than 100 characters')
  }
  
  // Check for potentially harmful content
  const suspiciousPatterns = [
    /<script/i,
    /javascript:/i,
    /on\w+\s*=/i,
    /<iframe/i,
    /<object/i,
    /<embed/i
  ]
  
  for (const pattern of suspiciousPatterns) {
    if (pattern.test(name)) {
      errors.push('Name contains invalid characters')
      break
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

export function validateAge(age: number): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (!Number.isInteger(age)) {
    errors.push('Age must be a whole number')
  }
  
  if (age < 3 || age > 18) {
    errors.push('Age must be between 3 and 18')
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

// Content security functions
export function sanitizeHtml(input: string): string {
  // Basic HTML sanitization - remove potentially dangerous tags and attributes
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/<object\b[^<]*(?:(?!<\/object>)<[^<]*)*<\/object>/gi, '')
    .replace(/<embed\b[^<]*(?:(?!<\/embed>)<[^<]*)*<\/embed>/gi, '')
    .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
    .replace(/javascript:/gi, '')
}

export function validateProjectContent(content: string): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (content.length > 1000000) { // 1MB limit
    errors.push('Project content is too large (maximum 1MB)')
  }
  
  // Check for potentially malicious content
  const maliciousPatterns = [
    /eval\s*\(/i,
    /Function\s*\(/i,
    /setTimeout\s*\(/i,
    /setInterval\s*\(/i,
    /document\.write/i,
    /innerHTML\s*=/i,
    /outerHTML\s*=/i
  ]
  
  for (const pattern of maliciousPatterns) {
    if (pattern.test(content)) {
      errors.push('Project content contains potentially unsafe code')
      break
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

// Permission checking functions
export async function checkUserPermission(
  action: string,
  resourceId?: string
): Promise<boolean> {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    
    if (!user) {
      return false
    }
    
    // Get user profile to check role
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', user.id)
      .single()
    
    if (!profile) {
      return false
    }
    
    // Admin users have all permissions
    if (profile.role === 'admin') {
      return true
    }
    
    // Check specific permissions based on action
    switch (action) {
      case 'view_child':
      case 'edit_child':
      case 'delete_child':
        if (!resourceId) return false
        return await checkParentChildRelationship(user.id, resourceId)
      
      case 'create_child':
        return profile.role === 'parent'
      
      case 'view_project':
      case 'edit_project':
      case 'delete_project':
        if (!resourceId) return false
        return await checkProjectAccess(user.id, resourceId)
      
      default:
        return false
    }
  } catch (error) {
    console.error('Permission check error:', error)
    return false
  }
}

async function checkParentChildRelationship(
  parentId: string,
  childId: string
): Promise<boolean> {
  try {
    const { data } = await supabase.rpc('is_parent_of_child', {
      child_user_id: childId
    })
    
    return data === true
  } catch (error) {
    console.error('Parent-child relationship check error:', error)
    return false
  }
}

async function checkProjectAccess(
  userId: string,
  projectId: string
): Promise<boolean> {
  try {
    const { data: project } = await supabase
      .from('projects')
      .select(`
        id,
        is_public,
        children!inner(parent_id)
      `)
      .eq('id', projectId)
      .single()
    
    if (!project) {
      return false
    }
    
    // Public projects are accessible to all
    if (project.is_public) {
      return true
    }
    
    // Check if user is the parent of the child who owns the project
    return project.children.parent_id === userId
  } catch (error) {
    console.error('Project access check error:', error)
    return false
  }
}

// Audit logging function
export async function logSecurityEvent(
  event: string,
  details: Record<string, unknown> = {},
  severity: 'low' | 'medium' | 'high' | 'critical' = 'medium'
) {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    
    await supabase.from('analytics_events').insert({
      user_id: user?.id || null,
      event_type: `security_${event}`,
      event_data: {
        ...details,
        severity,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent,
        url: window.location.href
      }
    })
  } catch (error) {
    console.error('Failed to log security event:', error)
  }
}

// Session security functions
export function validateSession(): boolean {
  try {
    // Check if session is still valid
    const lastActivity = localStorage.getItem('lastActivity')
    if (!lastActivity) {
      return false
    }
    
    const lastActivityTime = new Date(lastActivity).getTime()
    const now = new Date().getTime()
    const sessionTimeout = 8 * 60 * 60 * 1000 // 8 hours
    
    if (now - lastActivityTime > sessionTimeout) {
      // Session expired
      localStorage.removeItem('lastActivity')
      return false
    }
    
    // Update last activity
    localStorage.setItem('lastActivity', new Date().toISOString())
    return true
  } catch (error) {
    console.error('Session validation error:', error)
    return false
  }
}

export function updateSessionActivity() {
  localStorage.setItem('lastActivity', new Date().toISOString())
}

// CSRF protection
export function generateCSRFToken(): string {
  const array = new Uint8Array(32)
  crypto.getRandomValues(array)
  return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('')
}

export function validateCSRFToken(token: string): boolean {
  const storedToken = sessionStorage.getItem('csrfToken')
  return storedToken === token
}

// Initialize CSRF token
export function initializeCSRF() {
  if (!sessionStorage.getItem('csrfToken')) {
    sessionStorage.setItem('csrfToken', generateCSRFToken())
  }
}

// Get CSRF token for requests
export function getCSRFToken(): string {
  return sessionStorage.getItem('csrfToken') || ''
}

