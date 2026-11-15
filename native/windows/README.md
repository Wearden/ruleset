# Native Windows catalogs

All three assignments use `native-windows-5`, preserve100 original IDs/severities and connect100 native evaluator entries. PWD002/009 inspect local SAM password-policy flags through metadata-only domain APIs; no password/hash or credential-store content is read. Canonical and agent-embedded manifests are byte-identical.

| Platform | Manifest SHA256 |
| --- | --- |
| Windows10 | `e87fffe7573be31a5b52623e5cdb64c78f4929ed0d27544e36919fe8cd32e782` |
| Windows11 | `524f383457d247d36ef5e33f71ace7e1c5d19bb1f09b08308175d982f6635438` |
| Server2022 | `dd4059fbc31815f25f2200e6bfadd9941a8433cf40897049e6210060e1aacfa7` |

Version4 deliberately strengthens two native observations. URA007 compares the exact Administrators/Local Service/Network Service/Service SID set, matching the retained remediation list. The old contains-Administrators audit could pass while unrelated accounts retained impersonation grants. Service observations now require both disabled startup and stopped runtime; disabled-but-running services fail, and transitional states return error. An absent service remains compliant. These changes let subsequent reports detect the same stored policy regressions that the typed writers address. Existing-token privileges, future Group Policy reapplication and whole-host attestation are not established.

Original YAML remains unchanged and is retained for traceability. Native normalization is not literal shell-output parity or verified CIS compliance. The native contains-mode deny-right actions retain additional denials; network-logon retains existing members while adding Administrators. They avoid the broader membership replacements in the old shell remediation. Other exact-set actions use the reviewed baseline SID sets. Exact pre-change membership remains available for rollback.

Windows has99 compiled write/restore handlers, independently guarded by local opt-in, LocalSystem, explicit core risk confirmation, private backups and recovery. Connected inspection does not imply a write handler or guarantee applicability to every machine. See the agent README for detailed provider bounds. Domain-controller user-right/account-policy writes are refused. No test, scan, native policy query/write, service action or recovery execution was run for this source checkpoint.

Version5 adds typed complexity/reversible-storage flag inspection and selected-flag remediation. Local domain identity is bound privately; the two flags have independent snapshots so batch apply/restore preserves other policy fields. Domain controllers and unavailable native APIs fail explicitly. No native policy call or test ran.
