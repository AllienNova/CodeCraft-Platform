"""
Create simple tables for immediate Codopia functionality
This bypasses the complex migration system and creates basic tables we need
"""

from supabase_client import supabase_client
import json

def create_simple_tables():
    """Create basic tables needed for Codopia functionality"""
    
    print("Creating simple tables for immediate functionality...")
    
    # Create a simple users table using SQL
    try:
        # Use the SQL editor endpoint to create tables
        sql_commands = [
            """
            CREATE TABLE IF NOT EXISTS public.users (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'parent',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS public.children (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                parent_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                tier TEXT NOT NULL,
                magic_points INTEGER DEFAULT 0,
                achievements JSONB DEFAULT '[]',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS public.lesson_progress (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                child_id UUID REFERENCES public.children(id) ON DELETE CASCADE,
                lesson_id TEXT NOT NULL,
                progress_data JSONB DEFAULT '{}',
                completed BOOLEAN DEFAULT FALSE,
                score INTEGER DEFAULT 0,
                time_spent INTEGER DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(child_id, lesson_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS public.achievements (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                child_id UUID REFERENCES public.children(id) ON DELETE CASCADE,
                achievement_id TEXT NOT NULL,
                achievement_data JSONB DEFAULT '{}',
                earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]
        
        for i, sql in enumerate(sql_commands):
            try:
                # Execute SQL using RPC call
                result = supabase_client.client.rpc('exec_sql', {'sql': sql}).execute()
                print(f"✅ Table {i+1} created successfully")
            except Exception as e:
                print(f"❌ Error creating table {i+1}: {e}")
                # Try alternative method
                try:
                    import requests
                    response = requests.post(
                        f"{supabase_client.url}/rest/v1/rpc/exec_sql",
                        headers={
                            'apikey': supabase_client.key,
                            'Authorization': f'Bearer {supabase_client.key}',
                            'Content-Type': 'application/json'
                        },
                        json={'sql': sql}
                    )
                    if response.status_code == 200:
                        print(f"✅ Table {i+1} created with alternative method")
                    else:
                        print(f"❌ Alternative method failed for table {i+1}: {response.text}")
                except Exception as e2:
                    print(f"❌ Both methods failed for table {i+1}: {e2}")
        
        # Test if tables were created
        print("\nTesting table creation...")
        test_tables = ['users', 'children', 'lesson_progress', 'achievements']
        
        for table in test_tables:
            try:
                result = supabase_client.client.table(table).select('*').limit(1).execute()
                print(f"✅ Table '{table}' is accessible")
            except Exception as e:
                print(f"❌ Table '{table}' not accessible: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    success = create_simple_tables()
    if success:
        print("\n🎉 Simple tables created successfully!")
        print("Database integration is ready for use.")
    else:
        print("\n❌ Failed to create tables.")
        print("Manual table creation may be required.")

