# GitHub security: from alert to reviewed fix

A small, deliberately vulnerable **learning-only** Flask application for a
5-8 minute GitHub security demonstration:

**CodeQL alert -> Copilot Autofix suggestion -> pull request -> tests -> human review.**

The catalog is synthetic, recreated in memory for each request, and made
read-only after seeding. There are no credentials, external services, customer
records, or deployment instructions.

> **Do not deploy this application or reuse its vulnerable query.**
> `GET /catalog` intentionally interpolates a request parameter into a SQLite
> SELECT. This fixture is expected to trigger CodeQL `py/sql-injection`.
> `main` retains the alert for repeatable demos; the native Autofix fix remains
> on a separate, unmerged pull request.

## Run locally (optional)

Use Python 3.12 or newer. The demonstration itself runs in GitHub; a web server
is not needed for CI or the presenter flow.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe app.py
```

The optional server binds only to `127.0.0.1:5000`, with debug and the reloader
disabled. Do not expose it through a tunnel, port forwarding, or a public host.
Stop it with Ctrl+C.

| Request | Benign result |
| --- | --- |
| `GET /` | Learning-only warning and catalog route |
| `GET /catalog` | The three synthetic catalog entries |
| `GET /catalog?category=books` | Two synthetic books |
| `GET /catalog?category=games` | One synthetic game |
| `GET /catalog?category=unknown` | An empty JSON array |

## Repository guardrails

- **CI** runs benign-behavior tests without starting a server. Passing tests
  are not evidence that the intentional vulnerability is safe.
- **CodeQL** uses advanced setup, the default Python security suite, and the
  official v4 action. The default suite includes `py/sql-injection`; no broader
  suite or intentionally outdated dependency is needed.
- Workflows use minimal job permissions and SHA-pinned actions. Dependabot
  proposes Python and GitHub Actions updates; it does not merge them.
- **Human review is required by the demo process.** Branch protection,
  required checks, secret scanning, and push protection are repository settings,
  not guarantees supplied by these files.

Do not enable CodeQL default setup alongside the advanced workflow. Never
disable scanning, dismiss the fixture alert, merge its fix, or enable auto-merge
just to make the demo look green.

See the [presenter runbook](docs/demo-runbook.md) for preparation, timing,
review criteria, and the optional synthetic custom-pattern push-protection
demonstration. Its repository-side setup is **pending** until the presenter
verifies it; custom-pattern controls have not been found in the current setup,
so omit that segment rather than promise it works. Built-in provider-pattern
push protection is a separate capability. No real token should ever be used.
