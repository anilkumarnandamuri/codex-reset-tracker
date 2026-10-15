# PLAN — codex-reset-tracker

## Goal
Small static site (GitHub Pages) showing time since the last global Codex usage-limit reset, the reset history, and a pace helper. Unofficial.

## Non-goals
- Claiming affiliation with OpenAI

## Milestones
- [x] **CRT-0** Existing work as of 2026-10-15 13:41 PT: Initial deploy (2026-10-13); Day 10 reset added; short reset confirmations recognized (456889b, 2026-10-14) — done (history) 456889b
- [ ] **CRT-1** Add a minimal Playwright smoke test (page renders, timer ticks, history list) with screenshots in artifacts/CRT-1/.

## Definition of done
Tests pass (Unknown (no test suite found).); for web UI a Playwright test passes with screenshots in `artifacts/<task-id>/`; HANDOFF.md rewritten; DECISIONS.md appended for real choices; reviewed; committed on `job/<task-id>`; never pushed.
