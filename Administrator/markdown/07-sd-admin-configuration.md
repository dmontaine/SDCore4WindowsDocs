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

> The sample output below is illustrative; the values on your system will
> differ where your configuration does.

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

### A name SD does not recognize stops it starting

An unrecognized parameter is not ignored. The parser abandons the file with
`Unrecognized configuration parameter`, and SD does not start.

That is why a name SD has dropped has to be taken out of the file. Eleven parameters have been removed (`APILOGIN`, `CODEPAGE`, `CREATUSR`,
`EXCLREM`, `FIXUSERS`, `GDI`, `JNLDIR`, `JNLMODE`, `PORTMAP`, `RINGWAIT` and
`TXCHAR`), and `INVCASE` and `FILERULE` are gone too. The
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
[Accounts and Security](01-accounts-and-security-2-making-an-account.html#the-operating-system-switches-sh-on-and-os-on)).
That holds for every session, a person at the console
included. The verb will not tell you
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
printer, and `config gpl` and `config contrib` display the license and the list
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
`SPOOLER`, `TEMPDIR`, `TERMINFO` and `YEARBASE`. (The list predates `MAXRLOCK`, `PWDELAY`,
`NETWAIT` and `NETREPLY`, which can be changed for the session in the same way.)

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
shown the exact command and been answered Run. The other 45 parameters are not changed from SD;
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
| `inert` | accepted, and nothing on Windows acts on it (none at present) |
| `unknown` | a name in the file that SD does not know |

A row marked `*` is one where the file and the running SD disagree. The box at the foot says for that
parameter whether the sessions started now will read the file's value (`session`) or SD keeps the old
one until it is restarted (`restart`). **A name in the file that SD does not know is listed at the end
as `unknown`, and the top of the page names it: SD does not start with it, and no new session starts
while the file holds it** (the section *A name SD does not recognize stops it starting* above). `D`
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

## Continued in

[Configuration: Changing a Parameter from
SD](07a-sd-admin-configuration-changing-from-sd.html) — set.config, the E key
and the first groups of parameters.
