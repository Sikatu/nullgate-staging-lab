# Nullgate — Private GitHub Staging Lab

**Goal:** Run reproducible **Nullgate alpha.4.21** tests on GitHub Actions using **Eclipse Temurin Java 25**, exactly **Purpur 1.21.11 build 2568**, and the actual plugin JAR. This repository template is an engineering lab, **not a release certification**.

## Setup (private repository)

1. Create a **new private GitHub repository** via https://github.com/new (suggested name `nullgate-staging-lab`). Never use a production authentication database or server account keys here.
2. Upload the **contents** of this extracted archive to the repository root, including `.github/workflows/nullgate-staging.yml`, `scripts`, `tests`, and `test-assets`. Git CLI will preserve the hidden `.github` directory. Keep the repo private because `test-assets` contains an unreleased plugin JAR.
3. Under repository **Actions**, allow the GitHub Actions workflow to run. The workflow is triggered on a push to `main` and supports manual `workflow_dispatch` runs.
4. Initially, the workflow performs a three-pass reproducible offline QA build followed by a **disposable real Purpur startup test**. The server binds to `127.0.0.1`, uses offline-mode only inside the sandbox, and has no external Minecraft client traffic.
5. To evaluate the full plugin dependency stack, add **the appropriate test-compatible PacketEvents, Geyser-Spigot, and Floodgate JARs** under `test-assets/dependencies/`. Test versions should match production compatibility expectations. These files are not bundled in this lab; obtain them from their official distribution sources.
6. Download workflow artifact logs/reports from each run. Self-hosted raw logs stay on the isolated runner by default and are not uploaded automatically. A PASS for startup is **not** proof of Premium verification, Bedrock login, authentication security, or Minecraft TPS under clients.

## What is included

- `.github/workflows/nullgate-staging.yml`: hosted reproducible JVM QA, real Purpur boot, and optional isolated self-hosted soak.
- `test-assets/Nullgate.jar`: **exact alpha.4.21 JAR**, pinned SHA-256 in `Nullgate.sha256`.
- `test-assets/alpha421-source-and-qa.zip`: previously prepared binary patch source and three-pass offline QA; **not full canonical Java source**.
- `scripts/verify_release.py`: fail-closed SHA/version and manifest integrity checks.
- `scripts/smoke.py`: launches and stops a disposable loopback Purpur process; fails on crash, missing server readiness, missing Nullgate startup evidence, ABI linkage exceptions, or Nullgate event exceptions. Prints JSON test limits. Records log artifacts.
- `tests/test_smoke.py`: positive and negative parser/unit tests.
- `docs/TEST_MATRIX.md`: strict definition of what is and is not certified.
- `docs/SELF_HOSTED.md`: how to add a **separate isolated runner** for longer tests.

## Expected initial limitations

**Only the Nullgate JAR and its offline QA files are bundled**, not Purpur, PacketEvents, Geyser, or Floodgate. Purpur is fetched from its **official pinned download URL**. Absent optional dependencies can cause features to be disabled; the boot smoke reports those dependencies as missing, rather than pretending they were tested. The manual self-hosted soak uses `--strict-dependencies` and refuses a PASS if they are not present.

Runtime startup depends on Purpur download availability, JDK installation, and library repositories for Password4j and SQLite. Network failures are **test environment failures**, not evidence that authentication passed. The smoke script does not inject Java or Bedrock clients, load fake password accounts, verify Mojang proofs, inspect TPS/MSPT, or validate disk recovery.

## Security rules

- GitHub Actions workflows are infrastructure-as-code; review proposed changes before running them with secrets or on self-hosted machines.
- Run only in a **private repo** with restricted write access, no untrusted pull-request execution on self-hosted runners, and no production network reachability. A self-hosted runner is **not isolated by GitHub**; use an ephemeral VM.
- Never commit `plugins/Nullgate/` with real databases, encryption keys, IP history, Premium account binding information, or Microsoft/Mojang credentials.
- Do **not** port-forward the offline-mode test server. Do **not** use bots to circumvent Mojang authentication. Real identity tests require legitimate test accounts and an operator-controlled environment.
- Keep separate approvals for staging and production. This lab does **not** approve Nullgate for production.

## Release gate

Certification requires canonical source rebuild, full Purpur/API dependencies, real Premium Java proofs, cracked Java and Bedrock sign-in flows, permission/GUI tests, UUID continuity, auth database recovery, legitimate multiplayer load, anti-bot false-positive measurements, and restart/rollback drills. See `docs/TEST_MATRIX.md`.
