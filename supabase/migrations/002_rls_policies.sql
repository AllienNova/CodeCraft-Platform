-- Codopia Platform Row Level Security (RLS) Policies
-- Migration: 002_rls_policies.sql
-- Author: Agent Athena (Database Architect)
-- Date: September 16, 2025

-- =====================================================
-- ENABLE ROW LEVEL SECURITY ON ALL TABLES
-- =====================================================

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE children ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE module_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE lesson_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_collaborators ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- PROFILES TABLE POLICIES
-- =====================================================

-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Users can insert their own profile (for registration)
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Admins can view all profiles
CREATE POLICY "Admins can view all profiles" ON profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- =====================================================
-- CHILDREN TABLE POLICIES
-- =====================================================

-- Parents can view their own children
CREATE POLICY "Parents can view own children" ON children
    FOR SELECT USING (parent_id = auth.uid());

-- Parents can insert children
CREATE POLICY "Parents can insert children" ON children
    FOR INSERT WITH CHECK (parent_id = auth.uid());

-- Parents can update their own children
CREATE POLICY "Parents can update own children" ON children
    FOR UPDATE USING (parent_id = auth.uid());

-- Teachers can view children in their classes (TODO: implement class relationships)
-- Admins can view all children
CREATE POLICY "Admins can view all children" ON children
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- =====================================================
-- SUBSCRIPTION POLICIES
-- =====================================================

-- Anyone can view active subscription plans
CREATE POLICY "Anyone can view active subscription plans" ON subscription_plans
    FOR SELECT USING (is_active = true);

-- Users can view their own subscriptions
CREATE POLICY "Users can view own subscriptions" ON subscriptions
    FOR SELECT USING (user_id = auth.uid());

-- Users can insert their own subscriptions
CREATE POLICY "Users can insert own subscriptions" ON subscriptions
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- Users can update their own subscriptions
CREATE POLICY "Users can update own subscriptions" ON subscriptions
    FOR UPDATE USING (user_id = auth.uid());

-- =====================================================
-- CURRICULUM CONTENT POLICIES
-- =====================================================

-- Anyone can view published modules
CREATE POLICY "Anyone can view published modules" ON modules
    FOR SELECT USING (is_published = true);

-- Admins can view all modules
CREATE POLICY "Admins can view all modules" ON modules
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Anyone can view published lessons
CREATE POLICY "Anyone can view published lessons" ON lessons
    FOR SELECT USING (is_published = true);

-- Admins can view all lessons
CREATE POLICY "Admins can view all lessons" ON lessons
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Anyone can view exercises for published lessons
CREATE POLICY "Anyone can view exercises for published lessons" ON exercises
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM lessons 
            WHERE id = exercises.lesson_id AND is_published = true
        )
    );

-- =====================================================
-- PROGRESS TRACKING POLICIES
-- =====================================================

-- Parents can view their children's progress
CREATE POLICY "Parents can view children progress" ON module_progress
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = module_progress.child_id AND parent_id = auth.uid()
        )
    );

-- Children can view and update their own progress (if we implement child accounts)
CREATE POLICY "Children can manage own progress" ON module_progress
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = module_progress.child_id AND parent_id = auth.uid()
        )
    );

-- Same policies for lesson progress
CREATE POLICY "Parents can view children lesson progress" ON lesson_progress
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = lesson_progress.child_id AND parent_id = auth.uid()
        )
    );

CREATE POLICY "Children can manage own lesson progress" ON lesson_progress
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = lesson_progress.child_id AND parent_id = auth.uid()
        )
    );

-- Exercise submissions policies
CREATE POLICY "Parents can view children exercise submissions" ON exercise_submissions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = exercise_submissions.child_id AND parent_id = auth.uid()
        )
    );

CREATE POLICY "Children can manage own exercise submissions" ON exercise_submissions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = exercise_submissions.child_id AND parent_id = auth.uid()
        )
    );

-- =====================================================
-- PROJECTS & PORTFOLIO POLICIES
-- =====================================================

-- Parents can view their children's projects
CREATE POLICY "Parents can view children projects" ON projects
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = projects.child_id AND parent_id = auth.uid()
        )
    );

-- Anyone can view public projects
CREATE POLICY "Anyone can view public projects" ON projects
    FOR SELECT USING (is_public = true);

-- Children can manage their own projects
CREATE POLICY "Children can manage own projects" ON projects
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = projects.child_id AND parent_id = auth.uid()
        )
    );

-- Project collaborators policies
CREATE POLICY "View project collaborators" ON project_collaborators
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = project_collaborators.child_id AND parent_id = auth.uid()
        ) OR
        EXISTS (
            SELECT 1 FROM projects p
            JOIN children c ON p.child_id = c.id
            WHERE p.id = project_collaborators.project_id AND c.parent_id = auth.uid()
        )
    );

-- =====================================================
-- COMMUNICATION POLICIES
-- =====================================================

-- Users can view messages they sent or received
CREATE POLICY "Users can view own messages" ON messages
    FOR SELECT USING (sender_id = auth.uid() OR recipient_id = auth.uid());

-- Users can send messages
CREATE POLICY "Users can send messages" ON messages
    FOR INSERT WITH CHECK (sender_id = auth.uid());

-- Users can view their own notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (user_id = auth.uid());

-- Users can update their own notifications (mark as read)
CREATE POLICY "Users can update own notifications" ON notifications
    FOR UPDATE USING (user_id = auth.uid());

-- =====================================================
-- ACHIEVEMENTS POLICIES
-- =====================================================

-- Anyone can view active achievements
CREATE POLICY "Anyone can view active achievements" ON achievements
    FOR SELECT USING (is_active = true);

-- Parents can view their children's achievements
CREATE POLICY "Parents can view children achievements" ON user_achievements
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = user_achievements.child_id AND parent_id = auth.uid()
        )
    );

-- =====================================================
-- ANALYTICS POLICIES
-- =====================================================

-- Users can view their own analytics
CREATE POLICY "Users can view own analytics" ON analytics_events
    FOR SELECT USING (user_id = auth.uid());

-- Parents can view their children's analytics
CREATE POLICY "Parents can view children analytics" ON analytics_events
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = analytics_events.child_id AND parent_id = auth.uid()
        )
    );

-- System can insert analytics events
CREATE POLICY "System can insert analytics" ON analytics_events
    FOR INSERT WITH CHECK (true);

-- Admins can view all analytics
CREATE POLICY "Admins can view all analytics" ON analytics_events
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

