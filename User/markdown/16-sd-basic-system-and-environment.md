Title: SD Basic - System and Environment
Subtitle: Asking SD about itself, about the machine, and about the session you are in.

This page covers the enquiries: what time is it, who am I, where is the data,
what did the last thing that failed say, and what may this account do. Most of
it is one function, `system()`, and most of the surprises are about which form
a path comes back in.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **Values that are particular to one machine — a user number, a computer
> name, a process id — are marked as examples; the shapes are not.** What you
> see back will differ in the value and match in the form.

## SYSTEM()

```
system(key)
```

### The session

| Key | | Value |
|---|---|---|
| `7` | terminal type | `windows` |
| `9` | CPU time used, ms | `45` |
| `12` | time, as `time()` | `70787` |
| `18` | **user number** | `67` (example) |
| `23` | break key enabled? | `1` |
| `24` | echo enabled? | `1` |
| `25` | is this a phantom? | `0` |
| `26` | prompt character | `?` |
| `1000` | `capturing` in effect? | `0` |
| `1001` | case inversion on? | `0` |
| `1029` | internal subroutine depth | `0` at the top, `1` inside a `gosub` |
| `1030` | login time, internal | `1851017987` |
| `1031` | operating system process id | `605` (example) |
| `1050` | administrator? | `0` |

### The machine

| Key | | Value |
|---|---|---|
| `31` | licence number | `0` |
| `42` | IP address | *empty* |
| `91` | **is this Windows?** | `1` |
| `1006` | Windows NT style? | **`0`** |
| `1009` | endian — 0 little | `0` |
| `1010` | platform name | `Windows` |
| `1012` | SD version | `W1.1-3` |
| `1013` / `1014` | user limit, without / with the phantom pool | `20` / `20` |
| `1015` | computer name | `Gitorli` (example) |
| `1017` | port number of a tcp connection | `0` |
| `1028` | system id | `1028` |

**Two of those three answer correctly and one does not.** `system(91)` reads
`1` and `system(1010)` reads `Windows`. **`system(1006)`, "Windows NT style?",
reads `0`** — it is the one to leave alone. **Ask `system(91)` whether this is
Windows**; it is the key this port sets deliberately for that purpose.

### Paths, and they are not all in the same form

| Key | | Value |
|---|---|---|
| `32` | the `sdsys` directory | `C:\ProgramData\SD\sdsys` |
| `38` | the temporary directory | `/cygdrive/c/WINDOWS/TEMP` |
| `1011` | the configuration file | `C:/ProgramData/SD/sd.conf` |
| `1024` | the directory SD was started in | `/cygdrive/c/Users/dmont/OneDrive/Documents` |

**Three different spellings of a Windows PATH come out of one function.** A
backslash path, a POSIX `/cygdrive/` path, and a forward-slash path with a
drive letter. `@sdsys` agrees with key 32 and `@path` — the account directory —
is in the POSIX form.

**A `/cygdrive/` path handed to a Windows program does not work.** Windows
reads it as drive-relative and either fails silently or complains that the
parent directory does not exist. This is not theoretical: it is what stopped
the full-screen editors working the first time they were built for this port.
There is a conversion function in the kernel and **an ordinary program cannot
call it** — see "What is not here". **Take the path from configuration rather
than from `system()` if a Windows program is going to see it.**

### Lists and structures

| Key | | |
|---|---|---|
| `1002` | the call stack | field per level: `path`, then `offset` and line pairs — `.../BP.OUT/ZZMATH` at line 41, then `$CPROC` |
| `1003` | open files | field per file, `unit` and path. **`$ipc` is always one of them** |
| `1025` | environment variables | **two fields**: field 1 every name, field 2 every value, value-mark separated |

`system(1025)` returns **2** fields, every name in the first — it is not a
list of `NAME=value` pairs.

### Time

| Key | | |
|---|---|---|
| `1005` | internal time | `date() * 86400 + time()` — the difference is **0** |
| `1020` | milliseconds since midnight | `9587454` |

`system(1020)` is the one to time something with: against a lock wait it gives
252 ms where `time()` gives 0.

### Where a file or an account is: `vocpath()` and `account.path()`

```
vocpath(filename {, dict.flag})
account.path(account)
```

`vocpath()` gives the operating system pathname of a file named through the VOC:
the data part, or the dictionary part if `DICT ` is written in front of the name
or the second argument is true. The file is opened as `open` opens it, so a
Q-pointer and the other forms `open` takes are resolved as `open` resolves them.
`status()` is 0 if it was found; a null string comes back with the error of the
open if it was not. `account.path()` gives the directory of an account from the
accounts register, in either case of the name, and a null string when there is no
such account.

**A path is told only where the session could open it.** The session's own
account directory and the files in it always; anything else only to an
administrator session (SDSYS), and to any other session the answer is a null
string (with `status()` 3035 from `vocpath()`). So a program cannot learn where
another account lives, or which accounts there are, by asking.

### Unique values, and a few more

| Key | | Value |
|---|---|---|
| `14` | characters waiting at the terminal | a snapshot; for **piped input** it is only what has been read ahead, so do not rely on it |
| `19` | a unique value from the date and time | two five digit numbers, the day and the second; a second value in the same second, from **any** process, gets a letter on the end (`a`, `b` … `z`, `aa`). The time is the process's own, so two users in different time zones can get the same value |
| `21` | a unique value from the date and a sequence | two five digit numbers, the day and a count that starts at 1 again each day |
| `45` | the name of the running program | its catalogue name |
| `1048` | a sequence number | unique across all sessions until SD restarts, then 1 again |
| `1049` | is `hush` in effect? | `0` or `1` |
| `1062` | has `signal()` been raised for this process? | `1` and **cleared by reading it**: `until system(1062)` is the loop of a phantom that waits to be told |
| `1067` | the default group size of a dynamic file | in bytes |
| `1086` | are string comparisons case sensitive in this program? | `0` after `$nocase.strings` or `casing off` |
| `1088` | where `maximum()` or `minimum()` found its element | the field, value and subvalue numbers joined by value marks: for `'61' : @vm : '42' : @fm : '71' : @vm : '57'` the maximum is `71` and `system(1088)` is `2` vm `1` vm `1`. The first of equal elements is the one. Null when the array has no number |

`signal(userno)` raises the flag in another process and is true if that process
is logged in. **SD signals only a process of the same login user**, or any
process when the caller is the administrator; to any other it gives false and
nothing happens. `child(userno)` is true while a phantom this process started
is running. See [SD TCL - Processes and Phantoms](30-sd-tcl-processes-and-phantoms.html).

## DATE, TIME and TIMEDATE

```
date()      time()      timedate()
```

Taken together at one instant:

| | |
|---|---|
| `date()` | `21423` — days since 31 December 1967 |
| `time()` | `70787` — seconds since midnight |
| `timedate()` | `19:39:47 26 AUG 2026` |
| `oconv(date(), 'D4-')` | `08-26-2026` |
| `oconv(time(), 'MTS')` | `19:39:47` |

`@date` and `@time` hold the same numbers, **but they are set once per command**
rather than read afresh, so in a long loop they do not move while `date()` and
`time()` do.

`timedate()` returns a formatted string, not a number. Do not do arithmetic on
it — see
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) for the
conversion codes.

## ENV()

```
env(name)
```

**`env()` is case sensitive and a wrong case looks exactly like a missing
variable.**

| | |
|---|---|
| `env('PATH')` | 926 characters |
| `env('path')` | **0 characters** |
| `env('ProgramData')` | `C:\ProgramData` |
| `env('NOSUCHVAR')` | empty |

Windows itself treats environment variable names as case-insensitive
everywhere else, which is what makes this worth knowing. `ProgramData` works
only because that is exactly how Windows spells it. **Get the spelling from
`system(1025)` field 1 rather than from memory.**

## CONFIG()

```
config(name)
```

On a stock installation:

| | |
|---|---|
| `config('FILERULE')` | `0` |
| `config('GRPSIZE')` | `2` |
| `config('MAXIDLEN')` | `63` |
| `config('NUMFILES')` | `80` |
| `config('NUMLOCKS')` | `100` |
| `config('SORTMEM')` | `4096` |
| `config('SPOOLER')` | empty |

**The name is case sensitive and at most eight characters. both failures now
look the same**, which is the point — a name that is too long is a name that
does not exist, and a caller cannot tell the two apart:

| | |
|---|---|
| `config('numlocks')` — right name, wrong case | empty, `status()` **1004** |
| `config('NOSUCHKEY')` — **nine** characters | empty, `status()` **1004** |

**Keep every `config()` name to eight characters and upper case.**

Neither call aborts the caller: a name that is too long comes back empty with
a status, the same as a name that does not exist.

## SYSMSG()

```
sysmsg(number {, substitution ...})
```

Returns the text of one of SD's own messages, with `%s` substitutions filled
in.

| | |
|---|---|
| `sysmsg(2831)` | `Unrecognised statement` |
| `sysmsg(6711, 'ABC')` | `Unable to find source record ABC` |
| `sysmsg(2201)` | `Account name '' is not in register` — an unfilled substitution comes back empty |
| `sysmsg(99999)` | `[99999] Message not found` |
| `sysmsg(1)` | `[1] Message not found` |

**A message number is not a `status()` code.** They are separate numbering
schemes that overlap. `status()` **3006** is *record not found*; `sysmsg(3006)`
is `Modes: `. Do not render a status code by passing it to `sysmsg()`.

`get.messages()` takes **no arguments** and returned **nothing** — zero fields
— in an ordinary session. It reports messages sent between sessions, and
nothing had sent any.

## Continued in

[SD Basic - Status, Encryption and the
Machine](16a-sd-basic-status-and-the-machine.html) — status codes, checksums,
encryption, umask, the @variables, os.execute and logmsg.
