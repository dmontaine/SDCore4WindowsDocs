Title: Operating System Access
Subtitle: The `sh` verb, and the per-account switch that decides who may use it.

`sh` runs a Windows command from the SD prompt. (The `!` form, a shorter name for
the same verb, does not exist: write `sh command`.) **Each
account has its own switch for it, `sh-on`, and a new account does not have
it** — SDSYS turns it on, account by account, with `modify.account`. Without it
the verb refuses.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

**The switch is a wall for an SD *session*.** A person who already has a Windows
shell on the machine does not need it; what such a person can and cannot do to
SD is in [SD installation](08-sd-installation.html), *What this does not
close*.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

## The verb

```
sh command
```

Everything after the verb is the command:

```
:sh echo hello-from-the-shell
hello-from-the-shell
```

**A bare `sh`, with nothing after it, starts an interactive shell** (Windows
PowerShell; the filter below is for a typed command). `exit` brings you back
to the SD prompt. It needs the account's `sh-on` switch like any other `sh`: an
account without it is refused first, with "<name> is not permitted to use the
operating system shell".

## The shell you get is Windows PowerShell 5.1

Not `pwsh`, and the difference bites:

**`&&` and `||` do not exist in that PowerShell**, and SD refuses a command that
holds one before PowerShell sees it (see the next section). Nor do the ternary,
null-coalescing or null-conditional operators. Chain with `;` in a script, and
test with `if ($?) { … }`.

## One rule about the shape of the command, for everybody

**The verb refuses a command that contains `;`, `|`, `&`, `$`, a backquote,
`<`, `>` or a newline**, before anything runs:

```
:sh echo alpha-beta | findstr alpha
Error 2 executing operating system command
:sh echo gamma > zzsh.txt
Error 2 executing operating system command
```

That is a sanitizer on what a one-line command may look like — a safety
measure against an accidental injection, not a permission — and it applies to
every account, SDSYS included, whether or not the account has `sh-on`. So **no
pipe, no redirection, no chaining and no variable expansion is available from
the prompt.** What an account that has the switch can do about that is the
obvious thing: write the work into a script file and run the script
(`sh powershell -File .\nightly.ps1`, or `sh .\nightly.cmd`). The script's own
contents are not filtered. This is why `sh-on` is a decision to give a person a
shell on the machine, not a decision to give them a restricted one.

## SD refuses to nest

```
:sh sd
SD is already running in this session - type EXIT to return to it.
```

The child shell is marked, and SD checks the mark:

```
:sh Get-ChildItem Env:SD_SESSION
Name                           Value
----                           -----
SD_SESSION                     1
```

**That is worth knowing when writing a script for `sh` to run** — anything it
invokes inherits `SD_SESSION`, so a script that starts SD as part of its work
will be refused, wherever it is called from.

## Who is allowed: a switch in the account's own record

**The permission is a field of the account's own register record** — field 7,
`yes` or `no` — and not a tier and not a file of names. Anything other than
`yes` means no, and a record that never had the field means no. It is written
by `create.account` (`sh-on`) and changed by `modify.account` *name* `sh-on` /
`sh-off`; each reports where the account now stands, both switches at once:

```
:modify.account fred sh-on
Account fred has SH yes, OS.EXECUTE no
```

**The switch is read when a session signs in or `logto`s into the account**,
so a change reaches the account the next time it is entered, and a session that
is already open keeps what it started with. To take the shell from somebody who
is signed in now, change the switch and then end their session. **It follows
the account, not the person:** a person who is allowed the shell in one account
is not allowed it in another that does not have the switch, and the reverse.

| | `sh` |
|---|---|
| the account has `sh-on` | runs the command, subject to the rule above |
| SDSYS | runs it, whatever the register says |
| anybody else | refused, and the command is never looked at |

```
fred is not permitted to use the operating system shell
```

is message 10053, and it names the person who signed in (`@logname`), not the
account. **A group account or an `other` account is refused `sh-on` and `os-on`**
("is a group account and has no Windows user, so it has no shell to permit"): a
shell is a fact about a person, and a group account is not one.

**The upgrade copies the old list once.** When SD was installed over a system
that kept `os.users`, the installer's `upgrade_gates` step copied, once, what the
file said about each user account's Windows user into that account's two
fields, filling only a field that was blank, so nobody lost a command they were
using. A later install does not turn anything back on that an administrator has
since turned off. The file `os.users` stays on disk, unread, and nothing
consults it.

## What this does not gate

**A program's `OS.EXECUTE` is not on this path**, and neither are the screen
editors, the embedded Python, or reaching an operating-system file by its path.
They are governed by the other switch, `os-on`, which is independent: `sh-off`
leaves it alone, and an account can be refused the shell and still run `edit`
and `micro`, and the reverse. See [Accounts and
Security](01-accounts-and-security-2-making-an-account.html#the-operating-system-switches-sh-on-and-os-on)
for everything `os-on` covers.

**The form that does go through this gate is `execute 'sh …'` from a program**,
because that runs the TCL verb.

## Over the API

**A session that arrived over the API is held to the same switch**: the API
server reads the account's `sh-on` and `os-on` when it enters the account, as
sign-in and `logto` do, so an account with `sh-on` has the shell over the API
and an account without it is refused there too. **That is what makes `sh-on`
on an account that also has the API route a shell behind its credential from
wherever the API port is reachable** — see *What `os-on` actually costs* in
[Accounts and Security](01-accounts-and-security.html). SDSYS reaches the API
from another computer only through the door `remote.sdsys api on` opens
([Remote Administration through the API](22a-remote-administration-through-the-api.html)). See also
[Remote Access and the Machine](05-remote-access-and-the-machine.html).

## Who has these verbs

`sh` is in every account's VOC — there is no tier to withhold it.
**Having the verb is not having the permission**: an account without `sh-on`
has the verb and is refused by it.

## SDSYS is a shell on this machine, and only on this machine

State this plainly to anyone with the credential for the `sdsys` Windows
account:

**SDSYS can run operating-system commands on the server as itself, the
Windows account it signed in as — from this machine, and nowhere else.**
Signing in to SDSYS at all means being at the console (or a remote-desktop
or remote-control product installed as a service, which Windows treats the
same way) — `sdsys` is denied ssh and denied network sign-in outright, so
there is no remote session for this to ever apply to.

The register is not consulted for SDSYS: the same identity check that grants
administration — see [Accounts and Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it)
— grants `sh` and `OS.EXECUTE` too, unconditionally. That is *narrower*
than the old model, not wider: an elevated session in an ordinary account
used to pass this gate as well, and no longer does. **The metacharacter rule
above applies to SDSYS too.**

### Why there is no tunnel to worry about here

**The old concern was an administrator tier reachable through a forwarded
ssh connection that arrives looking local.** That does not apply to SDSYS:
`sshd_config`'s `AllowGroups` never includes the `sdsys` Windows account, so
there is no ssh session for SDSYS to exist in the first place, tunnelled or
not — the refusal is at the door, before authentication, not a check on
where the connection appears to originate. The API has its own rule for the
same account, separately: it is shut to SDSYS from another computer unless the
administrator opens it for chosen addresses with `remote.sdsys api on`
([Remote Administration through the API](22a-remote-administration-through-the-api.html)). See
[Remote access and the machine](05-remote-access-and-the-machine.html).

**An ordinary account's own `sh-on` or `os-on` is a different question and
still deserves the same caution.** `os-on` plus API access on *any* account
puts an operating-system shell behind that account's own credential,
reachable from wherever the API is reachable from — see [What `os-on`
actually costs](01-accounts-and-security-3-edit-switches.html#what-os-on-actually-costs). That
risk did not go away with the tiers; it just no longer has anything to do with
being an administrator.

The verify suite asserts all of this — the local session working, the remote one
refused, and an ordinary account admitted over that same remote route as the
control — so a future change that quietly reopened it shows up as a failing test
rather than as a page that had silently become false.

## Leaving SDSYS by `logto` is one-way

Working in `SDSYS` is elevated. **The moment that session `logto`s anywhere
else, the administrator flag is cleared and the elevated helper is
stopped** — and there is no `logto` back.

```
:logto sales
```

This session is now `sales`, an ordinary account. `logto sdsys` from here is
refused, whatever the session's elevation, unless this very session signed in to
Windows as the `sdsys` account at its desktop: that session, and only that one,
may `logto sdsys` to come back. SDSYS is first reached one way only, by signing
in to Windows as the `sdsys` account and starting `sd` fresh. See
[Accounts and Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).

**This is deliberate, and stricter than the old design it replaced.** A
session that could `logto` back into SDSYS would let the elevated helper
outlive the rights it belongs to; refusing the return closes that rather
than relying on the helper alone to behave.

**A Windows process cannot give up its own administrator rights, and SD tells
you so.** The flag and the helper end at the `logto`, but the Windows process
that is running the session stays elevated (high integrity, 24
privileges). A program that session starts, where the account's switches allow
one, can use those rights. So, once per `logto` out of `SDSYS`, SD prints:
*"This session started as an administrator and keeps its Windows administrator
rights in account ... A program it starts can use them. Sign out and sign in to
... to work without them."* **To work as that account without the rights, sign
out and sign in to it.** An ordinary account moving to another account sees
nothing, because it never had them.

The step is quiet for the ordinary case: a session moving between two
ordinary accounts never had privilege, so nothing is given up and nothing
is written to the audit trail.

## The documentation in the shared account

```
docs.install directory
load.help
```

**SD starts no program for an account whose `os-on` and `sh-on` are off: there is no
exception.** The documentation PDFs are files in the `pdf` directory of the shared
account (`C:\ProgramData\SD\group_accounts\shared\pdf`), which every SD user may read.
A person reads one by copying it, or by opening it with a reader they start
themselves. A help box that has more in the documentation names the PDF on its last
line, exactly as it is named in the `pdf` directory: the book comes first, then the
chapter (`administrator-01-accounts-and-security.pdf`; the books are `user`,
`administrator` and `gettingstarted`).

**No SD user can add, change or remove a document there.** The installer makes the
directory with its own permissions: SYSTEM and Administrators full control, `sdusers`
read only. It does not take the shared account's own permission, which lets
`sdusers` write.

### Where the documents come from

The PDFs are generated from the documentation and are not part of the source tree.
**A release package carries them**, in a folder `pdf` beside the installer, and
**the installer puts them in the shared account with `docs.install`**. An installer
run without that folder says so in `C:\ProgramData\SD\shared-docs.log`, and the
install goes on. At any other time, or for documents of your own, SDSYS runs:

```
docs.install C:\path\to\the\pdf\files
```

which copies every `*.pdf` of that directory into the shared account's `pdf`
directory. A file is copied only if its name is lower case letters, digits and
`. _ -`, ends in `.pdf` and does not begin with a dot, and the file begins with
`%PDF-`; anything else is skipped and named. A document already there is replaced.

**The changes document comes with the installer.** A release package holds, beside
the installer, the document that lists what changed in the release as
`sd-core-for-windows-<version>-changes.pdf`, `.html` and `.md`. The installer copies
each of them into the same `pdf` directory. A file that is a link, or whose name has
a capital or another character, is not copied, and the log says so.

### The context help: `load.help`

The `[?]` button on the administrator's pages shows help kept in the file `context.help`
of the shared account, one record to a setting. The installer fills it from the text under
`helptext` in the SD system directory; `load.help` does the same by hand, after that text
changes (it enters the shared account, writes the records that differ, and returns to the
account it began in). **It replaces the shipped records and keeps any you added** under
another id (the count says how many). Reading the help is not gated: the text is the
product's own documentation of its screens, so an account whose `shared.read` you withdrew
still gets it, and SDSYS, whose own `OPEN` does not follow `shared`, does too.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).
