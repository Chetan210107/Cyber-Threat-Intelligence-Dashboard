# Authentication Data Design

## Tables

### users

Stores platform identities.

Important fields:

- `id`
- `email`
- `password_hash`
- `full_name`
- `is_active`
- `mfa_enabled`
- `last_login_at`
- `created_at`
- `updated_at`

Indexes:

- Unique index on `email`
- Index on `is_active`

### roles

Defines RBAC roles.

Important fields:

- `id`
- `name`
- `description`
- `is_system`

Indexes:

- Unique index on `name`

### user_roles

Associates users and roles with a normalized many-to-many relationship.

### refresh_tokens

Tracks session refresh tokens so they can be revoked or rotated.

Important fields:

- `id`
- `user_id`
- `jti`
- `token_hash`
- `expires_at`
- `revoked_at`
- `last_used_at`
- `created_at`

Indexes:

- Unique index on `jti`
- Index on `user_id`
- Index on `expires_at`

### password_reset_tokens

Stores one-time recovery tokens.

### audit_logs

Immutable event log for authentication and authorization actions.

## Relationships

- A user can have many roles.
- A role can be assigned to many users.
- A user can have many refresh tokens over time.
- A user can have many password reset tokens over time.
- Audit events may optionally reference the acting user.
