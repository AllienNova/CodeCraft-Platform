


_**Codopia Platform: Database Migration Plan**_

**Project Codename:** Phoenix

**Author:** Agent Aegis (Security & Integration Specialist)

**Date:** September 16, 2025

**Version:** 1.0

---

## 1. Introduction

This document provides a detailed plan for migrating the Codopia platform's database from the existing Flask/SQLite environment to a robust and scalable PostgreSQL database managed by Supabase. This migration is a cornerstone of the platform's evolution, enabling enhanced performance, security, and the ability to leverage Supabase's powerful features, including real-time capabilities and Row Level Security.

The primary focus of this plan is to ensure a seamless and lossless transition of all user data, including parent and child accounts, project data, and learning progress. The migration will be executed with a zero-downtime strategy to maintain a consistent and uninterrupted user experience.

## 2. Migration Goals & Objectives

*   **Data Integrity:** Ensure 100% data integrity and consistency between the source and target databases. No data loss is acceptable.
*   **Zero Downtime:** The migration process will be designed to be transparent to users, with no service interruptions.
*   **Preservation of Relationships:** All data relationships, particularly the parent-child account structure, will be accurately preserved.
*   **Scalability and Performance:** The new PostgreSQL database will be optimized for scalability and performance to support Codopia's growth.
*   **Enable New Features:** The migration will enable the use of advanced Supabase features, such as real-time updates, which will be leveraged to enhance the user experience.




## 3. Detailed Migration Plan

### 3.1. Pre-Migration Checklist

- [ ] **Backup:** Perform a full backup of the existing Flask/SQLite database.
- [ ] **Schema Freeze:** Implement a schema freeze on the source database to prevent any structural changes during the migration process.
- [ ] **Environment Setup:** Set up the Supabase project, including the PostgreSQL database and all necessary extensions.
- [ ] **Migration Scripts:** Develop and test the data migration scripts in a staging environment.
- [ ] **Validation Scripts:** Develop and test scripts to validate the migrated data.

### 3.2. Schema Mapping

The following table details the mapping from the Flask/SQLAlchemy models to the new Supabase/PostgreSQL tables:

| Flask Model      | Supabase Table        | Key Fields & Transformations                                                                                                                                                               |
| ---------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `User`           | `auth.users`, `profiles` | `id` (Integer) -> `id` (UUID), `password_hash` (bcrypt) -> `encrypted_password`, `role` -> `role` (enum). A `profiles` table record will be created for each `auth.users` record.          |
| `ChildProfile`   | `children`            | `id` (Integer) -> `id` (UUID), `parent_id` (Integer) -> `parent_id` (UUID), `tier` -> `tier` (enum). The `parent_id` will be updated to reference the new UUID of the parent in the `profiles` table. |
| `Project`        | `projects`            | `id` (Integer) -> `id` (UUID), `child_id` (Integer) -> `child_id` (UUID).                                                                                                                  |
| `Progress`       | `lesson_progress`     | `id` (Integer) -> `id` (UUID), `child_id` (Integer) -> `child_id` (UUID).                                                                                                                  |
| `Achievement`    | `user_achievements`   | `id` (Integer) -> `id` (UUID), `child_id` (Integer) -> `child_id` (UUID).                                                                                                                  |

### 3.3. Data Migration Scripts

The migration will be performed using a set of Python scripts that connect to both the source and target databases.

**1. User Migration Script:**

```python
import bcrypt
from supabase import create_client, Client

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Fetch users from Flask DB
flask_users = fetch_all_users_from_flask()

for user in flask_users:
    # Create user in Supabase Auth
    created_user = supabase.auth.admin.create_user(
        email=user['email'],
        password=user['password_hash'], # Supabase handles bcrypt hashes
        email_confirm=True,
        user_metadata={'role': user['role']}
    )

    # Create corresponding profile
    supabase.table('profiles').insert({
        'id': created_user.id,
        'email': user['email'],
        'role': user['role'],
        'created_at': user['created_at']
    }).execute()
```

**2. Child Profile Migration Script:**

```python
# Fetch child profiles from Flask DB
flask_children = fetch_all_child_profiles_from_flask()

for child in flask_children:
    # Get parent's new Supabase UUID
    parent_profile = supabase.table('profiles').select('id').eq('email', child['parent_email']).single().execute()
    parent_id = parent_profile.data['id']

    # Insert child profile into Supabase
    supabase.table('children').insert({
        'parent_id': parent_id,
        'name': child['name'],
        'age': child['age'],
        'tier': determine_tier(child['age'])
    }).execute()
```

### 3.4. Data Validation Strategy

Post-migration, a thorough validation process will be executed to ensure data integrity.

*   **Row Counts:** Compare the row counts of each migrated table between the source and target databases.
*   **Data Consistency:** Perform random sampling of records from both databases and compare the data to ensure consistency.
*   **Relationship Integrity:** Write queries to verify that all foreign key relationships have been correctly preserved.
*   **Authentication Testing:** Test user logins with a sample of migrated accounts to ensure that the password migration was successful.

## 4. Rollback Plan

In the event of a critical failure during the migration, the following rollback plan will be executed:

1.  **Halt Migration:** Immediately stop all migration scripts.
2.  **Restore Backup:** Restore the Supabase database to the pre-migration backup.
3.  **Re-point DNS:** If the DNS has already been switched, re-point it to the legacy Flask application.
4.  **Analyze Failure:** Perform a root cause analysis of the failure and revise the migration plan accordingly.


