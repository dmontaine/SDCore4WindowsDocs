Title: Security and the operating system
Subtitle: Reaching the machine from inside SD, how privileged work is done, and the audit trail.

This page continues [Security](12-security.html).

## Reaching the operating system from inside SD

**There are three ways out of SD onto the machine, and each is a switch of the
account.** (Until 25 October 2026 they were a list of people in a file,
`os.users`; the switches are now fields of the account's own record, and the
file is no longer read.)

| | What it is | Governed by |
|---|---|---|
| **`sh`** and `!` | a shell at the `:` prompt | the account's `sh-on` switch |
| `OS.EXECUTE` | the operating system from inside a BASIC program | the account's `os-on` switch |
| **`edit`** and **`micro`** | a text editor, running outside SD | the account's `os-on` switch |

`os-on` also decides whether the account may name a file outside its own
directory (by its path, through a pointer, with `dir()`, as a print file); the
narrower `sd-on` allows the directories of other SD accounts the person could
`logto`. **The switches are in the register, which is in SDSYS and is
read-only to everybody else on disk.** That ACL is the whole of the protection:
without it a user grants themselves any of them in one line.

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
entered — and SDSYS has no API session to be checked.** An ordinary account
with `sh-on` gets `sh` over the API exactly as it would anywhere else, which
is the real risk `sh-on` or `os-on` plus API access creates — the
*Administrator* set's *Accounts and Security* chapter has the detail.
**SDSYS itself never reaches this path**: it carries no SD credential to
authenticate an API connection with by design, and the API is refused to it
outright regardless — see [API access](09-api-access.html).

**4. Nothing in SD limits what you then do.** Once a switch is on, SD is not
standing between that person and the machine — **the boundary from that point
on is their own Windows account's permissions**, and nothing else. An editor
can open any file they are allowed to open, in the data tree or outside it. A
shell is held to one rule only: at the prompt `sh` and `!` refuse a pipe, a
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
cannot read or change them.

Before that they went where every SD user could write, and the second
consequence was the serious one: **another SD user could replace the script
between SD writing it and SD running it, and their version would run with full
administrator privilege.**

**If `PSTMP` is missing, SD refuses the privileged work** rather than falling
back to the old location. You see the command fail rather than quietly running
unprotected.

## The audit trail

`C:\ProgramData\SD\sdsys\audit` records **every login, every refused login,
every `logto`, every refused `logto`, and every `grant` and `revoke`**, with
date, time and the Windows user it belonged to. **It also records what an
administrator does to accounts and to remote access**: `create.account`,
`delete.account` and `restore.account` (a completed one only), the
`modify.account` changes that add or remove a group member, suspend, unsuspend,
change an account's ssh and API routes or its `sh` and `os` switches, and
`remote.api` and `remote.ssh` when they change something. An account line
names the account it concerns.

```
2026-08-16 11:42:07 user=don uid=1 pid=8624 logto account=SDSYS
2026-10-06 21:03:55 user=sdsys uid=1 pid=4120 delete.account account=ANN
2026-10-06 21:04:31 user=sdsys uid=1 pid=4120 remote.api local
```

Every word before the first `=` is lower case. What follows an `=` is as it
was: an account name keeps its case, and so does the text of a reason. A
file that was started before this was the rule holds both spellings, so search
it without regard to case.

**The refusals are the interesting half.** An entry saying somebody who is
not an administrator asked for SDSYS by name, or asked for an account they have
not been granted, is the thing worth seeing. **Failed API logins are recorded
too, with the reason.**

**This is not the error log and does not behave like it.** The error log throws
away its oldest half when it fills; the audit file is **renamed with the date
and time and a new one started, so nothing is ever discarded.** Removing the
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
