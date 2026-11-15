# Source and semantic review

Reviewed 2026-11-15. Original benchmark YAML was copied without byte changes. The original project is untouched; .env, databases, node_modules and caches were not copied.

## Linux filesystem mappings

The 10 LNX-FS controls map to 16 upstream rule files: seven kernel module controls and three combined mount controls, each with nodev/nosuid/noexec components. See exact pinned source paths in sources.lock.json. A same-intent mapping is not a claim of identical semantics or Ubuntu profile membership.

Observed difference: legacy module commands accept only `install /bin/true` in modprobe output. The pinned upstream OVAL template accepts `/bin/true`, `/bin/false` and their `/usr/bin` equivalents, normalizes hyphens/underscores, allows trailing comments and for Ubuntu requires a blacklist as well as install blocking. The upstream remediation template uses `/bin/false` plus blacklisting. A machine following that upstream remediation can therefore fail the old Wearden check. Do not copy the old matching expression into the Go implementation and call it equivalent.

The upstream OVAL template checks configuration files across several directories. It is not itself proof that the running kernel has unloaded the module or that configuration precedence was fully resolved. Native Go checks must explicitly define and test effective configuration and current module state before asserting protection. Unsupported or unreadable evidence must remain visible as error/not_applicable as appropriate.

Mount-option mappings are one-to-many. Each combined Wearden control requires all three options on the relevant mount, not just one successful upstream check. Verify actual mount selection and effective options, plus whether the specific partition is applicable. No remediation was run.

## Content scope

Only filesystem mappings have been reviewed in this pass. Remaining Linux categories and all Windows control values are legacy-unverified. The selected Ubuntu CIS profile is locally available as reference only and is Git-ignored because its text explicitly says it includes CIS Benchmark content; the repository-level BSD license alone is not treated as blanket clearance for that content. Metadata and generic rule-source imports are not a CIS certification claim.

## Windows

Reference packages are release-specific. Existing windows-10/windows-11 folders lack release-specific applicability; the legacy Windows 11 metadata itself warns that the control set originated from Server 2022. Do not apply server settings blindly to workstations or generalize Windows 11 24H2 values to every release. No package contents, executable tools or scripts have been installed, executed or committed. Microsoft policy value import remains pending applicable terms and per-setting review.

## Integration boundary

This repository currently contains content and provenance, not a running scanner. The Go rewrite will consume reviewed native rule definitions. Template rendering and running SCAP/Ansible tooling are not needed to inspect the selected sources and were not installed.
