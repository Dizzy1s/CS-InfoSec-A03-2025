# System Patterns

- **Architecture**: Flask monolith with Jinja templates + SQLite (ctf_lab.db).
- **Auth**: Username = student roll number, password seeded per student or
  default, stored in SQL (hashed for baseline safety even though app is
  intentionally vulnerable elsewhere).
- **Flag Storage**: Each challenge contains a flag string in the database and
  per-user completion mapping.
- **Vulnerability Modules**:
  - SQLi: Leaderboard search, executive contracts lookup (stacked/UNION), and
    blind vault console endpoints all concatenate input directly into SQL.
  - XSS: Stored payload rendered unescaped in a discussion list.
  - CSRF: Sensitive action (e.g., change flag ownership) lacks CSRF token and
    accepts cross-origin POST.
- **Gamification & Scoring**: Submissions now store dynamic points (higher for
  earlier captures); dashboard + admin views pull from `student_stats`, which
  tracks cumulative points/captures per student. Admin console surfaces totals
  and lets instructors download `ctf_lab.db`.
- **Admin Access**: `/admin/login` authenticates against the `admins` table;
  panel lists captures and offers DB download.

