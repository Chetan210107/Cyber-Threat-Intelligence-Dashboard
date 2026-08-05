# Module 2: User Onboarding & Profile Architecture

## Summary

This module extends the authentication foundation with a one-to-one user profile flow that starts after registration and can be skipped if a profile already exists.

## Backend Design

- `UserProfile` is a one-to-one extension of `User`.
- Profile logic is isolated into repository, service, controller, and route layers.
- All profile endpoints are protected with JWT.
- Username availability is checked separately so the UI can provide live feedback.

## Frontend Design

- Authentication routes now lead into onboarding routes.
- A Welcome screen introduces the onboarding flow.
- A Complete Profile screen collects identity, education, organization, country, bio, avatar, and theme preference.
- A Profile screen allows editing and displays the stored profile.
- A placeholder Dashboard screen completes the flow for now.

## Flow

- Register or login.
- If no profile exists, show Welcome.
- Continue to Complete Profile.
- Save profile and move to Dashboard.
- If a profile already exists, skip onboarding and move to Dashboard.
