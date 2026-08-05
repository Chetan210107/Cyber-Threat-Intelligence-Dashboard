# Authentication Module

## Architecture Summary

The authentication module uses a layered Flask backend and a React-based UI shell. HTTP routes stay thin, controllers orchestrate requests, services enforce business rules, repositories isolate persistence, and schemas validate input.

## Folder Explanation

- `backend/controllers`: request orchestration
- `backend/routes`: RESTX resources and URL binding
- `backend/services`: authentication business logic
- `backend/repositories`: database access abstraction
- `backend/models`: SQLAlchemy entities
- `backend/schemas`: Marshmallow validation and response schemas
- `backend/security`: password and token helpers
- `frontend/src/pages`: auth screens
- `frontend/src/services`: API client functions
- `frontend/src/styles`: global visual system

## Database Explanation

The module normalizes identity and authorization data into users, roles, mapping tables, refresh tokens, password reset tokens, and audit logs. That structure supports RBAC, token rotation, password recovery, and traceable security events.

## API Documentation

- `POST /api/v1/auth/register`: create a user account
- `POST /api/v1/auth/login`: authenticate a user
- `POST /api/v1/auth/refresh`: rotate access and refresh tokens
- `POST /api/v1/auth/logout`: revoke the active refresh token
- `GET /api/v1/auth/me`: retrieve the authenticated identity
- `POST /api/v1/auth/password-reset/request`: request password reset instructions
- `POST /api/v1/auth/password-reset/confirm`: complete a password reset

## Security Review

- Passwords are hashed before persistence.
- Refresh tokens are stored as hashes and can be revoked.
- Token claims include role information for RBAC checks.
- Invalid request payloads return structured errors.
- Sensitive actions are logged for auditability.

## Testing Guide

- Run unit tests for helper functions and response formatting.
- Add service tests for registration, login, refresh, and logout.
- Add API tests around validation failures and privilege boundaries.

## Git Commit Message

- `feat(auth): scaffold enterprise authentication module`

## README Updates

- Document the auth module as the active implementation slice.
- Add backend and frontend setup notes once environment bootstrapping is added.
