# user_profiles Table

## Purpose

Stores the analyst identity and onboarding data associated with one authenticated user.

## Fields

- `id`
- `user_id` foreign key to `users.id`
- `full_name`
- `username`
- `college`
- `course`
- `organization` optional
- `country`
- `bio`
- `avatar`
- `preferred_theme`
- `created_at`
- `updated_at`

## Relationships

- One user has one profile.
- One profile belongs to one user.

## Constraints

- `user_id` is unique.
- `username` is unique.
- JWT is required for all profile APIs.
