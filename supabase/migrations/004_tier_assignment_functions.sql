-- Tier Assignment and Parent-Child Relationship Functions
-- Migration: 004_tier_assignment_functions.sql
-- Author: Agent Aegis (Security & Integration Specialist)
-- Date: September 16, 2025

-- Function to determine tier based on age
CREATE OR REPLACE FUNCTION determine_tier(child_age INTEGER)
RETURNS tier_type
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF child_age <= 7 THEN
        RETURN 'magic_workshop';
    ELSIF child_age <= 12 THEN
        RETURN 'innovation_lab';
    ELSE
        RETURN 'professional_studio';
    END IF;
END;
$$;

-- Function to automatically set tier when child is created or age is updated
CREATE OR REPLACE FUNCTION set_child_tier()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Automatically set tier based on age
    NEW.tier := determine_tier(NEW.age);
    
    -- Update the updated_at timestamp
    NEW.updated_at := NOW();
    
    RETURN NEW;
END;
$$;

-- Trigger to automatically set tier on insert and update
DROP TRIGGER IF EXISTS trigger_set_child_tier ON children;
CREATE TRIGGER trigger_set_child_tier
    BEFORE INSERT OR UPDATE OF age ON children
    FOR EACH ROW
    EXECUTE FUNCTION set_child_tier();

-- Function to validate parent-child relationships
CREATE OR REPLACE FUNCTION validate_parent_child_relationship()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if the parent exists and has the 'parent' role
    IF NOT EXISTS (
        SELECT 1 FROM profiles 
        WHERE id = NEW.parent_id 
        AND role = 'parent'
    ) THEN
        RAISE EXCEPTION 'Invalid parent_id: Parent must exist and have parent role';
    END IF;
    
    RETURN NEW;
END;
$$;

-- Trigger to validate parent-child relationships
DROP TRIGGER IF EXISTS trigger_validate_parent_child ON children;
CREATE TRIGGER trigger_validate_parent_child
    BEFORE INSERT OR UPDATE OF parent_id ON children
    FOR EACH ROW
    EXECUTE FUNCTION validate_parent_child_relationship();

-- Function to create profile after user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    -- Create a profile for the new user
    INSERT INTO public.profiles (id, email, full_name, role, created_at, updated_at)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', ''),
        COALESCE(NEW.raw_user_meta_data->>'role', 'parent')::user_role,
        NOW(),
        NOW()
    );
    
    RETURN NEW;
END;
$$;

-- Trigger to automatically create profile when user signs up
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION handle_new_user();

-- Function to get children for a parent with tier information
CREATE OR REPLACE FUNCTION get_parent_children(parent_user_id UUID)
RETURNS TABLE (
    id UUID,
    name TEXT,
    age INTEGER,
    tier tier_type,
    tier_display_name TEXT,
    tier_description TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    last_active TIMESTAMP WITH TIME ZONE
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name,
        c.age,
        c.tier,
        CASE 
            WHEN c.tier = 'magic_workshop' THEN 'Magic Workshop'
            WHEN c.tier = 'innovation_lab' THEN 'Innovation Lab'
            WHEN c.tier = 'professional_studio' THEN 'Professional Studio'
            ELSE 'Unknown'
        END as tier_display_name,
        CASE 
            WHEN c.tier = 'magic_workshop' THEN 'Ages 5-7 • Visual block coding with magical themes'
            WHEN c.tier = 'innovation_lab' THEN 'Ages 8-12 • Advanced blocks and app building'
            WHEN c.tier = 'professional_studio' THEN 'Ages 13+ • Real programming languages and tools'
            ELSE 'Unknown tier'
        END as tier_description,
        c.avatar_url,
        c.created_at,
        c.updated_at,
        COALESCE(
            (SELECT MAX(last_accessed_at) FROM lesson_progress WHERE child_id = c.id),
            c.created_at
        ) as last_active
    FROM children c
    WHERE c.parent_id = parent_user_id
    AND c.is_active = true
    ORDER BY c.created_at ASC;
END;
$$;

-- Function to get child progress summary
CREATE OR REPLACE FUNCTION get_child_progress_summary(child_user_id UUID)
RETURNS TABLE (
    total_lessons INTEGER,
    completed_lessons INTEGER,
    total_modules INTEGER,
    completed_modules INTEGER,
    total_time_minutes INTEGER,
    achievements_count INTEGER,
    projects_count INTEGER
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE((SELECT COUNT(*) FROM lesson_progress WHERE child_id = child_user_id), 0)::INTEGER as total_lessons,
        COALESCE((SELECT COUNT(*) FROM lesson_progress WHERE child_id = child_user_id AND status = 'completed'), 0)::INTEGER as completed_lessons,
        COALESCE((SELECT COUNT(*) FROM module_progress WHERE child_id = child_user_id), 0)::INTEGER as total_modules,
        COALESCE((SELECT COUNT(*) FROM module_progress WHERE child_id = child_user_id AND status = 'completed'), 0)::INTEGER as completed_modules,
        COALESCE((SELECT SUM(time_spent_minutes) FROM lesson_progress WHERE child_id = child_user_id), 0)::INTEGER as total_time_minutes,
        COALESCE((SELECT COUNT(*) FROM user_achievements WHERE child_id = child_user_id), 0)::INTEGER as achievements_count,
        COALESCE((SELECT COUNT(*) FROM projects WHERE child_id = child_user_id), 0)::INTEGER as projects_count;
END;
$$;

-- Function to safely delete child and all related data
CREATE OR REPLACE FUNCTION delete_child_safely(child_user_id UUID, parent_user_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    child_exists BOOLEAN;
BEGIN
    -- Check if child exists and belongs to the parent
    SELECT EXISTS(
        SELECT 1 FROM children 
        WHERE id = child_user_id 
        AND parent_id = parent_user_id
    ) INTO child_exists;
    
    IF NOT child_exists THEN
        RAISE EXCEPTION 'Child not found or does not belong to this parent';
    END IF;
    
    -- Delete related data in correct order (due to foreign key constraints)
    DELETE FROM user_achievements WHERE child_id = child_user_id;
    DELETE FROM exercise_submissions WHERE child_id = child_user_id;
    DELETE FROM lesson_progress WHERE child_id = child_user_id;
    DELETE FROM module_progress WHERE child_id = child_user_id;
    DELETE FROM project_collaborators WHERE child_id = child_user_id;
    DELETE FROM projects WHERE child_id = child_user_id;
    DELETE FROM children WHERE id = child_user_id;
    
    RETURN TRUE;
END;
$$;

-- Function to update child profile with validation
CREATE OR REPLACE FUNCTION update_child_profile(
    child_user_id UUID,
    parent_user_id UUID,
    new_name TEXT DEFAULT NULL,
    new_age INTEGER DEFAULT NULL,
    new_avatar_url TEXT DEFAULT NULL
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    child_exists BOOLEAN;
    update_data RECORD;
BEGIN
    -- Check if child exists and belongs to the parent
    SELECT EXISTS(
        SELECT 1 FROM children 
        WHERE id = child_user_id 
        AND parent_id = parent_user_id
    ) INTO child_exists;
    
    IF NOT child_exists THEN
        RAISE EXCEPTION 'Child not found or does not belong to this parent';
    END IF;
    
    -- Validate age if provided
    IF new_age IS NOT NULL AND (new_age < 3 OR new_age > 18) THEN
        RAISE EXCEPTION 'Age must be between 3 and 18';
    END IF;
    
    -- Validate name if provided
    IF new_name IS NOT NULL AND LENGTH(TRIM(new_name)) = 0 THEN
        RAISE EXCEPTION 'Name cannot be empty';
    END IF;
    
    -- Update the child record
    UPDATE children 
    SET 
        name = COALESCE(TRIM(new_name), name),
        age = COALESCE(new_age, age),
        avatar_url = COALESCE(new_avatar_url, avatar_url),
        updated_at = NOW()
    WHERE id = child_user_id;
    
    RETURN TRUE;
END;
$$;

-- Function to get tier-appropriate content for a child
CREATE OR REPLACE FUNCTION get_tier_content(child_tier tier_type)
RETURNS TABLE (
    module_id UUID,
    module_name TEXT,
    module_description TEXT,
    module_order INTEGER,
    lesson_count INTEGER,
    estimated_hours INTEGER
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id as module_id,
        m.name as module_name,
        m.description as module_description,
        m.order_index as module_order,
        COALESCE((SELECT COUNT(*) FROM lessons WHERE module_id = m.id AND is_published = true), 0)::INTEGER as lesson_count,
        m.estimated_duration_hours as estimated_hours
    FROM modules m
    WHERE m.tier = child_tier
    AND m.is_published = true
    ORDER BY m.order_index ASC;
END;
$$;

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_children_parent_tier ON children(parent_id, tier);
CREATE INDEX IF NOT EXISTS idx_children_age ON children(age);
CREATE INDEX IF NOT EXISTS idx_children_active ON children(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_lesson_progress_child_status ON lesson_progress(child_id, status);
CREATE INDEX IF NOT EXISTS idx_module_progress_child_status ON module_progress(child_id, status);

-- Grant necessary permissions
GRANT EXECUTE ON FUNCTION determine_tier(INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION get_parent_children(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_child_progress_summary(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION delete_child_safely(UUID, UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION update_child_profile(UUID, UUID, TEXT, INTEGER, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_tier_content(tier_type) TO authenticated;

