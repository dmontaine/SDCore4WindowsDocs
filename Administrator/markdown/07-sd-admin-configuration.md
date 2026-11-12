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
GRPSIZE=4
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
parameters it is the only one. Fourteen tuning parameters can also be changed from SD itself, with
`set.config` or the `E` key of `tool.config` (see *Changing a parameter from SD*, below).

**23 parameters can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, which the session read
from `sd.conf` when it started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 23 are `DUMPDIR`, `FLTDIFF`, `FSYNC`, `GRPSIZE`, `INTPREC`,
`LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MUSTLOCK`, `OBJECTS`, `OBJMEM`, `RECCACHE`,
`SAFEDIR`, `SDCLIENT`, `SH`, `SH1`, `SORTMEM`, `SORTMRG`, `SORTWORK`,
`SPOOLER`, `TEMPDIR`, `TERMINFO` and `YEARBASE`.

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

**A session reads `sd.conf` itself when it starts.** It does not copy the
settings the service left in shared memory, which an SD user with a shell could
change. So an edit to a setting a session keeps for itself (the 23 above, and
others such as `USRDIR` and `GRPDIR`) reaches the sessions started after it,
without a restart. **A bad line in `sd.conf` stops a new session from starting**,
with the message `sd -start` gives, until it is repaired; SD and the sessions
already running are not affected. Every SD user's session opens the file, so it
stays readable by `sdusers`; only administrators can change it.

## The parameters on one screen: `tool.config`

```
tool.config
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more). **It looks, and
it can change 14 of the parameters**; it writes no file itself. A change is made by the verb
`set.config` (see *Changing a parameter from SD*, below) through SDSYS's elevated helper, and only
after you have typed a value, the page has checked it against the range SD enforces and a box has
shown the exact command and been answered Run. The other 37 parameters are not changed from SD;
editing the file as an administrator and restarting SD stays the way to change them.

The page has three views. **P, the parameters**: one row for every parameter SD knows, from the table
`config.table` in the system directory, which names every parameter SD reads. The columns are
the value this SD is running with (what `config()` reports), the value `sd.conf` says now (the file is
read again, a parameter written twice counted the way SD counts it, the flag parameters added up),
the default (what SD uses when the file does not say), when a change takes effect and whether anything
acts on it:

| Takes effect | Meaning |
|---|---|
| `session` | a session reads `sd.conf` itself when it starts, so an edit reaches the sessions started after it, and not the ones already running |
| `restart` | the parameter sizes or starts the system (everything in the shared memory segment, the API's settings); it takes effect when SD is next started |
| `now` | a program reads `sd.conf` each time it uses the parameter (`BACKUPDIR`), so a change needs no restart and no new session |

| Status | Meaning |
|---|---|
| `live` | something acts on it |
| `file` | read from `sd.conf` by a program each time it is used, not by the kernel (`BACKUPDIR`) |
| `inert` | accepted, and nothing on Windows acts on it (`SPOOLER`: SD prints through Windows printing) |
| `unknown` | a name in the file that SD does not know |

A row marked `*` is one where the file and the running SD disagree. The box at the foot says for that
parameter whether the sessions started now will read the file's value (`session`) or SD keeps the old
one until it is restarted (`restart`). **A name in the file that SD does not know is listed at the end
as `unknown`, and the top of the page names it: SD does not start with it, and no new session starts
while the file holds it** (the section *A name SD does not recognise stops it starting* above). `D`
shows only the rows where the file and SD disagree, and `S` only the parameters the file sets. The last
column, `Change`, says `e` for a parameter the page can change (press `E`) and `by hand` for every
other.

`SDSYS` and `BACKUPDIR` cannot be read with the `config()` function; the page says `(not readable)`
for what SD is running with and shows the file's value. `DEBUG` is not compared: the function reports
it in another form than the file writes it.

**B, the backup directory**: the directory saved with `set.backup.directory` and whether it is there;
**R, the report**: the operating system part of `settings.report` (ssh, the API and its firewall rule,
the SD service and the groups), made when the view is opened and on F5. It holds no key and no
password hash. `F5` reads the file, the backup directory and the report again; `E` changes the
parameter under the cursor, or says why it cannot be changed here; `F1` explains the page; `Ctrl-Q`
leaves. Opening the page writes the audit line `tool start app=tool.config`; a change writes the line
of `set.config` (below), and nothing else the page does is written.

### Changing a parameter from SD: `set.config` and the `E` key

```
set.config cleanup 600
```

The administrator's verb (SDSYS's VOC only). It changes **one** line of `C:\ProgramData\SD\sd.conf`:
the first word is a parameter name (letters and digits; SD makes it capitals, as the file spells it)
and the second a whole number of up to seven digits. It runs SDSYS's elevated helper
(`sd-confset.ps1` in SD's program folder) to make the change; the helper checks everything again and is
the authority. `set.config` prints `CLEANUP is now 600 in sd.conf` and, for a parameter that sizes the
system, that it takes effect when SD is next stopped and started (`sd -restart`, or `Stop-Service SD`
then `Start-Service SD`), or, for one a session reads for itself, that sessions started from now on use
it. A refusal prints the helper's own sentence after `sd.conf was not changed:` and writes nothing.

**What the helper does.** It accepts only the 14 parameters in the first table below, and only a value
inside the range SD itself enforces for that parameter when SD starts (so it cannot accept
what SD would refuse). It adds or replaces the line **inside the `[sd]` section**, the only place SD
reads (a line appended after another section's header would be ignored without a word); a second
line for the same parameter in an `[sd]` section is dropped, because SD keeps the last one; every
other line, comments included, is kept exactly as it was, with the file's own line ends. The new file
is written beside the old one and put in its place by one Windows replace, which keeps the old file's
permissions, so a session that reads the file at that moment sees either the old text or the new,
never half of it. **The file as it was is kept as `C:\ProgramData\SD\sd.conf.bak`** (one generation;
a second change replaces it with the file as it was before that change). A change that says what the
file already says writes nothing and leaves the `.bak` alone. A file holding anything but plain ASCII
is refused, not rewritten. The helper writes `C:\ProgramData\SD\sd.conf` and nothing a caller passes
moves it; when the session reads another file (the `SD_CONFIG` variable) the page says so in its box.
Only an administrator's session can ask: the verb refuses any other, and `sd.conf` is closed to
everyone else. SD has no key that puts `sd.conf.bak` back; from an elevated PowerShell prompt,
`Copy-Item C:\ProgramData\SD\sd.conf.bak C:\ProgramData\SD\sd.conf` does.

**One audit line** for each time the helper is asked: `set.config key=cleanup value=600 status=ok`, or
`status=refused`. Every changeable parameter is a number, so the value is written.

**On the page.** `E` on a row whose `Change` column says `e` asks for the new value (the question
shows what SD runs with and what the file says), checks that it is a whole number inside the range
before anything else happens, and then shows the exact command in the toolkit's box with a plain
sentence about when it takes effect. Cancel, which is what Enter chooses, runs nothing. Run runs
`set.config` and the page reads the file and SD's own values again and says what changed: the file's
old and new value, and what SD is running with. `E` on any other row writes nothing: it shows why the
parameter is not changed from SD, and the exact line to add by hand, as an administrator, in the
`[sd]` section of the file SD reads.

**The 14 parameters** are the tuning ones: capacity, performance, timeouts and the printer's defaults.
Each is range-checked by SD and each only sizes or times something SD does; none is a door, a path, a
command, a log or a security setting:

| Parameter | Range | Takes effect |
|---|---|---|
| `CLEANUP` | 30 to 3600 | restart |
| `DHCACHE` | 0 to 1024 | session |
| `GRPSIZE` | 1 to 8 | session |
| `LGNWAIT` | 0 to 32767 | restart |
| `LPTRHIGH` | 10 to 32767 | session |
| `LPTRWIDE` | 10 to 1000 | session |
| `MAXCALL` | 10 to 1000000 | session |
| `MAXRLOCK` | 0 to 100000 | session |
| `NETREPLY` | 1 to 3600 | session |
| `NETWAIT` | 1 to 3600 | session |
| `NUMLOCKS` | 1 to 32767 | restart |
| `RECCACHE` | 0 to 32 | session |
| `SORTMRG` | 2 to 10 | session |
| `USPLIT` | 0 to 1 | restart |

**The other 37 are not changed from SD**, and the helper refuses them by name (a name it does not
know at all it refuses with a different sentence, because an unknown name in `sd.conf` stops SD from
starting). They are the doors and what they allow (`APIPORT`, `NETDIRS`, `NETFILES`, `SDCLIENT`),
every path and command, the log, dump and diagnostic settings, the security throttle `PWDELAY`, the
sizes and combinations that SD does not check or checks against each other, and the ones that change
what existing programs compute. Change them by hand, as before. The page shows the same sentence in
its box:

| Parameter | Why it is not changed from SD |
|---|---|
| `APIPORT` | A door: it opens the API listener to the network. |
| `BACKUPDIR` | A directory: set.backup.directory saves it, with its own checks of the path. |
| `CMDSTACK` | Sizes a table in shared memory and SD checks no range: a mistake shows only at the next start. |
| `DEADLOCK` | A diagnostic: 2 makes SD write a file of the locks involved; set it by hand while you hunt one. |
| `DEBUG` | Debugging flags of the kernel: they change what SD writes and exposes. |
| `DUMPDIR` | A directory: process dumps are written there and can hold what a session had in memory. |
| `ERRLOG` | Sizes the error log; SD checks no range, and a small size discards its oldest entries sooner. |
| `FDS` | Limits the file descriptors SD uses; SD checks no range: a mistake shows at the next start. |
| `FLTDIFF` | Changes how every program compares floating point numbers. |
| `FSYNC` | Trades the safety of data against speed; flag bits that SD does not check. |
| `GRPDIR` | A directory: group accounts are made there. |
| `INTPREC` | Changes the results of arithmetic in programs that already exist. |
| `MAXIDLEN` | Structural: the longest record id of the whole system, which reaches every file and program. |
| `MUSTLOCK` | Makes a write fail unless the record is locked first, which can stop programs that exist. |
| `NETDIRS` | A door: it widens what an API session may reach beyond its own account. |
| `NETFILES` | A door: bit 2 gates API request 29, a remote open of an account. |
| `NUMFILES` | Sizes the open file table in shared memory; SD checks no range. |
| `NUMUSERS` | Sizes the user table, which bounds who can sign on; SD checks no range. |
| `OBJECTS` | Limits the programs a session keeps in memory; SD checks no range. |
| `OBJMEM` | Limits the memory those programs may take; SD checks no range. |
| `PDUMP` | Flag bits that say when a process dump is written; a dump can hold what a session had in memory. |
| `PHANTOMS` | Must agree with USERPOOL: a wrong combination stops SD from starting. |
| `PWDELAY` | A security throttle: the pause after a failed network sign-on; 0 removes it. |
| `SAFEDIR` | Changes how SD replaces the files of a directory file, by writing a new one and renaming it. |
| `SCREENTHEME` | Text that SD acts on; SD checks no value. |
| `SDCLIENT` | A door: restricts what an API session may do, and a lower value loosens it. |
| `SDSYS` | The system directory: SD cannot start, or finds another system, if it is wrong. |
| `SH` | A command SD runs as an interactive shell. |
| `SH1` | A command SD runs for a shell command line. |
| `SORTMEM` | A size in kilobytes that SD does not check, so a mistake shows only when a sort runs. |
| `SORTWORK` | A directory: the work files of a large sort are written there. |
| `SPOOLER` | Nothing on Windows acts on it. |
| `TEMPDIR` | A directory: temporary files are written there. |
| `TERMINFO` | A directory: terminal definitions are read from there. |
| `USERPOOL` | The highest user number: PHANTOMS is checked against it; a mistake stops SD. |
| `USRDIR` | A directory: user accounts are made there. |
| `YEARBASE` | Changes how every program reads a two-digit year; SD checks no range. |

**What this does not do.** It does not restart SD: a `restart` parameter changes the file and the
running SD keeps its old value until it is stopped and started. It does not reach a file other than
`C:\ProgramData\SD\sd.conf`. It cannot change a parameter that SD does not range-check, however
useful that would be; such a parameter joins the list when SD itself checks it.

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
| `GRPSIZE` | 4 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given. **4 since 12 Nov 2026** (the shipped `sd.conf` said 2): Linux measured 200,000 records of 130 bytes with 5 to 11 percent of their groups overflowed at 2 KB and under 2 percent at 4 KB. A system that is already installed keeps the `sd.conf` it has, and so keeps 2 until you change it; a file keeps the size it was made with |
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
