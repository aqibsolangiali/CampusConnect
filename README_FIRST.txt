CAMPUSCONNECT GITHUB UPGRADE

1. Open GitHub Desktop > CampusConnect > Repository > Show in Explorer.
2. Copy README.md, SECURITY.md, docs/, assets/, frontend/ and GITHUB_ABOUT.txt from this ZIP into the repository folder.
3. When Windows asks about README.md or frontend/src/main.jsx, select Replace. Do not delete your existing backend/ folder.
4. Open GitHub Desktop > Changes. Review the listed files and confirm .env and secrets are not present.
5. Commit with message: Improve CampusConnect documentation and deployed API connectivity.
6. Click Push origin.
7. Render frontend Static Site > Environment: VITE_API_URL = https://campusconnect-1-l4h2.onrender.com; then Save, rebuild and deploy.
8. Render backend Web Service > Environment: CORS_ORIGINS = https://campusconnect-web-mvbs.onrender.com and SECRET_KEY = an original long private random value. Check DATABASE_URL if persistence required.
9. GitHub repository About (gear icon): copy text from GITHUB_ABOUT.txt and set Website.
10. Test demo in browser. The backend is not changed by this package, so all existing API/security limitations remain.

WARNING: The ZIP contains documentation, an authentic screenshot, and a small frontend API connectivity fix. It does not provide a production security audit or fix authentication/session limitations.
