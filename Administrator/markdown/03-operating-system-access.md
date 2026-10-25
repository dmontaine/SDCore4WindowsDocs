Title: Operating System Access
Subtitle: The `sh` and `!` verbs, and the per-account switch that decides who may use them.

`sh` runs a Windows command from the SD prompt. `!` is the same verb under a
shorter name. **Each account has its own switch for them, `sh-on`, and a new
account does not have it** — SDSYS turns it on, account by account, with
`modify.account`. Without it both verbs refuse. (Before 25 October 2026 the
permission was a record in a file, `os.users`, keyed to the person; it is now a
field of the account, and `os.users` is no longer read.)

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

> **The listings of `echo` and of the nesting refusal were produced by running
> them**, on SD Core for Windows W1.0-0, from an unelevated session in an
> account that was on the list. **The rest of this page was rewritten from the
> source when the per-account switch was carried from SD Core for Linux, and has
> not been run on a Windows installation since.**

## The two verbs

```
sh command
! command
```

Everything after the verb is the command:

```
:sh echo hello-from-the-shell
hello-from-the-shell
:! echo via-the-bang-form
via-the-bang-form
```

**There is no interactive shell at the prompt.** A bare `sh`, with nothing
after it, is refused with the same "Error 2" as below, so a script, a phantom
or a scheduled job that types it does not hang waiting for somebody at a
keyboard. (Until 25 October 2026 a bare `sh` from an account on the `os.users`
list handed control to an interactive PowerShell and **waited for ever** when
there was nobody at the keyboard.) For a session of your own, sign in to
Windows.

## The shell you get is Windows PowerShell 5.1

Not `pwsh`, and the difference bites:

```
:sh echo delta && echo epsilon
At line:1 char:12
+ echo delta && echo epsilon
+            ~~
The token '&&' is not a valid statement separator in this version.
```

(That listing is from the W1.0-0 run, when `&&` still reached the shell; since
25 October 2026 SD refuses the command before PowerShell sees it, see the next
section.) **`&&` and `||` do not exist in that PowerShell.** Nor do the ternary,
null-coalescing or null-conditional operators. Chain with `;` in a script, and
test with `if ($?) { … }`.

## One rule about the shape of the command, for both verbs and for everybody

**Both verbs refuse a command that contains `;`, `|`, `&`, `$`, a backquote,
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

**This is stricter than SD Core for Windows used to be.** Until 25 October
2026 an account that was on the `os.users` list had pipes, redirection and
chaining at the prompt (a ruling of 17 August 2026), and only a session that was
not on the list met the filter. The filter is now the same for everyone, as in
SD Core for Linux.

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

| | `sh` and `!` |
|---|---|
| the account has `sh-on` | runs the command, subject to the rule above |
| SDSYS | runs it, whatever the register says |
| anybody else | refused, and the command is never looked at |

```
don is not permitted to use the operating system shell
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
Security](01-accounts-and-security.html#the-operating-system-switches-sh-on-and-os-on)
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
[Accounts and Security](01-accounts-and-security.html). SDSYS has no API
route at all. See also
[Remote Access and the Machine](05-remote-access-and-the-machine.html).

## Who has these verbs

`sh` and `!` are in every account's VOC — there is no tier to withhold them.
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
where the connection appears to originate. The API is refused the same
way, for the same account, separately. See
[Remote access and the machine](05-remote-access-and-the-machine.html).

**An ordinary account's own `sh-on` or `os-on` is a different question and
still deserves the same caution.** `os-on` plus API access on *any* account
puts an operating-system shell behind that account's own credential,
reachable from wherever the API is reachable from — see [What `os-on`
actually costs](01-accounts-and-security.html#what-os-on-actually-costs). That
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

This session is now `sales`, an ordinary account, permanently for its own
lifetime. `logto sdsys` from here — or from any other account — is refused
outright, whatever the session's elevation: SDSYS is reached one way only,
by signing in to Windows as the `sdsys` account and starting `sd` fresh. See
[Accounts and Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).

**This is deliberate, and stricter than the old design it replaced.** A
session that could `logto` back into SDSYS would let the elevated helper
outlive the rights it belongs to; refusing the return closes that rather
than relying on the helper alone to behave.

The step is quiet for the ordinary case: a session moving between two
ordinary accounts never had privilege, so nothing is given up and nothing
is written to the audit trail.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).
