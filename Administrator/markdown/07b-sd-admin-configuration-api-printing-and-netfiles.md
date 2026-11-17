Title: Configuration: The API, Printing and the Rest
Subtitle: The parameters for the API, file transfer, printing, sorting, diagnostics, the screen, the shell, and NETFILES.

This page continues [Configuration: Changing a Parameter from
SD](07a-sd-admin-configuration-changing-from-sd.html).

## The API

| Parameter | Default | Effect |
|---|---|---|
| `APILOCAL` | unset (0) | 1 makes the API listener (`APIPORT`) listen on `127.0.0.1` only, so only this computer can reach it; 0 or no line, every address. `remote.api local` writes it and `remote.api on` takes it away (see *Remote Access and the Machine*) |
| `APIPORT` | 4247 | Switches the API on. Any number above zero means on, and SD listens on port 4247 whatever the number is; the port cannot be changed. If the line is absent no socket is created at all, which is how the API is turned off. A file that says `APIPORT=4243` still means on |
| `BACKUPDIR` | unset | The folder `backup.account` and `restore.account` use. Set by `set.backup.directory`, not by hand - see [Backing Up and Restoring Accounts](01b-backup-and-restore.html) |
| `NETDIRS` | unset | Directories outside any account that an account without `os-on` may still open by path (every session), separated by semicolons because a Windows path contains a colon |
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright (no file can be opened, so no dictionary can be evaluated either), refuses `SDIConv`, `SDOConv`, `SDIConvs` and `SDOConvs` a conversion code that reads a file (`T` with a file) or calls a program (`U`), and refuses `SDOpenSeq`, `SDExecute`, `SDTrans` and `SDRTrans`; `2` additionally refuses any subroutine not compiled as callable from a client |

Unset is the strict value for `NETDIRS`. With nothing there, an API session can
open files in the account it is standing in and nothing else. It never grants
the credential store, the global catalog, `os.users` or the account register,
and naming those has no effect. A directory listed here is reachable by every
API session in every account, so it is a decision about the machine rather than
about one account.

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
| `SPOOLER` | empty | The Windows printer a print job goes to when `setptr` names none (`at` wins); empty is the Windows default printer. On SD Core for Linux it is the spooler command instead |

## Sorting

| Parameter | Default | Effect |
|---|---|---|
| `SORTMEM` | 4096 kb | Above this much data a sort works on disk instead of in memory |
| `SORTMRG` | 4 | Files merged at once in a disk sort. Range 2 to 10 |

## Numbers and dates

| Parameter | Default | Effect |
|---|---|---|
| `INTPREC` | 13 | Digits of precision in integer arithmetic. Range 0 to 14 |
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

`STARTUP` (a command run when SD starts) was removed in W1.1-3. It never ran. A
line that still has it stops SD from starting, with a message that says to remove
the line.

## The screen

| Parameter | Default | Effect |
|---|---|---|
| `SCREENTHEME` | unset (`mono`); `paper` in the shipped `sd.conf` | The color theme that a program using the `SCREEN` statement gets when it does not choose one: `paper`, `night`, `mono`, `classic` or `blue`. `paper` is black and dark blue text on light gray, with the menu bar and menus the other way round (light gray on black); `night` is white and yellow text on black, its menus black on light gray; `mono` uses only reverse video, underline and bold and reads on any terminal. The shipped `sd.conf` says `SCREENTHEME=paper`, so the toolkit pages and any program that opens a screen show paper on a color terminal on a fresh install; the IDE, SED and the debugger follow it too (the IDE falls back to paper for a name that is not a theme). A terminal with no color (a phantom, a pipe) is `mono` whatever the line says, and so is a name that is not a theme, without an error. A program that asks for a theme gets that one. A program reads the value with `config('SCREENTHEME')`. **A person's own choice wins for that person**: Ctrl-T or View > Theme on any full-screen program keeps the theme chosen as the record `theme.`*login name* of the file `&menus&` in the account they are in, and every full-screen program starts in it from then on; `SCREENTHEME` is what a person who has never chosen sees. To give someone the site's theme again, delete that record |

## The shell

| Parameter | Default | Effect |
|---|---|---|
| `SH` | PowerShell, interactive | The shell a bare `sh` starts |
| `SH1` | PowerShell, non-interactive | The shell `sh command` uses |

Both are full paths on a real install:

```
SH        C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NoLogo
SH1       C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -Command
```

**Both run at the account's own Windows permissions, and only for an account
that has the `sh-on` switch** (see *Accounts and Security*, "The
operating-system switches: `sh-on` and `os-on`"). The difference between them
matters: `SH1` carries `-NonInteractive` and `SH` does not, so a bare `sh` in a
phantom or a scheduled job hands control to a shell with nobody at the keyboard.
Operating system access has its own page in this set.

## `NETFILES` and SDNet

**`NETFILES` is not what SDNet uses.** A `server;file` VOC reference is
refused whatever it holds (the old SDNet is gone), and the value is parsed,
stored, shown by `config` and readable with `config('NETFILES')`. **One thing
still reads it:** the API server's request 29, "open an SDNet file", which
opens the file that a VOC entry of the named account names, for a client that
has signed in. It is refused unless bit 2 of `NETFILES` is set. The delivered
value is 0, so as delivered the request is refused; leave it at 0 unless an API
client needs it. With bit 2 set the request is still refused unless the
account's NET switch is on (`net-on`, off as delivered), and under `SDCLIENT`;
when it opens the file, the connection's containment applies: only the account
the session stands in, the shared `SDSYS` entries (read only) and the
directories named in `NETDIRS`. The SDNet **client** (`set.server`, `set.netlogin`, a VOC
pointer of type `N`; see [SDNet](12a-sdnet.html)) does not read `NETFILES`.

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
