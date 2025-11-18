# Active Context

- Task: Build a vulnerable training web app demonstrating SQLi, XSS, and CSRF.
- Requirements gathered from user conversation (Nov 18, 2025).
- Current implementation:
  1. Flask 3 + SQLite backend with Jinja UI (landing, dashboard, labs, flags) branded as `#4CK P07470` with potato logo.
  2. `init_db.py` updates existing DBs in place and only wipes them with
     `--reset`; seeds students via CSV plus default flags/leaderboard/contracts/
     shipments, admin creds, and `student_stats`.
  3. Multiple SQLi labs (leaderboard, contracts, blind vault console) plus XSS/CSRF labs operational with guidance and hidden flag hints.
  4. Flag submission workflow awards decaying scores per flag and updates persistent `student_stats` totals for scoreboard/history.
  5. Admin console (`/admin`) reports stats, scoreboard, latest captures, allows DB download, and includes a reset button to wipe progress.
  6. `instructions.md` documents exploit payloads/commands for instructors.
  7. Landing/login now feature hacker-themed graphics & dark background motif.
- Remaining ideas: optional instructor dashboard, extra challenges, deployment
  automation for preferred hosting provider.

