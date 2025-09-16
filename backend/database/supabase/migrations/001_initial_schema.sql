-- Codopia Platform Database Schema
-- Migration: 001_initial_schema.sql
-- Author: Agent Athena (Database Architect)
-- Date: September 16, 2025

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE user_role AS ENUM ('parent', 'teacher', 'admin', 'child');
CREATE TYPE tier_type AS ENUM ('magic_workshop', 'innovation_lab', 'professional_studio');
CREATE TYPE subscription_status AS ENUM ('active', 'inactive', 'cancelled', 'past_due');
CREATE TYPE project_status AS ENUM ('draft', 'in_progress', 'completed', 'shared');
CREATE TYPE lesson_type AS ENUM ('interactive', 'video', 'reading', 'project', 'assessment');

-- =====================================================
-- CORE USER MANAGEMENT TABLES
-- =====================================================

-- Profiles table (extends Supabase auth.users)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    role user_role NOT NULL DEFAULT 'parent',
    phone TEXT,
    timezone TEXT DEFAULT 'UTC',
    language TEXT DEFAULT 'en',
    onboarding_completed BOOLEAN DEFAULT FALSE,
    marketing_consent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Children profiles
CREATE TABLE children (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    parent_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 3 AND age <= 18),
    tier tier_type NOT NULL,
    avatar_url TEXT,
    bio TEXT,
    interests TEXT[],
    learning_goals TEXT[],
    accessibility_needs TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SUBSCRIPTION & BILLING TABLES
-- =====================================================

-- Subscription plans
CREATE TABLE subscription_plans (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price_monthly DECIMAL(10,2),
    price_yearly DECIMAL(10,2),
    features JSONB,
    max_children INTEGER,
    tier_access tier_type[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User subscriptions
CREATE TABLE subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    plan_id UUID REFERENCES subscription_plans(id) NOT NULL,
    status subscription_status NOT NULL DEFAULT 'active',
    stripe_subscription_id TEXT UNIQUE,
    stripe_customer_id TEXT,
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CURRICULUM & CONTENT TABLES
-- =====================================================

-- Curriculum modules (Magic Workshop, Innovation Lab, Professional Studio)
CREATE TABLE modules (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tier tier_type NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    estimated_duration_hours INTEGER,
    learning_objectives TEXT[],
    prerequisites TEXT[],
    cover_image_url TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual lessons within modules
CREATE TABLE lessons (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    module_id UUID REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    type lesson_type NOT NULL,
    order_index INTEGER NOT NULL,
    content JSONB, -- Flexible content structure
    estimated_duration_minutes INTEGER,
    difficulty_level INTEGER CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    learning_objectives TEXT[],
    resources JSONB, -- Links, files, etc.
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Interactive coding exercises
CREATE TABLE exercises (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    instructions JSONB,
    starter_code TEXT,
    solution_code TEXT,
    test_cases JSONB,
    hints JSONB,
    difficulty_level INTEGER CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    estimated_time_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- LEARNING PROGRESS & ANALYTICS TABLES
-- =====================================================

-- Child progress through modules
CREATE TABLE module_progress (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    module_id UUID REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    status project_status DEFAULT 'draft',
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    time_spent_minutes INTEGER DEFAULT 0,
    UNIQUE(child_id, module_id)
);

-- Child progress through individual lessons
CREATE TABLE lesson_progress (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE NOT NULL,
    status project_status DEFAULT 'draft',
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    time_spent_minutes INTEGER DEFAULT 0,
    notes TEXT,
    UNIQUE(child_id, lesson_id)
);

-- Exercise submissions and attempts
CREATE TABLE exercise_submissions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    exercise_id UUID REFERENCES exercises(id) ON DELETE CASCADE NOT NULL,
    code TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    test_results JSONB,
    hints_used INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 1,
    time_spent_minutes INTEGER DEFAULT 0,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- PROJECTS & PORTFOLIO TABLES
-- =====================================================

-- Student projects (portfolio items)
CREATE TABLE projects (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT, -- 'game', 'app', 'story', 'art', etc.
    status project_status DEFAULT 'draft',
    code TEXT,
    assets JSONB, -- Images, sounds, etc.
    preview_url TEXT,
    share_url TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    likes_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project collaborators (for group projects)
CREATE TABLE project_collaborators (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE NOT NULL,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    role TEXT DEFAULT 'collaborator', -- 'owner', 'collaborator', 'viewer'
    invited_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    joined_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(project_id, child_id)
);

-- =====================================================
-- COMMUNICATION & SOCIAL FEATURES
-- =====================================================

-- Messages between users (parents, teachers, children)
CREATE TABLE messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    sender_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    recipient_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    subject TEXT,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    parent_message_id UUID REFERENCES messages(id), -- For threading
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications system
CREATE TABLE notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    type TEXT NOT NULL, -- 'achievement', 'message', 'reminder', etc.
    title TEXT NOT NULL,
    content TEXT,
    data JSONB, -- Additional structured data
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ACHIEVEMENTS & GAMIFICATION
-- =====================================================

-- Achievement definitions
CREATE TABLE achievements (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon_url TEXT,
    tier tier_type,
    category TEXT, -- 'completion', 'creativity', 'collaboration', etc.
    points INTEGER DEFAULT 0,
    requirements JSONB, -- Conditions to unlock
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User achievements (earned badges)
CREATE TABLE user_achievements (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE NOT NULL,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE NOT NULL,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(child_id, achievement_id)
);

-- =====================================================
-- ANALYTICS & REPORTING
-- =====================================================

-- Learning analytics events
CREATE TABLE analytics_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    child_id UUID REFERENCES children(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_data JSONB,
    session_id TEXT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Profiles indexes
CREATE INDEX idx_profiles_role ON profiles(role);
CREATE INDEX idx_profiles_email ON profiles(email);

-- Children indexes
CREATE INDEX idx_children_parent_id ON children(parent_id);
CREATE INDEX idx_children_tier ON children(tier);
CREATE INDEX idx_children_age ON children(age);

-- Progress indexes
CREATE INDEX idx_module_progress_child_id ON module_progress(child_id);
CREATE INDEX idx_lesson_progress_child_id ON lesson_progress(child_id);
CREATE INDEX idx_exercise_submissions_child_id ON exercise_submissions(child_id);

-- Projects indexes
CREATE INDEX idx_projects_child_id ON projects(child_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_is_public ON projects(is_public);

-- Messages indexes
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Notifications indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);

-- Analytics indexes
CREATE INDEX idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX idx_analytics_events_child_id ON analytics_events(child_id);
CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_created_at ON analytics_events(created_at);

