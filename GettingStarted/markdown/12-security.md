Title: Security
Subtitle: Who you are, what that gets you, and what actually protects the database.

The identity model in SD Core is not OpenQM's and not SD on Linux's. It is
worth understanding before you test anything else, because several behaviors
that look like bugs are consequences of it.

## What ships secured, before you change anything

**A fresh install starts closed and stays closed until an administrator
opens something remote.** Nothing below is a setting you have to remember to
apply — it is what `create.account` and the installer already do:

| | |
|---|---|
| Every SD account | a standard Windows account with no privileged token — see [Being a Windows administrator gets you nothing](#being-a-windows-administrator-gets-you-nothing) |
| ssh | `ForceCommand`s straight into `sd`, no shell reachable that way — see [ssh access](08-ssh-access.html) |
| ssh and the API, per account | **off for a new account**; SDSYS gives each account the route it needs (`ssh`, `api`, `both`) — see [Managing accounts](05a-managing-accounts.html) |
| `sh`, `OS.EXECUTE`, the editors, the embedded Python, and operating-system files named by path | **off for a new account**, in two independent switches (`sh-on`, `os-on`) that SDSYS turns on account by account — see [Security and the operating system](12a-security-and-the-operating-system.html#the-shell-and-operating-system-access-are-per-account-switches) |
| Saving a change to a VOC, a program file or a dictionary (and compiling) | **off for a new account**, in three independent switches (`voc-on`, `bp-on`, `dict-on`) that SDSYS turns on account by account; reading is never stopped — see [Managing accounts](05a-managing-accounts.html) |
| `NETDIRS` | a line in `sd.conf`, **empty as delivered**: directories outside every account, separated by semicolons, that an account without `os-on` may read and write by pathname as it does inside its own directory. Listing one opens it to every such account, on every route, so list only a directory meant for all of them — see [Security and the operating system](12a-security-and-the-operating-system.html) |
| The NET gate | **off for a new account**: the `net-on` switch, which SDSYS turns on (`modify.account` *name* `net-on`), is what lets an account open a file held on another SD server, and the account must also be named in that server's list. Turning it on lets the account's programs read that server's files, and change them only where the server is defined as `write` and the other server's administrator allowed it; `NETFILES` in `sd.conf` (0 as delivered) must have bit 2 set before an API client may open an `account;file` file here — see [Not in SD Core](14-not-in-sd-core.html) |
| File transfer | **off twice as delivered**: the system switch `XFER` in `sd.conf` is 0, and a new account's `xfer-on` switch is off. SDSYS sets `XFER=1` and turns `xfer-on` on for an account. Opening both lets that person bring plain-text files into their own account, and take copies of its records out, with an sftp client over their ssh login: one directory each way, within the size limits, and no shell — see [ssh access](08-ssh-access.html) |
| Scheduled jobs | **nothing is allowed or scheduled as delivered**. An account's command runs unattended only when SDSYS lists its name for that account (`set.batch add`), and SDSYS's own jobs (`set.job`) exist only when SDSYS adds them. A listed command runs with nobody at the keyboard, as the account's Windows user; a `set.job` job runs one of two fixed commands (`backup-all`, `update-accounts`) as the administrator — see [Scheduled jobs](04-scheduled-jobs.html) |
| The `shared` account | the one door that is **open** in a new installation, on purpose: every account can read the data files of the `shared` account by file name, and none can write them — see [The shared account](#the-shared-account-is-open-to-read-by-design) |
| The API | off (`APIPORT` unset in `sd.conf`) until an administrator turns it on — see [API access](09-api-access.html) |
| SDSYS from a listed user's own login on this computer | **off**: both lists (`local.sdsys ssh` and `local.sdsys api`) are empty. An administrator who lists a Windows user lets that user, from any session of theirs on this computer, become SDSYS with SDSYS's SD password; the Administrator set's *Reaching SDSYS from Your Own Login* says what that means and how to take a name off |
| SDSYS | no ssh sign-in as SDSYS, ever (a listed user's route from this computer is the row above); no API route from another computer until an administrator has opened that door for chosen addresses (`remote.sdsys api on`), and then its SD password stands between those addresses and the administrator — the one thing this page treats as non-negotiable rather than a default |
| The console and Remote Desktop | denied to every ordinary account (`sdsshonly`) — see [Accounts](05-account-types.html) |

**Only SDSYS administers SD.** No other account, whatever its Windows group
membership and whether or not it is elevated, can create, change or delete
accounts, grant `sh-on` or `os-on`, or catalog globally.

**An ssh session's reach is bounded by NTFS, not by SD.** Every file it
touches, inside SD or through a granted `sh` or `OS.EXECUTE`, is opened under
that user's own Windows token, so the account's file permissions are the
boundary.

**The administrator can open any of it up — `os-on`, `sdapi`, `sdssh` — and
that is a decision for their own environment, not a default to second-guess.**
Securing the transport and shipping a closed-by-default system is what this
installer is responsible for; what an administrator does with the accounts
they create afterward is theirs.

**Further hardening beyond the defaults is available, not built-in.** An
account can be locked into a single application by removing `basic` and
`run` from its own VOC (so it can neither compile nor run anything else)
and disabling its break key (`pterm break off`, so it cannot interrupt out
to a TCL prompt). Neither is a keyword on `create.account` — both are done
by hand, per account, when that account's whole purpose is one application
and nothing else.

## The shared account is open to read, by design

**The `shared` account that the installer makes is the one place where the
default is open rather than closed.** Every account, new or old, can open its
data files by file name (`shared.read` is on unless SDSYS turns it off with
`shared-read-off`), and none can write them until SDSYS gives it
`shared-write-on`. Nobody but SDSYS can sign on to `shared` or change the
structure of its files. So **anything placed in `shared` is readable by every
account that has not had the right taken away: put nothing in it that is not
meant for everyone.** An account with `sh-on` or `os-on` can also reach the
files from the operating system. The verbs, programs and catalog of `shared`
are never reached from another account. See [Accounts](05-account-types.html#the-shared-account).

## Signing in asks for no password

**The operating system has already authenticated you. SD asks Windows who you
are.**

| | |
|---|---|
| `sd`, no account named, Windows login `sdsys`, elevated | you land in **SDSYS** |
| `sd`, no account named, any other Windows login | you land in **the SD account with your own name** |
| no SD account of that name | refused — *Account %1 not in register* (5018) |
| not in `sdusers` | refused at the door — *not registered for SD use* (5009) |
| `sd -a<name>` | **refused unless `<name>` is your own account** (10051) |
| `logto sdsys` from any other account | **refused** to every session that did not sign in to Windows as `sdsys` at its desktop, whether or not it is elevated — 10002, audited `logto refused account=sdsys reason=sdsys is entered by its own session only`; the administrator's own session, having gone to another account, may `logto sdsys` to come back (audited as `logto account=sdsys`) |

**As delivered, SDSYS is reached one way only: sign in to Windows as the account literally
named `sdsys`, and run `sd` elevated.** (An administrator can list Windows users who may
also reach it from their own login on this computer; both lists are empty as delivered.)
Being a Windows administrator —
elevated or not — grants nothing by itself, and there is no route from any
other account into SDSYS once a session has started. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**SDSYS has its own Windows sign-in password**, set once during installation
in the window that appears after the wizard closes. It is an ordinary
Windows password, not something SD stores or checks — see
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**`sd <command>` never asks you to set a password.** It runs and exits, so it
is not a session anybody is being invited into. See
[Running SD](03-running-sd.html#the-command-line).

## Being a Windows administrator gets you nothing

**Being in the `Administrators` group, elevated or not, is not being an SD
administrator.** The one and only privileged account is SDSYS, reached the
one way described above. An elevated ordinary account starts `sd` faster —
no UAC prompt mid-session — but that is the whole of what elevation does for
it; every SD-level check is unchanged.

**This is deliberate and total, not a special case for remote sessions.**
SDSYS itself is refused ssh outright. The API is shut to SDSYS from every other
computer until the administrator opens that door for chosen addresses
(`remote.sdsys api on` *address*), and then only SDSYS's own SD password stands
between those addresses and the administrator; open it only for addresses you
trust, and shut it again (`remote.sdsys api off`) when it is not needed. On
this machine it is accepted by the local connection, from a program
signed in to Windows as SDSYS and elevated — see [ssh access](08-ssh-access.html)
and [API access](09-api-access.html). There is no "administrator, but only
locally" middle case.

## Taking an account out of use without deleting it

**`modify.account fred suspended`** denies entry at all three ways in — ssh and
the console, **`logto`**, and the API. It is reversible with nothing to
remember: the VOC and every Windows group membership are left exactly as they
are — suspending sets one field, unsuspending clears it.

**Understand what it is and is not, because the name oversells it.**

| | |
|---|---|
| **It is** | an SD control. The three doors SD owns are shut |
| **It is not** | a Windows control. Nothing is withdrawn there |

So a suspended user's ssh connection is still accepted and SD still starts
before refusing them. **SDSYS can still `logto` into a suspended account**,
which is deliberate — that is how you look at one.

**If you are suspending an account to contain somebody rather than to park
it, disable the Windows account too.** Everything on this page rests on
Windows identity; a control that does not touch Windows cannot be the whole
answer.

## Understand what the security position rests on

**NOTHING IN SD CHECKS A SECRET AT CONSOLE OR ssh LOGIN. ACCESS IS ENTIRELY
OPERATING-SYSTEM GROUP MEMBERSHIP.**

That is not a weakening. Every SD process opens the database directly, in your
own process, under your own token. There is no data server standing between
you and the files. So:

> **While SD runs as the invoking user, account passwords organize access; they
> do not secure it.**

A password gate inside SD is not a file security boundary. The old password
model implied one the filesystem never enforced. This states the real position
instead of dressing it up.

**Passwords still matter for the API**, which is a separate door and does
require one — see [API access](09-api-access.html).

## What actually protects the database

### The tree is private from the rest of the machine

`C:\ProgramData` grants `BUILTIN\Users` read and execute by inheritance, so the
Windows default is world-readable and snooping needs no privilege at all. The
installer **breaks inheritance first** and grants narrowly: SYSTEM,
`Administrators` and `sdusers`.

**This is the step that makes the data private, and nothing at run time
Substitutes for it.**

### Your account directory is locked to you

`C:\ProgramData\SD\user_accounts\<name>` is granted to that account's own
group, to administrators and to the system, **and to nobody else**.

Without that, every SD user could read and rewrite every other user's account
files from Explorer or a command prompt — outside SD, so none of SD's own
permission checks applied. SD refuses to let you **`logto`** an account
you are not a member of; this makes the files agree with that.

**Nothing you type changes, and your own account is unaffected** — you are a
member of its group.

> A directory whose Windows group has been removed is **skipped deliberately**
> and named in the report. Locking it to a group that no longer exists would
> take the account away from the person who owns it.

### The system directories are read-only to ordinary users

These parts of the SD data area are readable by everyone who needs them and
writable only by an administrator:

```
sdsys\accounts    the register of accounts
sdsys\$map        sdsys\messages    sdsys\newvoc     sdsys\voc
sdsys\bp          sdsys\cat         SD's own programs
sdsys\voc_template  sdsys\voc_removed  sdsys\voc_removed.saved
sdsys\config.table
sdsys\syscom      sdsys\terminfo    sdsys\terminfo.src  sdsys\helptext
sdsys\dir_dict    sdsys\licence     sdsys\contrib    sdsys\start.default
sdsys\agent-pack  sdsys\bp.out      sdsys\pcode.out  sdsys\stacks (SDSYS's command history)
sdsys\dict.dic    sdsys\voc.dic     sdsys\$map.dic   sdsys\accounts.dic
sdsys\$hold       sdsys\$hold.dic   (your held output is in your own account's $hold)
sd.conf           the configuration read at start-up
```

**The `sdsys` folder itself takes no new file from an ordinary user.** What is
already in it keeps the access it has, so the entries below still work.

**Nothing an ordinary user does needs to write them** — not the spooler, not
saved lists, not a phantom. The commands that *do* write them are already
administrator commands and are unaffected.

**Left writable by every SD user, deliberately:** `sdsys\$ipc`, `sdsys\errlog`
(every session adds to the error log) and `sdsys\prt` (the print queue).
`sdsys\dumps` and `sdsys\pstmp` have access lists of their own.

**`sdsys\$ipc` is deliberately unchanged.** Every session writes to it, and
it is how a **`phantom`** is given its command. **What a phantom takes from it is
sealed:** `phantom` gives the new process a secret in its environment and seals the
records with it, and the new process runs nothing from them unless the seal checks
(*Processes and phantoms* in the User's guide).

The global catalog and the pcode library are locked the same way.

> **Every install sets these, an upgrade included.** If the closing screen says
> one was NOT locked, it names the path; run this from an elevated prompt with
> that path:
>
> ```
> powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\secure-sysdirs.ps1" -Path "C:\ProgramData\SD\sdsys\accounts"
> ```
>
> For the `sdsys` folder itself, add `-KeepChildren`:
>
> ```
> powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\secure-sysdirs.ps1" -Path "C:\ProgramData\SD\sdsys" -KeepChildren
> ```

### `batch.jobs` is read-only to ordinary accounts

The allow-list [Scheduled jobs](04-scheduled-jobs.html) reads from is readable
by every SD user (needed, since `login` checks it on their behalf) and writable
only by an administrator: the installer locks it with the same script as the
other permit files. A user who could add a line to their own record would be
granting themselves the unattended command line.

### The credential file

**No password is stored in the file SD keeps account passwords in**: SD keeps a
scrambled verifier that cannot be turned back into a password. **Being able to
replace one would be enough to take over an account**, so the installer locks
the file to the administrators and SD's own service. To check it, from an
**ordinary** (not administrator) prompt:

```
icacls "C:\ProgramData\SD\sdsys\$CRED"
```

If that prints permissions, the file is open: reinstall. **If it says "Access is
denied", it is protected — which is what you want.**

## Continued in

[Security and the operating
system](12a-security-and-the-operating-system.html) — reaching the operating
system from inside SD, privileged work, and the audit trail.
