# Cyber Threat Intelligence Dashboard (CTID)

CTID is a dark-mode cyber threat intelligence dashboard built as an enterprise-style web application for SOC and cybersecurity workflows. The project is being developed module by module with a Flask backend and a React + TypeScript frontend.

## Features Completed So Far

- Secure authentication with JWT access and refresh tokens
- Registration and login flows
- Logout and basic RBAC foundation
- Onboarding flow after registration
- User profile creation, viewing, and editing
- Username availability checking
- Dashboard shell with collapsible sidebar and top navigation
- Responsive layout with placeholder pages for future security modules

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- Tailwind CSS-ready styling approach

### Backend

- Python
- Flask
- Flask-RESTX
- SQLAlchemy
- Marshmallow
- Flask-JWT-Extended
- Flask-Migrate
- Flask-CORS

### Data and Tooling

- SQLite for local development
- Node.js and npm
- Pytest

## Project Structure

```text
CTID/
├── backend/
│   ├── controllers/
│   ├── middlewares/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── security/
│   ├── services/
│   ├── tests/
│   ├── utils/
│   └── app.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── data/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.ts
├── architecture/
├── database/
├── docs/
└── README.md
```

## Installation & Setup

### Backend

1. Open a terminal in the project root.
2. Activate the Python virtual environment.
3. Install backend dependencies.
4. Start the Flask app.

```powershell
Set-Location -Path 'C:\Users\Admin\Videos\CTID'
& .\.venv\Scripts\Activate.ps1
Set-Location -Path '.\backend'
pip install -r requirements.txt
python app.py
```

### Frontend

1. Open a second terminal.
2. Install frontend dependencies.
3. Start the Vite dev server.

```powershell
Set-Location -Path 'C:\Users\Admin\Videos\CTID\frontend'
npm install
npm run dev
```

### Local URLs

- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:5000
- Backend health check: http://127.0.0.1:5000/health

## Screenshots

Placeholder section for future project screenshots:

- Authentication screen
- Welcome / onboarding screen
- Complete profile screen
- Dashboard shell
- Profile page

## Future Roadmap

- Threat Intelligence module
- IOC Search module
- Malware Intelligence module
- MITRE ATT&CK explorer
- Reports and export workflows
- Settings and user management
- Analytics widgets and dashboard cards
- Notifications and alert handling
- Production database and deployment hardening

## License

This project is licensed under the MIT License.
