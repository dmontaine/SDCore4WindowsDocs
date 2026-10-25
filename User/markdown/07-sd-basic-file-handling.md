Title: SD Basic - File Handling
Subtitle: Opening files, reading and writing records, locking, and transactions.

This page covers the statements that reach the database: opening a file,
reading and writing whole records or single fields, the locking that keeps two
sessions out of each other's way, and transactions.

Sequential files — ordinary operating-system files read a line at a time — are
in [SD Basic - Sequential Files](10-sd-basic-sequential-files.html). Select lists are in
[SD Basic - Select Lists](08-sd-basic-select-lists.html).

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Opening

```
open {dict,} file.name to file.variable {readonly}
   then statements
else statements

openpath pathname to file.variable {readonly}
   then statements
else statements
```

`open` looks the name up in the account's VOC. `openpath` takes an operating
system path and bypasses the VOC entirely.

**The `else` branch is where a missing file arrives, and it is not
optional.** A program that omits it does not compile. Never leave it empty:

```
open 'CUSTOMERS' to f.cust else
   stop 'Cannot open CUSTOMERS'
end
```

**`dict` opens the dictionary rather than the data portion** —
`open 'dict', 'CUSTOMERS' to f.dict else ...`.

`close file.variable` releases it. A file left open is closed when the program
ends, so `close` matters mainly in a long-running program that opens files in a
loop.

### Flushing the file cache

```
flush.dh.cache {local | no.wait}
```

A dynamic file that a program closes is kept open in a cache of recently closed
files, so that opening it again is quick. A program that is about to do
something outside SD that fails while a file is still open somewhere (moving the
file, say) can ask every process to close its cached files. `flush.dh.cache`
does that and waits, for up to four seconds, for the other processes to say they
have; a process waiting at an `input` does not answer until a key arrives, so it
costs the four seconds. **no.wait** asks and carries on; **local** flushes only
the calling process.

## Reading

```
read variable from file.variable, record.id then ... else ...
readv variable from file.variable, record.id, field then ... else ...
matread matrix from file.variable, record.id then ... else ...
```

| | |
|---|---|
| `read` | the whole record into one dynamic array |
| `readv` | a single field |
| `matread` | the record spread across a dimensioned matrix, one field per element |

For a record holding `alpha` and `beta|gamma`:

| | Result |
|---|---|
| `read got from f, 'R1'` | `then` branch; `dcount(got, @fm)` is `2` |
| `read got from f, 'NOSUCH'` | **`else` branch** |
| `readv fv from f, 'R1', 2` | `beta\|gamma` |

**A missing record is the `else` branch, not an error.** And `status()` after
one reads **3006**, which is how you tell "no such record" from a real failure
such as a permission problem.

**`matread` puts everything past the end of the matrix into element zero.**
A three-field record read into `dim mm(2)` gives `mm(1)` = `f1`,
`mm(2)` = `f2` and **`mm(0)` = `f3`**. Nothing is lost and nothing is reported.

**`inmat()` does not tell you it happened** — it reads `0` after that
`matread`, not `3`. It reports the element count after `matparse`, not after
`matread`. If a record may have more fields than your matrix, `read` it and use
`dcount(rec, @fm)`, or size the matrix from the dictionary.

After `matbuild` and `matwrite`, `inmat()` gives the index of the last element
that went into the string or record, or `0` when the zero element of the matrix
was added at the end.

## Writing

```
write variable to file.variable, record.id
writev variable to file.variable, record.id, field
matwrite matrix to file.variable, record.id
```

Writing creates the record if it does not exist and replaces it if it does.
There is no "insert only" form — read first if that distinction matters, and
hold a lock between the read and the write or two sessions will both find it
absent.

### Letting the file number its records: `creating.seqkey`

```
write variable to file.variable creating.seqkey id.variable {on error ...}
writeu variable to file.variable creating.seqkey id.variable {on error ...}
```

A **hashed** file keeps a counter in its header. With `creating.seqkey` the record is written
under the counter's next value, **1** in a file that has never used it, and `id.variable`
is given that id (as text). An update lock on the new id is taken for the write and
released before the next statement, or with `writeu` **kept**. In a transaction the id is
taken at the `write`, not at the `commit`, so a transaction that does not commit leaves a gap.
**A directory file is refused** (*WRITE ... CREATING.SEQKEY needs a hashed file*, message 12353;
status 3005 under `on error`) and `id.variable` is left as it was. `fileinfo(file, 1031)` is
the id of the last record written this way (0 if none), and `configure.file` *file* `next` *n*
sets the next id (`next query` shows it).

**An id that already names a record is skipped.** Before it uses an id, `write ... creating.seqkey`
looks in the file: if a record is already there (written by a copy, by a load, or by a program that
chose its own numbers) it takes the next id instead, so that record is never overwritten. **This is
SD's behaviour, not openQM's** - openQM does not look, and its manual tells the programmer to write
every record of the file this way. The skipped numbers leave gaps. In a transaction only the records
already committed to the file are looked at; an id this process took earlier is never given out twice.
**`clear.file` keeps the counter**, so the ids go on from where they were; `configure.file`
*file* `next 1` starts them again. A file made by `copy` starts its own counter at 1, even when
records with numeric ids were copied in; the skipping is what protects them. The counter is changed in
the file header at once, so a power failure can leave it one behind the records; setting it with
`configure.file ... next` puts that right. The client library
has it as `SDWriteSeqKey` and `SDWriteuSeqKey` ([SD Client API](37-sd-client-api.html)). On a file
reached through an `N` pointer to another SD server it works only with the administration
group on that server ([Programming with a Remote File](42-sd-programming-with-a-remote-file.html)).

### `fcontrol`: the counter, a test for an id, the minimum modulus

```
result = fcontrol(file.variable, action {, qualifier})
```

`fcontrol` has openQM 4's action numbers, and the tokens `FC$...` are in `keys.h`. An ordinary
program may use it; it changes only the file it is given.

| action | token | what it does |
|---|---|---|
| 2 | `FC$SET.SEQ.KEY` | the qualifier *n* (1 or more) becomes the next id `write ... creating.seqkey` gives out; returns 1 |
| 3 | `FC$GET.SEQ.KEY` | takes the next id and moves the counter on, so a program can reserve an id without writing a record; the null string if the file is not hashed |
| 5 | | does the user have access to the field position in the qualifier? Always 1: SD has no field level encryption |
| 6 | `FC$VALID.ID` | 1 if the qualifier could be the id of a record of this file (not null, not longer than the limit, no mark characters; a directory file also applies its name mapping), else 0 |
| 7 | `FC$MINMOD` | sets the minimum modulus of a hashed file to the qualifier (1 or more); returns 1 |

Actions 2, 3 and 7 are refused on a file opened `readonly`: `status()` is 3018 and the result is 0
(null for 3), and the counter is not touched. On a file that is not hashed `status()` is 3005; a
qualifier under 1 sets `status()` to 1. **In this release `fcontrol` does not do `FC$SYNC` (1) or
`FC$CRLF` (4):** a program that asks for either is stopped with *FCONTROL cannot do this action in SD*
(message 12359) rather than being told it worked, and any other action number stops it with *the
action is not one SD knows* (message 12360). Forced writes are asked for when the file is opened
(*Forced writes* below), not with `fcontrol`; SD for Linux has since made both work, and this release
does not have that yet. A program written for openQM that uses those two will need changing. The
qualifier may be left out where the action does not use it. The internal programs' own function is called `fcontrol.int` and is not available to
ordinary programs. On a file reached through an `N` pointer to another SD server the call goes to
that server, and needs the administration group there (page 42).

### Forced writes: `sync`

A file that must survive a power failure can be told to write to disk as it goes. Without it SD, like any
program that writes files, leaves data in the operating system's cache for a short while.

```
open 'LEDGER' to f.ledger sync else stop 'cannot open'
openpath 'C:/data/ledger' to f.ledger sync else stop
x = fileinfo(f.ledger, FL$SYNC)          ;* 1 if this open has it on
```

With the state on, every write and delete flushes the primary and the overflow subfiles before the
statement returns. The `S` flag in field 6 of the file's VOC entry (an `F` entry) gives the same state to every
`open` of it, and bit 4 of the `FSYNC` parameter in `sd.conf` gives it to every hashed file. **It is much slower: a write costs a disk flush, so use it on the
files that need it and not on all.** It protects the file you flagged and nothing else on the machine, and a file
that is not hashed (a directory file) does not take it. openQM's `fcontrol(f, FC$SYNC, ...)`, which turns it on or
off for a file already open, is not provided here.

### Line terminators: the letters `L C B X`

A directory file record is a file of text, and a field mark in a record is a line end on the disk. What counts as a line end
when the record is read back, and what is written for a field mark, is the *line terminator mode* of the open file. There are
four, with the openQM numbers:

| mode | letter | a line ends at | a lone CR | a lone LF | `write` puts for a field mark |
|---|---|---|---|---|---|
| 0 LF | `L` | LF | data | (that is the end) | LF |
| 1 CRLF | `C` | CR LF | data | data | CR LF |
| 2 BOTH | `B` | CR LF or LF | data | (end) | LF |
| 3 NOCR | `X` | LF, with the CRs thrown away | dropped | (end) | LF |

The last line end of a record is not turned into a field mark in any mode, so a record `a`, LF, `b`, LF reads as `a<FM>b`. An
open file starts in the mode its VOC entry names with one of the letters in field 6 (a capital or a small letter; a hashed file
ignores them). **A file with no letter behaves as it always has here:** a `read` ends a line at CR LF or LF and keeps a lone
CR, a `write` ends it with CR LF, a `readseq` ends a line at LF and drops a CR in front of it, a `writeseq` adds CR LF. So a
program that never asks changes nothing. The modes are for a directory that another system's tools write: a CRLF file read in
mode 2 or 3 has no stray CR on each line (it has one on every line in mode 0), and a file read in mode 1 can hold an LF inside
a line. `readseq` and `writeseq` follow the same four modes (see [SD Basic - Sequential Files](10-sd-basic-sequential-files.html));
`mark.mapping off` (image mode) turns the conversion off altogether, whatever the mode, and `readblk`, `writeblk`, `osread` and
`oswrite` never use it. openQM's `fcontrol(f, FC$CRLF, mode)`, which changes the mode of one open file variable, is not provided
here; the letter in the VOC entry is the way to choose.

`delete file.variable, record.id` removes a record. After
`delete f, 'R2'`, reading `R2` takes the `else` branch.

`clearfile file.variable` empties the file but leaves it in place.

## Locking

SD locks a **record**, not a row or a page, and the lock belongs to the session.

```
readu variable from file.variable, record.id {locked ...} then ... else ...
readvu variable from file.variable, record.id, field ...
matreadu matrix from file.variable, record.id ...
recordlocku file.variable, record.id
recordlockl file.variable, record.id
release {file.variable {, record.id}}
```

| | |
|---|---|
| `readu` | read **and take an update lock** |
| `readl` | read and take a shared read lock |
| `recordlocku` | take an update lock without reading |
| `release` | give locks back |

`write` releases the lock it finds. `release` with no arguments releases
everything the session holds.

```
recordlocked(file.variable, record.id)
```

reports the state. After `readu`, `recordlocked(f, 'R1')` is **2**;
an unlocked record reads **0**; after `release f, 'R1'` it is **0** again.

**The `locked` clause is the only way not to wait.** Without it, a `readu`
against a record another session holds **blocks until that session lets go**.
With it, control goes to the `locked` branch immediately:

```
readu rec from f, id locked
   print 'Someone else is editing that record.'
   return
end then
   ...
end else
   ...
end
```

A program without a `locked` clause is a program that can hang a user
indefinitely with no message. **Any interactive read-for-update should have
one.**

`filelock` and `fileunlock` lock a whole file, and `lock` / `unlock` take one
of 64 numbered general-purpose semaphores — used to serialise something that is
not a record at all, such as a report run.

**The rest of this is its own page.** What the other session sees, what every
`recordlocked()` code means, how to find out **who** holds a lock, and how long
a wait actually is, are all in [SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html), which
covers what two sessions running at once see of each other.

## Transactions

```
begin transaction
   ...
   commit
   ...
   rollback
end transaction
```

Everything written between `begin transaction` and `commit` either all lands or
none of it does. `rollback` discards the lot.

**Locks taken inside a transaction are held until it ends**, whichever way it
ends. That is what makes the transaction safe and also what makes a long one
expensive — keep the span short, and never wait for user input inside one.

**And inside a transaction you must already hold the lock on every record you
write.** The same `write` that works outside one fails inside it with
*"Error 3023 (o/s 0) writing record (Possible full disk?)"*, which is a lock
error wearing a disk error's message. [SD Basic - Locks and Transactions](14-sd-basic-locks-and-transactions.html) has
the detail, along with what `commit`, `rollback` and simply reaching
`end transaction` each do.

## Asking about a file

```
fileinfo(file.variable, key)
```

On a newly created dynamic file:

| Key | Meaning | Result |
|---|---|---|
| `0` | is this variable an open file? | `1` |
| `1` | the VOC name it was opened by | `ZZWORK` |
| `2` | the path on disk | `/cygdrive/c/ProgramData/SD/user_accounts/don/ZZWORK` |
| `3` | file type | `3` |
| `5` | modulus | |
| `6` | minimum modulus | `1` |
| `7` | group size | |
| `11` | current load percentage | |
| `13` | does the file have alternate key indexes? | |
| `1001` | read-only? | |
| `1003` | size in bytes, excluding indexes | |
| `1021` (`FL$WHO`) | the user numbers of the other sessions that have the file open, a field mark between them | `14` or `14` : `@fm` : `22`, null when there are none |
| `1100` (`FL$HOLDERS`) | the same sessions as text, for messages | `14 (ann), 22 (don)` |

**Key `1021` is the openQM `FL$WHO`, and the caller is left out** unless it has the file
open through more than one file variable. `1021` returned the text form until 17 Oct 2026; code
that wants text for a message now asks `1100`, and SD's own "cannot gain exclusive access"
messages do. Compile with `$include keys.h`, so that the names carry whatever number they have.

File types: `1` SH, **`3` DH — an ordinary dynamic file**, `4` directory, `5`
sequential.

> **The PATH comes back in POSIX form, not as a Windows path** —
> `/cygdrive/c/ProgramData/...`, not `C:\ProgramData\...`. **Handing that
> string to a Windows program does not work** — Windows reads it as a
> drive-relative path and either fails silently or reports that the parent
> directory does not exist. This is not a theoretical caution: it is what
> stopped the full-screen editors working the first time they were built for
> this port.
>
> **And the conversion function is not available to an ordinary program.**
> The kernel can convert such a path, and `kernel()` is an internal-only
> intrinsic — a `kernel(...)` call in a user account does not
> compile, and the compiler's complaint is *"Matrix KERNEL is not referenced in
> a DIM statement"*, reported at the last line of the program. See
> [SD Basic - System and Environment](16-sd-basic-system-and-environment.html). **So a path a Windows program is going
> to see should come from your own configuration, not from `fileinfo()`.**

> **There is no record-count key.** Key `6` is the *minimum modulus* and reads
> `1` on a small file whatever it contains — `1` with two records
> present and `1` again after `clearfile`. To count records, `select` the file
> and read `selectinfo(list, 3)`, or count in a `readnext` loop.

`dir(pathname)` lists an operating-system directory as a dynamic array — name,
size and modification time per entry.

## Reaching another file's data

```
trans({dict} file.name, record.id, field, action)
rtrans({dict} file.name, record.id, field, action)
xlate({dict} file.name, record.id, field, action)
```

All three fetch one field of one record from a named file, opening it if
needed. `trans` and `xlate` are the same function under two names; `rtrans`
takes an already-open file variable instead of a name.

The *action* says what to do when the record is missing — **or when the file
cannot be opened at all**, which takes the same action:

| | |
|---|---|
| **x** | return the null string, and say nothing (the default) |
| **v** | return the null string and print an error (`Cannot open 'name'` for a file) |
| **c** | return the record id itself |
| **n** | return the record id itself |

(Before 14 Oct 2026 a file that would not open always printed the message,
whatever the action. A program that relied on the message now needs **v**.)

A *field* of `0` returns the record id.

**These open a file on every call unless it is already open.** In a loop over
many records that is a real cost — `open` the file once and use `rtrans`, or
read it directly.

## Creating and configuring

```
create.file path {directory | dynamic}
create file.variable then ... else ...
configure.file file.variable, key, value
```

Most applications create files with the `create.file` **command** rather than
the statement — from BASIC, `execute 'create.file ...'` is the usual route, and
it is what the examples on this page use.

`set.trigger` attaches a program that runs on every write or delete to a file.
A trigger runs inside the caller's transaction, so anything it does is part of
the same all-or-nothing unit.

## What is not here

Nothing in the file-handling group has been removed from this port, but two
things about it changed:

| | |
|---|---|
| **VFS** | the virtual file system layer has been **removed from the C entirely**. `fileinfo()` never reports a VFS type, and the type code is gone |
| **The data tree is private** | `C:\ProgramData\SD` is protected by an access-control list. A file created by SD is reachable through SD, and not by an ordinary Windows user poking at the directory |

## See also

[SD Basic - Select Lists](08-sd-basic-select-lists.html) · [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) ·
[SD Basic - Sequential Files](10-sd-basic-sequential-files.html) · [SD Basic - Alternate Key Indexes](09-sd-basic-alternate-key-indexes.html).
