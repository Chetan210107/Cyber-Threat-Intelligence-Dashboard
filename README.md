# Cyber Threat Intelligence Dashboard (CTID)

CTID is a dark-mode cyber threat intelligence dashboard built as an enterprise-style web application for SOC and cybersecurity workflows. The project is being developed module by module with a Flask backend and a React + TypeScript frontend.

## Features Completed So Far

- Secure authentication with JWT access and refresh tokens
- Registration and login flows
- Logout and basic foundation
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

## External API Configuration

CTID is prepared to use external cybersecurity intelligence services for future threat-intelligence features. Credentials are loaded locally through environment variables and are not required for the current dashboard foundation. No external API requests are made by this milestone.

### NVD

**Purpose:** CVE and vulnerability intelligence for future vulnerability analysis and enrichment in CTID.

- Request an API key from the [NVD API key request page](https://nvd.nist.gov/developers/request-an-api-key).
- Add the key locally using the `NVD_API_KEY` environment variable.

### VirusTotal

**Purpose:** IP address, domain, URL, and file-hash reputation and intelligence for future indicator analysis in CTID.

- Obtain an API key from the VirusTotal account/API section. See the [VirusTotal getting started documentation](https://docs.virustotal.com/reference/getting-started).
- Add the key locally using the `VIRUSTOTAL_API_KEY` environment variable.

### AbuseIPDB

**Purpose:** IP reputation and abuse information for future network indicator analysis in CTID.

- Obtain an API key from the [AbuseIPDB API account page](https://www.abuseipdb.com/account/api).
- Add the key locally using the `ABUSEIPDB_API_KEY` environment variable.

### Local Setup

1. Copy `.env.example` to `.env`.
2. Add the actual provider keys to `.env`.
3. Keep `.env` private and store it only on your local machine.
4. Never commit `.env`; it remains protected by `.gitignore`.
5. `.env.example` is safe to commit because it contains placeholders only.

Safe local format:

```text
NVD_API_KEY=your_nvd_api_key
VIRUSTOTAL_API_KEY=your_virustotal_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_api_key
```

API keys are credentials. Never publish them on GitHub, place them in source code, include them in tests or documentation, or expose them in logs, errors, or responses. CTID reports missing credential names without displaying credential values.

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
