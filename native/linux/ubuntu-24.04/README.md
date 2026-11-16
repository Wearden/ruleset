# Ubuntu 24.04 native catalog

`catalog.json` is the authoritative full native Linux catalog:

- Benchmark: `ubuntu-24.04-native`
- Ruleset version: `native-linux-4`
- Envelope version: `1`
- 88 controls preserving all IDs and severities from `ruleset/linux/ubuntu-24.04`
- SHA-256: `9ab1d9cdcbc84b1f5e8b6a7ea4a290e17fa19a945b90e520b3c536928b938155`

The exact file is embedded from `agent-linux/internal/config/catalog.json`. Core may assign a subset with the same benchmark/version, but each definition must match the agent's embedded allowlist exactly. The digest in core configuration covers the exact assigned response bytes, including subset serialization.

`filesystem.json` remains the original 10-control filesystem baseline with benchmark `ubuntu-24.04-native-filesystem`, version `1`. It is backward compatible and is not the full catalog.

The full catalog has 87 entries connected to native evaluators and one explicit unsupported entry. Evaluators intentionally return error when evidence is unavailable or interpretation is outside their reviewed subset. File policy findings are configuration observations, not daemon reload or effective runtime attestations. Package installation does not imply activation. Service mask observations implement a conservative subset of legacy enablement audits and do not attest that an already running service stopped. Version 3 connects five UFW controls to bounded, read-only nftables observations; it does not add mutation permissions.

| Kind | Entries |
| --- | ---: |
| kernel_module | 7 |
| mount_options | 3 |
| package_installed | 7 |
| apt_https | 1 |
| apt_authentication | 1 |
| service_disabled | 12 |
| sysctl | 12 |
| journald_config | 2 |
| sudo_logfile | 1 |
| file_metadata | 9 |
| sshd_config | 14 |
| policy_config | 8 |
| pam_history | 1 |
| uid_zero | 1 |
| filesystem_metadata | 3 |
| ufw_runtime | 5 |
| unsupported | 1 |

The explicit manual control is `LNX-USR-006`. UFW configuration files alone cannot establish loaded netfilter state. The legacy USR-006 audit reads shadow contents, which this agent deliberately does not open. The runtime emits an explicit error finding for every selected unsupported control, preserving coverage and preventing unsupported checks from inflating scores.

## Reviewed read-only policy providers

`LNX-PKG-005` parses the ordered apt configuration parts and main configuration, including scoped keys, comments, quoted values and anonymous lists. Explicit authentication, weak/insecure-repository and source trust bypasses fail. Includes, clears, malformed or ambiguous syntax and resource limits return error. Configuration/source input is bounded to 128 files per group and 8 MiB combined. The finding describes reviewed configuration files, not cryptographic package verification, command-line options, alternate environment-selected configuration or a running apt invocation. Authentication files and keyrings are not opened.

`LNX-LOG-006` resolves literal sudoers includes restricted to `/etc/sudoers.d`, preserves ordering and checks the global logfile setting against `/var/log/sudo.log`. Scoped logfile overrides, dynamic include/path syntax, recursion, continuations and ambiguous syntax return error. Limits are 128 included files and 8 MiB. No log file is opened, and the result is a global file-policy observation rather than validation of all sudoers grammar or external NSS policy.

`LNX-PAM-007` requires an explicit required/requisite pam_pwhistory module with remember at least five before password-writing modules. History and password-writing modules must bind to the shared candidate with use_authtok. Reviewed standard modules and the ordinary post-history pam_unix jump are accepted; unreviewed modules, include stacks, alternate configuration/storage, bypass/reset control syntax or implicit history length return error. The public pwhistory.conf policy is checked for unsupported storage overrides without opening its history database. The observation is confined to common-password configuration. Password history/hash databases are never opened; other PAM service entry points, root exemptions and installed module integrity are outside this file-policy observation.

## Bounded filesystem metadata providers

`LNX-USR-007..009` implement the legacy `find / -xdev` audit scope: the root filesystem device and mountpoint metadata, with no descent into other devices. They are not a claim about every local filesystem. `/proc`, `/sys` and `/dev` are never descended. If an excluded special directory shares the root device, the audit cannot pass because coverage is incomplete. Symlinks are inspected as metadata and are not deliberately followed. Bind mounts sharing the root device are subject to the same resource bounds.

Traversal reads directory entries and lstat/stat metadata, never regular file contents. Findings contain counts and coverage errors, without paths, names or file contents. Maximums are 100,000 entries, directory depth 64 and a cooperative five-second traversal budget per control; directory reads occur in batches of 128. Inaccessible/changing entries, unavailable native metadata and exceeded bounds produce error unless an observed violation already disproves the policy, in which case the finding is fail. Kernel-blocked filesystem I/O cannot be preempted by this cooperative budget. No atomic filesystem snapshot is claimed.

USR-009 additionally reads only the public numeric identity metadata in passwd/group and the lookup source policy in nsswitch.conf. It requires explicit files-only passwd and group sources. External, compatibility, systemd/dynamic or conditional NSS sources return error because the agent cannot faithfully classify their owners. Shadow, gshadow, opasswd, hash/history stores, SSH keys and protected file contents are not read. A host using dynamic NSS therefore needs manual ownership review even though the provider is implemented.

No shell or legacy YAML command executes. No tests or native scans were run, at the user's request. Compiler checks do not validate kernel/runtime behavior. The native evaluators and policy semantics require subsequent authorized Linux lab validation.

## Read-only UFW runtime provider

FW002..006 inspect the current network namespace through nftables v0.3.0. The agent only lists tables/chains/rules and sends GETGEN/GETRULE queries. It never flushes, adds, deletes or applies firewall state. A single socket has an eight-second deadline; snapshots require an unchanged generation, at most 32 tables/512 chains/8192 rules and 128 expressions per rule. Raw expression names/counts are checked because the upstream decoder can omit unknown expressions.

The reviewed backend is nft-backed UFW with canonical IPv4/IPv6 filter hooks at priority zero. Extra hooked chains, dormant/owned filter tables, legacy iptables tables, unavailable privileges, unsupported encodings and changing snapshots yield error. IPv6 must be covered by UFW or explicitly disabled on all existing interfaces and all/default configuration. The observation applies to the agent's network namespace, not other namespaces.

FW002/003 compare live default policies and persistent defaults. They do not claim that exception rules deny all traffic. FW004 symbolically follows a new non-loopback TCP SYN to port22, requiring a reachable UFW user ACCEPT; no packet is transmitted. FW005 proves before/user chain reachability for the reviewed TCP65535 path. FW006 requires configured logging and a reachable reviewed kernel logger on that input path. Log sampling/storage delivery is not attested.

The interpreter accepts bounded jumps/returns, protocol/port/TCP-flag comparisons, non-loopback predicates, NEW conntrack state, selected TCP/comment/conntrack/address-type matches, counters and native kernel log expressions. A native packet-rate limit is modeled only within a log-only rule. Unknown address/interface predicates, xtables LOG/limit/reject extensions, sets, dynamic expressions, routing/NAT interactions and unreviewed bytecode return error. Common UFW configurations can therefore still require manual review. A connected provider is not a guarantee of pass/fail coverage for every UFW deployment.
