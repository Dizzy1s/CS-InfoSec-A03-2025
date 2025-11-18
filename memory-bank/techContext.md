# Tech Context

- **Backend**: Python + Flask 3 with SQLite (ctf_lab.db) and Jinja templates.
- **Frontend**: Server-rendered Bootstrap UI baked into Flask (no separate SPA
  needed for vulnerabilities). Branding now `#4CK P07470` with custom SVG logo.
- **Auth & Sessions**: Cookie-based session management; intentionally omit some
  protections (e.g., SameSite) for CSRF demo. Separate admin session stored in
  `admins` table with hashed credentials.
- **Dev Environment**: Windows host; project currently empty.
- **Tooling Needs**: Database seeding via `init_db.py` reading instructor CSV
  (roll_no, name, password, email) plus sample dataset for local use. Script
  also seeds contracts/shipments tables, default admin credentials, and the
  `student_stats` table powering the persistent scoreboard.

