Title: Other hardening
Subtitle: The catalog and pcode locks, the logs, line endings, and the rest of the smaller changes.

Everything on this page is a change you may notice while testing, grouped by
what it touches. The identity model and the file permissions are on
[Security](12-security.html); this is the remainder.

## The global catalog

**Adding to or removing from the system-wide catalog requires SDSYS,
whichever way you ask for it.**

This matters because the system-wide catalog holds the programs SD runs for
everybody, `$login` among them. **Replacing one runs your code in every session
on the machine, SDSYS included; deleting one stops everybody signing
in.**

**Nothing changes for local and private cataloging**, which is what
programmers use day to day:

```
catalog bp myprog          private catalog, this account
catalog bp myprog local    this account's VOC
```

Both still work, in any account you are allowed to **`logto`** into. The only thing
an ordinary user can no longer do is catalog a program whose name starts with
`!`, `_` or `$` — those characters mean *system-wide*. Name it without
one.

**To catalog system-wide you need to be SDSYS** — sign in to Windows as
SDSYS and start `sd` elevated. There is no other route in to try instead.

## The pcode library

`<sysdir>\bin` holds the pcode library — the interpreter itself, which SD loads
into shared memory at start-up and every session then runs.

It is readable by SD users and writable only by administrators, so that no SD
user can replace what everybody else's session executes, including an
administrator's. Nothing
needs to write it after an install — only the process that starts SD reads it,
and that is already elevated. **Anything that writes into
`<sysdir>\bin` is refused unless it runs elevated.**

## Scheduled jobs

A scheduled task can run an SD command without administrator rights, and only
the commands an administrator has named for it. The permit list is the SDSYS
file `batch.jobs`, locked read-only to SD users by the same control that locks
the other permit files.

It has its own page: **[Scheduled jobs](04-scheduled-jobs.html)**.

## The logs

There are three, and they are not interchangeable.

| File | Where | For |
|---|---|---|
| `audit` | `C:\ProgramData\SD\sdsys` | **who did what** — logins, refusals, **`logto`**, grants. See [Security and the operating system](12a-security-and-the-operating-system.html#the-audit-trail) |
| `errlog` | `C:\ProgramData\SD\sdsys` | diagnostics, and API connection records |
| `sd-elevate.log` | `C:\ProgramData\SD` | **what the elevation helper actually did** |

### `sd-elevate.log`

It records when a helper started for a session, each script it was asked to
run, the exit code that came back, and when it stopped.

**Only administrators can read or write it.** Ordinary SD users are not on
its permissions at all. That is different from the audit trail, which SD users
*can* add to because SD writes it as them; nothing unelevated ever writes this
one.

**It is a diagnostic, not the audit trail.** For *who obtained privilege and
when*, read `audit`. This file answers *"the account was not created — what
actually happened"*.

**If the file is missing, nothing is logged and SD does not create one.** That
is deliberate: a log created on the fly would inherit permissions letting every
SD user rewrite it, and **a record of privileged work that its own subjects can
edit is worse than none.** A reinstall keeps whatever is already there.

### The error log records who connects to the API port

Every accepted API connection adds a line naming the Windows process and
account at the other end:

```
API connection from 127.0.0.1:59314 - pid 11448, DESKTOP-1\sam
```

**Nothing is refused on the strength of it.** This records who connected; it
does not decide who may. The API's own checks are unchanged.

**A connection forwarded over ssh shows `sshd`, not the person at the far
end.** The tunnel ends on this machine, so the process that connects genuinely
is `sshd`. What the line distinguishes is a client running *on* this machine
from one arriving through a tunnel; **it cannot name a remote person.**

> **This matters beyond the log.** SD admits an administrator's API session
> from another computer only from an address the administrator listed, and it
> decides that from the address the connection came from. A tunnelled
> connection arrives from `127.0.0.1` because it really does start here, so it
> is treated as this computer: the addresses of that door never admit it, and
> it is SDSYS only if the process that connects runs as a Windows user the
> administrator listed with `local.sdsys api`. A listed user's tunnel is that
> user. If that matters to you, keep the list empty and turn port forwarding
> off in `sshd_config`; no check inside SD can see through a tunnel.

**Listed users are a third way to SDSYS, and it is off as delivered.** The administrator can list
Windows users (`local.sdsys ssh add`, `local.sdsys api add`) who may become SDSYS from this computer
with SDSYS's SD password. Both lists are empty until someone lists a name. A connection from
`127.0.0.1` is admitted as SDSYS only for a program SD identifies, in the way this line does, as
running as a listed user, and never by the addresses of `remote.sdsys api`. List only your own
administrator login, and check with `local.sdsys` that the lists say what you expect.

*"peer process not identified"* means the client had already gone by the time
the connection was looked up. It is not an error and the connection proceeds
normally.

### Two things about error-log trimming

**`ERRLOG` applies to these lines too.** The background daemon writes an entry
per connection, and discards the oldest part of the log on reaching the
`ERRLOG` size in `sd.conf`. **If you have set `ERRLOG`
unusually large, consider what an entry per connection adds to it.**

**After the log is trimmed, its first line may have no timestamp.** An entry
is two lines — a timestamped header and the message indented below it — and
trimming restarts the file at a **line**, not at an entry, so the first message
can be left without its header. **This is not damage** and no entry after it is
affected.

## Line endings

Reading and writing follow separate rules.

### Reading — files edited in Notepad or saved from Excel

Directory files exist so you can edit their records with an ordinary Windows
editor, and Windows editors end each line with CR+LF. **SD takes the CR+LF
pair as the end of a line**, so the CR is not left on the end of the data: a
CSV saved by Excel reads cleanly in its last column, and `READCSV`, `READSEQ`
and reading a directory file record all behave the same way.

**A CR on its own is data** and is left exactly as it is. Only the CR+LF
pair that ends a line is treated as a line ending, so this cannot alter data
that happens to contain a CR.

### Writing

Anything SD writes that an ordinary Windows program can open ends its lines
with CR+LF: records in a directory file, `WRITESEQ` and `WRITECSV` output,
command output captured with `COMO`, printer output sent to a file, and the
error log.

SD's CSV statements are documented as following RFC 4180, and **that standard
asks for CR+LF.**

**Dynamic files are unaffected** — they are stored in SD's own format and are
not readable by other programs.

**A file can contain both endings**, because SD does not rewrite what is
already there. SD reads either, so this is untidy rather than a problem.

## The terminal

**The default terminal type is `windows`.** `term` on its own should say
`Device : windows`.

A terminal has two spellings for an arrow key: in its ordinary state it sends
`ESC [ D` for Left, and the other spelling `ESC O D` only after the application
asks it to switch — **which SD never does.** The shipped `windows` definition
lists the first spelling, the one cmd, PowerShell and Windows Terminal send; it
is an exact copy of `linux`, because what matters is the byte protocol, not the
name of an operating system.

**An account keeps the terminal setting in its VOC** until that VOC is updated;
an upgrade runs `update.accounts` for you, and you can run it yourself. Until
then, `term windows` sets it for the session. **26 definitions ship, compiling
to 37 terminal names** — the extra names are aliases such as `vt200` and
`wyse60` — so `term wyse60` still works.

**A name that is not installed is refused and your current type is kept** —
*"Unrecognized terminal name"* — so a typo costs you nothing. **`term` with no
argument reports the type actually in force**, which is how to check.

Watch for near-misses all the same. There is no `vt320` definition; `vt220`
or `xterm` does the same job. `terminfo.src` ships with SD, so `sdtic` can add
a definition that is not there.

**Backspace works**, at the prompt and when you are asked for a password.

### The page is 140 × 43, not 80 × 24

**SD's default terminal size is 140 columns by 43 lines.** **A console window narrower than that makes wide reports
look wrapped or truncated**, which reads as a formatting bug and is not one. SD's
own full-screen programs (`sed`, `ced`, `ide`, the home screen) want at least
140 columns by 43 lines and refuse a smaller window.

`term` reports the size in force, above the `Device` line:

```
:term
Page width: 140
Page depth: 43
Device    : windows
```

**The size is worked out at login**, in this order: the `LINES` and `COLUMNS`
environment variables if they are numeric, otherwise the terminfo entry's
`lines` and `cols`, **otherwise 43 and 140** — then raised to a minimum of
10 × 20 if smaller. So a console or ssh session normally gets its real window
size and 140 × 43 is the fallback when nothing answers, which is the case for a
phantom or a piped script.

> **`term default` restores it, and it prints nothing when it does.** It sets
> the same 140 × 43 the login path falls back to and returns silently, so run a
> bare `term` after it to see the result. `term 120,36` does the same by hand
> for the old size.

## Paths

**A Windows PATH typed at the command prompt is read whole.** `C:\Data\Sales`
is one path, so `create.account other`, which is given a folder to put the
account in, puts it there.

Forward slashes work too. **Both are read the same way.**

## PowerShell execution policy — leave it alone

This is a hardening page, so it is worth saying plainly: **tightening your
PowerShell execution policy does not break SD, and loosening it does not help
SD.** Set it to whatever your own security policy wants.

SD does a lot of its Windows-side work — `create.account`, `append.sd.path`,
`remote.api`, `remote.ssh` and the editor verbs — by running a small
PowerShell script that the installer put in `C:\Program Files\SD`. Each one is
launched with `-ExecutionPolicy Bypass` **on that single command line**, which
applies to that one process and that one script. It does not change the
machine, and it does not affect any other script you or anyone else runs.

**If you loosened the policy to get SD working, put it back.** SD's scripts do not
need it. The `sh` verb still gives
you a PowerShell prompt under your machine's own policy — SD lifts the
restriction only for the scripts it installed itself, never for a shell you
type into.

**The one case that does stop SD is Group Policy.** A policy that sets the
execution policy outranks anything a program can pass on a command line. Run
`Get-ExecutionPolicy -List`: if `MachinePolicy` or `UserPolicy` reads
`Restricted` or `AllSigned`, SD's administrative commands will fail and only
your Windows administrator can change it. `Undefined`, `RemoteSigned`,
`Unrestricted` or `Bypass` on those two rows are all fine. **The Installed
Scripts page in the Administrator set has the detail.**

## Running SD

| | |
|---|---|
| The service | **String Database (SD)** |
| After an unclean shutdown | SD starts anyway, once the daemon's own liveness — not just the segment's presence — is checked. See [Running SD](03-running-sd.html) |
| Nested sessions | SD will not start a second time inside itself — see [Running SD](03-running-sd.html) |
| `sd <command>` | needs an elevated session, or an entry in `batch.jobs` — see above |
| End of piped input | ends the session — at the command prompt, at `PAUSE` and at the Ctrl-R search |

## Setting no password

The end of the installer and SD's own prompt say what no password costs.
Without a password you cannot use ssh or the API, **and that is stronger than
"some things will not work":** with no password the
account can be used **only at that computer** — at the keyboard, or through
Remote Desktop or similar remote-control software — **and only from a session
run as administrator.**

You can still choose it, and SD asks again the next time you open the account.
