# Native Windows catalogs

All three assignments use `native-windows-4`, preserve 100 original IDs/severities and connect 98 native evaluator entries. PWD002/009 remain explicit manual controls; no password/credential store is opened. Canonical and agent-embedded manifests are byte-identical.

| Platform | Manifest SHA256 |
| --- | --- |
| Windows10 | `2df49b303378022e406951e4695488ac569ce2d949a073bc16a6e84271e40108` |
| Windows11 | `4e8b19a3fbbeca02af7a7886aa71018f112efcfc68d3bbbd4bea5f450fd4819b` |
| Server2022 | `222f2e494a442551890a9cd8ab9c2bd406484e1494ccc096698339810f7cd410` |

Version4 deliberately strengthens two native observations. URA007 compares the exact Administrators/Local Service/Network Service/Service SID set, matching the retained remediation list. The old contains-Administrators audit could pass while unrelated accounts retained impersonation grants. Service observations now require both disabled startup and stopped runtime; disabled-but-running services fail, and transitional states return error. An absent service remains compliant. These changes let subsequent reports detect the same stored policy regressions that the typed writers address. Existing-token privileges, future Group Policy reapplication and whole-host attestation are not established.

Original YAML remains unchanged and is retained for traceability. Native normalization is not literal shell-output parity or verified CIS compliance. The native contains-mode deny-right actions retain additional denials; network-logon retains existing members while adding Administrators. They avoid the broader membership replacements in the old shell remediation. Other exact-set actions use the reviewed baseline SID sets. Exact pre-change membership remains available for rollback.

Windows has83 compiled write/restore handlers, independently guarded by local opt-in, LocalSystem, explicit core risk confirmation, private backups and recovery. Connected inspection does not imply a write handler or guarantee applicability to every machine. See the agent README for detailed provider bounds. Domain-controller user-right/account-policy writes are refused. No test, scan, native policy query/write, service action or recovery execution was run for this source checkpoint.
