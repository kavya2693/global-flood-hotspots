# Checklist

- [x] Idea, target role and distinct skill recorded
- [x] 8+ comparable repos surveyed
- [x] Gate 1 closed
- [x] ADR-0001 written
- [x] Data contract defined
- [x] Dataset reproducible from one command
- [x] Core module implemented
- [x] Tests pass locally, output captured
- [ ] Lint and format clean — ruff not installed locally; CI runs it
- [x] One-command end-to-end run verified on this machine
- [x] Gate 2 closed
- [ ] Dockerfile builds and runs — UNVERIFIED. The Dockerfile is written and CI
      runs the same steps natively, but no Docker daemon was available on this
      machine, so the image has not actually been built. Not assumed to work.
- [ ] CI workflow green on GitHub
- [x] .env.example present, no real values
- [x] prepush-scan.sh passes
- [x] 10+ incremental commits
- [x] Public repo created, pushed, remote HEAD == local HEAD
- [x] Root README index updated

Distinct skill claimed: provenance-enforced dataset construction, where the
validator that rejects unsourced figures is written and tested before the data
it governs exists.
