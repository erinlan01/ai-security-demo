# Presenter runbook: alert to human-reviewed fix

**Duration:** 5-8 minutes after preparation.
**Audience takeaway:** detection, an AI-assisted fix, automated evidence, and
human judgment are distinct steps.

This repository is intentionally vulnerable and learning-only. All catalog
records are synthetic. Do not run a public server, connect external data,
paste a real credential, or merge the demonstration fix.

## Verified preparation snapshot

Verified on **2026-10-08 (UTC)**. Recheck these settings before presenting;
this is a recorded rehearsal, not a guarantee that settings cannot change.

| Control / evidence | Verified result |
| --- | --- |
| Dependency graph | On |
| Dependabot alerts | On |
| Dependabot security updates | Enabled, not paused |
| Secret Protection | Enabled; the settings UI reported no additional licenses consumed |
| Repository push protection | Enabled; an actual training-token push was rejected |
| Copilot Autofix | On; native generation requested for alert 1, result and PR pending |
| CodeQL | Advanced workflow succeeded; default setup not configured |
| CodeQL finding | [Alert 1: `py/sql-injection`](https://github.com/erinlan01/ai-security-demo/security/code-scanning/1), open on `main` |
| Implementation checks | [CI succeeded](https://github.com/erinlan01/ai-security-demo/actions/runs/37802970287); [CodeQL succeeded](https://github.com/erinlan01/ai-security-demo/actions/runs/37802970256) |

No custom pattern is needed for the verified push-protection rehearsal.
Custom-pattern controls were not found in the current UI; do not claim that
capability or purchase products to enable it. Required checks and branch
protection are not established by this snapshot.

## Prepare before presenting

1. Open the repository's **Actions** and **Security** tabs. Verify the `CI` and
   advanced `CodeQL` workflows completed on the current `main` commit.
   CodeQL default setup must remain disabled. Successful analysis and an open
   security alert can coexist: the workflow reports analysis completion, not
   a clean security bill of health.
2. Under **Security > Code scanning**, find **SQL query built from
   user-controlled sources**, rule `py/sql-injection`, in `app.py`. Confirm
   it is open on `main`, not dismissed. The default Python CodeQL suite includes
   this rule, which is supported by Copilot Autofix. Actual fix generation
   still depends on GitHub availability and the specific alert.
3. Use GitHub's native **Generate fix** / Copilot Autofix action on that alert.
   Wait for the suggestion before the live session; analysis and generation
   are asynchronous and may take longer than the presentation.
4. Follow GitHub's native flow to put the suggestion on a separate branch and
   pull request. Fill out **Change / Evidence / Human review**. Keep the PR
   open and unmerged, leave auto-merge off, and record the alert, PR, CI run,
   and CodeQL run URLs in presenter notes. Do not check human-review boxes
   until someone actually reviews the change.
5. Review and, if necessary, add a regression test **on the fix branch**:
   an ordinary category containing an apostrophe must be treated as a literal
   value and return an empty array without a server error. Keep the benign
   tests passing. Do not add a test on `main` that locks in vulnerable behavior.
6. The coordinating presenter owns repository settings. Verify required checks
   and human-review controls separately if you plan to claim enforcement.
   Recheck repository secret scanning and push protection, and rehearse the
   official inactive training-token exercise below in isolation. Files in this
   repo do not enable these settings.

Do not substitute a manually authored fix for a native Autofix suggestion.
If no suggestion is available, show the real alert and explain that generation
is pending rather than implying the workflow has completed.

## Live flow

| Time | Show | Say / verify |
| --- | --- | --- |
| 0:00-0:45 | README and tiny catalog | "This is synthetic, in-memory, read-only data. The query is intentionally unsafe; this is not a deployment template." |
| 0:45-2:00 | Open CodeQL alert on `main` | Follow the path from Flask `request.args` to the interpolated query and SQLite `execute`. Explain that read-only storage limits damage but does not prevent SQL injection or unintended reads. |
| 2:00-3:15 | Native Copilot Autofix suggestion | Show the explanation and proposed diff. "The tool proposes; a person evaluates." Confirm provenance from the alert rather than claiming any handwritten change is Autofix. |
| 3:15-4:30 | Separate, unmerged fix PR | Show Change / Evidence / Human review. Inspect parameter binding and preservation of the catalog response. Do not accept simplistic quote removal as a security fix. |
| 4:30-5:30 | PR CI and CodeQL results | Show benign tests and the fix-branch regression test. Confirm the target alert is addressed in PR analysis, while it remains open on `main` because the PR is unmerged. |
| 5:30-6:30 | Human review | Ask the reviewer to check the whole diff, behavior, and evidence. Passing tests are not a security guarantee. End the core demo without merging. |
| 6:30-8:00 | Optional, preverified push protection | Show the rejection of GitHub Skills' inactive training token before it enters GitHub. Explain why preventing a push differs from detecting a committed secret. |

For a five-minute slot, shorten the diff walkthrough and omit the optional
push-protection segment. No application server is required.

## Optional verified push-protection demonstration

Use only the **inactive training token** supplied by
[GitHub Skills: Enable push protection](https://github.com/skills/introduction-to-secret-scanning/blob/main/.github/steps/3-enable-push-protection.md).
The presenter verified that official source before the rehearsal. Open the
source again before repeating the exercise and confirm it still identifies
the token as inactive training material. If it has changed or cannot be
verified, skip the segment. Do not invent a token-shaped substitute or use
your own token, even an expired one. The full training token is intentionally
not reproduced here.

### Recorded rejection

The isolated local rehearsal commit
`80ebb70d8a65b96d05cf17062d3973ac20245a34` was pushed toward
`HEAD:refs/heads/demo/push-protection-rehearsal`. GitHub rejected the push with
exit code `1`, `GH013`, and `GITHUB PUSH PROTECTION`, identifying a
**GitHub Personal Access Token** in `push-protection-training.txt:3`.

No bypass was used, no secret-bearing remote branch was created, and no real
credential was involved. The local commit is evidence of an attempted push,
not a commit available on GitHub. Keep any displayed rejection output free
of the full training token and any bypass URL.

### Repeat safely

1. Verify repository push protection is still enabled. Use an isolated,
   disposable clone with no unrelated work, starting from clean `main`.
   Create a disposable local branch; do not use `main` or the Autofix branch.
2. Copy only the official inactive training token into a local
   `push-protection-training.txt` fixture and commit it locally. Do not place
   it in this repository's maintained documentation, application, or PR.
3. Attempt a normal push to `demo/push-protection-rehearsal`. Show the actual
   rejection and provider detection. **Do not bypass**, grant an exception,
   or follow a bypass link. No custom pattern is required.
4. If the push succeeds, stop and do not claim protection worked. Remove the
   disposable remote branch and investigate settings and the training source
   before presenting again. Do not replace the fixture with a real credential.
5. After rejection, remove the training token from **every unpushed commit**
   before any retry. Deleting the file in a new commit is insufficient: its
   earlier content remains in the history GitHub scans. For this disposable
   exercise, discard the isolated clone and start a fresh clone from clean
   remote `main`; do not discard a checkout containing unrelated work.
6. Confirm the rejected remote branch does not exist, no bypass was granted,
   and neither `main` nor the Autofix PR contains the fixture.

**An empty secret-scanning alerts page is compatible with a successful
rejection.** The leak was prevented before the commit reached the repository.
Do not present this as detection or remediation of a historical committed
secret. A real historical leak requires a separate response, including
revoking/rotating the credential and cleaning affected history; this exercise
does not create or demonstrate such a leak.

## Troubleshooting and repeatability

| Symptom | Next step |
| --- | --- |
| No CodeQL run | Check Actions permissions and the advanced workflow; manually run `CodeQL` on `main` if necessary. |
| Default setup conflicts with advanced setup | Disable default setup before rerunning the committed advanced workflow. |
| Analysis completes but no target alert | Confirm the analyzed commit contains the interpolated query, inspect CodeQL logs and alert filters, and verify the Python analysis category. Do not fabricate an alert. |
| Autofix unavailable or still generating | Verify the alert's support and repository availability; wait or show the pending state. Do not label a manual patch Autofix. |
| Fix PR CI fails | Inspect and correct the suggestion on its branch, preserving its provenance. Rerun the checks before claiming success. |
| Alert still open on `main` | Expected: the fixed PR is deliberately unmerged. Show the PR's analysis separately. |
| Branch protections are absent | Describe human review as the demo process, not an enforced repository guarantee. |
| Training-token push does not block | Stop that segment; verify settings and the official training source. Never bypass or replace it with a real secret. |
| Secret-scanning alerts remain empty after rejection | Expected for a prevented leak; show push-rejection evidence rather than claiming a historical alert exists. |
| Retry remains blocked after deleting the file | The token is still in an earlier unpushed commit. Remove it from all unpushed history, or discard only the isolated disposable clone and start clean. |

Reuse the existing alert and unmerged PR for the next presentation. Avoid
duplicate fix PRs or closing/dismissing the original alert. Dependency updates
are ordinary reviewed maintenance, not part of the vulnerable fixture.

## References

- [CodeQL SQL injection query](https://codeql.github.com/codeql-query-help/python/py-sql-injection/)
- [Responsible use of Copilot Autofix](https://docs.github.com/en/code-security/responsible-use/security-and-quality-ai-features)
- [Advanced CodeQL setup](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning)
- [GitHub Skills inactive training-token exercise](https://github.com/skills/introduction-to-secret-scanning/blob/main/.github/steps/3-enable-push-protection.md)
