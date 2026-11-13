Title: Changes in W2.0-0
Subtitle: What was added, changed and removed since W1.1-3 (10 October 2026), by section and in alphabetical order.
Columns: 23 11 66

**This is the list of what changed between W1.1-3 (10 October 2026) and W2.0-0 (called W1.2-0 until 10 November 2026).** It is kept up to date as the
release is built. It was started on 25 October 2026 from the Linux list for L1.2-0 (SD Core for Linux and SD Core for
Windows carry the same openQM items) and the release changelog (`sdsys/changelog`, section "W2.0-0 - in progress"),
which has the full story of each change: what it does, why, and what it does not do. This document is the short form.
**Nothing in it has been run on a real Windows installation yet.**

## How to read it

- Every row is one thing that was **added**, **changed** or **removed**. A fix is a change.
- The rows are grouped into sections, and **within each section they are in alphabetical order**.
- A row is one or two lines. The User and Administrator manuals have the detail; so does the changelog.
- Names are in lower case as SD writes them. `$mode` words, options and BASIC keywords are written the same way.
- Everything that lets a program reach beyond its own account, or leave the machine, is **off as delivered**, with one
  exception: the files of the shared account can be opened by name (`shared-read-off` takes that away from an account).
  The administrator turns the rest on, account by account, and can turn it off again.
- A comment at the end of a row, `<!--s` then item numbers then `-->`, names the spreadsheet items the row covers. It is
  for whoever maintains this document and does not show on the page.
- What SD Core for Windows does not have yet, and SD Core for Linux does, is not listed here. SDNet, the home screen and the
  full-screen tools, the editors `sed`, `ced` and `ide`, the master files and the AI helper (`ai`, `set.ai` and `tool.ai`)
  are in this release. The master files are files of pointers to every account's VOC,
  dictionary and BASIC records (`tool.entries`); the earlier design's complete copies are dropped.

## Read this first: changes that alter what an existing system does

| Name | Change | What |
|---|---|---|
| `@who` | Changed | was the account name in upper case (`DON`); now lower case (`don`), as on SD Core for Linux. A program that compares it with an upper-case name must use `downcase()` or `upcase()` on both sides |
| A new account | Changed | had the shell and `os.execute` open to its person and ssh and the API on; now has **no shell, no `os.execute`, no ssh, no API** and no right to save a VOC, a program file or a dictionary, and every gate is closed until SDSYS opens it (`modify.account`); it can open the files of the shared account by name, read only |
| A person's shell and `os.execute` | Changed | were granted to the Windows person in `os.users`, so they followed the person into every account; now they are two settings of the account, and `os.users` is no longer read |
| A session at the console | Changed | was not held to its account's directory when it opened a file by its path (only a session over the network was); now every session is, unless its account has `os-on`, or `sd-on` for another SD account |
| AccuTerm and SDTerm | Removed | were supported; use terminal type `xterm` or `vt100` |
| An `sh` command | Changed | an account that was listed in `os.users` could use pipes, redirection and chaining; now no account can |
| An upgrade | Changed | copies once what `os.users` said about each user account's Windows user into that account's `sh` and `os` settings, and switches the three edit gates on once for each user account whose setting is blank; it never switches on a setting an administrator turned off |
| Dictionary divide by zero | Changed | stopped the report; now gives zero |
| `fileinfo(f, 1021)` | Changed | gave text such as `12 (don), 14 (ann)`; now the user numbers of the other sessions that have the file open, and the text form is key **1100** |
| `intprec` and `sortmem` | Changed | were 13 and 1024; now **11** and **4096** (set the old values in `sd.conf` if you need them) |
| Removed features | Removed | words and modes that existed to imitate other products (55 `option` words, 35 `$mode` words, and the second spellings and forms of statements, clauses, functions, conversions, TCL verbs and query keywords, each listed in [REMOVED](#removed)), and other things: see [REMOVED](#removed) |
| `select file field` | Changed | a field not otherwise used was ignored; now it is `saving multivalued field`, so the list holds the values |
| The terminal's size | Changed | every session started at the terminal type's 120 by 36; now SD asks the terminal how big it is at the start and when it is resized (`term w,h` still sets it by hand) |
| `when field` with no operator | Changed | kept the null values; now keeps the values that are **not** null |

## Sections

**Built from the openQM list** (each row is an item on the feature spreadsheet): [ADMIN](#admin) · [API](#api) ·
[BASIC](#basic) · [DATA](#data) · [FILES](#files) · [QUERY](#query) · [SYSTEM](#system) · [TCL](#tcl) · [TOOLS](#tools).

**[REMOVED](#removed)**: what SD no longer has, and what to write instead.

**[New Features Unique to SD Core](#new-features-unique-to-sd-core)**, not part of openQM and not on the spreadsheet:
[Administration](#administration) · [AI](#ai) · [API and client library](#api-and-client-library) · [Encryption](#encryption) ·
[Files](#files-1) · [Installer](#installer) · [Screen library and terminals](#screen-library-and-terminals) · [SDNet](#sdnet) ·
[Security](#security) · [System](#system-1).

**[NO CHANGE](#no-change)**: openQM items that needed nothing.

## ADMIN

Administrator commands from the openQM list.

| Name | Change | What |
|---|---|---|
| `inhibit.login` | Added | administrator only: stops new sessions while maintenance is done; a killed backup no longer locks everybody out <!--s 387 g46--> |
| `logout` | Changed | `logout n group` also ends the phantoms n started; `logout` of a session whose process has gone clears the entry and its locks <!--s 386--> |
| `newvoc.mods` | Changed | applied to SDSYS's own VOC when SD is installed, as it already was to new accounts and by `update.accounts` <!--s 501--> |
| `set.batch` | Added | allows or stops allowing a paragraph or sentence that an account may run from the command line (`sd -a<account> <command>`, as a scheduled job does), after checking it in that account's VOC; none is allowed as delivered; until now `batch.jobs` was edited by hand |

## API

The server side of the API, the client library and the language headers.

| Name | Change | What |
|---|---|---|
| client library headers | Added | C# (`sdclient.cs`) and PHP (`sdclient.php`) beside the six already there; neither has been run against a runtime <!--s g200--> |
| client library: dictionary | Added | `sdevaluate`, `sdevalconv`, `sdiconv`, `sdoconv`, `sdiconvs`, `sdoconvs` <!--s 247 409--> |
| client library: files | Added | `sdopenseq`, `sdreadseq`, `sdreadblk`, `sdwriteseq`, `sdwriteblk`, `sdseek`, `sdweofseq` <!--s 441--> |
| client library: more functions | Added | `sdrevision`, `sdgetvar`, `sdsystem`, `sdindices`, `sdtrans`, `sdrtrans`, `sdtxn` <!--s 89 195 410 499 442--> |
| client library: threads | Added | each thread has its own session, transfer buffer and arguments; several threads may use the library <!--s 456--> |
| `master.login` | Changed | the paragraph runs for API connections as for interactive and phantom sessions <!--s 170--> |

## BASIC

Statements, functions, `$mode` words and compiler directives.

| Name | Change | What |
|---|---|---|
| `~=` | Added | comparison that ignores case <!--s 430--> |
| `account.path()`, `vocpath()` | Added | the pathname of an account and of a file named in the VOC, told only where the account may open it <!--s g107 g193 86--> |
| `arg.present()`, `reusing()` | Added | whether the caller passed an argument, and whether with `reuse()` <!--s g108 g169--> |
| `$basic.options` | Changed | a `mode` line takes a list and a minus turns a mode off; an `include` line names records or files that every program includes <!--s 406 407 290--> |
| `bool()` and friends | Added | `bool()`, `is.null()`, `numeric()`: Boolean, SQL-null and numeric conversions <!--s g109 g144 g161 451--> |
| `@build.time`, `@line` | Added | the time the program was compiled and the source line it stands on <!--s 506 211--> |
| `casing on` and `off` | Added | case sensitivity of string comparisons for the rest of the program <!--s g111 g274--> |
| `ceil()` and `floor()` | Added | `ceil()`, `floor()`, `roundup()`, `rounddown()`: whole numbers above and below, and rounding in steps <!--s g112 g129 g174 g175--> |
| `child()`, `signal()` | Added | whether a user number is a running phantom of this process; raises a signal in another process <!--s g113 g182 301--> |
| `class ... inherits as` | Added | the inherited class's object variable can be named; an empty `()` is accepted after a method name <!--s 374 237--> |
| `class` initial values | Added | a `public` or `private` variable may start with a value; `inherits` passes constants to the inherited class <!--s 356 565--> |
| `class` lookup | Changed | a class with 32 names or more is searched through an index, many times faster <!--s 13--> |
| `class`: `restricted` | Added | a name for the class and the classes that inherit it, and no one else <!--s g168--> |
| `class`: `run` | Added | `run` of a class module or its catalogue name makes the object, runs its `main` and lets it go <!--s 484--> |
| `clearcommon name` | Added | sets the variables of the named common block to zero <!--s 52--> |
| `compare()` | Changed | an `i` after `l` or `r` in the justification compares ignoring case; `compares()` does it over two arrays <!--s 307 g114--> |
| `convert()` | Changed | `mcn-`, `mc/n-`, `mcs`, `mcp` with a quoted replacement character, `mt` with `m`, `md` options in any order <!--s 23 183 198 298 488--> |
| `dir()` | Changed | includes the size of each file <!--s 366--> |
| `fix()` | Added | a number with a fixed number of decimals, rounded or cut off <!--s 472--> |
| exceptions | Added | `try`, `catch`, `throw`, `caught()` and `@exception`; many run time errors are caught under openQM's `sys.` names; `dumping` and `saving.stack` <!--s 353 354 355 295 309--> |
| `execute ... stacklist` | Added | keeps the default select list and puts it back when the command returns <!--s 61--> |
| `execute.list` | Added | runs commands for each id of list 0 in turn <!--s g38--> |
| `fcontrol()` | Added | the openQM function: next sequential key, valid id, minimum modulus, line terminator modes, forced writes <!--s 452 102--> |
| `field()` and `vslice()` | Changed | take an asterisk for the number of elements and a subvalue slice <!--s 212 132--> |
| `flush.dh.cache` | Added | makes every process close the dynamic files it keeps cached <!--s 83 123--> |
| `for` with a list | Added | a loop over a list of values, and over the elements of a delimited string, with a delimiter <!--s 84 300--> |
| `get var from device` | Added | reads from a FIFO, port, character device or `openseq` file a character at a time, with a timeout <!--s 583--> |
| `getlocks()`, `testlock()` | Added | information about file and record locks; the owner of a task lock <!--s 508 42--> |
| `getpu()` | Added | the `pu$pathname` key (`pu$form.queue` was added and removed again, see REMOVED) <!--s 214--> |
| `groupstore` and `revremove` | Added | `groupstore`, `revremove`, `setrem`, `rmvd()`: statements and functions over delimited strings <!--s g136 g170 g172--> |
| `$ifdef`, `$ifndef` | Changed | accept `and` and `or` between token names <!--s 219--> |
| `inmat()` | Changed | after `matches` or `matchfield()` it is the number of the pattern that matched; after `matbuild` and `matwrite` it is the element count; a collection array is accepted <!--s 315 454 591--> |
| `input ... fill` | Added | shows a fill character in every empty cell of the field <!--s 389--> |
| `input ... no.echo` | Added | shows nothing as the user types <!--s 168 363--> |
| `input ... raw` | Added | reads exactly the number of characters given, as they arrive <!--s 548--> |
| `inputif` | Added | reads a line only if one is already there, else takes `else` <!--s 584--> |
| `inputnull`, `inputtrap` | Added | a single character typed alone makes the answer null, or sends the program to a label <!--s 408--> |
| `last()` and more | Added | `last()`, `lasts()`, `nv()`, `ns()`: the final element of a delimited string; value and subvalue position numbers (`left()` and `right()` were added and removed again, see REMOVED) <!--s g171 g162--> |
| `locate ... by` | Added | `c` forces a case-sensitive search and `n` a case-insensitive one <!--s 419--> |
| `matchess` and `trimws` | Added | `matchess`, `matchfields`, `trimws`, `trimw()`: `matches`, `matchfield` and `trimw` over a dynamic array; `trimw` trims white space <!--s 302 g152 g153 g189--> |
| matrix arguments | Changed | a matrix passed as an argument needs no `dim` in the receiving subroutine; `if mat a = mat b` compares two matrices; the compiler no longer reports an undimensioned argument <!--s 44 111 519--> |
| `matstr()` | Added | converts a two dimensional matrix to a dynamic array <!--s 509--> |
| `matwritecsv` | Added | one CSV line of every element of a matrix <!--s g154--> |
| `digest()` | Added | the md5, sha1, sha256, sha384 or sha512 digest of a string or a file (`md5()` was added and removed again, see REMOVED) <!--s 63 g118--> |
| `mergelist()` | Added | merges two lists by a mode; a mode for lists not in order; fixed for an empty list <!--s 420 539 566 g155--> |
| `$mode debug.equates` | Added | keeps `equate` and `$define` tokens in the object so the debugger can show, set and watch them <!--s g218 246 239--> |
| `$mode explicit` | Added | a variable must be named in a `dim` statement before it is used <!--s g220 234--> |
| `$mode` lists | Changed | `$mode` takes several names separated by commas, each with an optional minus <!--s 105--> |
| `$mode non.durable.txn` | Added | a committed nested transaction writes nothing until the outer one commits <!--s g221 442--> |
| `$mode partial.expressions` | Added | `a and b` and `a or b` stop evaluating as soon as the value is known <!--s 417--> |
| `$mode strict.equate` | Added | warns when a name given to `equate` or `$define` is also a statement or function name <!--s 582--> |
| `$mode trap.unused.main` | Added | `trap.unused` for the program's own variables <!--s g227--> |
| `no.query` on cataloguing | Added | the `basic` command, the `$catalogue` directive and the `catalogue` line of `$basic.options` take `no.query`, which stops the compiler asking before it removes an older entry <!--s 27 191--> |
| `open ... non.transactional` | Added | a write through that file variable is not undone by a rollback <!--s 64--> |
| `openseq` | Added | `creating` makes the file at once; `shared` lets several processes append; a block device can be opened <!--s 485 397 112--> |
| `option()` | Added | reads and sets the state of an option <!--s 224 473--> |
| `ospath()` | Added | keys `os$fullpathx` and `os$info`; and any program, not only an internal one, may now call `ospath()` with openQM's key numbers 0 to 18, behind the account's OS access (`os$uid`, `os$gid` and `os$modes` answer 0 on Windows; key 18 is the owner's Windows account name) <!--s 293 432 233--> |
| `parse()` and `ttyget()` | Added | `parse()`, `sort.compare()`, `ttyget()`, `ttyset`: split by a pattern; compare by a sort rule; the terminal modes as an array <!--s g166 g183 g187 g190 g191--> |
| `phantom` statement | Added | starts a phantom from a program; the log name may be a variable <!--s 390 351--> |
| `precision inherit` | Added | takes the precision of the calling program <!--s 201--> |
| `@pstat` | Added | text a program leaves for `pstat` to show <!--s 492--> |
| `quotes()` family | Added | `quotes()`, `squotes()`: enclose every element of a dynamic array in quotes <!--s 11--> |
| `read` etc. as a condition | Added | `read`, `readnext`, `open` and the like may be the condition of `while` or `until` <!--s 206--> |
| `recordlocku` | Changed | fixed: it did not always trap an illegal record id <!--s 528--> |
| `redim` | Added | resizes a matrix passed to a subroutine as an argument <!--s 215--> |
| `regex()` | Added | regular expression matching <!--s 510--> |
| `seek` | Changed | fixed: a negative offset from the end of a sequential file was refused <!--s 259--> |
| select list variables | Added | `formlistv`, `getlistv`, `writelist`, `movelist`, `movelistv`: select list variables and numbered lists <!--s 291 g134 g135 g195 g156--> |
| `select.socket()` | Added | waits on the sockets held in a matrix <!--s 161 g176--> |
| `selectindexv` family | Added | `selectindexv`, `selectleftv`, `selectrightv`: index scans into a select list variable <!--s g177--> |
| `send` | Added | `writeseq`, or with a colon `writeblk`, to a file opened with `openseq` <!--s g178--> |
| `socket.info()` | Changed | fixed: `skt$info.open` on a number, a string or an unassigned variable stopped with a fatal error <!--s 249--> |
| `!sort` | Changed | sorts a select list variable; the internal sort is open to programs <!--s 274 371--> |
| `sselectv`, `sselectn` | Added | sorted selects into a select list variable; `right.aligned` and `descending` <!--s 209 243 367--> |
| `status()` after a transaction | Added | 0 if it committed, 1021 if it rolled back <!--s 19--> |
| string arithmetic | Added | `sadd`, `ssub`, `smul`, `sdiv`, `scmp`: exact string arithmetic on numbers of any length and any decimals <!--s 391 468--> |
| substring assignment | Added | `s[3] = "xy"` overwrites the last three characters <!--s 41 325--> |
| `trans()` family | Changed | `trans()`, `rtrans()`: accept `a`, `s` and `c` items and an `l` link; a file that will not open takes the error action of the call <!--s 43 182 7--> |
| variable names | Changed | a name with two or more underscores together (`a__b`) is valid <!--s 336--> |
| `watch` | Changed | the debugger's `watch variable operator value` stops only when the condition is met <!--s 45--> |

## DATA

Data collections, JSON, XML, CSV and the verbs that import them.

| Name | Change | What |
|---|---|---|
| collection arrays | Added | `mat()`, `c{list, n}`, `ins ... as`, `del`, `inmat()` on an array |
| collection file verbs | Added | `ed`, `copy`, `compare.files`: work on a collection file; the post-write trigger no longer crashes the process |
| collection files | Added | `create.file name collection`; records are collections stored as JSON; `read` and `write` them whole; `ct` shows JSON <!--s 304--> |
| `collection()` and `c{name}` | Added | a collection is a set of named values read and written by name; `enumerate()`, `element.exists()` <!--s 311 518 529 339--> |
| `csv.mode` | Added | how `printcsv`, `writecsv` and `formcsv()` quote, with a delimiter, quote and escape character <!--s 173 200--> |
| `d` conversion: `i` code | Changed | fixed: the ISO week number is worked out without `yi` beside it (it gave whatever number was left in memory) |
| `element` keyword in queries | Added | names an element of a collection file by its path, in a display list, `with`, `by`, `sum` and the like |
| `expand()` and links | Added | a link `"file:id"` is followed; `trans()` of an `e` item |
| file variable in a collection | Changed | a collection holding a file variable is written to a collection file as a null |
| `hu` conversion | Added | `oconv` and `iconv` escape and unescape |
| `indices` on `e` items | Added | a data collection element can be indexed; a query with `with` on it uses the index |
| `jboolean()` and `jtype()` | Added | `jboolean()`, `jnull()`, `jtype()`: true, false and null in collections, and the type of a value; a Boolean type <!--s 312--> |
| `jparse()`, `jbuild()` | Added | JSON text into a collection and back |
| `mcdx` conversion | Changed | fixed: gives hexadecimal both ways, as `mx` does (`oconv` returned the number unchanged); kept as a second name of `mx` for programs moved from openQM |
| operators on an element | Added | `+=`, `-=`, `*=`, `/=`, `:=` change an element in place |
| the debugger and collections | Added | `/c`, `/c{path}` and `dump c{sub} pathname` show and write a collection; diving in with `/*` no longer crashes <!--s 530--> |
| `xml` keyword for queries | Added | `list ... xml` writes the report as XML, with an optional DTD or schema <!--s g211 g202--> |

## FILES

File handling: opening, indexes, triggers, print files, sorting, sequential files.

| Name | Change | What |
|---|---|---|
| `account:file` file names | Changed | always available, with no `filerule` setting: a name in no VOC entry with one colon opens that account's file, with exactly the checks of a Q-pointer (an account you may `logto`, not suspended) |
| `analyse.file` | Changed | `statistics` shows a histogram of group utilisation <!--s 360--> |
| `analyse.index` | Added | every index with its number of values and spread <!--s g9--> |
| `catalog -name` | Added | a hyphen is a global catalogue prefix; `delete.catalog -name` removes it <!--s 217--> |
| `clear.file` | Changed | fixed: a `no.resize` file keeps its modulus <!--s 590--> |
| `configure.file ... reporting` | Added | shows how many records have been converted <!--s 172--> |
| `create.file` | Added | `comment`, `multifile` and a relative `pathname` kept relative in the VOC <!--s 383 522 278--> |
| `create.index` | Added | `no.case`: keys that differ only in case are one key; `deleting` replaces an index; a default location in `$index.path` <!--s 54 424 184--> |
| `dir_dict` | Added | three items for a directory file's dictionary: `days`, `dtm` and `owner` <!--s 181--> |
| directory file line ends | Added | line terminator modes (`l`, `c`, `b`, `x`) and triggers <!--s 177--> |
| `directory files` ids | Changed | the record ids may hold bytes 128 to 247 <!--s 34--> |
| `disable.index` | Added | stops an index being kept up to date for a large load; `build.index` switches it on <!--s g28--> |
| exclusive access | Changed | a command that needs a file to itself names the user holding it when it cannot get it <!--s 107--> |
| `file.stat` | Added | one line per file: type, modulus, records, bytes and flags; limited to named files; with dictionaries <!--s 109 152 g40--> |
| `find.file`, `find.program` | Added | what a file is; the catalogue entries of a program <!--s g42 g43--> |
| `fixdir` | Added | takes the carriage returns out of directory file items that came from a Windows system <!--s 458--> |
| hashed files | Changed | a split that finds the disk nearly full stops before the file's size is changed; `sdfix -z` clears dead space <!--s 329 33--> |
| `hold.file.logger` | Added | a catalogued subroutine called when a hold file print unit opens and closes <!--s 56--> |
| `l-type` dictionary links | Added | usable in an `i`-type; links may follow links, up to ten, and reach `a`, `s` and `e` items <!--s 7 204 544--> |
| `list.common detail` | Added | shows where each common block was created <!--s 362--> |
| `list.index` | Changed | the report may go to a printer <!--s 73--> |
| `list.triggers` | Added | every trigger subroutine used by the files of an account, multifiles, dictionaries and directory files included <!--s 74 187 321--> |
| `listf`, `listfl`, `listfr` | Changed | list a multifile line by line, and take `with` and `without trigger`, `encryption` and `replication` <!--s 3 185--> |
| print unit mode 3 | Changed | takes an update lock on the `$hold` item while it is written <!--s 53--> |
| `rebuild.all.indices` | Added | rebuilds the indices of every file in the account <!--s 58--> |
| `select` of a directory file | Changed | fixed: at the open-file limit it closes the oldest cached file and goes on <!--s 279--> |
| `set.file` | Changed | the target may be a `q`-pointer; a `q`-pointer with no file name points at the VOC <!--s 32 435--> |
| `set.trigger` | Changed | fixed: refused every function name; takes `all`; no longer needs exclusive access <!--s 388 157--> |
| sort of long records | Changed | the disk sort handles records and keys over 32 KB <!--s 455--> |
| sort with many work files | Changed | fixed: a sort that needs more work files than `sortmrg` put records with equal keys out in an order that depended on `sortmem` and `sortmrg`, and a `unique` sort could keep a later record; now they come out in the order they arrived |
| deleting from a large index | Changed | fixed: removing the last entry under a branch of an index of three levels cut the rest of that branch out of every lookup by key; rebuild an index that has had deletions with `build.index` |
| trigger on a read | Changed | fixed: a locally catalogued read trigger could end the process <!--s 317--> |
| `vocname` letters | Added | `r` opens a file read-only, `n` non-transactionally, `s` with forced writes, from field 6 of its VOC entry <!--s 197 380 102--> |

## QUERY

The query processor and the dictionary.

| Name | Change | What |
|---|---|---|
| `absent.ignore` | Added | do not print the `not found` list for ids that are not in the file <!--s 25--> |
| `break.on "'n'"` | Added | starts a new page and numbers it 1 again <!--s 16--> |
| `by.exp` | Changed | more than one `by.exp` in the same association is sorted <!--s 572--> |
| `csv 3` | Added | every item quoted, numbers too <!--s 26--> |
| dictionary expressions | Changed | divide by zero is zero (an `if` with a part missing, a format after a value and hyphens in names were added and removed again, see REMOVED) <!--s 36 48 270 271 423 547 564--> |
| `for`, `from none` | Added | `search file for "text"`; `from none` ignores an active list 0 <!--s 190 378--> |
| `in`, `not.in` | Added | test a value against a saved list or a file record <!--s 94--> |
| `median`, `mode`, `range` | Added | figures at the end of a report and each breakpoint <!--s 231 g209--> |
| `$mode` in an `i`-type | Added | an `i`-type may begin with `$mode` for a few of the compiler modes <!--s 489--> |
| `no.page` | Changed | accepted on any query command <!--s 379--> |
| options | Added | (`query.sort.no.case`, `clear.select`, `query.string.comp`, `query.str.comp.all` and `default.mv` were added and removed again, see REMOVED) <!--s 140 299 412 205 403--> |
| `$query.defaults` | Changed | field 3 holds default words for `select`, `sselect` and `search`; field 4 the format of the id column <!--s 122 405--> |
| `reformat ... @record` | Added | appends the whole source record <!--s 546--> |
| `reporting` | Added | `n record(s) examined` for every thousand records <!--s 416--> |
| `rpt` | Added | repeats a single valued field on each line of a report on a multivalued one <!--s g210--> |
| `scan`, `search ... display` | Added | show the lines of a record that hold the strings; `search all` searches the id too; strings may come from a file <!--s 437 447 221 141--> |
| `select file field` | Changed | a field no clause uses is `saving multivalued field` <!--s 39--> |
| `show` | Changed | `b` goes to the bottom; `sort.sup`; a missing record is listed and the command ends <!--s 477 495 524--> |
| `sorted.sample n` | Added | counts the records after the sort <!--s 438--> |
| `vertically` | Changed | `fmt` for the name and data format; `$vlist` sets them for the file; multivalued data and a wrapped line are told apart <!--s 160 579 580--> |
| `when field` | Changed | with no operator keeps the values that are not null <!--s 543 343--> |
| `x` breakpoint control | Added | captures the previous value of a break field in `@bpv` <!--s 232--> |

## SYSTEM

The kernel, `sd.conf`, and the numbered keys.

| Name | Change | What |
|---|---|---|
| `-quiet` | Changed | `sd -quiet` suppresses the VOC update question <!--s 533--> |
| `-status` | Added | `sd -status` shows the version, start time and process counts <!--s 511--> |
| `cleanup=n` | Added | seconds between the checks that clear sessions that ended without logging out <!--s 98 g283--> |
| `config` | Changed | lists the new settings; `config()` reads them |
| `deadlock=2` | Added | saves the lock tables when a deadlock is found <!--s 500--> |
| `fileinfo()` | Added | the keys 1022 to 1040 as the openQM manual numbers them; `fl$seqtype`, `fl$locks`; 1021 now answers the user numbers <!--s 62 113 498 337--> |
| `intprec` | Changed | default 11 <!--s 6--> |
| lock table | Changed | the time each lock was taken and each wait began is noted; more than 65,535 locks in a file work; a program that filled the table can be logged out <!--s 487 344 532--> |
| `numlocks` | Changed | range checked, 1 to 32767 |
| `phantoms=u,n` | Added | keeps user numbers for phantoms started with `user` <!--s 31 g296--> |
| process dump | Changed | shows the length of each string, the variables of objects and the environment <!--s 22 125 569 439--> |
| `pterm` keys | Added | `pterm erase`, `ctrl.filter`, `mark`: which key erases; control characters filtered; control keys that type the marks <!--s 155 253 254--> |
| `sd.conf` parameters | Added | `dhcache`, `lgnwait`, `maxrlock`, `pwdelay`, `userpool`: `sd.conf` parameters, each optional with the old fixed number as the default <!--s 90 46 313 106 551--> |
| `sortmem` | Changed | default 4096 <!--s 535--> |
| `status` | Changed | file times are in the user's time zone; field 27 is the file pathname <!--s 96 585--> |
| `system()` keys | Added | 14, 19, 20, 21, 33, 35, 45, 1016, 1036, 1037, 1040, 1045, 1047, 1048, 1049, 1051, 1062, 1065, 1067, 1071, 1073, 1083, 1086, 1088 <!--s 65 66 114 192 225 244 206 294 307 308 326 421 433 586 587 g252 g253 g254 g255 g256 g260 g261 g265 g266 g267 g270 g271 g274 g276--> |
| terminfo | Changed | `eblink`, `eprot`, `edim`, `erev`, `ebold` capabilities; `xmc#1` in the two ADDS 4000 entries <!--s 47 545--> |
| the call name | Changed | can be as long as 128 characters (the lower of 128 and `maxidlen`) <!--s 241--> |
| the startup process | Changed | its `@tty` is `startup` <!--s 91--> |
| time zone and `epoch()` | Added | `epoch()`, `mvdate()`, `mvtime()`, `mvdate.time()`, `mvepoch()`; `set.timezone` and `config timezone` <!--s 69 124 g126 g157 g158 g159 g160 g181 g310--> |
| `usplit=1` | Added | interactive users take the lowest user number, phantoms and API sessions the highest <!--s g312--> |

## TCL

Commands and VOC verbs that every account has, and the command language.

| Name | Change | What |
|---|---|---|
| `block.print`, `block.term` | Added | print text, or show it on the terminal, in letters seven rows high <!--s g11 g12--> |
| `catalog ... local relative` | Added | stores the object file's path relative to the account <!--s 131--> |
| `catalog` overwrite | Changed | pointing a local catalogue entry at a different object file asks first <!--s 490--> |
| `catalog` prefix | Added | a prefix separate from the call name; `$private.catalog` or `$private.catalogue` <!--s 210 93--> |
| catalogue name as a command | Changed | a program run by its catalogue name takes `lptr`, `no.page` and the like <!--s 146--> |
| command stack | Changed | `.c-` undoes a `.0`; the stack is kept in the account the user entered <!--s 296 396--> |
| `command.logging` | Added | a log of every command this session runs, in the account directory, readable by its owner only <!--s 444 g16--> |
| `como` | Added | `append`, `in file`; `$como` ids pass the same name transform <!--s 8 361 9--> |
| `compare.files` | Added | counts the records only in one, only in the other, in both but different <!--s 534--> |
| `ct` | Changed | `id.sup`, `num.sup`; lower case file names; the object code of a compiled dictionary item is not shown <!--s 242 347 373--> |
| `decatalog` | Added | deletes a local catalogue entry and its object code <!--s 576--> |
| `delete` | Changed | a record another user holds locked is reported and skipped <!--s 50--> |
| `delete.account` | Changed | not stopped by a file it cannot open when it looks for references <!--s 348--> |
| `delete.common all except` | Added | deletes every named common block but those listed <!--s 425--> |
| `docs.install` | Added | SDSYS puts a directory of PDFs into the shared account's `pdf` directory; the installer runs it on the `pdf` folder beside it, and copies the release's changes document there too |
| `ed` | Changed | `l` with no text as the first command works; marks typed in input; `ev` on a compound `i`-type; line numbers show positions in edit values mode; `spool` closes the printer; external commands; automatic ids <!--s 264 268 320 331 375 446 523 305--> |
| `fstat` | Changed | wider columns <!--s 55--> |
| `fstat.user` | Added | file activity of each session <!--s g44--> |
| `git` option | Added | a directory file keeps `.gitignore` and `.gitattributes` under their own names <!--s g238--> |
| `hot spot monitor` | Changed | counts opens, reads, writes and deletes of each program <!--s 491--> |
| `if` in a paragraph | Added | `exists`, `not.exists`, `in` and `not.in`, with `no.case` <!--s 28 230 426 476--> |
| inline prompts | Changed | largely case insensitive; may use quoted prompt strings <!--s 171 377--> |
| `k` entry in the VOC | Changed | fixed: a `k` entry over a locally catalogued program stopped with "Unable to load" <!--s 263--> |
| list merges | Changed | `merge.list` finds a key without scanning, so large lists merge in seconds <!--s 414--> |
| `list.item` | Changed | numbers lines beyond 999 with as many digits as needed <!--s 349--> |
| `listu`, `who`, `pstat` | Changed | `!listu` too: show the account and the login name; `listu detail`; the blocking user and when a wait began <!--s 12 24 29 38 77 121 289 427 577--> |
| `logto reset all` | Added | discards all programs, menus and paragraphs at every command level <!--s 30--> |
| `map local`, `map no.page` | Added | list the locally catalogued programs; heading once <!--s 153 287--> |
| `move.list` | Added | the command form of `movelist` <!--s g62--> |
| `multisort` | Added | `!multisort` sorts several related lists by one of them <!--s 568--> |
| `option` words | Added | `dir.dtm`, `git`, `inherit.ownership` and `spool.command` (twenty more were added and removed again, see REMOVED) <!--s 288 79 314 428 461 445 37 57 154 165 404 429 49 g230 g231 g232 g233 g237 g239 g240 g241 g242 g245 g247 g248--> |
| `oscopy` | Added | copy an operating system file; `overwrite`, `append`; `!oscopy` and `!ioscopy` (a whole tree) for programs <!--s 517 369--> |
| `phantom` | Added | `no.msg`, `data`, `log`, `group` and `user` options; `!phlog` gives a phantom's log record; a phantom started while SD is suspended gives back its place <!--s 87 137 364 483 31 385 280--> |
| phantom and terminal lists | Added | `list.phantoms`, `list.term.types`: the phantoms and no one else; the terminal types <!--s 381 g49--> |
| `private vocabulary` | Added | `$private.voc`: a file of commands searched after all other command sources <!--s 1--> |
| `profiler` | Added | records what the programs of a session do and where <!--s g66 g203--> |
| `redo` | Added | runs a command again and again, `times` and `every` <!--s 188--> |
| saved list verbs | Changed | `save.list`, `get.list`, `delete.list`: `keep`, `deleting`, `count.sup`, a default name, a name left out, `in file` <!--s 2 384 387 401 494--> |
| `selectindex` | Added | the command form of the statement <!--s 119--> |
| `setptr` | Changed | `form.feed`, `inform`, `eject`, `as ... in file`; the digits of `next` <!--s 51 59 70 139 448--> |
| `show.list` | Added | a page at a time, starring and clearing items <!--s 449--> |
| `sort.list`, `select.dir` | Added | sort a saved list; select the files of a directory <!--s 158 465--> |
| `sp.view` | Changed | `by field`; `x` deletes the item shown; shows where output goes for every print unit mode <!--s 450 560--> |
| `term` | Changed | takes two numbers for the default printer <!--s 466--> |

## TOOLS

The debugger, from the openQM list.

| Name | Change | What |
|---|---|---|
| `debugger` | Changed | full-screen display on a terminal with an alternate screen; `/*` for every variable; `^`; `window n`; `set v = token`; a stop before each `case`; a blank line repeats the last command; `brk` lists the breakpoints <!--s 21 67 97 142 193 203 327 335 513 550--> |
| `debugger` phantom | Changed | an `@variable` is read from the process being debugged <!--s 251--> |

## REMOVED

These were in W1.1-3 - or were added and taken out again during W2.0-0 - and **SD no longer has them**. This is the one place where a removal is listed,
whatever the area it belonged to. Most were removed because they existed only to make SD behave like another MultiValue
product, or gave a second way to do something SD already does one way. **A program, a login paragraph or a `$basic.options` record that uses one has to
be edited**; the last column says what to write instead. A program that was compiled with a removed mode keeps what it was
compiled with until it is compiled again.

| Name | Change | What |
|---|---|---|
| AccuTerm terminal types | Removed | the eleven `-at` terminal types and AccuTerm's escape sequences |
| `$mode` words that imitated other products | Removed | `prclose.default.0` (write `printer close on` *unit*), `unassigned.common` (a common variable starts as zero), `no.case.invert` (give `input` the `nocaseinvert` clause) and `optional.then.else` (a `read` takes a `then` or an `else`) are refused now with *Unrecognised mode name*; `conditional.statements`, `implied.stop` (end a program with `stop`) and `exception.save.stack` (write `saving.stack` on the `catch`) were added and removed within W1.2-0, so they never shipped |
| `option` words that imitated other products | Removed | `option pick` and 22 words, refused now with *Option name not recognised*: `assoc.unassoc.mv`, `pick.breakpoint`, `pick.breakpoint.u`, `pick.explode`, `pick.grand.total`, `pick.implied.eq`, `pick.null`, `pick.wildcard`, `qualified.display`, `with.implies.or`, `query.no.case`, `query.priority.and`, `ampm.upcase`, `crdb.upcase`, `no.date.wrapping`, `space.mct`, `lock.beep`, `ed.no.query.fd`, `create.file.upcase`, `select.keep.case`, `debug.rebind.keys`, `proc.a`. SD does what it did with them off: write `with city = "Reno"`, use `like` for wildcards, brackets and `or` for the order of tests, `no.case` after an operator or `option query.sort.no.case` for case; times and amounts are `am`, `pm`, `cr`, `db`; a date such as 31 February rolls into the next month; a lock wait is silent; `fd` in `ed` asks first; `create.file` names a file in lower case |
| screen save and restore | Removed | `save.screen()` and `restore.screen`: still exist and do nothing the terminal could see |
| `sdterm` terminal type | Removed | with SDTerm and SDConsole, and the `term display` line about them |
| `term 120,36` at login | Removed | new accounts no longer carry it in their `login` paragraph |
| second names for statements | Removed | `$insert` (write `$include`), `include` without the `$` (write `$include`), `com` (write `common`), `dimension` and `redimension` (write `dim` and `redim`), `enter` with `$mode pick.enter` (write `call`, or `chain` to hand control on for good), `perform` (write `execute`), `printerr` (write `inputerr`), `remark` (write `rem`), `rqm` (write `sleep`), `sub` (write `subroutine`, also after `local`, `private` and `public`) and `tclread` (read `@sentence`): the compiler refuses each |
| second forms of statement clauses | Removed | `execute ... setting` (write `returning`), `execute ... passlist` with no variable (it did nothing: name the variable, or leave the clause out), `input ... for` and `input ... timeout` (write `waiting`), `opentemp ... ecs` (a word that was read and ignored: it is an ordinary name now, so the compiler warns that it is never assigned a value) and the bracketed Pick form `locate(expr, array, f, v; position; order)` (write `locate expr in array<f, v> setting position`) |
| second names for functions and variables | Removed | `ereplace()` (write `change()`, which takes -1 for every occurrence), `sentence()` (read `@sentence`), `swapmarks()` (it returned its argument), `terminfo.ex()` (write `terminfo()`) and `@system.set` (write `@system.return.code`) |
| `mcd`, `mcx` and `mcxd` conversions | Removed | second spellings of `mx`: an invalid conversion code now, STATUS 2 (`mcdx` stays, as `mx`) |
| second spellings of query keywords | Removed | `col.spcs` (write `col.spaces`), `display.name` (`col.hdg`), `evaluate` (`eval`), `calculate` (`calc`), `intersection` and `difference` (`intersect` and `diff`, also in `merge.list`), `margin` (`left.margin`), `stats` (`statistics`), `supp` (`hdr.sup`) and `only` (`id.only`): **a new account does not have their VOC records**, and the next `update.accounts` removes them from existing accounts, through the deletion list (saved copy first; a record of your own with the same name is kept; `restore.voc` puts one back) |
| `only` and `id.only` before the file name | Removed | `list only customers` is refused: write `list customers id.only` |
| `=>`, `=<` and `><` | Removed | the mirrored spellings of `>=`, `<=` and `<>`; as for the keyword synonyms, a new account has no record for them and an old account keeps its own |
| eleven `option` words | Removed | `run.no.page` and `paginate.on.heading` (a run is paginated unless `run ... no.page` says not), `pick.ml.conv.mask` (a left bracket in `ml` / `mr` is the round-bracket negative style), `chained.select` (a select does not run the data queue), `default.mv` (a blank S/M flag is single valued), `query.string.comp` and `query.str.comp.all` (`=` and `ne` compare as BASIC does), `assoc.all` (the dictionary's associations are used), `query.footer.pause` (no pause after a page footer), `query.merge.print` (a report closes printer 0) and `keep.old.object` (a failed compile leaves no object code). Each behaves as it did with the option off; their numbers stay reserved |
| `dquote()`, `dquotes()`, `swap()`, `xlate()` | Removed | second names of `quote()`, `quotes()`, `change()` and `trans()`: write those |
| `caption`, `nopage`, `col.hdr.space` | Removed | `caption` and `nopage` were second names of `grand.total` and `no.page`; `col.hdr.space` (a blank line under the column headings) was added and taken out again: end a heading with a blank line |
| `listdict`, `edit.list` | Removed | write `list dict` *file*, and `ed $savedlists` *name* |
| loose forms of a dictionary expression | Removed | an `if` with no `then` or no `else` is refused again (messages 2950 and 2951), a hyphenated item name such as `cust-no` is read as a subtraction, and a format string straight after a value needs its operator |
| `$mode execute.clearlist`, `open.fail.zero.fvar`, `pick.readnext` | Removed | added and taken out again in this release: the default select list is not cleared before an `execute` (use `clearselect 0`), the file variable of a failed `open` stays unassigned, and a `readnext` that takes its `else` sets the id variable to the null string. Their mode bits stay reserved |
| three more `option` words | Removed | `chain.keep.common` (`chain` always discards the unnamed common), `backslash.not.quote` (on Windows a backslash in a command line is always an ordinary character, never a string quote, because it separates the parts of a pathname) and `correlative.reuse` (a shorter array's missing values count as zero unless an operand says `reuse()`) |
| `inputclear` | Removed | write `clearinput`; the file type constant `FL$TYPE.SH` (a static hashed file SD never had) is gone too |
| `@am`, `@svm`, `@user`, `@user.no`, `@filename` | Removed | second names of variables that stay: write `@fm`, `@sm`, `@logname`, `@userno` and `@file.name` (a dictionary item of your own that says `@filename` stops compiling until changed) |
| `go`, `go to`, and `#` before a compiler directive | Removed | write `goto` (also in `on ... goto`) and `$ifdef`, `$define`, `$include` |
| second spellings of query words | Removed | `avg`, `enum`, `vert`, `percent`, `pct`, `%`, `header`, `footer`, `first`, `#` and `&`: write `average`, `enumerate`, `vertically`, `percentage`, `heading`, `footing`, `sample`, `ne` and `and`; a `break.on` control `l` is no longer ignored when `u` is given too; and a name that is `f` and a number is a field only if the dictionary has an item of that name |
| terminal case inversion | Removed | `pterm case invert` / `noinvert` (and the line in `pterm display`), `input ... nocaseinvert`, the `invcase` setting of `sd.conf` (a kept `sd.conf` is cleaned by the installer), `system(1001)`, `pterm(PT$INVERT)` and the `no.invert` option of `sed`; `keyinc()` is now the same as `keyin()`, and field 2 of `ttyget()` is always 0. Type in the case you want |
| `nano` | Removed | the second external editor, with its syntax file and the page about it (the shared parts moved to the `micro` page): write `micro`, `sed` or `ed` |
| `set.queue`, `sp.assign`, `getpu(pu$form.queue)`, `system(1066)` | Removed | Pick style form queues were added and taken out again in this release: use `setptr` with the settings you want |
| `copyp`, `copy.listp` | Removed | the Pick-style copy and its saved-list form (`copy.listp` was added and removed again in this release): write `copy` and `copy.list` |
| `make.index` | Removed | write `create.index` and then `build.index` |
| `list.union`, `list.inter`, `list.diff` | Removed | the saved-list twins of `merge.list`: `get.list` the two lists and `merge.list 1 union 2 to 3` (or `intersect`, `diff`) |
| `cd` | Removed | the short name of `compile.dict`: write `compile.dict` |
| `md` | Removed | the Pick name for the VOC (a Q-pointer to `voc`): write `voc` |
| `create.file ... no.case` and `... case` | Removed | every file is case insensitive, so neither word means anything; `configure.file ... no.case` stays for converting an old file |
| `catalogue`, `$catalogue`, `no.catalogue` | Removed | the British spellings: write `catalog` (the verb, and the `$basic.options` word), `$catalog` and `no.catalog` |
| `bscan`, `root`, `key()` | Removed | added and taken out again in this release: scan an index with `selectindex`, `selectleft` / `selectright` and `setleft` / `setright` |
| `call "file name"` | Removed | the Pick style call was added and taken out again in this release: catalogue the program and call it by name |
| `is.alnum()`, `is.alpha()`, `is.digit()`, `is.graph()`, `is.mark()`, `is.space()`, `left()`, `right()`, `md5()` | Removed | added and taken out again in this release: use `alpha()`, `num()` and `matches` for the character tests, `s[1, n]` and `s[n]` for the ends of a string, and `digest(s, 0, 'md5')` |
| `adds()`, `subs()`, `muls()`, `divs()` | Removed | added and taken out again in this release: the operators `+ - * /` work element by element on dynamic arrays |
| four more `option` words | Removed | `no.sel.list.query` (`no.query` alone skips the question *Use active select list?*), `catalogue.local` (`catalog` and `delete.catalog` with no word work on the private catalogue; say `local`), `inherit.mfile.path` (a new multifile subfile goes in the directory named for the file unless `pathname` says otherwise) and `correlative.nocase` (a correlative is case blind through its own `A;NOCASE;` flag or an I-type's `$mode nocase.strings`) |
| `analyse.file` | Removed | the British spelling: write `analyze.file` (the American one stays) |
| `cleardata`, `clearinput`, `clearprompts`, `clearselect` | Removed | the run-together second names of `clear.data`, `clear.input`, `clear.prompts` and `clear.select` (the BASIC statements of the same names are not affected) |
| `cs` | Removed | second name of `clr`: write `clr` |
| `delete.catalogue` | Removed | the British spelling: write `delete.catalog` |
| `rename` | Removed | second name of `cname`: write `cname`. (`cname` still takes the comma form, `cname old, new`.) |
| `sp.open` and `sp.close` | Removed | write `printer keep.open` and `printer close` |
| `sd -l` | Removed | "apply new licence": SD has no licence, and it set a flag nothing read; `sd -l` is an unrecognised option now |
| terminal types of old hardware | Removed | the Data General, MDC Prism, Prime and Televideo 910 definitions: `dg210 dg-ansi dg-generic dg6053-old dg100 prism2 prism4 prism5 prism7 prism8 prism9 prism12 prism14 p4 p5 p7 p8 p9 p12 p14 pt100 pt200 wren fenix pt100w pt200w wrenw fenixw pt250 pt250w tvi910` (31 of the 82 names `list.term.types` showed). Use `ansi`, `vt100` or `xterm` |
| `system:account:file` file names | Removed | bit 2 of `FILERULE` and a Q-pointer's fourth field named a file on another system and opened nothing; the name form is gone and a Q-pointer with a fourth field is refused (3003) |
| eleven `sd.conf` settings, `sd -<n>`, and the `gdi` and `raw` words of `setptr` | Removed | `apilogin`, `codepage`, `creatusr`, `exclrem`, `fixusers`, `gdi`, `jnldir`, `jnlmode`, `portmap`, `ringwait` and `txchar` (the first two groups did nothing; `fixusers` and `portmap` gave a connection a fixed user number): a line naming one stops SD from starting, so the installer takes it out of a kept `sd.conf`; `config('...')` no longer answers them and `config` no longer lists them; `sd -<n>` (start with a given user number) is gone; `setptr` always uses its raw mode, and its `gdi` and `raw` words are no longer keywords |
| six `option` words and `keep.select` | Removed | `unass.warning`, `div.zero.warning` and `non.numeric.warning` (with the shortcut `sdbasic.warnings`): an unassigned variable, a divide by zero and a non-numeric value are always errors, so test the value first; `inherit`: a phantom starts with every option off; `query.sort.no.case`: a sort is by case (`sp.view ... by field no.case` still ignores it, by sorting the list itself); `clear.select` and the `keep.select` statement: a select list left active is left for the next command, and `clear.select` clears it |
| twenty-two `$mode` words | Removed | `string.locate`, `composite.readnext`, `pick.read`, `selectv`, `pick.select`, `stdfil`, `stdfil.shared`, `write.delete.then.else`, `autolock`, `pick.substr`, `pick.substr.assign`, `compatible.append`, `pick.convert`, `count.overlap`, `index.overlap`, `change.no.overlap`, `case.sensitive`, `for.store.before.test`, `pick.jump.range`, `optional.final.end`, `pick.matrix` and `heading.no.eject`: each is refused with *Unrecognised mode name*, and the program does what it did with the mode off (the `keep.select` statement went in the same way with `option clear.select`); write `heading no.eject` for the last, and name the file variable for `stdfil`. `selectv` *file* `to` *var* stays a statement. The programs that used `$mode stdfil` and `$mode selectv` had no replacement; an I-type may no longer say `$mode count.overlap`, `index.overlap`, `change.no.overlap` or `compatible.append` |
| seven more `option` words | Removed | `numeric.exponent` (`123.45E-2` is not numeric), `suppress.abort.msg` (`abort` always says where it ran), `dir.sel.omit.hidden` (a select of a directory file includes dot files), `no.phantom.notify` (a phantom always tells its parent), `force.reload`, `stacked.account` (an `execute` of `logto` stays in the account it went to) and `command.level.locks` (a file variable that goes closes its file and its locks) |
| `$mode time.ms` and `$mode default.unass.args` | Removed | write `system(1020) / 1000` for milliseconds; a default argument value needs `var.args` |
| `closeseq` and `equ` | Removed | write `close` and `equate` |
| `extract()`, `replace()`, `insert()`, `delete()` and `subr()` | Removed | write `a<f,v>`, `a<f,v> = x`, `ins x before a<f,v>`, `del a<f,v>` and `call` or `deffun` |
| `procread`, `procwrite`, `@pib`, `@sib`, `@pob`, `@sob` | Removed | leftovers of PROC, which went earlier |
| `!` (the shell verb) | Removed | write `sh command` |
| the global catalog prefixes `*` and `-` | Removed | `!` and `$` stay, and `_` names a recursive pcode program |
| the word forms of query operators | Removed | `equal`, `greater`, `less`, `before`, `after`, `matches`, `matching`, `not.matching` and `spoken`: write `eq`, `gt`, `lt`, `like`, `unlike` and `said` (the word `not` stays) |
| `colour`, `without`, `no.grand.total` | Removed | write `color`, `with no` and `grand.total "'L'"` |
| fourteen dead query keywords | Removed | `verify`, `verify.sup`, `exclusive`, `creating`, `inquiring`, `portrait`, `odd`, `even`, `mark`, `space`, `no.label`, `no.object`, `static` and `encrypt` were read by nothing; `group` stays |
| `setptr` print mode 5 and the `version` keyword | Removed | the terminal's auxiliary printer port; a file is made in the current format |
| old terminal definitions | Removed | `addsviewpoint`, `viewpoint`, `adds4000`, `viewpoint60`, `vp60`, `vp`, `vpa2`, `vt52`, `hpgeneric`, `hp`, `ibm-pc`, `ibm5051`, `5051`, `glasstty` and `kermit`: use `ansi`, `vt100` or `xterm` (`wyse50` and `wyse60` stay) |
| VOC record type M (menu) | Removed | a VOC record of type M is no longer run as a menu |
| `FILERULE` | Removed | the sd.conf parameter and the `path:pathname` form of file name (write an F-pointer); the `account:file` form is always on now (see FILES) |
| `listf`, `listfl`, `listfr`, `listk`, `listpa`, `listph`, `listq`, `listr`, `lists`, `listv` | Removed | `list voc with type = "F"` (and `and is.remote = ""` / `and is.remote` for local / remote files), `"K"`, `"PA"`, `"PH"`, `"Q"`, `"R"`, `"S"`, `"V"` for the other types; add `ftype desc data.name dict.name` after `voc` for the file columns |
| `sd.voclib` | Removed | nothing: the file held only the ten sentences above, and its VOC pointer is removed from every account |
| C dictionary item type (and the compiler's C-type mode, @ANS return) | Removed | write the calculation as an I-type; it may call a catalogued subroutine with SUBR(); compile.dict says message 12998 for a C item |
| A and S dictionary item types (the correlative, `a;nocase;`, an `if` in field 8) | Removed | write the item as a `d` item (a field of the record) or an `i` item (a value worked out from the record; the correlative's calculation goes here). `compile.dict` says message 12943 for an A or S item and makes no object code; a query that names one stops with *Unexpected A type item (NAME) in query sentence*. An index made from one is no longer used, so a query on its field scans: delete it with `delete.index` |
| create.file name,part | Removed | create each part as an ordinary file (create.file part) and share the dictionary with create.file part using dict name |
| create.file ... multifile | Removed | create an ordinary file; the word is now an unexpected token |
| delete.file name,part | Removed | delete.file part (each part is an ordinary file); the multifile cancel question (6133) is gone |
| open "name,part" (BASIC) and file,part in TCL verbs | Removed | open the part by its own VOC name; a comma is part of the name, so "a,b" is only found if a VOC record is called a,b |
| VOC field 4 (multifile component list) | Removed | none; the field is ignored and the record is read as an ordinary F-pointer |
| PARSER$MFILE (!parser key 5) | Removed | PARSER$GET.TOKEN |
| error 3031 (component not found) and 3032 (no component name) | Removed | none; the numbers are retired |
| the Pick style matrix in the run-time system | Removed | nothing could make one since `$mode pick.matrix` went; the matrix descriptor type, its opcode (reserved), its flag and their branches in the kernel, the debugger and the process dump are gone, with messages 1136 and 1139, `readnext` mode 0, the wait path of a remote `write`/`delete` under `autolock`, and the option-flags field of a phantom's start-up record and its seal. No program changes |
| dictionary field numbers 9998 and 9999 | Removed | a `d`, `a` or `s` item whose location was 9998 gave the item count and one whose location was 9999 the record length in bytes; they are ordinary field numbers now. Write an I-type with `@ni` or `len(@record)` |

## New Features Unique to SD Core

Everything in this section is SD Core's own. None of it is on the openQM list, so none of it has a row in the
feature spreadsheet: the administrator's gates and the shared account, the screen library, the installer's additions and
the fixes to SD's own code. The sections above are the openQM items that were built, with the changes they made.

### Administration

| Name | Change | What |
|---|---|---|
| `bp-on` and `bp-off` | Added | per-account switch for saving a change to a program file (source or object code), and for compiling and cataloguing |
| `create.account` audit line | Changed | the audit line ends `gates=` with every access the command granted, or `gates=none`, and `start=menu` or `start=terminal` when a start word was typed |
| `create.account` start words | Added | `start-menu` or `start-terminal` says where the new account starts and `pins-on` lets the person add programs to their home screen; two different start words, or a word that is neither, are refused before anything is made |
| `dict-on` and `dict-off` | Added | per-account switch for saving a change to a dictionary |
| home screen | Added | a tile whose action is `menu:name` opens a page of its own with a Back tile (Esc, Backspace go back); **View > Recent group** keeps the tiles a person started last, off as delivered; `set.tile account recent off` forbids it |
| `list.shared` | Added | SDSYS's list of the files of the shared account that an account with `shared.read` can open by name |
| `remote.sdsys` | Added | remote administration over ssh by a separate account, SDRADMIN (never a Windows administrator; one fixed list of account commands); shut as delivered, opened only by the administrator with `remote.sdsys on` or the installer's unticked page; see Administrator 22 for what opening it means |
| `lock.tracer` | Added | administrator only: logs every lock taken and released, with program and line, to the file `locktrace`, which only the SD service writes |
| audit trail | Changed | the SD service writes it, naming each session's Windows user (`DOMAIN\name`) and process as Windows sees them; one user's records past 600 in a minute are dropped with one line saying how many; it starts a new file at 1 MB while SD runs |
| `list.voc.removed` | Added | administrator only: the VOC records SD no longer ships, with the release each went in and what to write instead; given an account, what the next `update.accounts` would do in it (changes nothing) |
| `modify.account` | Changed | takes more than one action in a command (`modify.account fred sh-on os-on voc-on`), all carried out or none; no action at all prints the usage |
| new account defaults | Changed | a new account has no shell, no `os.execute`, no ssh, no API and no edit rights; SDSYS opens each, account by account |
| `restore.account` | Changed | fixed: no longer overwrites a different global program of the same name |
| `restore.voc` | Added | administrator only: puts back the newest saved copy of a VOC record the update removed, or all of an account's; never overwrites a record the account holds, and audits what it puts back |
| `run.in` | Added | administrator only (SDSYS's VOC only): runs one command from a fixed list (`basic`, `catalog`, `decatalog`, `delete.catalog`, `compile.dict`, and `debug`, which runs the program in a separate unelevated SD process of that account as the local account `sdrunin`, its screen and keyboard relayed to the administrator's window) inside another registered account and is always back in SDSYS afterwards, even when the command aborts; the command is rebuilt from checked words, `basic` is always given `no.catalog`, the account's LOGIN does not run, and the entry and the return are audited; the command does not run as the administrator: its command and option words must be SD's own entries in the account's VOC (the record of the same name in `newvoc`: one that is missing or changed is refused before anything happens), only the one edit gate it needs is on, `sh` and `os.execute` are off; a path it writes outside the account and a file with a trigger are refused, and during it `$execute`, an include or dictionary from outside the account, `logto` and a Q-pointer out of the account are refused |
| `sd-on` and `sd-off` | Added | per-account switch: programs may reach files under the directory of any SD account the user could `logto` |
| `sh` and `os` switches | Added | `sh-on`, `sh-off`, `os-on`, `os-off`: per-account switches for the shell and for `os.execute`, off for a new account; they belong to the account, not to the Windows person |
| `shared` account | Added | a group account whose files every account opens by name, with no `logto` or pointer; made by the installer; its Windows group `sdg_shared` has no members |
| `shared-read-off` | Added | withdraws the shared account's files from one account (on for every account as delivered); `shared-read-on` gives them back |
| `shared-write-on` | Added | lets one account change the shared account's files (off as delivered); `shared-write-off` takes it away |
| `set.config` | Added | changes one of 14 tuning parameters of `sd.conf` (administrator, through SDSYS's elevated helper): a name on the helper's list and a whole number inside the range SD enforces; the old file is kept as `sd.conf.bak` |
| `set.job` | Added | the administrator's scheduled jobs: makes, changes, deletes or starts now one of two fixed jobs (`backup-all`, `update-accounts`) on one of five schedules, each a Task Scheduler task that runs as SDSYS with no stored password, through the job helper `sd-jobs.ps1`; alone, lists them with their next and last runs; each change audited, and every audit line of a run ends `job=`*name*; nothing is scheduled as delivered, and uninstalling removes every job |
| `ssh` and `api` | Changed | a new account gets neither; `create.account user name ssh`, `api` or `both` and `modify.account` change it |
| `tool.accounts` | Added | full-screen page of every account: its kind, suspension, the gates that are on and who is signed on; suspends or lifts, adds or takes away a person of a group account, creates (the verb asks for a password on the terminal) and deletes (after the name is typed; the account's Windows profile is removed with it, so there is no question about the home folder) |
| `tool.config` | Added | full-screen page that shows every `sd.conf` parameter with what SD is running with, what the file says, the default and when a change takes effect, and names a line SD does not know; `E` changes one of 14 tuning parameters through `set.config` |
| `tool.jobs` | Added | full-screen Scheduled jobs page: every account with the paragraphs and sentences it may run from the command line, changed through `set.batch` behind a box answered Run (an account's schedule is still a task of its own Windows user); its Jobs view (`J`) lists the administrator's scheduled jobs and makes, changes, deletes (the name typed) and starts them through `set.job` |
| `tool.remote` | Added | full-screen page for everything that reaches SD from outside: the API and ssh doors as the machine reports them (changed after a box, and the word OPEN to turn one on; the API with the terminal given to `remote.api`, which asks whether to restart SD), the routes of each user account, the SDNet servers (delete, define with the terminal given to `set.server`), who is connected, and this machine's TLS identity. SD Core for Linux's view of the `sdsys` ssh login is not carried |
| `update.accounts` deletion list | Changed | after the copy from `newvoc` it removes from the account's VOC the records on SD's deletion list (`sdsys/voc_removed`), but only the record SD shipped (not one of your own, not a `[locked]` one unless it is a verb), after saving a copy, and audits it; before `newvoc.mods` |
| `voc-on` and `voc-off` | Added | per-account switch for saving a change to a VOC |

### AI

Off as delivered: no provider, no key, and no account has the gate. On Windows SDSYS, and any administrator of the machine,
can read a provider's key; turning the AI on sends what a person types to the provider's servers.

| Name | Change | What |
|---|---|---|
| `ai` gate | Added | per-account switch, `ai-on` and `ai-off` (also on `create.account`): membership of the Windows group `sdaiusers`, read by the helper at each request; off as delivered, except for the installing user's own account when the installer's "open every access gate" box is ticked; SDSYS needs none and may always use the AI once a provider and key are set |
| `ai` line | Added | the home screen, every toolkit page but `tool.keys`, the IDE and `sed`, the collection editor, the debugger and the dictionary form: type a request, see what will be sent (Cancel the default), and accept or reject what the AI proposes; it never runs anything itself, and SD's own files are never sent |
| `ai` verb | Added | asks an AI one question; shows the question and the size of all that will be sent, and sends only on `y` or `yes` |
| `sd-ai` service | Added | the AI helper: a Windows service running Linux's Python helper under the all-users Python 3.13 or later, as `NT SERVICE\sd-ai`, on the pipe `\\.\pipe\sd-ai` (SD checks the pipe's owner first); keys encrypted with DPAPI for that account in `C:\ProgramData\SD\ai\keys`; set up by the installer only when such a Python is there, otherwise by `install-aihelper.ps1` |
| `set.ai` | Added | SDSYS chooses the provider, model and key from the prompt; `set.ai models` lists the provider's own model names, and a model it does not list is warned about; needs the all-users Python |
| `tool.ai` | Added | SDSYS page: Anthropic, OpenAI, Google, DeepSeek or custom, one provider for every account, each named provider with its address and a default model (a key is all it needs), each account's gate; S, one setup dialog: the key in a password field and the model chosen from the provider's own list |

### API and client library

| Name | Change | What |
|---|---|---|
| api server loop | Changed | fixed: a client that hung up at the wrong moment, or sent a false packet length, left its server process tied up |
| client library: `sdchecksum` | Added | a checksum computed on the client |
| `creating.seqkey` over the API | Added | the server's record-id counter gives the id, over the API |

### Encryption

Three simple layers, with no vault and nothing on by default.

| Name | Change | What |
|---|---|---|
| `encrypt.key` | Added | asks for a key on a hidden prompt and puts it in the key ring |
| key ring subroutines | Added | `!keyset`, `!keyclear`, `!keylist`: fill, empty and list the session's key ring, kept in the memory of its own process |
| `sdkey()` and friends | Added | `sdsalt()`, `sdkey()`, `sdrandkey()`: a salt, a key from a passphrase, and a random key for `sdencrypt()` and `sddecrypt()`, open to every program; every `sdencrypt()` uses a fresh random nonce <!--s 504 g116 g123--> |
| `xe` conversion | Added | a dictionary item with `xe` (or `xe;name`) shows a field decrypted for a session that holds the key and the cipher text for one that does not; `iconv` encrypts |

### Files

| Name | Change | What |
|---|---|---|
| group size of a new file | Changed | `grpsize` is 4 (KB) in the shipped `sd.conf` and the built-in value when it is absent; it was 2 and 1. An installed system keeps its `sd.conf`, and a file keeps the size it was made with |
| right justified index keys | Changed | a right justified index made now keeps its keys in one order: the empty key, numbers by value (decimals too), then text, so 1, 01 and +1 are one key and `build.index` loses no id. An index made before keeps the old order; an index made on SD Core for Linux since 25 Oct 2026 now opens here, and an index made here now cannot be opened by an older release |
| `sdfix`, `sdidx`, `sdconv` | Changed | fixed several faults (see the changelog); `sdidx -m` says why it cannot make the directory |
| sort of equal or ordered keys | Changed | fixed: a long run of equal or already ordered keys took minutes; now a fraction of one |

### Installer

| Name | Change | What |
|---|---|---|
| group account folders | Changed | `group_accounts` is locked like `user_accounts`, and every group account's folder is set again on every install and upgrade; a folder that is really a link is skipped |
| elevated helper | Changed | the elevated helper that SD starts when SDSYS signs in at the console runs only a file named `$PS.TMP.<number>` in the system directory's `pstmp` folder, which is where SD writes the scripts it hands over, and refuses any other path, name, folder or link; a process of the same user can still put such a file there |
| SDNet groups and folder | Added | the groups `sdfiles`, `sdfileswrite` and `sdfilesadmin`, with no members, and the folder `sd-net` (stored server logins), whose access list lets `sdusers` list it and add a sub-folder and nobody else in |
| shared account | Added | made by the installer: group `sdg_shared` with no members, and a directory open to `sdusers` with Modify; an existing account named `shared` that SD did not make stops the install before anything is changed; `make-shared.log` in the data folder says what was done |
| source | Changed | the complete source (C, `gpl.bp`, build and installer scripts) is `SDCore4Windows-source-<version>.zip` beside the installer and is no longer installed: SDSYS has no `gpl.bp` folder or VOC entry, and an upgrade removes the ones an earlier release installed |
| uninstall | Changed | removing SD with its data also removes the group `sdg_shared` |
| `upgrade_editgates` | Added | switches the three edit gates on once for every existing user account whose setting is blank, so no account loses what it had |
| `upgrade_gates` | Changed | copies once what `os.users` said into the account's `sh` and `os` settings, and fills only a blank setting, so a kept `no` stays |

### Screen library and terminals

The screen statement and its library, and what changed in the terminal handling around it. The library is Linux's code carried here; it has not yet been run on a Windows console.

| Name | Change | What |
|---|---|---|
| console window at start | Changed | SD makes a classic console window smaller than 140 columns by 43 lines that size when it starts, or as big as the screen allows; it never makes a window smaller, and a Windows Terminal window or a script's console is left alone |
| `debugger` full-screen display | Added | on a terminal that reports its size and has an alternate screen the debugger takes the whole screen; F1 help, F4 the program's screen; a terminal without one (the `windows` type today) keeps the line-by-line debugger |
| immediate messages | Changed | `message ... immediate` is shown in a box over the alternate screen, or as lines and `Press return to continue` |
| `screen` statement | Added | menus, dialogues and forms from BASIC; tabs, text areas, tables and trees; scroll bars and progress bars; the mouse |
| `screen form fill`, `stretch` | Added | a form that takes the whole window and follows it: a text area or table with `stretch` gets the spare room and what lies beyond it moves, with no code in the program; below the form's own size one warning holds the keyboard |
| `screen move` size | Changed | a text area, table or tree takes a new size, and a label or entry field a new width; a text area or table keeps what it holds |
| themes | Added | `paper` (the delivered one: a new install's `sd.conf` says `SCREENTHEME=paper`), `night`, `mono`, `classic` and `blue`; `screentheme=` in `sd.conf` chooses the default (no line means `mono`); Ctrl-T on a page changes it and keeps the choice for you; a color theme is refused where the terminal cannot show color |
| toolkit window size | Changed | a page of the full-screen toolkit refuses a window of more than 500 columns by 300 lines before it takes the screen (opening one cost time as the square of the height); "Press Enter to return" no longer names the home screen |
| window size | Changed | SD reads the terminal's window size at the start and when it is resized; `kernel(k$winsize)` answers it; `term w,h` holds until the next resize |

### SDNet

Files on another SD server. All of it is off as delivered. The client is Linux's, carried here; it is compiled and its
free checks pass, and it has not been run against another server.

| Name | Change | What |
|---|---|---|
| `files-admin-on`, `files-admin-off` | Added | per-account: the Windows group `sdfilesadmin`; the files-only login may also configure, index, create and delete files on this server; needs `files-on` and `files-write-on` first; off for a new account, and the installer does not turn it on |
| `files-on`, `files-off` | Added | per-account: the Windows group `sdfiles`, the files-only API login (files and nothing else); off for a new account; `sdapi` wins |
| `files-write-on`, `files-write-off` | Added | per-account: the Windows group `sdfileswrite`; without it a files-only login cannot write, delete, lock or clear; needs `files-on` first |
| `list.servers`, `delete.server` | Added | the administrator's list of defined servers, and removal of one <!--s g52 g26--> |
| `net-on`, `net-off` | Added | per-account NET switch: one of the four things that must all be true before a remote file opens (the switch, a defined server, your login on it, a VOC pointer) |
| `netwait`, `netreply` | Added | `sd.conf` settings, 1 to 3600 seconds, for a connection and a reply; a silent server is given up on <!--s 235 g291--> |
| `open.socket` | Changed | the fourth argument is the number of seconds to wait for the connection, zero for no limit of SD's own; it was the unused security context <!--s 174--> |
| remote files, a pointer | Added | a VOC entry whose first field is `n` points to a file on another server |
| remote file administration | Added | for a login in `sdfilesadmin`: `analyse.file`, `configure.file`, `create.index` and the other index verbs, `create.file ... server` and `delete.file` of a pointer, `fcontrol()` and `write ... creating.seqkey` on a remote file |
| remote files, cache | Added | a short record cache; `logto` closes the connections |
| remote files, index | Added | `indices`, `selectindex`, `setleft`, `setright`, `selectleft` and `selectright`; a query uses the other machine's index |
| remote files, query | Added | `list`, `count`, `sort`, `select`, `list.item`, `list dict` on a remote file; `fileinfo` type 7 |
| remote files, refusal | Changed | the server's own words are shown, not `status 0`; a lost connection is an error <!--s 256--> |
| remote files, reply checked | Changed | a reply that cannot be true is a lost connection at once |
| remote files, write | Added | for a server defined `write` and a login in the other server's write group: `write`, `delete`, `clearfile`, the locking reads and release |
| remote lock functions | Added | `recordlocked()`, `getlocks()`, `filelock`, `fileunlock`: work on a remote file |
| remote `select` | Changed | fixed: a server error stopped the program with an abort |
| SDNet logins | Added | `set.netlogin`, `delete.netlogin`: a person's login on a server, kept as derived values and never the password, in a folder only that person and the administrators can open |
| `set.server` | Added | defines a server; `connect` shows its key hash for you to confirm <!--s g84 147--> |
| `settings.report` | Changed | the `[api]` section shows the hash of the API's public key, the figure another administrator pins |
| tls reads | Changed | fixed: a half record or a late ticket made a read wait without limit |
| uninstall | Changed | removing SD with its data also removes the groups `sdfiles`, `sdfileswrite` and `sdfilesadmin`; removing a person removes their stored server logins |

### Security

Fixes that close a way round a gate, and what the gates now ask.

| Name | Change | What |
|---|---|---|
| audit trail, control characters | Changed | fixed: a value written to the audit trail that held a newline started a false line; a control character, DEL or a mark is now written as `?` |
| `kernel(k$internal, n)` | Changed | only a program compiled in internal mode may set internal mode; reading it (`-1`) is unchanged |
| api request 29 | Changed | fixed: it opened a file for any login once `netfiles` bit 2 was set; it now needs the account's NET switch (`net-on`), and a VOC pointer that leads out of the account needs the `os` switch |
| group account folders | Changed | `C:\ProgramData\SD\group_accounts` is locked like `user_accounts`; before, a group account whose own folder failed to lock kept the access every SD user has to the data tree |
| internal programs | Changed | the internal-mode bit in an object file is honoured only for an object from the global catalogue, which only SDSYS can write, or for the administrator; for any other object it is ignored |
| operating system paths | Changed | `dir()`, `select.dir`, `oscopy`, `!oscopy`, `!ioscopy`, `deleteseq` of a path, `setptr ... as pathname`, a print file made at a path and a VOC pointer out of the account each ask the account's `os` switch, and `sd-on` for another SD account; every session is held to it, the console included |
| hang-up and fault | Changed | fixed: a session whose connection dropped while it was writing the error log or the audit trail waited for itself for ever, and every later login behind it; the "Received termination signal" line is now written outside the signal, and a session that faults gives back its locks before it logs |
| phantom debugger messages | Changed | `pdebug` and the phantom it debugs leave each other their messages in `sd\pdebug` in the `AppData\Local` folder of the user's profile (a private folder, made with access for that user, SYSTEM and Administrators only), not in `$ipc`, which every SD user can write; the two must be the same Windows user; message 12953 when the store cannot be set up |
| `phantom` start-up records | Changed | `$ipc` is a file every SD user can write, so the records a new phantom runs, stacks and sets (command, `DATA` lines, log file, options) are sealed with a secret given only to the new process in its environment; a phantom whose records do not check runs nothing, says so and writes `phantom refused` to the audit trail |
| print file refusal | Changed | outside the account: the message names the account instead of printing `%1` |
| `sh` command | Changed | no account may use pipes, redirection or chaining in an `sh` command |
| VOC pointers | Changed | an `f` pointer must lead into the account (or be what the stock VOC says), and a `q` pointer is followed only into an account the person could `logto` |

### System

| Name | Change | What |
|---|---|---|
| `sd -status` | Changed | fixed an overrun on a server that recorded no start time |
| `sd -stop` and `sd -restart` | Changed | an SD process still running ten seconds after the termination signal is ended with SIGKILL, and the stop says how many; before, it was left running with SD gone under it |
| terminal size | Changed | SD asks the terminal for its size at the start and when it is resized, instead of using the terminal type's 120 by 36 |

## NO CHANGE

Items on the openQM list that were looked at for this release and needed no change to SD: the defect is not in SD, the
feature was already there, or it does not apply. They are here so that nobody looks for them above.

| Name | Change | What |
|---|---|---|
| `*` comment line in a paragraph | None | already works <!--s g2--> |
| 64-bit versions | None | no change in this release <!--s 196--> |
| `between` in a `when` clause | None | no change recorded <!--s 248--> |
| `$echo` | None | already there in W1.1-3 <!--s g1--> |
| `formlist` bad data | None | no change recorded <!--s 265--> |
| hangup at the break key prompt | None | already ends the process by itself <!--s 266--> |
| inherited public variable | None | beside a function of the same name: already found <!--s 342--> |
| `insert` appending a field | None | `insert`, `ins` and `<-1>`: no change recorded <!--s 475--> |
| `itype()` | None | no change recorded <!--s 328--> |
| `list.users` | None | removed in an earlier release with the other user verbs; the administrator uses `listu` <!--s g53--> |
| `locate` insertion position | None | also a very long numeric item: no change recorded <!--s 527 556--> |
| `loop` ... `repeat` | None | already there in W1.1-3 <!--s g59--> |
| `matbuild` trailing elements | None | unassigned elements at the end: no change recorded <!--s 557--> |
| `matchfield()` `n-mx` pattern | None | at the start of the template: no change recorded <!--s 562--> |
| memory alignment in `redim` | None | no change recorded <!--s 382--> |
| negative default argument | None | for an optional argument: the defect cannot occur, because the feature it belongs to was not in SD <!--s 324--> |
| Pick wildcards in `ne` | None | nothing to fix: the Pick wildcards (`option pick.wildcard`) were removed on 27 October 2026 <!--s 322--> |
| `qmbasic.warnings` | None | `sdbasic.warnings` was removed on 27 October 2026 with the three warning options <!--s g251--> |
| `$qmcall` | None | already there as the `$sdcall` flag, which lets a restricted client session call a subroutine <!--s g212--> |
| `readv` fatal error | None | no change recorded <!--s 559--> |
| record cache and case | None | no change recorded <!--s 330--> |
| `set.date` | None | SD still has the command; nothing was withdrawn <!--s 78--> |
| the `u` format in a report | None | already wraps a long value as `t` and `l` do <!--s 531--> |
| the user limit reached | None | login prints message 1000 and exits cleanly <!--s 275--> |
| `update.account` | None | already there in W1.1-3 <!--s g102--> |
