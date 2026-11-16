# Ubuntu 22.04 native catalog

Assignment: `ubuntu-22.04-native`. Version: `native-linux-2204-2`.
Canonical and embedded manifest SHA256: `1e76403efd65f140041cc49d4c3b981619b798f550355056e14cad3b73971c78`.

All 100 original Ubuntu22.04 IDs and severities are retained: 99 entries connect to native providers; USR006 explicitly requires manual review because its legacy audit reads credential-file contents. The shared 88 controls have the same original audit blocks and severities as Ubuntu24.04. Their native definitions and limitations are described in [the Ubuntu24.04 catalog](../ubuntu-24.04/README.md). This is source coverage, not verified CIS compliance or runtime parity.

The additional 12 controls are read-only. AUD001 inspects the public dpkg status for auditd installation. AUD002 inspects persistent systemd wants/requires links against the selected regular auditd unit, rejecting masks, aliases, generated/transient/control overrides, unsafe paths and ambiguous links. The standard merged-usr /lib alias is accepted only when it points exactly to usr/lib. Other layouts require review. This preserves the legacy audit's enablement scope; neither the old audit nor this provider proves the daemon is running.

AUD003..012 send only AUDIT_LIST_RULES on an unicast NETLINK_AUDIT socket. They do not register an audit daemon, subscribe to events, read audit logs or issue add/delete/set requests. The kernel can require CAP_AUDIT_CONTROL in the initial user/PID namespaces even for listing. Unavailable privileges or unsupported evidence returns error. No watched file is opened, including shadow/gshadow; findings expose only fixed evidence descriptions.

The selector checks cover sudoers paths, time-change syscalls, account-file watches, hostname/domain syscalls or hosts/issue watches, AppArmor watches, login/session paths, permission-change syscalls, EACCES exit filters and uid/euid inequality or exec syscalls. The legacy grep audits required at least one matching selector. The native implementation inspects structured always/exit rule metadata, with explicit x86_64/i386 syscall maps, rather than executing or parsing auditctl output.

Pass means a reviewed selector is present. It does not prove complete syscall/path/architecture coverage, lack of earlier suppression, the meaning of every other predicate, global audit enablement, event emission or durable storage. Those limitations must remain visible when interpreting the score. Kernel allocation failure can also omit rules from a returned list; two identical lists are a stability check, not an attested atomic/full snapshot.

Both ordered lists must have identical SHA256 digests. One shared six-second deadline, 64 KiB datagram bound, 16 MiB per-list bound and 8192-rule bound limit collection. Sender, sequence, multipart completion and string/array lengths are checked. Changing snapshots, oversized or malformed messages and unreviewed syscall architectures produce error. No shell command or firewall write is enabled by this catalog. The shared 27 mutation handlers remain a separate local opt-in capability; none of the 12 additional audit controls has a write handler.

Source references inspected for the protocol layout and replies:

- [Linux5.15 auditfilter.c](https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux/+/v5.15/kernel/auditfilter.c): audit_pack_string, audit_krule_to_data and audit_list_rules_send.
- [Linux5.15 audit.c](https://raw.githubusercontent.com/torvalds/linux/v5.15/kernel/audit.c): audit_make_reply and audit_netlink_ok.

No tests, live audit queries, service operations or native scans were executed. Compilation does not establish native behavior.
