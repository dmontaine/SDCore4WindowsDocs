Title: Installing SD Core
Subtitle: What the installer does to the machine, the two kinds of installation, and the choices it puts in front of you.

There is no compiler to run and no dependency to resolve. SD Core for Windows
ships as a single `sd-setup-W1.1-3.exe`, carries its own runtime beside
`sd.exe`, and installs in one pass.

This is the largest single difference from the regular SD version — that, and
the fact that this version is for Windows and not Linux. In regular SD,
`installsdai.sh` existed because ScarletDME targeted four distributions and the
end user had to compile; Windows has one target and one ABI, so none of that
transfers.

## Before you start

**You need an elevated session.** The installer creates local groups, sets
file permissions, registers a service and assigns user rights. You can start
the install from a normal console session — you will get an elevation prompt.

**SD cannot be installed silently.** This is deliberate, not a missing
feature. The installer asks questions whose answers cannot be defaulted safely
— which kind of installation, whether to expose ports, and the password on the
account it makes for you.

**The installer does not ask where to put SD.** Both roots are fixed. See
[What lands where](01-installation-2-what-lands-where-and-changing-it.html#what-lands-where).

### It checks the machine before it changes anything

The installer refuses to start, and changes nothing, if it finds:

- another ssh server using port 22, or
- an ssh service that is not part of Windows, installed even if it is not
  running, or
- Windows' own ssh server with settings somebody has already changed.

It tells you what it finds — the service and its path, or the directive that
was added — so you can decide what to do. You may **remove the other ssh
server, or put the ssh configuration back the way Windows shipped it, and run
the installer again.**

Why it is this strict: accounts SD creates cannot log in to Windows at all, so
ssh is one of only two ways they reach the machine — and SD configures the ssh
server so those sessions land inside SD and cannot reach a command prompt. **SD
can only promise that about a server it installed and configured itself.**

## What you are asked

There is one kind of installation. What varies is how the machine can be
reached afterwards, and whether Python is installed with it — a few tick
boxes on one page.

The boxes appear only on a **first** install. An upgrade shows no tasks page at
all: the machine already carries the answers, and every one of these settings
has a command that changes it afterwards. The one exception is Python (see
*4. Python*), which an upgrade asks about on a page of its own.

### 1. System integration

| | Default |
|---|---|
| Add SD Core to the system PATH, so `sd` runs from any directory | **ticked** |

Changed afterwards with `append.sd.path on` or `off`.

### 2. The ssh server

**Installing an ssh server is optional, and the box is not ticked.** When the
`ssh-server` folder that comes with the installer is beside it, ticking the box
installs Microsoft's OpenSSH server from that folder as one step of the install,
with no network. Without that folder the server downloads from Windows Update,
which can take up to 30 minutes; the Ready to Install page and the progress line
say so before it starts.

What you see depends on what the machine already has:

| Machine | Boxes | Defaults |
|---|---|---|
| No ssh server | *Install the OpenSSH server*, and indented under it *Let other computers connect* | both unticked |
| Server present, firewall shut | *Let other computers connect* | unticked |
| Server present, firewall open | *Let other computers connect* | **ticked** |

The second box is a child of the first, so Windows grays it out until the
parent is ticked. You cannot ask for remote ssh access without an ssh server.

The last row matters on a machine that already uses ssh: the box shows the
**current** firewall scope, so leaving it alone changes nothing in either
direction. `OpenSSH-Server-In-TCP` is Windows' own shared rule and not SD's, so
defaulting it to unticked and applying that would silently loopback-lock the
ssh a site already relies on.

When the `ssh-server` folder was beside the installer, the installer keeps a copy
of Microsoft's OpenSSH installer (about 6.5 MB) in the SD folder, whether or not
the box was ticked, so that `ssh.server install` can install the server later
with no network.

Changed afterwards with `ssh.server install` or `remove`, and `remote.ssh on`
or `off`.

### 3. The API

| | Default |
|---|---|
| Provide the SD Core API (port 4247) | **unticked** |
| Let other computers on your network reach it | **unticked** |

**The API is off unless you ask for it.** Decline it and SD is installed with a
configuration carrying no `APIPORT` line, so no socket is opened at all — not a
listener behind a closed firewall, but no listener.

Again the second box is a child of the first. The pair appears only when there
is no existing configuration file to read the answer from.

Changed afterwards with `remote.api on`, `local` or `off`.

### 4. Python

| | Default |
|---|---|
| Install Python for all users | **unticked** |

**Python is needed only for SD BASIC's `PY_` functions.** The release zip
carries python.org's own Python installer in its `python\` folder, so nothing
is downloaded. The box appears only when that folder is beside the installer
and the machine has no all-users Python 3.13 or later already. Ticked, it
installs Python for every user of the computer and adds it to the system PATH.

**An upgrade asks the same question** on a page of its own, because it shows no
tasks page. That page appears only when the `python\` folder is beside the
installer and no all-users Python 3.13 or later is registered; the box is
**unticked**. An upgrade from a release that had no Python support is therefore
asked once. A silent upgrade shows no page and asks nothing.

Python is a separate product with its own entry in *Apps*; uninstalling SD Core
leaves it in place.

### The AI helper (no box)

**The AI helper needs no Python.** Every install and upgrade sets up the
Windows service `sd-ai`, which is the only part of SD that talks to an AI
provider; the AI is off as delivered. To set the service up again, run this in
an **elevated** PowerShell window:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\install-aihelper.ps1" -Install
```

It exits 0 when the helper is running; its log is
`C:\ProgramData\SD\install-aihelper.log`. The
service sends nothing until SDSYS has chosen a provider and set its key and an
account has its `ai` gate: the Administrator set's *The AI Helper* says how, and
what leaves the machine.

### 5. Your own account's access gates

One box, unticked. A first install makes an SD account for the Windows user who runs it. **Like every
SD account it starts with every access gate closed:** no ssh, no API, no shell
(`sh`), no `os.execute`, no `sd.accounts`, no right to save a change to a VOC, a
program file or a dictionary, no SDNet, no writing the shared account's files, no
files-only login, no administering files over that login, no use of the AI, no
pins on the home screen, no recovery copy of unsaved editor text, no file transfer
(`receive` and `send`). Tick the box and the installer opens every one of those on your account,
reads the result back, and the last screen says whether they all opened; if any
did not, `C:\ProgramData\SD\attach-account.log` names each one and the word to
give for it. It opens only your account. `files-admin-on` administers files on
this server over the files-only login, and `ai-on` lets your account send text
to the AI provider SDSYS chooses (nothing is sent until a provider and its key
are set), so tick the box only on a machine where you want both. File transfer also needs `XFER=1` in
`sd.conf`, which the box does not set: the account's switch alone moves nothing. A silent install ticks it with `/TASKS=opengates`. An upgrade does
not show the box and leaves the account as it is.

SDSYS opens a gate afterwards with `modify.account` *account* *word*, one word at a
time or several together: `both` (ssh and the API), `sh-on`, `os-on`, `sd-on`,
`voc-on`, `bp-on`, `dict-on`, `net-on`, `shared-write-on`, `files-on`,
`files-write-on`, `files-admin-on` (it needs the two before it), `ai-on`, `pins-on` and
`recovery-on`. The same word with `-off` closes it again (`none` closes ssh and the API).
Which computers can reach SD from the network is still decided by boxes 2 and 3.

### 6. Where new sessions start

One box in group 5, *Start new sessions at the command prompt, not the home
screen*, unticked. Unticked, a session that signs on opens the full-screen home
screen of tiles, and its Terminal tile gives the command prompt; ticked, a session
signs on at the `:` prompt and `HOME` opens the home screen. This sets the system default only: SDSYS changes it later
with `set.start.default menu` or `set.start.default terminal`, and an account
can have a start of its own (`modify.account` *account* `start-menu`,
`start-terminal` or `start-default`). SDSYS itself always starts at the command
prompt. A silent install chooses the command prompt with `/TASKS=startprompt`. An
upgrade does not show the choice and keeps the start the system already has. If
the command prompt was chosen and could not be set, the last screen says so and
`C:\ProgramData\SD\set-start-default.log` says why.

### An installation with neither is a supported choice

Leaving every remote box unticked gives a working SD that nothing outside the
machine can reach. That is a real deployment rather than a degraded one.

**Be aware of what it means for accounts.** Accounts SD creates are denied the
Windows console and Remote Desktop, so they reach SD over ssh or over the API
and nothing else — including at this keyboard, where an ssh account arrives by
`ssh localhost`. With no ssh server on the machine, `create.account … ssh` and
`… both` are refused, because the account could sign in nowhere. `api` and
`none` still work, and `none` is meaningful: an application account reached only
by `logto`.

The refusal is tested against the machine when you type the command, not
against a decision recorded at install time. Install an ssh server later and
`create.account … ssh` simply starts working.

## Continued in

[Installing SD Core: What Lands Where and Changing
It](01-installation-2-what-lands-where-and-changing-it.html) — where the files
go, what the installer creates, OpenSSH, the full-screen editors, changing any
of it afterwards, and the end of the installation.
