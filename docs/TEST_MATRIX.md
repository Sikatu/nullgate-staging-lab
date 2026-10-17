# Nullgate test coverage and release gates

| Test | GitHub-hosted CI | Isolated self-hosted runner | Actual authenticated clients |
|---|---|---|---|
| SHA256/version/build integrity | Yes | Yes | Not needed |
| Archived 3-pass JVM QA | Yes | Yes | Not needed |
| Genuine Purpur 1.21.11 startup | Yes | Yes | Not needed |
| Known Java linkage error/Nullgate event exception startup detection | Yes, during startup | Yes, during observed runtime | More event coverage required |
| PacketEvents/Geyser/Floodgate initialization | Only when separately supplied | With exact staged dependencies | Needed for end-to-end |
| Premium Mojang session proof each reconnect | NO | No, without clients | **Required** |
| Cracked Java registration/password/timeout | NO | No, without clients | **Required** |
| Bedrock verified Floodgate identity | NO | No, without clients | **Required** |
| Admin permission revocation mid-GUI query | NO | Could build dedicated test driver | **Required** |
| Anti-bot false-positive testing | NO | With correctly designed test driver | **Required** |
| 25/50/100-player real-world MSPT/TPS | NO | Only if hardware/client environment supports it | **Required** |
| DB crash/timeouts + recovery | NO | Dedicated test procedure required | **Required** |
| Full canonical source/API compile | BLOCKED: original source missing | BLOCKED | Source required |

## Results definitions

`PASS` from `smoke-report.json` = the local loopback Purpur **boot and shutdown smoke** passed. `production_certified` is always `false`. A 60-minute self-hosted run is an **idle soak** unless real test clients are added and verified; do not label it a multiplayer stress test.

## Security and approval

Keep Nullgate's offline-mode test server bound to localhost. Do not expose public authentication traffic, generate excessive third-party requests, or automate real user credentials. Do not auto-migrate UUIDs or overwrite player records. Require owner approval before connecting a production data source or network.
