Title: SD Client API
Subtitle: The sdclilib client library, its functions across four language bindings, and the server status codes.

The SDClient API lets an external application connect to SD, open
files, read and write records, execute commands, call subroutines,
and manage select lists — all through a single shared library.

**The API is a normal way for any account to use SD**, not a facility reserved
for developers and administrators. A person running a custom GUI program that
talks to SD needs API access and may need nothing else.

## The library

Four DLLs are installed. They are built from one source: each pair is the same
code compiled twice under two output names, so the two files are not identical
on disk but behave identically.

| | |
|---|---|
| 64-bit | `sdclilib.dll` and `sdclient.dll` |
| 32-bit | `qmclilib.dll` and `qmclient.dll` |

The `*clilib` names are what existing applications ask for; the `*client` names
are for new work. **Renaming one to the other does not work**: an import library
records the DLL name its symbols come from, so an application built against
`sdclilib` loads `sdclilib.dll` whatever you call the file on disk. That is why
both names are built rather than one being a copy of the other.

> **The architecture must match the application, not the machine.** A 32-bit
> application on 64-bit Windows needs the 32-bit DLL. The 32-bit build is a
> shipping deliverable rather than a testing convenience.

### Where they are, and how to use them

```
C:\Program Files\SD\usr\clients\client64\     sdclilib.dll  sdclient.dll
C:\Program Files\SD\usr\clients\client32\     qmclilib.dll  qmclient.dll
```

Copy the DLL your application needs either **beside the application's own
executable** or into `C:\Windows\System32`. Those are the two supported routes
and either works.

> **`C:\Program Files\SD\usr\bin` is normally on the system PATH**, because the
> installer offers to put it there — the *"Add SD Core to the system PATH"*
> task, which is ticked unless you untick it, and it is what makes `sd` run from
> any directory. **All four client DLLs live in that directory too**, so an
> application may find one without your having copied anything. That is
> convenient, and it is not the same as choosing which copy it loads: PATH order
> decides, and a stale copy earlier on the PATH wins. **Put the DLL where your
> application will find it deliberately.**

`usr\clients` holds the DLLs **and one import library for each** — `.dll.a`
files, GNU-style, for linking rather than loading:

```
client64\     libsdclilib.dll.a  libsdclient.dll.a
client32\     libqmclilib.dll.a  libqmclient.dll.a
```

They sit beside the DLLs so that everything a client *build* needs is in one
place. **No header travels with them**: `sdclilib.h` reaches every installation
at `C:\ProgramData\SD\sdsys\syscom\sdclilib.h`.

**All four DLLs also appear in `C:\Program Files\SD\usr\bin`, beside `sd.exe`**,
and each copy is byte-identical to the one under `usr\clients`. The 32-bit pair
is there because `usr\bin` is on the PATH, and that is where a **32-bit
administrative utility** finds its client. Those copies are the server's own and
are not the ones you should be taking — with one exception, which is the next
section. **The import libraries are deliberately not in `usr\bin`**: a linker
input has no business in a directory that goes on the PATH.

## Connection

| | |
|---|---|
| `SDConnect(host, port, user, pass, account)` | over the network, to port **4247** (the default when you name none) |
| `SDConnectLocal(account)` | on the same machine. Sends no password and never did |

> **`SDConnectUDS` (Unix Domain Socket) is not available, on either
> port.** It sent its credential over the socket in a way that predates
> SCRAM, and was removed here for the same reason the old cleartext API
> login was: `SDConnect` and `SDConnectLocal` are the two routes.

### SDConnectLocal has a requirement the other does not

`SDConnectLocal` starts a session by running `sd.exe`, and **it looks for
`sd.exe` beside itself** — in the directory the loaded DLL came from, not on
the PATH.

So a copy of the DLL sitting next to your own application will not make a local
connection: there is no `sd.exe` there. Two ways round it:

| | |
|---|---|
| Load the copy in `usr\bin` | it is beside `sd.exe`, which is why that copy exists |
| Use `SDConnect` instead | connect to `127.0.0.1` on port 4247 like any other client |

`SDConnectLocal` sends no password at all. It takes the identity of the process
that called it and checks that account's grants, so the account has to be one
the calling Windows user may enter.

**The login is SCRAM-SHA-256.** A client that sends a password in
clear is refused. The server sets a puzzle only someone who knows the
password can answer, and the password itself is never sent in any
form. The server also proves itself to the client — another program
that grabbed the port before SD started cannot pretend to be SD.

> **Run `modify.password` again for every account that uses the API**
> after upgrading. The stored credentials changed shape and the old
> ones cannot be converted — the password was never kept anywhere, by
> design.

**The connection is encrypted.** Every connection, over the network or local,
is wrapped in TLS 1.3 before the login, and the client library does this
itself. A program linked against an older copy of the library cannot connect;
relink it. The GettingStarted set's *API access* page has the whole story.

A session is confined to its own account. An API session can open
everything inside its own account and the shipped SDSYS files every
account needs, but cannot open, rename, delete or list anything else.

**An API session runs as the Windows user who logged in**, not as the SD
service, so it reaches files with that user's access and the records it
creates are owned by that user. `SH` and `OS.EXECUTE` work from an API session
only if the account it entered has the `sh-on` and `os-on` switches (off for a new
account); an administrator should weigh that before giving either to an account
that also has the API route.

**A session whose server has ended** — its `AUTOLOGOUT` period ran out, the administrator logged it out, the process was killed — does not hang the client: the next request on it comes back empty, `SDError()` says the pipe or connection failed, and `SDDisconnect()` cleans it up. A session can set its own limit by executing the `AUTOLOGOUT` command (`SDExecute("AUTOLOGOUT 10")`: ten minutes idle; the period is in minutes, 0 turns it off).

**`MASTER.LOGIN`.** If the administrator has put a `MASTER.LOGIN` paragraph in the SDSYS VOC it is run when an API session first enters an account, before that account's own `LOGIN` paragraph, as it is for a terminal session; entering another account with `SDLogto` runs the new account's `LOGIN` only. A session can be recognized inside either paragraph by `@TTY`, which is `apisrvr`.

**Threads** (from 15 Oct 2026; before that the library kept its state in plain globals and a program with more than one thread could not use it safely). The client library may be used from several threads of one process, as OpenQM's QMClient may, on these rules:

- **The current session belongs to the thread.** `SDSetSession` and `SDGetSession` act on the calling thread's own selection, so two threads can work on two sessions at the same time. A thread that has not selected a session starts on session 0, which is the one the first connection of the process received; a thread given a session by another thread must `SDSetSession` it before use.
- **A session must not be used by two threads at the same time.** The library does not serialise requests on one session. If more than one thread can reach it, take your own lock round each action, and treat an `SDExecute` and the `SDRespond` calls that answer it as one action.
- **The table of sessions is shared**, so `SDConnect`, `SDConnectLocal`, `SDDisconnect` and `SDDisconnectAll` may be called from any thread; each connect is given a slot of its own however many start at the same moment.
- **The transfer buffer and the `SDCallx` / `SDGetArg` arguments are per thread**, so one thread's call does not overwrite another's results. They are released when the thread ends, or when no session is left.
- **A connection that fails keeps its slot for the thread that made it**, so that `SDError()` still says why after another thread has connected and disconnected; the slot is given back by that thread's next `SDConnect`, `SDSetSession` or `SDDisconnect`, by its end, or by `SDDisconnectAll`.
- The same applies to a session that dies under its thread (`SDConnected()` is false for it and `SDError()` says why).

*Not changed:* a local session is still a server process of its own (`sd.exe`), so a program that starts many threads each with a local session starts that many `sd.exe` processes.

*Measured:* a test program with no server running (`gplsrc\sdclilib\tests\thread_smoke.c`) shows two threads each keeping their own connect error, 32 threads connecting, failing and disconnecting together without meeting a session or error that is not theirs, and the slots of ended threads free again. A run of several threads against a real server has not been made.

### How big a request may be, and what the server does with one it cannot accept

Every request starts with a 4-byte length that counts the whole packet, itself included, and a 2-byte request code, so the smallest packet is 6 bytes. The client library never sends one that breaks the rules below, so a program using it does not meet them; they matter to a program that speaks the protocol itself, and to anyone probing the port.

| When | A packet may declare |
|---|---|
| before the client has logged in (the server is still the SD service's own process, running as LocalSystem) | 6 to 65,536 bytes. The login messages are all under 4 KB |
| after the login | 6 to 1,073,741,832 bytes: the largest SD string (1,073,741,822) plus the 10 bytes of header the client library allows for, the number `SD_MAX_PACKET_BYTES` in the library |

A packet that declares anything else (below 6, negative, or over the limit) is not read: the server ends the session at once and writes one line to the Windows Application event log, source `sd_Log` (`API packet length ... refused (before login)` or `(after login)`). The same test applies to the reply a client sends to an `INPUT` prompt.

*Before 13 Nov 2026 the Windows client library refused any reply over 256 MB, so a record larger than that could be written through it but not read back, and `SDWriteBlk` and `SDWriteSeq` stopped at the same size.*

## Server status codes

| Constant | Value | Meaning |
|---|---|---|
| `SV_OK` | 0 | success |
| `SV_ON_ERROR` | 1 | an `ON ERROR` clause fired |
| `SV_ELSE` | 2 | an `ELSE` clause fired |
| `SV_ERROR` | 3 | an error occurred |
| `SV_LOCKED` | 4 | the record is locked by another session |
| `SV_PROMPT` | 5 | the command issued a prompt and is waiting for input |

## Function reference

### Connection management

| Function | Returns | Description |
|---|---|---|
| `SDConnect(host, port, user, pass, account)` | Boolean | connect over TCP. A connection that fails returns false and `SDError()` says why; the session number it was given is the current one afterwards, so **select the session you were using with `SDSetSession`** before going on |
| `SDConnectLocal(account)` | Boolean | connect on the same machine |
| `SDConnected()` | Boolean | is a session active |
| `SDDisconnect()` | none | end the current session |
| `SDDisconnectAll()` | none | end all sessions |
| `SDGetSession()` | Integer | get the current session number |
| `SDSetSession(session)` | Boolean | switch to a session |
| `SDLogto(account)` | Boolean | switch to another account: true if the server moved there, false (and `SDError()` says why) if not, in which case the session stays where it was |

**Sessions.** One program can hold up to **1024** sessions at once, each with its own server process, number and account (it held four before 15 Oct 2026). The server's own user table (`USERPOOL`, 1023 by default) is the real ceiling. Open more than one with `SDConnect` or `SDConnectLocal`, one after another, noting `SDGetSession()` each time, and move between them with `SDSetSession`.

### File operations

| Function | Returns | Description |
|---|---|---|
| `SDOpen(filename)` | Integer (file number) | open a file |
| `SDClose(fileNo)` | none | close a file |
| `SDRead(fileNo, id, err)` | String | read a record |
| `SDReadl(fileNo, id, wait, err)` | String | read with a shared lock |
| `SDReadu(fileNo, id, wait, err)` | String | read with an update lock |
| `SDWrite(fileNo, id, data)` | none | write a record |
| `SDWriteu(fileNo, id, data)` | none | write with an update lock |
| `SDDelete(fileNo, id)` | none | delete a record |
| `SDDeleteu(fileNo, id)` | none | delete with an update lock |
| `SDRecordlock(fileNo, id, updateLock, wait)` | none | set a record lock |
| `SDRecordlocked(fileNo, id)` | Integer | query the lock on a record, as `recordlocked()` does: **-3** another user holds a file lock, **-2** an update lock, **-1** a read lock; **0** not locked; **1** this session holds a read lock, **2** an update lock, **3** a file lock. A file number that is not open gives 0 and `SDError()` says so |
| `SDRelease(fileNo, id)` | none | release a record lock |
| `SDMarkMapping(fileNo, state)` | none | enable/disable mark mapping |

### Record manipulation

| Function | Returns | Description |
|---|---|---|
| `SDExtract(src, fno, vno, svno)` | String | extract a field, value or subvalue |
| `SDIns(src, fno, vno, svno, newdata)` | String | insert into a dynamic array |
| `SDDel(src, fno, vno, svno)` | String | delete from a dynamic array |
| `SDReplace(src, fno, vno, svno, newdata)` | String | replace a field, value or subvalue |
| `SDLocate(item, src, fno, vno, svno, pos, order)` | Boolean | find a position for ordered insert |

### String functions

| Function | Returns | Description |
|---|---|---|
| `SDField(str, delim, first, occurrences)` | String | extract a field from a delimited string |
| `SDDcount(src, delim)` | Long | the number of delimited items: 1 more than the number of times `delim` occurs, counting non-overlapping occurrences from the left; 0 for a null string or a null delimiter. **The delimiter may be more than one character** (`a::b::c` by `::` is 3); before 15 Oct 2026 only its first character was used |
| `SDChange(str, old, new, occurrences, start)` | String | replace substrings |
| `SDMatch(src, template)` | Boolean | match a string against a pattern |
| `SDMatchfield(src, template, component)` | String | extract a matched component |
| `SDSubstr(...)` | String | substring (language-specific) |
| `SDChecksum(data)` | Long | the number SD's own `checksum()` gives for the same string, worked out in the library **with no connection to SD**. A byte of 128 or more is taken as a signed character, as the server reads it. A check for accidental damage, not a hash for security (the message digests are the server's `digest()`); the null string is 0 |

### Command execution

| Function | Returns | Description |
|---|---|---|
| `SDExecute(cmnd, err)` | String | execute a TCL command |
| `SDRespond(response, err)` | String | respond to a prompt from `SDExecute` |
| `SDEndCommand()` | none | end a multi-line command |
| `SDCall(name, argcount, ...)` | none | call a cataloged subroutine; the arguments the subroutine changed are put back into yours |
| `SDCallx(name, argcount, ...)` | none | the same call, but your arguments are **not** changed: read each one the subroutine changed with `SDGetArg(n)` afterwards |
| `SDGetArg(argNo)` | String | argument *n* (1 to 20) of the last `SDCallx`; free it with `SDFree` |

> `SDCall` and `SDCallx` are variadic: 0 to 20 arguments. Each binding
> provides per-arity wrappers — `SDCall0` through `SDCall20`, and
> `SDCallx0` through `SDCallx20`.

### Select lists

| Function | Returns | Description |
|---|---|---|
| `SDSelect(fileNo, listNo)` | none | select all records in a file |
| `SDSelectIndex(fileNo, indexName, indexValue, listNo)` | none | select by index value |
| `SDSelectLeft(fileNo, indexName, listNo)` | String | select left of an index cursor |
| `SDSelectRight(fileNo, indexName, listNo)` | String | select right of an index cursor |
| `SDSetLeft(fileNo, indexName)` | none | position cursor left |
| `SDSetRight(fileNo, indexName)` | none | position cursor right |
| `SDReadNext(listNo, err)` | String | read next select list id |
| `SDReadList(listNo, err)` | String | read the whole list as a dynamic array |
| `SDClearSelect(listNo)` | none | clear a select list |
| `SDIndices(fileNo, indexName)` | String | `indices()` on the server: with a null name the names of the file's alternate key indexes, with a name that index's details; the null string for an index the file has not |

### The server: revision, variables, SYSTEM(), TRANS() and transactions

| Function | Returns | Description |
|---|---|---|
| `SDRevision()` | String | the client's revision on its own before a connection; once connected, the client's and the server's, as two values separated by a value mark. Works without a connection |
| `SDGetVar(name)` | String | the value of an `@` variable on the server, with or without the `@`, in either case. The names it knows are `@SELECTED`, `@LOGNAME` (also `@USER`), `@WHO`, `@PATH`, `@USERNO`, `@TTY`, `@DS`, `@SENTENCE`, `@COMMAND`, `@SYSTEM.RETURN.CODE`, `@USER.RETURN.CODE`, `@DATE`, `@TIME`, `@ID`, `@ANS` and `@USER0` to `@USER4`; any other name gives the null string, not an error |
| `SDSystem(key)` | String | `system(key)` on the server |
| `SDTrans(file, id, field, action)` | String | `trans()` on the server. `field` is a dictionary name, a field number or -1 for the whole record; `id` may be several ids separated by value marks; `action` is `X` (null if the record is missing, the default) or `C` (the id). The marks of the answer are lowered one level, as `trans()` lowers them. The `B` (binary open) action is refused |
| `SDRTrans(file, id, field, action)` | String | the same with the marks left as they are |
| `SDTxn(mode)` | none | **1** start a transaction, **2** commit, **3** abort, **4** commit *non-durably*: a transaction nested in another is merged into its parent, which alone writes to the files (see *Locks and transactions*). Modes 2 to 4 need a transaction to be running; a mode out of range or a commit with nothing to commit is refused with a message and the session goes on |

`SDTrans` and `SDRTrans` open the file and its dictionary on the server, so a session that the administrator has restricted with `SDCLIENT` is refused them (message 5262, "File access is disabled").

### Dictionary items and conversions

| Function | Returns | Description |
|---|---|---|
| `SDEvaluate(dictFileNo, names, data, id)` | String | evaluate dictionary items on the server against a record. `dictFileNo` is the number `SDOpen("DICT name")` gave, `names` one name or several separated by value marks, `data` the record (it becomes `@RECORD`) and `id` its id (`@ID`; pass the null string when the item does not use it). The answers come back joined by **item marks** (character 255). D and I items work; an I-type that is not compiled is compiled for the call and the dictionary is **not written to**. A name that is not in the dictionary gives the null string; a phrase or other item that defines no data, and an expression that will not compile, give the null string with `SDError()` saying which. Conversion codes in the item are *not* applied |
| `SDEvalConv(dictFileNo, names, data, id)` | String | the same, and the item's output conversion is applied to each value of its answer |
| `SDIConv(data, code)` | String | `iconv()` on the server, which has every conversion code |
| `SDOConv(data, code)` | String | `oconv()` on the server |
| `SDIConvs(data, code)` | String | `iconvs()`: the conversion is applied to each element of a dynamic array in turn |
| `SDOConvs(data, code)` | String | `oconvs()` |

After a conversion `SDStatus()` is **the conversion's own status** - 0 after a successful one, otherwise as `iconv()` and `oconv()` describe it - and it is for that call alone: the next successful conversion leaves it 0. These need a connection. **A session that the administrator has restricted with `SDCLIENT` cannot reach a file or call a program, so it is refused a conversion code that does either** - a `T` code with a file in it, or a `U` code; the ordinary codes (dates, masked decimals, case) are not affected.

### Sequential files

| Function | Returns | Description |
|---|---|---|
| `SDOpenSeq(file, id, modes)` | Integer | open a sequential file, as `openseq` does. With an `id`, `file` is the name of a **directory file** and `id` the item in it; with a **null `id`**, `file` is a **pathname**. Returns a file number, or **0** with `SDStatus()` and `SDError()` saying why. A file that is not there yet gets a number and is made by the first write. `modes` is added up from: **2** give up with a locked answer if another process has the file (without it the call waits), **16** read only, **256** append, **512** overwrite (empty the file on opening), **1024** flush after every write, **4096** shared (append, for several writers) |
| `SDReadSeq(fileNo, err)` | String | the next line, without its terminator. `err` is the server's answer: **2** at the end of the file, where the string is empty |
| `SDReadBlk(fileNo, bytes, actual)` | String | up to *bytes* bytes (1 to 100,000,000). `actual` is how many came back: fewer at the end of the file, **0** with nothing left. The data may hold any byte, zero included, so read it by `actual` and not by its terminator |
| `SDWriteSeq(fileNo, rec)` | none | write a line and a terminator |
| `SDWriteBlk(fileNo, rec, bytes)` | none | write exactly *bytes* bytes, no terminator added |
| `SDSeek(fileNo, offset, relTo)` | none | position: *relTo* **0** from the start, **1** from here, **2** from the end (a negative offset counts back) |
| `SDWeofSeq(fileNo)` | none | cut the file off at the current position |
| `SDClose(fileNo)` | none | close it (the same function as for any file) |
| `SDWriteSeqKey(fileNo, rec)` | String | **not a sequential file function**: write *rec* to the **hashed** file `SDOpen` gave, under the id the file's own counter gives it (`write ... creating.seqkey`), and return that id. The update lock the write takes is released before the call returns. A directory file is refused, with the null string and `SDError()` saying a hashed file is needed |
| `SDWriteuSeqKey(fileNo, rec)` | String | the same, and the update lock is **kept** (`writeu`) |

Their numbers begin at 10001 and are not those of `SDOpen`, so a number of one kind given to a function of the other is refused. The counter starts at 1 and is set with `configure.file ... next` ([SD Basic - File Handling](07-sd-basic-file-handling.html)).

**The gates are the ones `openseq` has for any program.** A session whose server is restricted with `SDCLIENT` cannot open any file. An item of a directory file is an SD file and is opened through the VOC, as `openseq` opens it; a file flagged trusted is refused. **A bare pathname is a Windows file, and an account without the `os-on` switch reaches only its own directory by it**: a file elsewhere on the disk, a sibling account's file and a path that climbs out with `..` are all refused with *... is not a file this account may open* (message 12350), and nothing is made. (The API server asks the account's own switch itself: it is an internal program, which the kernel does not otherwise hold to the gate.)


### Packages

| Function | Returns | Description |
|---|---|---|
| `SDEnterPackage(name)`, `SDExitPackage(name)` | Boolean | **not supported**: licensed packages are not part of SD and the server refuses both. The library still exports them, and the language headers do not declare them |

### Error handling

| Function | Returns | Description |
|---|---|---|
| `SDError()` | String | get the last error message |
| `SDDebug(mode)` | none | enable/disable debug mode |
| `SDStatus()` | Long | get the last server status code |
| `SDFree(ptr)` | none | free a returned pointer |

## Continued in

[SD Client API: Language Bindings](37b-sd-client-api-bindings.html) — the six
language headers and what the API cannot do
