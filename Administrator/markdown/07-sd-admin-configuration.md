Title: Configuration
Subtitle: The sd.conf file, the two ways to read a setting, and every parameter SD accepts.

SD reads one configuration file at start-up. It sizes the shared memory
segment, sets the limits every session inherits, and names the directories SD
writes to.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

> Every listing on this page was produced by running it, on SD Core for Windows,
> from an SDSYS session.

## The file

```
C:\ProgramData\SD\sd.conf
```

The server and the client both read the `SD_CONFIG` environment variable first
and fall back to that path. The file is installed only if it does not already
exist and is marked never to uninstall, so edits to it survive an upgrade and
survive removal of the product.

It is plain text in one section:

```
[sd]
SDSYS=C:\ProgramData\SD\sdsys
GRPSIZE=2
NUMUSERS=20
```

Lines beginning `#` are comments. The shipped file is heavily commented and
those comments record why each value was chosen. Read them before changing
anything.

### A name SD does not recognise stops it starting

An unrecognised parameter is not ignored. The parser abandons the file with
`Unrecognised configuration parameter`, and SD does not start.

That is why a name SD has dropped has to be taken out of the file. On 27 October
2026 eleven parameters were removed (`APILOGIN`, `CODEPAGE`, `CREATUSR`,
`EXCLREM`, `FIXUSERS`, `GDI`, `JNLDIR`, `JNLMODE`, `PORTMAP`, `RINGWAIT` and
`TXCHAR`), and `INVCASE` before them; `FILERULE` followed on 28 October 2026. The
installer removes those lines from an `sd.conf` it keeps across a re-install or an
upgrade, and logs which it removed. A file copied in by hand must have them taken
out before SD will start.

Range failures behave the same way. `GRPSIZE`, `INTPREC`, `LPTRHIGH`,
`LPTRWIDE`, `MAXCALL`, `RECCACHE`, `SORTMRG` and `MAXIDLEN` are bounds-checked
once the file has been read, and a value outside its range stops start-up with
a message naming the parameter.

## Reading the settings

The `config` verb reports what is in force:

```
:config
Virtual Machine Version Number W1.1-3
APIPORT   4247
CMDSTACK  99
DEADLOCK  0
DUMPDIR   C:\ProgramData\SD\sdsys\dumps
ERRLOG    50 kb
...
YEARBASE  1930
```

SD accepts **51** parameters. The verb prints all of them except `BACKUPDIR`,
`NETDIRS` and `SDSYS`, and `DEBUG` and `FDS` only when they are set.

`NETDIRS` is the one to know about. It names the directories outside any
account that an account **without** `os-on` may still open by their path (see
[Accounts and Security](01-accounts-and-security.html#the-operating-system-switches-sh-on-and-os-on)).
Since 25 October 2026 that holds for every session, a person at the console
included; before, it held for an API session only. The verb will not tell you
what it is set to. Read it from the file.

The `config()` function reads one parameter from a program:

```
group.size = config('GRPSIZE')
```

**48 parameters are readable this way.** The three that are not are `BACKUPDIR`,
`SCREENTHEME` and `SDSYS`. The name is truncated to eight
characters before it is matched; no parameter name is longer than eight, so
that only shows up if you pass something which is not a parameter.

Two further forms exist. `config lptr` reports the settings of the default
printer, and `config gpl` and `config contrib` display the licence and the list
of contributors.

## Changing a parameter

Editing `sd.conf` and restarting SD is the durable route, and for most
parameters it is the only one.

**23 parameters can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, taken from shared memory
when the session started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 23 are `DUMPDIR`, `FLTDIFF`, `FSYNC`, `GRPSIZE`, `INTPREC`,
`LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MUSTLOCK`, `OBJECTS`, `OBJMEM`, `RECCACHE`,
`SAFEDIR`, `SDCLIENT`, `SH`, `SH1`, `SORTMEM`, `SORTMRG`, `SORTWORK`,
`SPOOLER`, `TEMPDIR`, `TERMINFO` and `YEARBASE`.

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

## Sessions and limits

| Parameter | Default | Effect |
|---|---|---|
| `NUMUSERS` | 20 | Maximum concurrent sessions. Sizes the user table in shared memory |
| `NUMFILES` | 80 | Maximum open files across all sessions |
| `NUMLOCKS` | 100 | Maximum record locks across all sessions. Range 1 to 32767 (the lock table's cells are 16 bits; a value outside it stops SD starting, which it did not before the check of 16 Oct 2026, when 40000 wrapped) |
| `MAXCALL` | 10000 | Maximum subroutine call depth. Range 10 to 1000000 |
| `CMDSTACK` | 99 | Depth of the command stack |
| `NETWAIT` | 5 | Seconds to wait for a connection to a server defined for SDNet (`set.server`, `set.netlogin`, a file opened through an `N` pointer): the TCP connection, then the TLS handshake, each. 1 to 3600; zero is refused |
| `NETREPLY` | 30 | Seconds to wait for each reply of such a server. 1 to 3600; zero is refused. `config('NETWAIT')` and `config('NETREPLY')` read them. See [SDNet](12a-sdnet.html) |
| `FDS` | unset | Limit on file descriptors. No limit when unset |
| `USERPOOL` | 1023 | The highest user number handed out; user numbers rotate through 1 to this, 0 always takes the lowest free one |
| `USPLIT` | 0 | `1`: interactive sessions take the lowest free user number and every other process (a phantom, an API session) the highest free one in 1 to `NUMUSERS`, so the two never meet. `PHANTOMS` and `USERPOOL` are ignored while it is on. `config('USPLIT')` reads it |
| `PHANTOMS` | unset | `base,range` — user numbers kept for phantoms started with `phantom user n`. Nobody else is given one: not a session, not an API session, not a phantom started without `user`. It must lie between 1 and the highest user number, or SD will not start. `config('PHANTOMS')` reads it as `base,range`, null when none are kept |
| `CLEANUP` | 300 | Seconds between the checks that look for sessions that ended without logging out (a killed terminal, a lost connection) and clear them from the user table. 30 to 3600. The daemon wakes every ten seconds, so an interval is kept to within ten seconds; a very short one costs a pass over the user table that often. `config('CLEANUP')` reads it |

## Files and locking

| Parameter | Default | Effect |
|---|---|---|
| `GRPSIZE` | 2 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given |
| `MAXIDLEN` | 63 | Maximum record id length. 63 is also the lower bound |
| `MUSTLOCK` | 0 | When 1, a `write` or `delete` requires the record to be locked first |
| `DEADLOCK` | 0 | When 1, SD traps deadlocks |
| `SAFEDIR` | 0 | When 1, directory files are updated by write-and-rename rather than in place |
| `RECCACHE` | 0 | Records cached per file. Range 0 to 32 |
| `FSYNC` | 0 | Bit flags controlling when SD forces data to disk |

## Directories

| Parameter | Default on a new install | Effect |
|---|---|---|
| `SDSYS` | `C:\ProgramData\SD\sdsys` | The system account. SD does not start if the global catalogue is not found beneath it |
| `USRDIR` | `C:\ProgramData\SD\user_accounts` | Where `create.account` puts a user account |
| `GRPDIR` | `C:\ProgramData\SD\group_accounts` | Where `create.account` puts a group account |
| `DUMPDIR` | `C:\ProgramData\SD\sdsys\dumps` | Where process dumps are written |
| `TEMPDIR` | `/cygdrive/c/WINDOWS/TEMP` | Temporary files |
| `SORTWORK` | `/cygdrive/c/WINDOWS/TEMP` | Work files for a sort that does not fit in memory |
| `TERMINFO` | empty | An additional terminfo directory. The shipped definitions are found without it |

`DUMPDIR` is set rather than left empty on purpose. A blank value falls back to
the system directory, which SD users can write to, and a process dump carries
the whole variable state of the session that wrote it. The installer makes the
dump directory write-only to SD users, so a dump can be added and nobody else's
can be listed or read.

`TEMPDIR` and `SORTWORK` are reported in POSIX form because that is how the
server's runtime addresses them. `C:\WINDOWS\TEMP` and
`/cygdrive/c/WINDOWS/TEMP` are the same directory.

## The API

| Parameter | Default | Effect |
|---|---|---|
| `APIPORT` | 4247 | Switches the API on. Any number above zero means on, and SD listens on port 4247 whatever the number is; the port cannot be changed. If the line is absent no socket is created at all, which is how the API is turned off. A file that says `APIPORT=4243` still means on |
| `BACKUPDIR` | unset | The folder `backup.account` and `restore.account` use. Set by `set.backup.directory`, not by hand - see [Backing Up and Restoring Accounts](01b-backup-and-restore.html) |
| `NETDIRS` | unset | Directories outside any account that an account without `os-on` may still open by path (every session, since 25 October 2026), separated by semicolons because a Windows path contains a colon |
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright (no file can be opened, so no dictionary can be evaluated either), refuses `SDIConv`, `SDOConv`, `SDIConvs` and `SDOConvs` a conversion code that reads a file (`T` with a file) or calls a program (`U`), and refuses `SDOpenSeq`, `SDExecute`, `SDTrans` and `SDRTrans`; `2` additionally refuses any subroutine not compiled as callable from a client |

Unset is the strict value for `NETDIRS`. With nothing there, an API session can
open files in the account it is standing in and nothing else. It never grants
the credential store, the global catalogue, `os.users` or the account register,
and naming those has no effect. A directory listed here is reachable by every
API session in every account, so it is a decision about the machine rather than
about one account.

`SDCLIENT` is not reported by the `config` verb and has no entry in the shipped
`sd.conf`. It defaults to 0, which permits everything.

## Printing

| Parameter | Default | Effect |
|---|---|---|
| `LPTRWIDE` | 80 | Default page width for the printer. Range 10 to 1000 |
| `LPTRHIGH` | 66 | Default page depth for the printer. Range 10 to 32767 |
| `SPOOLER` | empty | The spooler to hand print jobs to |

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

The difference between them matters. `SH1` carries `-NonInteractive` and `SH`
does not, so a bare `sh` in a phantom or a scheduled job hands control to a
shell with nobody at the keyboard. Operating system access has its own page in
this set.

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
directories named in `NETDIRS`. This is read from the source and has not been
run on an install. The SDNet **client** (`set.server`, `set.netlogin`, a VOC
pointer of type `N`; see [SDNet](12a-sdnet.html)) does not read `NETFILES`.

There is no `FILERULE` parameter any more (removed 28 October 2026). **The
`account:file` form of a file name is always available** (back on 3 November 2026,
for programs moved from openQM): a name that is in no VOC record and has one colon,
such as `open 'sales:orders'`, opens that account's file exactly as a Q-pointer to it
would, with the same checks: the account must be registered, the person must be able
to `logto` it, and it must not be suspended. It reaches nothing a Q-pointer could not.
A drive-letter pathname such as `C:\data\x` has one colon too; it is read as account
`C`, which is not registered, so it is not found. The `path:` form is gone, and so is
the old `system:account:file` form. To reach a directory outside the accounts, put an
F-pointer in the VOC, where the operating-system access switches apply to it. A
Q-pointer whose fourth field names another system is refused with status 3003 and is
not opened as a local file.

There is no licence parameter and no licence verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
licence text.
