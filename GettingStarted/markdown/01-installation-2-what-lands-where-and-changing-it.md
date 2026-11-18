Title: Installing SD Core: What Lands Where and Changing It
Subtitle: Where the files go, what the installer creates, OpenSSH, the editors, and changing the choices afterwards.

This page continues [Installing SD Core](01-installation.html).

## What lands where

| What | Where | Was, on Linux |
|---|---|---|
| Binaries, and the MSYS2 DLLs beside them | `C:\Program Files\SD\usr\bin\` | `/usr/local/bin` |
| The changelog | `C:\Program Files\SD\changelog` | — |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |
| The SDSYS account | `C:\ProgramData\SD\sdsys\` | `/usr/local/sdsys` |
| User accounts | `C:\ProgramData\SD\user_accounts\` | `/home/sd/user_accounts` |
| Group accounts | `C:\ProgramData\SD\group_accounts\` | `/home/sd/group_accounts` |
| POSIX shared memory | `C:\ProgramData\SD\shm\` | `/dev/shm` |

**`usr\bin` is load-bearing, not tidiness.** Shipping `msys-2.0.dll` beside the
executable relocates the POSIX root to the DLL's directory minus two
components, so only that depth puts `/` on `C:\Program Files\SD\`. Do not move
the binaries.

**The DLLs ship beside `sd.exe` on purpose.** Do not change their location.

**The source is beside the installer, not installed.** SD Core is free
software under the GNU General Public License, version 3 or later. Its complete
source - the C, the system programs' BASIC (`gpl.bp`) and the build and
installer scripts - is `SDCore4Windows-source-<version>.zip` beside
`sd-setup-<version>.exe`, with a `.txt` file naming the commit it was built
from. The installer puts none of it on the machine: SDSYS holds the compiled
system programs (`gpl.bp.out`), and its VOC has no `gpl.bp` entry. An upgrade
removes the `gpl.bp` folder and VOC entry an earlier release installed.

### Configuration

Server and client both read `SD_CONFIG`, then fall back to
`%ProgramData%\SD\sd.conf`.

`sd.conf` is installed `onlyifdoesntexist` and marked never to uninstall, so
your edits survive both upgrade and removal.

## What the installer creates on the machine

| | |
|---|---|
| `sdusers` | grants access to the files under `C:\ProgramData\SD`. Everyone who uses SD needs it |
| `sdsshonly` | carries the two deny rights that confine an account to ssh. Every account **`create.account`** makes joins it, unconditionally |
| `sdu_<name>` | one per account, created by **`create.account`** |
| `sdg_shared` | the group of the **shared account**, which the installer makes: files that every account can open by name (the Administrator guide's "The Shared Account"). It has no members |
| `sdaiusers` | the AI gate: a person in it may use the AI provider SDSYS chooses. Made empty (the "open every access gate" box adds your own account) |
| the service | **String Database (SD)** |
| the AI helper service | **`sd-ai`** (*SD Core AI helper*), running as the virtual account `NT SERVICE\sd-ai`, with its folder `C:\ProgramData\SD\ai` (settings and keys) and its program in `C:\Program Files\SD\lib\sd-ai`. It sends nothing until SDSYS has chosen a provider and set a key |
| ACLs | inheritance is broken on `C:\ProgramData\SD` and access granted narrowly. This is what makes the database private from the rest of the machine |

**You must sign out and back in after being added to `sdusers`.** Windows
group membership is carried in your logon token. Until you get a new one, you
cannot read the data tree at all, and the symptom looks like a broken install.

## OpenSSH

**The OpenSSH server is installed only if you ask for it**, and the box is not
ticked. This section covers what happens when you do ask.

Accounts SD creates cannot log in to Windows, so they reach the machine over
ssh or through an API client. An installation offering neither is usable by
nobody but you — which is a legitimate choice, and worth making knowingly. A
local-only machine is served by `ssh localhost`, which needs no network.

**It is slow and it looks like a hang.** `Add-WindowsCapability` hands off to
`TiWorker` and can work for minutes with nothing on screen. **Never kill it** —
interrupting Windows servicing mid-flight is how the component store gets
corrupted. It may also leave a reboot pending, which is real; SD itself needs
none.

**If it cannot be installed, the install still succeeds.** It is a Features on
Demand capability and can be blocked by policy, a WSUS with no source, a
metered connection or an offline machine. The installer reports it in as many
words, with the command to retry — and you should read that report, because in
that state **no account but yours can sign in anywhere.**

It is the same command either way, and it is repeated here because the closing
report is easy to close. From an elevated prompt:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\install-ssh.ps1"
```

It exits **0** installed and running, **2** installed but Windows wants a
restart before the service exists, **1** failed — and it prints which, so run
it in a window you can read rather than expecting a log. It is safe to run
twice: on a machine that already has the server it says so and changes
nothing.

## The full-screen editors

**The installer makes sure the two terminal editors are on the machine**,
because the **`edit`** and **`micro`** verbs run them. It puts both beside
`sd.exe`, in `usr\bin` of the install folder, and the verbs run those copies
first. Neither is offered as a choice, for the same reason the ssh
server is not: an account with a verb that does nothing is worse than either
answer.

**If one is missing, the installer looks for it on the machine and then tries
winget; if it cannot be installed, the install still succeeds.** No winget, no
network or a policy in the way all end the same: SD is complete and one editor
verb is not — **`ed`**, the line editor, needs nothing. What happened is in
`C:\ProgramData\SD\install-editors.log`, and to do it by hand afterwards,
from an elevated prompt:

```
winget install -e --id Microsoft.Edit --scope machine
winget install -e --id zyedidia.micro --scope machine
```

**The scope is not optional.** Without it winget installs into the profile of
whoever ran it, and accounts SD creates cannot log in to Windows at all — so a
per-user copy is one they can never reach.

## Changing any of it afterwards

Every choice on the tasks page has a verb that changes it later, and that is
why an upgrade does not ask again. All four are SDSYS's — signed in to
Windows as SDSYS, elevated — and all four report when given no keyword:

| | |
|---|---|
| `ssh.server install` \| `remove` | add or remove the OpenSSH server |
| `remote.ssh on` \| `off` | who may reach it |
| `remote.api on` \| `local` \| `off` | whether SD opens its API socket, and who may reach it |
| `append.sd.path on` \| `off` | whether `sd` runs from any directory |

They are covered in the SD Core for Windows administrator documentation, under
*Remote access and the machine*.

`remote.api on`, `local` and `off` change the socket SD opens (on every address,
on `127.0.0.1` only, or none), which it decides at start-up, so they offer to
restart SD — and that restart ends every session including the one that asked.
An install whose API is not for other computers listens on `127.0.0.1` only.

The underlying scripts are still on the machine and can be run directly if you
prefer, from an elevated prompt:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\api-firewall.ps1" -Open
```

## At the end

The wizard's last page lists what Setup did, and any step that did not
complete with the command to run. There are no popups. The installer then
**finishes, and opens a window** with three steps in turn: the SDSYS password,
your own SD Core password if you have none yet, and the installation check. It
does not leave a wizard page waiting behind the session.

A Start Menu entry, **Check the SD installation**, runs the check again at any
time. It closes on a keypress.

## Continued in

[Installing SD Core: Warnings and Things to
Know](01-installation-3-warnings-and-things-to-know.html) — what to know
before you install, after the install, when a step reports that it did not
complete, and uninstalling.
