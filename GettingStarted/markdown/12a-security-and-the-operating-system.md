Title: Security and the operating system
Subtitle: Reaching the machine from inside SD, how privileged work is done, and the audit trail.

This page continues [Security](12-security.html).

## The shell and operating-system access are per-account switches

**SD is delivered with the ways out of SD shut, and the administrator opens
them one account at a time.** A new user account has none of these until
SDSYS turns it on (`modify.account` *name* `sh-on` / `os-on`):

| | What it is | The switch |
|---|---|---|
| **`sh`** | a shell at the `:` prompt | `sh-on` |
| `OS.EXECUTE` | the operating system from inside a BASIC program | `os-on` |
| **`edit`** and **`micro`** | a text editor, running outside SD | `os-on` |
| the embedded Python | arbitrary code in the account's own process | `os-on` |
| a file or directory of the operating system **by its path**, outside the account's own directory | `OPENSEQ` and `OPENPATH` with a path, `DIR()` and `select.dir`, `DELETESEQ` of a path, `!OSCOPY`, `!IOSCOPY` and the `oscopy` verb, printing into a file by path | `os-on` |

`sed` is not in the table: it runs inside SD, so editing a record of an SD file
needs no switch. The narrower `sd-on` allows the directories of other SD
accounts the person could `logto`. **The switches are in the register, which is
in SDSYS and is read-only to everybody else on disk.** That ACL is the whole of
the protection: without it a user grants themselves any of them in one line.

**Without a switch SD says so in words** — "*name* is not permitted to use the
operating system shell", "*name* is not permitted to use OS.EXECUTE", or "*name*
has no OS access, so outside its own account it can reach by pathname only a
directory the administrator opened to all (SDSYS can give it: `modify.account`
*name* `os-on`)" — and a program is told with status 3035, so `OPEN ... ELSE`
and `DELETESEQ ... ELSE` take their ELSE as for any other refusal.

**What an account without `os-on` still has** is everything that stays inside
SD: every file its VOC names (dictionaries and other SD files included) and
anything inside its own directory.

**A VOC pointer is held to the same rule.** A file pointer in an account's VOC
must lead inside the account (or be one of the pointers SD itself puts in every
VOC), so a pointer written by hand at a system directory or at another account's
directory is refused, status 3035, unless the account holds `os-on`. **A
Q-pointer into another account is followed only if you could `logto` that
account** — whether or not you hold `os-on`. The Administrator set's *Accounts
and security* chapter has the full rule.

**One setting of the administrator's opens a directory without `os-on`.**
`NETDIRS` in `sd.conf` lists directories outside every account that an account
without `os-on` may read and write by pathname, as it may inside its own
directory. It is empty as delivered; the Administrator set's *Configuration*
chapter has it. An entry that is a drive root or the root of a network share
(`\\server\share`) is refused, because it would hold a whole volume.

**Four rules hold for all of them:**

**1. A blank switch means no.** A new account has all of them off, and an
installation with accounts from before has the old list copied into the
switches once, at the upgrade.

**2. SDSYS passes on its own**, regardless of the register, so an empty
register cannot lock the machine's own administrator out. This is *narrower*
than the identity check might suggest — it is not "elevated," it is "signed in
to Windows as the `sdsys` account and running `sd` elevated," and nothing
less passes. An elevated session in any other account gets no exemption at
all; it is checked against the account's switches exactly like an unelevated
one. See [Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**3. An API session is checked the same way as any other, by the account it
entered — and an SDSYS session, which exists only when the administrator has opened that door, is the administrator's own.** An ordinary account
with `sh-on` gets `sh` over the API exactly as it would anywhere else, which
is the real risk `sh-on` or `os-on` plus API access creates — the
*Administrator* set's *Accounts and Security* chapter has the detail.
**SDSYS reaches the API from another computer only through the door the
administrator opens with `remote.sdsys api on`**, shut as delivered — see
[API access](09-api-access.html).

**4. Nothing in SD limits what you then do.** Once a switch is on, SD is not
standing between that person and the machine — **the boundary from that point
on is their own Windows account's permissions**, and nothing else. An editor
can open any file they are allowed to open, in the data tree or outside it. A
shell is held to one rule only: at the prompt `sh` refuses a pipe, a
redirect, a chain and a variable, for every account; the way round is a script
file.

> **So `sh-on` and `os-on` are statements of trust in an account.** They are
> not a convenience to be handed out because somebody asked for a full-screen
> editor. Grant them on the same basis you would grant a shell account on the
> machine, because that is close to what you are granting.

**How to grant and remove them** is on
[Administrator commands](06-administrator-commands.html#how-you-grant-it).

## Privileged work is done through a script, not a command line

When SD creates an account, sets a password or edits a group, it writes a short
script to a file and runs it, rather than putting a password on a command line
where any local user could read it through Task Manager or WMI.

Those scripts go in **`PSTMP`**, a directory of its own inside the database
directory, where each file belongs to the session that wrote it. Other SD users
cannot read or change them. In a directory every SD user could write,
**another SD user could replace the script between SD writing it and SD running
it, and their version would run with full administrator privilege**, which is
why it is not there.

**If `PSTMP` is missing, SD refuses the privileged work.** You see the command
fail rather than quietly running unprotected.

## The audit trail

`C:\ProgramData\SD\sdsys\audit` records **every login, every refused login,
every `logto`, every refused `logto`, and every `modify.account add`/`delete`**,
with date, time and the Windows user it belonged to. **It also records what an
administrator does to accounts and to remote access**: `create.account`,
`delete.account` and `restore.account` (a completed one only), the
`modify.account` changes that add or remove a group member, suspend, unsuspend,
change an account's ssh and API routes or its `sh` and `os` switches, and
`remote.api` and `remote.ssh` when they change something. An account line
names the account it concerns.

```
2026-08-16 11:42:07 user=sam uid=1 pid=8624 logto account=SDSYS
2026-10-06 21:03:55 user=sdsys uid=1 pid=4120 delete.account account=ANN
2026-10-06 21:04:31 user=sdsys uid=1 pid=4120 remote.api local
```

Every word before the first `=` is lower case, the event names included
(`login`, `logto`, `logto refused`, `api refused`, `elevation granted`,
`modify.account route api`). What follows an `=` is data and keeps its case:
the account name as it is registered, a `reason=` text, and what a caller
typed in `command=`. A file written by an older version may hold upper case
lines, which are not rewritten, so match without regard to case when you search
a long-lived file.

**An account's gates are on the trail whenever they are given.** `modify.account`
writes one line for each word it carries out (`modify.account sh-on account=fred`;
several words in one command give several lines), and `create.account` records
the gates it granted at creation as well:

```
2026-10-19 15:35:26 user=sdsys uid=1 pid=8326 create.account account=witm1 type=user gates=sh-on,os-on,files-on,files-write-on
2026-10-19 15:35:27 user=sdsys uid=2 pid=8614 create.account account=witm2 type=user gates=none
```

`gates=` lists, in lower case, every access the new account was given, always
in this order whatever order the words were typed: `ssh`, `api`, `sh-on`,
`os-on`, `voc-on`, `bp-on`, `dict-on`, `net-on`, `files-on`, `files-write-on`,
`files-admin-on`, `ai-on`, `shared-read-off`, `shared-write-on`, `pins-on`,
`recovery-on`, `xfer-on`. It says `none` when there is none. The line is
written only after the account has been made: a creation that is refused (an
empty password, say) leaves no line.

**The refusals are the interesting half.** An entry saying somebody who is
not an administrator asked for SDSYS by name, or asked for an account they have
not been granted, is the thing worth seeing. **Failed API logins are recorded
too, with the reason** — and **before** the three-second wait SD adds to slow
down guessing, so a program that hangs up during the wait is recorded as well.

**This is not the error log and does not behave like it.** The error log throws
away its oldest half when it fills; the audit file is **renamed with the date
and time and a new one started when it reaches one megabyte (by the audit
service as it writes, and by `sd -start`), so nothing is ever discarded.** Removing the
old ones is your decision — SD will not do it for you, and they will
accumulate.

| SD users can | SD users cannot |
|---|---|
| **add** to it | read it, change a record in it, empty it, rename or delete it |

**Windows itself refuses, not SD**, so a user cannot quietly remove the line
that records what they did. Administrators can read it and do anything else to
it as well: this raises the floor against ordinary users rather than trying to
constrain somebody who owns the machine.

> Windows keeps its own separate record of account and group changes in the
> Security event log. **Read the two together.**

## What is still not true

**SD users are not isolated from each other's data at the file level, beyond
the Per-account directory lock.** Everyone who uses SD needs file access to
the tree, because their own process does the I/O. Anyone deploying SD for ten
people over ssh should be told that plainly.

**SD has no file-level access control of its own** on the console and ssh
paths. The one place a path gate does exist is the API, where a session is
confined to the account it stands in — see
[API access](09-api-access.html#a-session-is-confined-to-its-own-account).
