## Change

Describe the change and link the CodeQL alert when applicable.
Identify whether GitHub's native Copilot Autofix generated the suggestion.
Do not describe a manually written fix as Autofix.

## Evidence

- [ ] Benign-behavior tests pass; include the CI run link.
- [ ] CodeQL analysis completes for this PR; include its result.
- [ ] For a security fix, add a regression test that treats input as data.
- [ ] Confirm no credentials, private data, or deployment configuration were added.

## Human review

- [ ] A human has checked the query uses bound parameters, not string escaping.
- [ ] Expected catalog behavior and read-only isolation are preserved.
- [ ] Review the entire suggestion; AI-generated changes are not automatically trusted.
- [ ] Keep the demonstration fix **unmerged** so `main` retains its fixture alert.

Do not enable auto-merge. Test success alone does not establish security.
