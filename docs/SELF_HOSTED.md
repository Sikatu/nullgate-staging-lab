# Optional isolated self-hosted runner

For credible long-running functional and load testing, use a separate disposable **Linux VM**, not your live Minecraft server and not a machine containing production auth secrets.

1. In the private GitHub repository, open **Settings → Actions → Runners → New self-hosted runner** and follow GitHub's *current* install commands for that runner token. Do **not** paste runner registration tokens into chats or repository files.
2. Register the runner with an additional label `nullgate-lab`.
3. Limit repository access to trusted maintainers, turn off pull-request execution for jobs targeting this runner, and firewall its network so the test server does not accept Internet connections. Restart/re-image this VM between untrusted jobs.
4. Supply exact staging versions of PacketEvents, Floodgate and Geyser-Spigot under `test-assets/dependencies/`, with separately reviewed licences and provenance. For real integration testing also supply legitimate test clients and authorized accounts separately; **this package has no real Minecraft client driver**.
5. Under GitHub **Actions → Nullgate 1.21.11 Staging Lab → Run workflow**, enable `run_self_hosted`. This executes a 60-minute *idle soak* and checks all three test dependency file names. It does not assert authenticated login or TPS results.
6. Inspect reported JVM exceptions and missing dependency warnings; validate the plugin security matrix manually before any staging acceptance decision.

GitHub's documentation cautions that self-hosted runners are not automatically ephemeral or isolated like GitHub-hosted runners. Treat the host as execution of repository code and never grant it production keys or privileged production network access.
