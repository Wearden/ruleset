# Wearden ruleset

Hardening content for the Wearden Go agents. These are draft rules, not a certified CIS assessment or a verified Microsoft baseline implementation.

## Layout

- `linux/ubuntu-22.04/`, `linux/ubuntu-24.04/`: original Ubuntu rules and profiles.
- `native/linux/ubuntu-22.04/`, `native/linux/ubuntu-24.04/`: matching native manifests and provider limits.
- `windows/windows-10/`, `windows/windows-11/`, `windows/server-2022/`: original Windows rules and profiles.
- Each version directory has `benchmark.yaml` metadata and category files with a `controls` list.
- `upstream/complianceascode/`: pinned upstream reference files. These are Jinja-templated source content, not directly executable Wearden rules.
- `sources.lock.json`: source commit, URLs, SHA-256 hashes, initial per-rule mappings and review status.
- `docs/legacy-benchmarks-readme.md`: original README preserved verbatim.
- `docs/source-review.md`: semantic differences and source limitations.

## Existing schema

Benchmark metadata contains `id`, `os`, `name`, `version` and `profiles`. A profile selects `controls: all` or explicit `control_ids`. Each control has a stable ID, `cis_ref`, title, OS, category, level, severity, description, rationale, impact, MITRE references, audit, remediation, rollback and reboot/risk flags. Audit has `type`, `command`, `expected` and `match`. The original schema is unchanged; its Python definition remains the legacy reference until the Go validator is implemented.

Legacy IDs and draft CIS references are preserved for traceability, not independently verified. In particular `full-top-100` is a historical profile ID; The same is true of the counts: Ubuntu 24.04 has 100 controls and Ubuntu 22.04 has 112 (ubuntu-24.04 has no separate `06-auditd.yaml`). Do not infer 100 checks or certified compliance from names.

## Sources and usage

ComplianceAsCode files are pinned to the commit in `sources.lock.json`. Preserve `upstream/complianceascode/LICENSE` and applicable notices when distributing covered content. The repo's MIT license does not replace third-party licenses. A CIS-branded profile downloaded for local comparison explicitly states that it includes CIS content; it is excluded from Git pending content-specific licensing review. No official CIS PDF has been copied into this repository.

Windows reference URLs identify Windows 10 22H2, Windows 11 24H2 and Server 2022 packages on Microsoft's official download site. No Microsoft package is redistributed here. The Windows 11 package directory was inspected in memory; no separate license/EULA filename was found. This does not grant redistribution permission. Review Microsoft's applicable terms before vendoring. OS release and machine role must be matched before adapting policies.

## Verification

From this repository run:

```powershell
python tools/verify_sources.py
```

This verifies locked bytes, source-path containment, mapping references and local control IDs using Python's standard library. It does not execute audit/remediation scripts, render upstream templates, validate the complete YAML schema, or prove OS behavior. Only the first 10 filesystem controls have upstream intent mappings; the native catalogs under `native/` cover 100 rules per platform (112 for Ubuntu 22.04).

Agents must implement reviewed local checks. YAML audit/remediation command strings are reference data, not permission to execute arbitrary commands received from core.
