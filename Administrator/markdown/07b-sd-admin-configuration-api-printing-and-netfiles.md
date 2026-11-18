Title: Configuration: The API, Printing and the Rest
Subtitle: The parameters for the API, file transfer, printing, sorting, diagnostics, the screen, the shell, NETDIRS and NETFILES.

This page continues [Configuration: Changing a Parameter from
SD](07a-sd-admin-configuration-changing-from-sd.html).

## The API

| Parameter | Default | Effect |
|---|---|---|
| `APILOCAL` | unset (0) | 1 makes the API listener (`APIPORT`) listen on `127.0.0.1` only, so only this computer can reach it; 0 or no line, every address. `remote.api local` writes it and `remote.api on` takes it away (see *Remote Access and the Machine*) |
| `APIPORT` | 4247 | Switches the API on. Any number above zero means on, and SD listens on port 4247 whatever the number is; the port cannot be changed. If the line is absent no socket is created at all, which is how the API is turned off. A file that says `APIPORT=4243` still means on |
| `BACKUPDIR` | unset | The folder `backup.account` and `restore.account` use. Set by `set.backup.directory`, not by hand - see [Backing Up and Restoring Accounts](01b-backup-and-restore.html) |
| `NETDIRS` | unset | Directories outside any account that an account without `os-on` may still open by path (every session), separated by semicolons because a Windows path contains a colon; see *`NETDIRS`: directories outside an account*, below |
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright (no file can be opened, so no dictionary can be evaluated either), refuses `SDIConv`, `SDOConv`, `SDIConvs` and `SDOConvs` a conversion code that reads a file (`T` with a file) or calls a program (`U`), and refuses `SDOpenSeq`, `SDExecute`, `SDTrans` and `SDRTrans`; `2` additionally refuses any subroutine not compiled as callable from a client |

Unset is the strict value for `NETDIRS`. With nothing there, an API session can
open files in the account it is standing in and nothing else. It never grants
the credential store, the global catalog, `os.users` or the account register,
and naming those has no effect. **An API session's file access is its own
account's, widened only by `NETDIRS`** (below, *`NETDIRS`: directories outside
an account*), which names directories every account without `os-on` may
additionally open, the API session's included. A directory listed there is
reachable by every such session in every account, so it is a decision about the
machine rather than about one account.

`SDCLIENT` is not reported by the `config` verb and has no entry in the shipped
`sd.conf`. It defaults to 0, which permits everything.

## File transfer over ssh

File transfer lets a person move plain-text files (CSV, JSON, BASIC source, any
text) into and out of their own account with an sftp client over the same ssh
login they use for SD. It is delivered off twice: `XFER` below is the system's
switch, and each account also needs `modify.account <account> xfer-on`. Both
must be on before anything can be transferred. **Turning them on lets that
person put files into, and take copies out of, their account from another
machine**, with the `receive` and `send` commands and an sftp client; what
that opens and how it is confined is in *Accounts and Security: File
transfer*. The parameters are read by each process as it starts, so a change
is seen by the next session and the next connection without restarting SD.

| Parameter | Default | Effect |
|---|---|---|
| `XFER` | 0 | `1` lets accounts that have `xfer-on` transfer files; `0` refuses every transfer |
| `XFERFILE` | 10240 | The largest file one transfer slot takes, in kilobytes (1 to 1048576) |
| `XFERSLOT` | 102400 | The most one slot takes in all its files, in kilobytes (1 to 4194304) |
| `XFERWAIT` | 600 | Seconds a slot waits for the sftp client's first connection (10 to 3600) |
| `XFERIDLE` | 120 | Seconds a slot stays open with nothing happening after a client has connected (10 to 3600). A file being sent keeps it open; one left half sent and silent this long is dropped |
| `XFERMAX` | 3600 | Seconds a slot may stay open at most; `0` removes the ceiling (0 to 86400). At the ceiling the transfer ends and a file that is not complete is dropped |
| `XFERKIND` | blank | The extensions a received file must have, separated by commas; blank takes any plain-text file (no NUL byte and no SD mark byte) |

None of them can be changed from `tool.config` or `set.config`; edit
`C:\ProgramData\SD\sd.conf` by hand (in an elevated editor). `config('XFER')` and the others read them.

## Printing

| Parameter | Default | Effect |
|---|---|---|
| `LPTRWIDE` | 80 | Default page width for the printer. Range 10 to 1000 |
| `LPTRHIGH` | 66 | Default page depth for the printer. Range 10 to 32767 |
| `SPOOLER` | empty | The Windows printer a print job goes to when `setptr` names none (`at` wins); empty is the Windows default printer |

## Sorting

| Parameter | Default | Effect |
|---|---|---|
| `SORTMEM` | 4096 kb | Above this much data a sort works on disk instead of in memory |
| `SORTMRG` | 4 | Files merged at once in a disk sort. Range 2 to 10 |

## Numbers and dates

| Parameter | Default | Effect |
|---|---|---|
| `INTPREC` | 11 | Digits of precision in integer arithmetic. Range 0 to 14 |
| `FLTDIFF` | 0.00000000002910 | Two floating point numbers closer together than this compare equal |
| `YEARBASE` | 1930 | The century a two-digit year is read into |

## Diagnostics

| Parameter | Default | Effect |
|---|---|---|
| `ERRLOG` | 50 kb | Size of the error log. A non-zero value below 10 KB is raised to 10 KB, and the oldest entries are discarded when it fills |
| `PDUMP` | 0 | Bit flags controlling when a process dump is written |
| `DEBUG` | unset | Bit flags enabling debugging features |
| `OBJECTS` | 0 (no limit) | Compiled programs held in memory at once |
| `OBJMEM` | 0 (no limit) | Memory those programs may occupy, in KB |

There is no `STARTUP` parameter. A line that names it stops SD from starting, with
a message that says to remove the line.

## The screen

| Parameter | Default | Effect |
|---|---|---|
| `SCREENTHEME` | unset (`mono`); `paper` in the shipped `sd.conf` | The color theme that a program using the `SCREEN` statement gets when it does not choose one: `paper`, `night`, `mono`, `classic` or `blue`. `paper` is black and dark blue text on light gray, with the menu bar and menus the other way round (light gray on black); `night` is white and yellow text on black, its menus black on light gray; `mono` uses only reverse video, underline and bold and reads on any terminal. The shipped `sd.conf` says `SCREENTHEME=paper`, so the toolkit pages and any program that opens a screen show paper on a color terminal on a fresh install; the IDE, SED and the debugger follow it too (the IDE falls back to paper for a name that is not a theme). On an upgrade that keeps the configuration, the installer adds `SCREENTHEME=paper` to a restored `sd.conf` that has no `SCREENTHEME` line, and changes a restored `SCREENTHEME=blue` (the delivered theme before W2.0-0) to `paper` once, leaving a comment line in the file that says so; set `SCREENTHEME=blue` again afterwards to keep the old look, and later installs leave it. Any other line, `mono` included, is left alone. A terminal with no color (a phantom, a pipe) is `mono` whatever the line says, and so is a name that is not a theme, without an error. A program that asks for a theme gets that one. A program reads the value with `config('SCREENTHEME')`. **A person's own choice wins for that person**: Ctrl-T or View > Theme on any full-screen program keeps the theme chosen as the record `theme.`*login name* of the file `&menus&` in the account they are in, and every full-screen program starts in it from then on; `SCREENTHEME` is what a person who has never chosen sees. To give someone the site's theme again, delete that record |

## The shell

| Parameter | Default | Effect |
|---|---|---|
| `SH` | PowerShell, interactive | The shell a bare `sh` starts |
| `SH1` | PowerShell, non-interactive | The shell `sh command` uses |

Both are full paths on a real install:

```
SH        C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NoLogo
SH1       C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command
```

**A value longer than 255 characters for `SH` or `SH1` stops SD** with "SH value is
longer than 255 characters." (or `SH1`). A value that fits is unchanged.

**Both run at the account's own Windows permissions, and only for an account
that has the `sh-on` switch** (see *Accounts and Security*, "The
operating-system switches: `sh-on` and `os-on`"). The difference between them
matters: `SH1` carries `-NonInteractive` and `SH` does not, so a bare `sh` in a
phantom or a scheduled job hands control to a shell with nobody at the keyboard.
Operating system access has its own page in this set.

## `NETDIRS`: directories outside an account

An account that has not been given `os-on` is held to its own directory: it
opens no file by pathname anywhere else. `NETDIRS` names directories that such
an account may reach all the same, for a site whose data lives in a shared
directory outside every account:

```
NETDIRS=D:\Data\Sales;D:\Data\Shared
```

The entries are absolute paths separated by semicolons (a Windows path holds a
colon). **Nothing is listed as delivered**: `sd.conf` has no `NETDIRS` line, and
every account is held to its own directory as before.

**What filling it opens.** Every account without `os-on`, on every route (a
terminal session, a phantom, the API), can then read, change, create and delete
files in the listed directories and below them, by pathname: `openseq`,
`openpath`, `dir()`, `select.dir`, `ospath`, `deleteseq`, a print file, an `f`
pointer in its VOC. The Windows permissions of the account's own user still apply. It is a smaller thing to open
than `os-on`, which opens the whole machine to one account, but it is opened for
every account at once: list only directories that hold nothing one account must
keep from another.

**What it does not open.** `sh` and `os.execute`, the edit gates (`voc-on`,
`bp-on`, `dict-on`), the shared account's rules and what the `ai` line may send
are separate and unchanged. The administrator and an account with `os-on` are
not affected: they reach every path already. `NETDIRS` is asked last: after the
account's own directory and the shared `SDSYS` entries, and after the `os-on` and
`sd-on` gates.

**Entries SD ignores.** An entry is left out, and named in the error log when SD
starts, when it is not an absolute path, is not an existing directory, is the
root of a drive, is the root of a network share (`\\server\share` or `//server/share`, with nothing below the share:
it holds a whole volume, as a drive root does), or holds or lies inside the SD system directory, the directory
of `sd.conf`, the user or group accounts directory (`USRDIR`, `GRPDIR`), or the
directory of any registered account. An account created later inside a listed
directory closes that entry at once. At most 16 entries are taken.

**How a path is judged.** The name a program gives is resolved first, and a
name that still holds a `.` or `..` component is refused, and so is a name SD
cannot resolve (a link that leads nowhere, say). It is then compared
with each entry ignoring upper and lower case, and the whole folder name must
match: `D:\Data\xkey` is not inside `D:\Data\x`.

A session reads the line when it starts, so a change reaches the sessions started
after it; no restart is needed. **A value longer than 191 characters is refused, by name**: SD does not
start, and a new session does not begin, with
`NETDIRS value is longer than 191 characters.` It is never cut, because
a cut path is a shorter directory and would admit more than you wrote. It is not
shown by `config()`, and `config('NETDIRS')` does not read it: read the file.

One API route is not widened: request 29, the old remote open of an account's
file that `NETFILES` gates (below). A pointer followed there must still lead
inside the account, whatever `NETDIRS` lists.

## `NETFILES` and SDNet

**`NETFILES` is not what SDNet uses.**
SDNet is the way a program opens a file that lives on another SD server: a VOC
entry of type `N`, a server you define with `set.server`, and a per-account
`net-on` switch, all off until SDSYS turns them on. It is built and is
described on the SDNet page of this set. None of it reads `NETFILES`,
and the older SDNet (a `server;file` VOC
entry, with each server's password in `sd.conf`) does not exist: that form of
name is refused. `NETFILES` is parsed, stored, shown by `config` and readable
with `config('NETFILES')`. **One
thing reads it:** the API server's request 29, "open an SDNet
file", answers "Remote server disallowed access" (7009) unless bit 2 of
`NETFILES` is set, and the files-only API route refuses request 29 whatever the
value is. **`NETDIRS` does not widen this request**: a pointer followed there must
still lead inside the account, whatever `NETDIRS` lists. **Setting the bit is not enough.** The request also refuses unless
`SDCLIENT` is 0, the account has a register record (a path names none), the
caller may enter the account by the same rule as `logto` (a member of its
group, the account not suspended, the reason never told to the caller), and
the account's `net-on` switch is on (SDSYS's own account excepted). It also asks the
operating-system question of the file the VOC names: a file pointer that leads out of
the account's folder is followed only if the account holds `os-on` (see *Accounts and
Security*, the VOC pointers section). Each
refusal is on the audit trail as `api refused request=29 reason=...`. The value
is 0 unless `sd.conf` sets it, and the installer does not, so the request is
refused as delivered. Leave it at 0: no client function in this set sends
request 29.

There is no `FILERULE` parameter. **The
`account:file` form of a file name is always available** (for programs moved from openQM): a name that is in no VOC record and has one colon,
such as `open 'sales:orders'`, opens that account's file exactly as a Q-pointer to it
would, with the same checks: the account must be registered, the person must be able
to `logto` it, and it must not be suspended. It reaches nothing a Q-pointer could not.
A drive-letter pathname such as `C:\data\x` has one colon too; it is read as account
`C`, which is not registered, so it is not found. The `path:` form is gone, and so is
the old `system:account:file` form. To reach a directory outside the accounts, put an
F-pointer in the VOC, where the operating-system access switches apply to it. A
Q-pointer whose fourth field names another system is refused with status 3003 and is
not opened as a local file.

There is no license parameter and no license verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
license text.
