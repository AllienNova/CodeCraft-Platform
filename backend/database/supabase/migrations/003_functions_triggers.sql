-- Codopia Platform Database Functions and Triggers
-- Migration: 003_functions_triggers.sql
-- Author: Agent Athena (Database Architect)
-- Date: September 16, 2025

-- =====================================================
-- UTILITY FUNCTIONS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to automatically assign tier based on age
CREATE OR REPLACE FUNCTION assign_tier_by_age()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.age >= 5 AND NEW.age <= 7 THEN
        NEW.tier = 'magic_workshop';
    ELSIF NEW.age >= 8 AND NEW.age <= 9 THEN
        NEW.tier = 'innovation_lab';
    ELSE
        NEW.tier = 'professional_studio';
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to create user profile after signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name',
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- Function to calculate progress percentage
CREATE OR REPLACE FUNCTION calculate_module_progress(child_uuid UUID, module_uuid UUID)
RETURNS INTEGER AS $$
DECLARE
    total_lessons INTEGER;
    completed_lessons INTEGER;
    progress_pct INTEGER;
BEGIN
    -- Count total lessons in the module
    SELECT COUNT(*) INTO total_lessons
    FROM lessons
    WHERE module_id = module_uuid AND is_published = true;
    
    -- Count completed lessons for the child
    SELECT COUNT(*) INTO completed_lessons
    FROM lesson_progress lp
    JOIN lessons l ON lp.lesson_id = l.id
    WHERE lp.child_id = child_uuid 
    AND l.module_id = module_uuid 
    AND lp.status = 'completed';
    
    -- Calculate percentage
    IF total_lessons = 0 THEN
        progress_pct = 0;
    ELSE
        progress_pct = ROUND((completed_lessons::DECIMAL / total_lessons::DECIMAL) * 100);
    END IF;
    
    RETURN progress_pct;
END;
$$ language 'plpgsql';

-- Function to update module progress when lesson is completed
CREATE OR REPLACE FUNCTION update_module_progress_on_lesson_completion()
RETURNS TRIGGER AS $$
DECLARE
    module_uuid UUID;
    new_progress INTEGER;
BEGIN
    -- Get the module ID for this lesson
    SELECT module_id INTO module_uuid
    FROM lessons
    WHERE id = NEW.lesson_id;
    
    -- Calculate new progress percentage
    SELECT calculate_module_progress(NEW.child_id, module_uuid) INTO new_progress;
    
    -- Update or insert module progress
    INSERT INTO module_progress (child_id, module_id, progress_percentage, last_accessed_at)
    VALUES (NEW.child_id, module_uuid, new_progress, NOW())
    ON CONFLICT (child_id, module_id)
    DO UPDATE SET
        progress_percentage = new_progress,
        last_accessed_at = NOW(),
        updated_at = NOW();
    
    -- Mark module as completed if 100%
    IF new_progress = 100 THEN
        UPDATE module_progress
        SET status = 'completed', completed_at = NOW()
        WHERE child_id = NEW.child_id AND module_id = module_uuid;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to award achievements
CREATE OR REPLACE FUNCTION check_and_award_achievements()
RETURNS TRIGGER AS $$
DECLARE
    achievement_record RECORD;
BEGIN
    -- Check for completion achievements
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        -- Award module completion achievement
        FOR achievement_record IN
            SELECT a.id FROM achievements a
            WHERE a.category = 'completion'
            AND a.requirements->>'type' = 'module_completion'
            AND a.requirements->>'module_id' = NEW.module_id::TEXT
        LOOP
            INSERT INTO user_achievements (child_id, achievement_id)
            VALUES (NEW.child_id, achievement_record.id)
            ON CONFLICT (child_id, achievement_id) DO NOTHING;
        END LOOP;
        
        -- Check for tier completion achievements
        DECLARE
            completed_modules INTEGER;
            total_modules INTEGER;
            child_tier tier_type;
        BEGIN
            -- Get child's tier
            SELECT tier INTO child_tier FROM children WHERE id = NEW.child_id;
            
            -- Count completed modules in tier
            SELECT COUNT(*) INTO completed_modules
            FROM module_progress mp
            JOIN modules m ON mp.module_id = m.id
            WHERE mp.child_id = NEW.child_id
            AND m.tier = child_tier
            AND mp.status = 'completed';
            
            -- Count total modules in tier
            SELECT COUNT(*) INTO total_modules
            FROM modules
            WHERE tier = child_tier AND is_published = true;
            
            -- Award tier completion achievement if all modules completed
            IF completed_modules = total_modules AND total_modules > 0 THEN
                FOR achievement_record IN
                    SELECT a.id FROM achievements a
                    WHERE a.category = 'completion'
                    AND a.requirements->>'type' = 'tier_completion'
                    AND a.tier = child_tier
                LOOP
                    INSERT INTO user_achievements (child_id, achievement_id)
                    VALUES (NEW.child_id, achievement_record.id)
                    ON CONFLICT (child_id, achievement_id) DO NOTHING;
                END LOOP;
            END IF;
        END;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to create notification
CREATE OR REPLACE FUNCTION create_notification(
    user_uuid UUID,
    notification_type TEXT,
    notification_title TEXT,
    notification_content TEXT DEFAULT NULL,
    notification_data JSONB DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    notification_id UUID;
BEGIN
    INSERT INTO notifications (user_id, type, title, content, data)
    VALUES (user_uuid, notification_type, notification_title, notification_content, notification_data)
    RETURNING id INTO notification_id;
    
    RETURN notification_id;
END;
$$ language 'plpgsql';

-- Function to increment project views
CREATE OR REPLACE FUNCTION increment_project_views()
RETURNS TRIGGER AS $$
BEGIN
    -- Only increment for public projects
    IF NEW.is_public = true THEN
        UPDATE projects
        SET views_count = views_count + 1
        WHERE id = NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger to update updated_at on profile changes
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger to update updated_at on children changes
CREATE TRIGGER update_children_updated_at
    BEFORE UPDATE ON children
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger to auto-assign tier based on age
CREATE TRIGGER assign_tier_on_child_insert
    BEFORE INSERT ON children
    FOR EACH ROW
    EXECUTE FUNCTION assign_tier_by_age();

-- Trigger to update tier when age changes
CREATE TRIGGER update_tier_on_age_change
    BEFORE UPDATE ON children
    FOR EACH ROW
    WHEN (OLD.age IS DISTINCT FROM NEW.age)
    EXECUTE FUNCTION assign_tier_by_age();

-- Trigger to create profile after user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- Trigger to update module progress when lesson is completed
CREATE TRIGGER update_module_progress_on_lesson_complete
    AFTER UPDATE ON lesson_progress
    FOR EACH ROW
    WHEN (NEW.status = 'completed' AND OLD.status != 'completed')
    EXECUTE FUNCTION update_module_progress_on_lesson_completion();

-- Trigger to check and award achievements
CREATE TRIGGER check_achievements_on_module_complete
    AFTER UPDATE ON module_progress
    FOR EACH ROW
    EXECUTE FUNCTION check_and_award_achievements();

-- Trigger to update updated_at on subscriptions
CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger to update updated_at on projects
CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- INITIAL DATA SETUP
-- =====================================================

-- Insert default subscription plans
INSERT INTO subscription_plans (name, description, price_monthly, price_yearly, features, max_children, tier_access) VALUES
(
    'Free Plan',
    'Perfect for trying out Codopia with basic features',
    0.00,
    0.00,
    '{"lessons_per_month": 5, "projects": 1, "support": "community"}',
    1,
    ARRAY['magic_workshop']::tier_type[]
),
(
    'Family Plan',
    'Full access to all tiers and unlimited learning',
    29.99,
    299.99,
    '{"lessons_per_month": -1, "projects": -1, "support": "priority", "family_dashboard": true, "progress_reports": true}',
    4,
    ARRAY['magic_workshop', 'innovation_lab', 'professional_studio']::tier_type[]
),
(
    'Classroom Plan',
    'Designed for teachers and educational institutions',
    99.99,
    999.99,
    '{"lessons_per_month": -1, "projects": -1, "support": "dedicated", "classroom_management": true, "bulk_enrollment": true, "custom_curriculum": true}',
    30,
    ARRAY['magic_workshop', 'innovation_lab', 'professional_studio']::tier_type[]
);

-- Insert sample achievements
INSERT INTO achievements (name, description, icon_url, tier, category, points, requirements) VALUES
(
    'First Steps',
    'Complete your first lesson in the Magic Workshop',
    '/achievements/first-steps.png',
    'magic_workshop',
    'completion',
    10,
    '{"type": "lesson_completion", "count": 1}'
),
(
    'Magic Master',
    'Complete all modules in the Magic Workshop',
    '/achievements/magic-master.png',
    'magic_workshop',
    'completion',
    100,
    '{"type": "tier_completion", "tier": "magic_workshop"}'
),
(
    'Innovation Rookie',
    'Complete your first app in the Innovation Lab',
    '/achievements/innovation-rookie.png',
    'innovation_lab',
    'completion',
    50,
    '{"type": "project_completion", "project_type": "app"}'
),
(
    'Code Collaborator',
    'Work on a project with another student',
    '/achievements/collaborator.png',
    null,
    'collaboration',
    25,
    '{"type": "collaboration", "min_collaborators": 1}'
),
(
    'Creative Coder',
    'Create 5 unique projects',
    '/achievements/creative-coder.png',
    null,
    'creativity',
    75,
    '{"type": "project_creation", "count": 5}'
);

