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

> `SDConnectUDS` (Unix Domain Socket) appears in the header but is not
> applicable on Windows. The Windows port supports local and TCP
> connections only.

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
creates are owned by that user. `SH` and `OS.EXECUTE` do not work from an API
session in this release.

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
| `SDConnect(host, port, user, pass, account)` | Boolean | connect over TCP |
| `SDConnectLocal(account)` | Boolean | connect on the same machine |
| `SDConnected()` | Boolean | is a session active |
| `SDDisconnect()` | none | end the current session |
| `SDDisconnectAll()` | none | end all sessions |
| `SDGetSession()` | Integer | get the current session number |
| `SDSetSession(session)` | Boolean | switch to a session |
| `SDLogto(account)` | Boolean | switch to another account |

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
| `SDDcount(src, delim)` | Long | count delimiters |
| `SDChange(str, old, new, occurrences, start)` | String | replace substrings |
| `SDMatch(src, template)` | Boolean | match a string against a pattern |
| `SDMatchfield(src, template, component)` | String | extract a matched component |
| `SDSubstr(...)` | String | substring (language-specific) |

### Command execution

| Function | Returns | Description |
|---|---|---|
| `SDExecute(cmnd, err)` | String | execute a TCL command |
| `SDRespond(response, err)` | String | respond to a prompt from `SDExecute` |
| `SDEndCommand()` | none | end a multi-line command |
| `SDCall(name, argcount, ...)` | none | call a catalogued subroutine (pass by reference) |
| `SDCallx(name, argcount, ...)` | Integer | call a catalogued subroutine (pass by value) |

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
| `SDRelease(fileNo, id)` | none | release a read lock |
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
| `SDEvaluate(dictFileNo, names, data, id)` | String | evaluate dictionary items on the server against a record. `dictFileNo` is the number `SDOpen("DICT name")` gave, `names` one name or several separated by value marks, `data` the record (it becomes `@RECORD`) and `id` its id (`@ID`; pass the null string when the item does not use it). The answers come back joined by **item marks** (character 255). D, A, S, C and I items all work; an I-type or correlative that is not compiled is compiled for the call and the dictionary is **not written to**. A name that is not in the dictionary gives the null string; a phrase or other item that defines no data, and an expression that will not compile, give the null string with `SDError()` saying which. Conversion codes in the item are *not* applied |
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

**Not run on Windows.** These functions and the requests behind them are carried from SD Core for Linux and compile; the Windows client library has not been run against a Windows server for any of them.

### Session and package management

| Function | Returns | Description |
|---|---|---|
| `SDEnterPackage(name)` | Boolean | enter a package context |
| `SDExitPackage(name)` | Boolean | exit a package context |
| `SDGetArg(argNo)` | String | get a command argument |

### Error handling

| Function | Returns | Description |
|---|---|---|
| `SDError()` | String | get the last error message |
| `SDDebug(mode)` | none | enable/disable debug mode |
| `SDStatus()` | Long | get the last server status code |
| `SDFree(ptr)` | none | free a returned pointer |

## Language bindings

The API headers define bindings for four languages. The function
signatures are identical in meaning; the syntax differs.

### Gambas3

```
Library "./sdclilib"
Extern SDConnect(Host As String, Port As Integer, UserName As String,
  Password As String, Account As String) As Boolean
Extern SDRead(FileNo As Integer, Id As String,
  ByRef Errno As Integer) As String
```

### PureBasic

```
PrototypeC.l P_SDConnect(host.p-utf8, port.l, user.p-utf8,
  pass.p-utf8, account.p-utf8)
PrototypeC.i P_SDRead(fno.l, id.p-utf8, *err)
```

Per-arity prototypes are provided for `SDCall` and `SDCallx`:
`P_SDCall0` through `P_SDCall20`, `P_SDCallx0` through `P_SDCallx20`.

### Free Pascal / Lazarus

```pascal
type
  TSDConnectFn = function(Host: PAnsiChar; Port: LongInt;
    User, Pass, Account: PAnsiChar): LongInt; cdecl;
  TSDReadFn = function(FileNo: LongInt; Id: PAnsiChar;
    Err: PLongInt): PAnsiChar; cdecl;
```

A `LoadSdCliLib` function loads the library and resolves all
function pointers; `UnloadSdCliLib` releases it.

### Python (ctypes)

```python
import ctypes
_lib = ctypes.CDLL('./sdclilib.dll')

SDConnect = _lib.SDConnect
SDConnect.argtypes = [ctypes.c_char_p, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
SDConnect.restype = ctypes.c_int

SDRead = _lib.SDRead
SDRead.argtypes = [ctypes.c_int, ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int)]
SDRead.restype = ctypes.c_char_p
```

Per-arity `CFUNCTYPE` definitions are provided for `SDCall` and
`SDCallx` wrappers.

## What the API cannot do

| | |
|---|---|
| `sh` and `OS.EXECUTE` | refused over the API |
| Open files outside the account | refused (status 3035 — *not permitted*) |
| Reach the credential file | never, and cannot be added |
| Enumerate accounts | refused; all three failure cases give the same message |

## Continued in

[SD BASIC - Python Integration](37a-sd-basic-python-integration.html) — the
other direction: a BASIC program reaching out to Python, rather than a
program outside SD reaching in.
