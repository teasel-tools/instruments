# Governance

## Merge policy

A PR is merged when:

1. CI passes (TOML valid, package exists, URLs resolve)
2. A maintainer has done a quick sanity check: no spam, plausible instrument, no obvious errors in the setup steps

CI is the gate. Human review is a lightweight check, not a quality audit.

## What maintainers don't do

- Pick winners between competing implementations. All packages for an instrument are listed.
- Verify that listed packages work correctly (I don't have own every hardware to check this)
- Block PRs for style preferences if CI passes

## Staleness

If a package disappears from its registry (PyPI, npm, Cargo), CI will flag it on the next PR that touches that file. A maintainer will then remove or update the entry.

## Becoming a maintainer

Open an issue. Active contributors with a track record of good PRs will be added.
