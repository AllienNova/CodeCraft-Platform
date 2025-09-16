-- Enhanced Row Level Security Policies
-- Migration: 005_enhanced_rls_policies.sql
-- Author: Agent Aegis (Security & Integration Specialist)
-- Date: September 16, 2025

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE children ENABLE ROW LEVEL SECURITY;
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
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- PROFILES TABLE POLICIES
-- =====================================================

-- Users can view and update their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Profiles are created automatically via trigger, no manual insert needed
CREATE POLICY "Profiles created via trigger only" ON profiles
    FOR INSERT WITH CHECK (false);

-- Users cannot delete their own profile (handled by auth.users cascade)
CREATE POLICY "Profiles cannot be deleted manually" ON profiles
    FOR DELETE USING (false);

-- =====================================================
-- CHILDREN TABLE POLICIES
-- =====================================================

-- Parents can view their own children
CREATE POLICY "Parents can view their children" ON children
    FOR SELECT USING (
        auth.uid() = parent_id
        AND is_active = true
    );

-- Parents can create children for themselves
CREATE POLICY "Parents can create children" ON children
    FOR INSERT WITH CHECK (
        auth.uid() = parent_id
        AND EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'parent'
        )
    );

-- Parents can update their own children
CREATE POLICY "Parents can update their children" ON children
    FOR UPDATE USING (
        auth.uid() = parent_id
        AND is_active = true
    );

-- Parents can soft-delete their children (set is_active = false)
CREATE POLICY "Parents can deactivate their children" ON children
    FOR UPDATE USING (
        auth.uid() = parent_id
        AND is_active = true
    ) WITH CHECK (
        auth.uid() = parent_id
    );

-- No direct deletion allowed (use soft delete)
CREATE POLICY "Children cannot be hard deleted" ON children
    FOR DELETE USING (false);

-- =====================================================
-- CURRICULUM CONTENT POLICIES (READ-ONLY FOR USERS)
-- =====================================================

-- All authenticated users can view published modules
CREATE POLICY "Users can view published modules" ON modules
    FOR SELECT USING (
        auth.role() = 'authenticated'
        AND is_published = true
    );

-- All authenticated users can view published lessons
CREATE POLICY "Users can view published lessons" ON lessons
    FOR SELECT USING (
        auth.role() = 'authenticated'
        AND is_published = true
    );

-- All authenticated users can view exercises for published lessons
CREATE POLICY "Users can view exercises for published lessons" ON exercises
    FOR SELECT USING (
        auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM lessons 
            WHERE id = lesson_id 
            AND is_published = true
        )
    );

-- Only admins can modify curriculum content
CREATE POLICY "Only admins can modify modules" ON modules
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

CREATE POLICY "Only admins can modify lessons" ON lessons
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

CREATE POLICY "Only admins can modify exercises" ON exercises
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

-- =====================================================
-- PROGRESS TRACKING POLICIES
-- =====================================================

-- Parents can view progress for their children
CREATE POLICY "Parents can view children progress" ON module_progress
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

CREATE POLICY "Parents can view children lesson progress" ON lesson_progress
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- System can create and update progress (via service role)
CREATE POLICY "System can manage module progress" ON module_progress
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "System can manage lesson progress" ON lesson_progress
    FOR ALL USING (auth.role() = 'service_role');

-- Parents can create progress entries for their children
CREATE POLICY "Parents can create children progress" ON module_progress
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

CREATE POLICY "Parents can create children lesson progress" ON lesson_progress
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- Parents can update progress for their children
CREATE POLICY "Parents can update children progress" ON module_progress
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

CREATE POLICY "Parents can update children lesson progress" ON lesson_progress
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- =====================================================
-- EXERCISE SUBMISSIONS POLICIES
-- =====================================================

-- Parents can view their children's exercise submissions
CREATE POLICY "Parents can view children submissions" ON exercise_submissions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- System can create submissions (via service role)
CREATE POLICY "System can create submissions" ON exercise_submissions
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Parents can create submissions for their children
CREATE POLICY "Parents can create children submissions" ON exercise_submissions
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- =====================================================
-- PROJECTS POLICIES
-- =====================================================

-- Parents can view their children's projects
CREATE POLICY "Parents can view children projects" ON projects
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
        OR is_public = true  -- Public projects visible to all
    );

-- Parents can create projects for their children
CREATE POLICY "Parents can create children projects" ON projects
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- Parents can update their children's projects
CREATE POLICY "Parents can update children projects" ON projects
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- Parents can delete their children's projects
CREATE POLICY "Parents can delete children projects" ON projects
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- =====================================================
-- PROJECT COLLABORATORS POLICIES
-- =====================================================

-- Users can view collaborators for projects they have access to
CREATE POLICY "Users can view project collaborators" ON project_collaborators
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM projects p
            JOIN children c ON p.child_id = c.id
            WHERE p.id = project_id
            AND (c.parent_id = auth.uid() OR p.is_public = true)
            AND c.is_active = true
        )
    );

-- Parents can manage collaborators for their children's projects
CREATE POLICY "Parents can manage project collaborators" ON project_collaborators
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM projects p
            JOIN children c ON p.child_id = c.id
            WHERE p.id = project_id
            AND c.parent_id = auth.uid()
            AND c.is_active = true
        )
    );

-- =====================================================
-- MESSAGING POLICIES
-- =====================================================

-- Users can view messages they sent or received
CREATE POLICY "Users can view their messages" ON messages
    FOR SELECT USING (
        sender_id = auth.uid() OR recipient_id = auth.uid()
    );

-- Users can send messages
CREATE POLICY "Users can send messages" ON messages
    FOR INSERT WITH CHECK (sender_id = auth.uid());

-- Users can update messages they sent (for editing)
CREATE POLICY "Users can update sent messages" ON messages
    FOR UPDATE USING (sender_id = auth.uid());

-- Users cannot delete messages (for audit trail)
CREATE POLICY "Messages cannot be deleted" ON messages
    FOR DELETE USING (false);

-- =====================================================
-- NOTIFICATIONS POLICIES
-- =====================================================

-- Users can view their own notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (user_id = auth.uid());

-- System can create notifications
CREATE POLICY "System can create notifications" ON notifications
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Users can update their notifications (mark as read)
CREATE POLICY "Users can update own notifications" ON notifications
    FOR UPDATE USING (user_id = auth.uid());

-- Users can delete their own notifications
CREATE POLICY "Users can delete own notifications" ON notifications
    FOR DELETE USING (user_id = auth.uid());

-- =====================================================
-- ACHIEVEMENTS POLICIES
-- =====================================================

-- All users can view available achievements
CREATE POLICY "Users can view achievements" ON achievements
    FOR SELECT USING (
        auth.role() = 'authenticated'
        AND is_active = true
    );

-- Only admins can manage achievements
CREATE POLICY "Only admins can manage achievements" ON achievements
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

-- =====================================================
-- USER ACHIEVEMENTS POLICIES
-- =====================================================

-- Parents can view their children's achievements
CREATE POLICY "Parents can view children achievements" ON user_achievements
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- System can award achievements
CREATE POLICY "System can award achievements" ON user_achievements
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- No manual updates or deletions of achievements
CREATE POLICY "Achievements cannot be manually modified" ON user_achievements
    FOR UPDATE USING (false);

CREATE POLICY "Achievements cannot be deleted" ON user_achievements
    FOR DELETE USING (false);

-- =====================================================
-- ANALYTICS EVENTS POLICIES
-- =====================================================

-- System can create analytics events
CREATE POLICY "System can create analytics events" ON analytics_events
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Admins can view all analytics events
CREATE POLICY "Admins can view analytics events" ON analytics_events
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

-- Parents can view analytics for their children
CREATE POLICY "Parents can view children analytics" ON analytics_events
    FOR SELECT USING (
        child_id IS NOT NULL
        AND EXISTS (
            SELECT 1 FROM children 
            WHERE id = child_id 
            AND parent_id = auth.uid()
            AND is_active = true
        )
    );

-- No updates or deletions of analytics events
CREATE POLICY "Analytics events are immutable" ON analytics_events
    FOR UPDATE USING (false);

CREATE POLICY "Analytics events cannot be deleted" ON analytics_events
    FOR DELETE USING (false);

-- =====================================================
-- SUBSCRIPTIONS POLICIES
-- =====================================================

-- Users can view their own subscriptions
CREATE POLICY "Users can view own subscriptions" ON subscriptions
    FOR SELECT USING (user_id = auth.uid());

-- System can manage subscriptions (via Stripe webhooks)
CREATE POLICY "System can manage subscriptions" ON subscriptions
    FOR ALL USING (auth.role() = 'service_role');

-- Admins can view all subscriptions
CREATE POLICY "Admins can view all subscriptions" ON subscriptions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

-- =====================================================
-- SUBSCRIPTION PLANS POLICIES (READ-ONLY FOR USERS)
-- =====================================================

-- All users can view active subscription plans
CREATE POLICY "Users can view active plans" ON subscription_plans
    FOR SELECT USING (
        auth.role() = 'authenticated'
        AND is_active = true
    );

-- Only admins can manage subscription plans
CREATE POLICY "Only admins can manage plans" ON subscription_plans
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() 
            AND role = 'admin'
        )
    );

-- =====================================================
-- SECURITY FUNCTIONS
-- =====================================================

-- Function to check if user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM profiles 
        WHERE id = auth.uid() 
        AND role = 'admin'
    );
END;
$$;

-- Function to check if user is parent of child
CREATE OR REPLACE FUNCTION is_parent_of_child(child_user_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM children 
        WHERE id = child_user_id 
        AND parent_id = auth.uid()
        AND is_active = true
    );
END;
$$;

-- Function to check if user has valid subscription
CREATE OR REPLACE FUNCTION has_valid_subscription()
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM subscriptions 
        WHERE user_id = auth.uid() 
        AND status = 'active'
        AND (current_period_end IS NULL OR current_period_end > NOW())
    );
END;
$$;

-- Grant execute permissions on security functions
GRANT EXECUTE ON FUNCTION is_admin() TO authenticated;
GRANT EXECUTE ON FUNCTION is_parent_of_child(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION has_valid_subscription() TO authenticated;

-- =====================================================
-- AUDIT LOGGING
-- =====================================================

-- Create audit log table for sensitive operations
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    action TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on audit log
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Only admins can view audit logs
CREATE POLICY "Only admins can view audit logs" ON audit_log
    FOR SELECT USING (is_admin());

-- System can create audit logs
CREATE POLICY "System can create audit logs" ON audit_log
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Audit logs are immutable
CREATE POLICY "Audit logs are immutable" ON audit_log
    FOR UPDATE USING (false);

CREATE POLICY "Audit logs cannot be deleted" ON audit_log
    FOR DELETE USING (false);

-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO audit_log (
        user_id,
        action,
        table_name,
        record_id,
        old_values,
        new_values,
        ip_address,
        user_agent
    ) VALUES (
        auth.uid(),
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END,
        inet_client_addr(),
        current_setting('request.headers', true)::json->>'user-agent'
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$;

-- Apply audit triggers to sensitive tables
CREATE TRIGGER audit_profiles_trigger
    AFTER INSERT OR UPDATE OR DELETE ON profiles
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();

CREATE TRIGGER audit_children_trigger
    AFTER INSERT OR UPDATE OR DELETE ON children
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();

CREATE TRIGGER audit_subscriptions_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();

-- Create indexes for audit log performance
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_table_action ON audit_log(table_name, action);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- =====================================================
-- RATE LIMITING
-- =====================================================

-- Create rate limiting table
CREATE TABLE IF NOT EXISTS rate_limits (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    action TEXT NOT NULL,
    count INTEGER DEFAULT 1,
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, action, window_start)
);

-- Function to check rate limits
CREATE OR REPLACE FUNCTION check_rate_limit(
    action_name TEXT,
    max_requests INTEGER,
    window_minutes INTEGER DEFAULT 60
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    current_count INTEGER;
    window_start TIMESTAMP WITH TIME ZONE;
BEGIN
    -- Calculate window start time
    window_start := date_trunc('hour', NOW()) + 
                   (EXTRACT(minute FROM NOW())::INTEGER / window_minutes) * 
                   (window_minutes || ' minutes')::INTERVAL;
    
    -- Get current count for this window
    SELECT count INTO current_count
    FROM rate_limits
    WHERE user_id = auth.uid()
    AND action = action_name
    AND window_start = window_start;
    
    -- If no record exists, create one
    IF current_count IS NULL THEN
        INSERT INTO rate_limits (user_id, action, window_start)
        VALUES (auth.uid(), action_name, window_start);
        RETURN TRUE;
    END IF;
    
    -- Check if limit exceeded
    IF current_count >= max_requests THEN
        RETURN FALSE;
    END IF;
    
    -- Increment counter
    UPDATE rate_limits
    SET count = count + 1
    WHERE user_id = auth.uid()
    AND action = action_name
    AND window_start = window_start;
    
    RETURN TRUE;
END;
$$;

-- Grant execute permission on rate limit function
GRANT EXECUTE ON FUNCTION check_rate_limit(TEXT, INTEGER, INTEGER) TO authenticated;

-- Clean up old rate limit records (run periodically)
CREATE OR REPLACE FUNCTION cleanup_rate_limits()
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM rate_limits
    WHERE created_at < NOW() - INTERVAL '24 hours';
END;
$$;

