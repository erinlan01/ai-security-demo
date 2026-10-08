# Presenter runbook: alert to human-reviewed fix

**Duration:** 5-8 minutes after preparation.
**Audience takeaway:** detection, an AI-assisted fix, automated evidence, and
human judgment are distinct steps.

This repository is intentionally vulnerable and learning-only. All catalog
records are synthetic. Do not run a public server, connect external data,
paste a real credential, or merge the demonstration fix.

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
   Secret scanning and custom-pattern push protection setup is **pending**
   until explicitly configured and tested; files in this repo do not enable it.

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
| 6:30-8:00 | Optional, preverified push protection | Demonstrate a repository custom pattern rejecting a synthetic marker before it enters GitHub, only if preparation below is complete. |

For a five-minute slot, shorten the diff walkthrough and omit the optional
push-protection segment. No application server is required.

## Optional synthetic custom-pattern demonstration

**Status: presenter-side configuration pending.** This is separate from CodeQL
and Autofix. Do not promise it works until the repository's available controls
have been checked. Do not purchase products or change organization-wide settings.

The presenter may create a repository-level secret-scanning custom pattern
named `Synthetic training marker` with secret format:

```text
DEMO_ONLY_[A-Z0-9]{24}
```

Use pattern boundaries compatible with GitHub's custom-pattern editor so
only a complete marker is matched. The marker represents **no service or
credential** and has no authentication capability. Never use a provider token,
even an expired one, and never paste any private material into the pattern editor.

1. Verify secret scanning and push protection are available and enabled for
   this public repository, and confirm that the custom pattern can itself be
   published and enabled for push protection. Run the editor's dry run first.
   If those controls are unavailable, skip this segment.
2. In an isolated disposable local checkout, create a disposable demo branch
   and a text file containing a marker built from `DEMO_ONLY_` followed by
   exactly 24 uppercase letters or digits. Do not modify `main` or the Autofix
   branch. Keep the complete marker out of shared documentation and logs.
3. Commit that synthetic-only file locally, then attempt a normal push.
   A rejected push with the custom-pattern explanation is the expected
   evidence. **Do not bypass** the warning or grant an exception.
4. If the push succeeds, do not claim protection worked. Stop, remove the
   disposable remote branch, and revisit the configuration before presenting.
5. After a blocked push, discard the isolated local demo checkout/branch.
   Confirm neither the marker nor a bypass entered `main` or the fix PR.

The repository contains the pattern description, not a complete matching
marker. This avoids pre-populating the exercise with secret-scanning alerts.

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
| Custom pattern does not block | Stop that segment; do not bypass or replace it with a real secret. |

Reuse the existing alert and unmerged PR for the next presentation. Avoid
duplicate fix PRs or closing/dismissing the original alert. Dependency updates
are ordinary reviewed maintenance, not part of the vulnerable fixture.

## References

- [CodeQL SQL injection query](https://codeql.github.com/codeql-query-help/python/py-sql-injection/)
- [Responsible use of Copilot Autofix](https://docs.github.com/en/code-security/responsible-use/security-and-quality-ai-features)
- [Advanced CodeQL setup](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning)
- [Secret-scanning custom patterns](https://docs.github.com/en/code-security/secret-scanning/using-advanced-secret-scanning-and-push-protection-features/defining-custom-patterns-for-secret-scanning)
