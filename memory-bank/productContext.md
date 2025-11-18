# Product Context

## Problem
Students need a controlled environment to learn how classic web
vulnerabilities work end-to-end, including how to identify them and how to
craft exploits that retrieve sensitive data (flags).

## Solution
- Web application with authentication based on student roll numbers.
- Each vulnerability is exposed through a dedicated feature:
  - SQL injection on a leaderboard/search view.
  - Stored XSS in a feedback/discussion board.
  - CSRF on a settings or flag submission workflow.
- Each challenge yields a unique flag stored in the SQL database.

## Experience Goals
- Simple landing page explaining the challenge outline.
- Dashboard after login showing available vuln modules and flag status.
- Clear success messaging and optional hints/documentation per challenge.

## Users
- Primary: Students in a security/infosec course practicing offensive skills.
- Secondary: Instructors monitoring progress and verifying flag captures.

