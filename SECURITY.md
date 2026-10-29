# CampusConnect — Security Policy

## Scope

CampusConnect is an independent student-built **portfolio/demo application**, not an official university service. Do **not** use real educational credentials or passwords you use elsewhere.

## Reporting a vulnerability

Please report suspected security issues **privately** to the repository owner through GitHub's **Security** tab (if private vulnerability reporting is enabled) or through the owner's listed profile contact method. Do not post unpatched exploit details in public issues.

## Current protections verified in the supplied code snapshot

- Password hashes generated with Argon2 through `pwdlib`.
- JWT bearer authentication with expiration and server-side validation on private endpoints.
- Personalized enrollments and bookmarks filtered by authenticated user ID.
- Duplicate enrollment and bookmark prevention through composite unique constraints.
- Pydantic validation of registration and API responses.

## Known limitations — must resolve before production use

- `backend/app/auth.py` has a fallback development `SECRET_KEY`. **Deploy with a unique, strong `SECRET_KEY` environment variable; never expose or commit the secret.** Rotate tokens/secrets if a known default was ever used.
- Browser JWTs currently persist in `localStorage`; production sessions should be hardened (e.g. HttpOnly secure cookies with CSRF controls).
- There is no login/signup rate limiting, email verification, abuse monitoring, or audit trail.
- The seeded database is demo data. Do not treat registration/enrollments as real college services.
- SQLite on an ephemeral host does not provide reliable persistence of real user state.
- `CORS_ORIGINS` only controls browser CORS policy; it is **not** an access-control mechanism.
- Deployment needs HTTPS, a durable database, migrations, logging, backups, and regular dependency security review.

## Handling personal data

Use fictional names and test email addresses where possible. Do not store sensitive student records in this demo. A future production version requires a defined retention policy, deletion workflow, and data access controls.
