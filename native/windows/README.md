# Native Windows catalogs

All three assignments use `native-windows-6`, preserve100 original IDs/severities and connect100 native evaluator entries. PWD002/009 inspect local SAM password-policy flags through metadata-only domain APIs; no password/hash or credential-store content is read. Canonical and agent-embedded manifests are byte-identical.

| Platform | Manifest SHA256 |
| --- | --- |
| Windows10 | `b753ecdea9136d2f83d5b4b1c6f4fdf2f821cb207cf4b970aae9079ede723295` |
| Windows11 | `07335ae771f4ff5922da3c155c767295a439d8300558f10febb8840f04d33a96` |
| Server2022 | `ef6d3b9f5cd16bbd759994465e7ae647994516d28f711353c1f7d63d769df59a` |

Version4 deliberately strengthens two native observations. URA007 compares the exact Administrators/Local Service/Network Service/Service SID set, matching the retained remediation list. The old contains-Administrators audit could pass while unrelated accounts retained impersonation grants. Service observations now require both disabled startup and stopped runtime; disabled-but-running services fail, and transitional states return error. An absent service remains compliant. These changes let subsequent reports detect the same stored policy regressions that the typed writers address. Existing-token privileges, future Group Policy reapplication and whole-host attestation are not established.

Original YAML remains unchanged and is retained for traceability. Native normalization is not literal shell-output parity or verified CIS compliance. The native contains-mode deny-right actions retain additional denials; network-logon retains existing members while adding Administrators. They avoid the broader membership replacements in the old shell remediation. Other exact-set actions use the reviewed baseline SID sets. Exact pre-change membership remains available for rollback.

Windows has100 compiled write/restore handlers, independently guarded by local opt-in, LocalSystem, explicit core risk confirmation, private backups and recovery. Connected inspection does not imply a write handler or guarantee applicability to every machine. See the agent README for detailed provider bounds. Domain-controller user-right/account-policy writes are refused. No test, scan, native policy query/write, service action or recovery execution was run for this source checkpoint.

Version5 adds typed complexity/reversible-storage flag inspection and selected-flag remediation. Local domain identity is bound privately; the two flags have independent snapshots so batch apply/restore preserves other policy fields. Domain controllers and unavailable native APIs fail explicitly. No native policy call or test ran.

Version6 evaluates explicit LSA protection modes by supported Windows version, accepting non-UEFI mode2 on Windows11 22H2+. The writer chooses mode2 there. Older supported releases require kernel Secure Boot to be off before a new mode1 write; otherwise they fail with manual firmware-review guidance. Original mode1 is retained when already compliant. No firmware variable or reboot API is invoked, and registry rollback does not certify firmware-lock removal. This conditional capability is recorded in the remaining-provider ledger.
