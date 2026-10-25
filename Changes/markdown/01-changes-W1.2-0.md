Title: Changes in W1.2-0
Subtitle: What was added, changed and removed since W1.1-3 (10 October 2026), by section and in alphabetical order.

**This is the list of what changed between W1.1-3 (10 October 2026) and W1.2-0.** It is kept up to date as the
release is built. It was started on 25 October 2026 from the Linux list for L1.2-0 (SD Core for Linux and SD Core for
Windows carry the same openQM items) and the release changelog (`sdsys/changelog`, section "W1.2-0 - in progress"),
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
- What SD Core for Windows does not have yet, and SD Core for Linux does, is not listed here. The list for Linux has the AI
  features, SDNet, the home screen and the full-screen tools, the master files and the full-screen editors `sed`, `ced` and `ide`.

## Read this first: changes that alter what an existing system does

| Name | Change | What |
|---|---|---|
| A new account | Changed | had the shell and `os.execute` open to its person and ssh and the API on; now has **no shell, no `os.execute`, no ssh, no API** and no right to save a VOC, a program file or a dictionary, and every gate is closed until SDSYS opens it (`modify.account`); it can open the files of the shared account by name, read only |
| A person's shell and `os.execute` | Changed | were granted to the Windows person in `os.users`, so they followed the person into every account; now they are two settings of the account, and `os.users` is no longer read |
| A session at the console | Changed | was not held to its account's directory when it opened a file by its path (only a session over the network was); now every session is, unless its account has `os-on`, or `sd-on` for another SD account |
| AccuTerm and SDTerm | Removed | were supported; use terminal type `xterm` or `vt100` |
| An `sh` command | Changed | an account that was listed in `os.users` could use pipes, redirection and chaining; now no account can |
| An upgrade | Changed | copies once what `os.users` said about each user account's Windows user into that account's `sh` and `os` settings, and switches the three edit gates on once for each user account whose setting is blank; it never switches on a setting an administrator turned off |
| Dictionary divide by zero | Changed | stopped the report; now gives zero |
| `fileinfo(f, 1021)` | Changed | gave text such as `12 (don), 14 (ann)`; now the user numbers of the other sessions that have the file open, and the text form is key **1100** |
| `intprec` and `sortmem` | Changed | were 13 and 1024; now **11** and **4096** (set the old values in `sd.conf` if you need them) |
| `select file field` | Changed | a field not otherwise used was ignored; now it is `saving multivalued field`, so the list holds the values |
| The terminal's size | Changed | every session started at the terminal type's 120 by 36; now SD asks the terminal how big it is at the start and when it is resized (`term w,h` still sets it by hand) |
| `when field` with no operator | Changed | kept the null values; now keeps the values that are **not** null |

## Sections

**Built from the openQM list** (each row is an item on the feature spreadsheet): [ADMIN](#admin) · [API](#api) ·
[BASIC](#basic) · [DATA](#data) · [FILES](#files) · [QUERY](#query) · [SYSTEM](#system) · [TCL](#tcl) · [TOOLS](#tools).

**[New Features Unique to SD Core](#new-features-unique-to-sd-core)**, not part of openQM and not on the spreadsheet:
[Administration](#administration) · [API and client library](#api-and-client-library) · [Encryption](#encryption) ·
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

## API

The server side of the API, the client library and the language headers.

| Name | Change | What |
|---|---|---|
| `master.login` | Changed | the paragraph runs for API connections as for interactive and phantom sessions <!--s 170--> |

## BASIC

Statements, functions, `$mode` words and compiler directives.

| Name | Change | What |
|---|---|---|
| `~=` | Added | comparison that ignores case <!--s 430--> |
| `account.path()`, `vocpath()` | Added | the pathname of an account and of a file named in the VOC, told only where the account may open it <!--s g107 g193 86--> |
| `adds`, `subs`, `muls`, `divs` | Added | arithmetic element by element over two dynamic arrays <!--s 207--> |
| `arg.present()`, `reusing()` | Added | whether the caller passed an argument, and whether with `reuse()` <!--s g108 g169--> |
| `$basic.options` | Changed | a `mode` line takes a list and a minus turns a mode off; an `include` line names records or files that every program includes <!--s 406 407 290--> |
| `bool()` and friends | Added | `bool()`, `is.null()`, `numeric()`: Boolean, SQL-null and numeric conversions <!--s g109 g144 g161 451--> |
| `bscan`, `root`, `key()` | Added | scan an alternate key index entry by entry, the openQM and Pick ways <!--s g110 g173--> |
| `@build.time`, `@line` | Added | the time the program was compiled and the source line it stands on <!--s 506 211--> |
| `call "file name"` | Added | calls a program compiled into a file without the catalogue <!--s 208--> |
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
| `ereplace()`, `fix()` | Added | replace with an occurrence and a start; a number with a fixed number of decimals <!--s 472--> |
| exceptions | Added | `try`, `catch`, `throw`, `caught()` and `@exception`; many run time errors are caught under openQM's `sys.` names; `dumping` and `saving.stack` <!--s 353 354 355 295 309--> |
| `execute ... stacklist` | Added | keeps the default select list and puts it back when the command returns <!--s 61--> |
| `execute.list` | Added | runs commands for each id of list 0 in turn <!--s g38--> |
| `fcontrol()` | Added | the openQM function: next sequential key, valid id, minimum modulus, line terminator modes, forced writes <!--s 452 102--> |
| `field()` and `vslice()` | Changed | take an asterisk for the number of elements and a subvalue slice <!--s 212 132--> |
| `flush.dh.cache` | Added | makes every process close the dynamic files it keeps cached <!--s 83 123--> |
| `for` with a list | Added | a loop over a list of values, and over the elements of a delimited string, with a delimiter <!--s 84 300--> |
| `get var from device` | Added | reads from a FIFO, port, character device or `openseq` file a character at a time, with a timeout <!--s 583--> |
| `getlocks()`, `testlock()` | Added | information about file and record locks; the owner of a task lock <!--s 508 42--> |
| `getpu()` | Added | `pu$form.queue` and `pu$pathname` keys <!--s 18 214--> |
| `groupstore` and `revremove` | Added | `groupstore`, `revremove`, `setrem`, `rmvd()`: statements and functions over delimited strings <!--s g136 g170 g172--> |
| `$ifdef`, `$ifndef` | Changed | accept `and` and `or` between token names <!--s 219--> |
| `inmat()` | Changed | after `matches` or `matchfield()` it is the number of the pattern that matched; after `matbuild` and `matwrite` it is the element count; a collection array is accepted <!--s 315 454 591--> |
| `input ... fill` | Added | shows a fill character in every empty cell of the field <!--s 389--> |
| `input ... no.echo` | Added | shows nothing as the user types <!--s 168 363--> |
| `input ... raw` | Added | reads exactly the number of characters given, as they arrive <!--s 548--> |
| `inputif` | Added | reads a line only if one is already there, else takes `else` <!--s 584--> |
| `inputnull`, `inputtrap` | Added | a single character typed alone makes the answer null, or sends the program to a label <!--s 408--> |
| `is.*` character tests | Added | `is.alnum`, `is.alpha`, `is.digit`, `is.graph`, `is.mark`, `is.space`: true if the first character is of that kind <!--s 223 g138 g139 g140 g142 g143 g145--> |
| `keep.select` | Added | with `option clear.select`, a program keeps what is left of list 0 <!--s g148--> |
| `last()`, `left()` and more | Added | `last()`, `lasts()`, `left()`, `right()`, `nv()`, `ns()`: the final element of a delimited string; the first or last characters; value and subvalue position numbers <!--s g150 g151 g171 g162--> |
| `locate ... by` | Added | `c` forces a case-sensitive search and `n` a case-insensitive one <!--s 419--> |
| `matchess` and `trimws` | Added | `matchess`, `matchfields`, `trimws`, `trimw()`: `matches`, `matchfield` and `trimw` over a dynamic array; `trimw` trims white space <!--s 302 g152 g153 g189--> |
| matrix arguments | Changed | a matrix passed as an argument needs no `dim` in the receiving subroutine; `if mat a = mat b` compares two matrices; the compiler no longer reports an undimensioned argument <!--s 44 111 519--> |
| `matstr()` | Added | converts a two dimensional matrix to a dynamic array <!--s 509--> |
| `matwritecsv` | Added | one CSV line of every element of a matrix <!--s g154--> |
| `md5()`, `digest()` | Added | the md5 digest, and md5, sha1, sha256, sha384 or sha512 of a string or a file <!--s 63 g118--> |
| `mergelist()` | Added | merges two lists by a mode; a mode for lists not in order; fixed for an empty list <!--s 420 539 566 g155--> |
| `$mode autolock` | Added | a `write`, `matwrite` or `delete` with no lock takes an update lock and releases it <!--s g213--> |
| `$mode conditional.statements` | Added | accepted; changes nothing, since `while` and `until` take these conditions anyway <!--s g217 206 434--> |
| `$mode debug.equates` | Added | keeps `equate` and `$define` tokens in the object so the debugger can show, set and watch them <!--s g218 246 239--> |
| `$mode default.unass.args` | Added | an argument passed unassigned takes its default <!--s g219--> |
| `$mode execute.clearlist` | Added | clears the default select list before each `execute` <!--s 521--> |
| `$mode explicit` | Added | a variable must be named in a `dim` statement before it is used <!--s g220 234--> |
| `$mode implied.stop` | Added | the code after the last `end` is a `stop`, not a `return` <!--s 81--> |
| `$mode` lists | Changed | `$mode` takes several names separated by commas, each with an optional minus <!--s 105--> |
| `$mode non.durable.txn` | Added | a committed nested transaction writes nothing until the outer one commits <!--s g221 442--> |
| `$mode open.fail.zero.fvar` | Added | a failed `open` leaves 0 in the file variable <!--s 514--> |
| `$mode` overlap words | Added | `change.no.overlap`, `count.overlap`, `index.overlap`: whether `change`, `ereplace`, `swap`, `count`, `counts`, `index` and `indexs` see overlapping occurrences <!--s g214 g215 g216--> |
| `$mode partial.expressions` | Added | `a and b` and `a or b` stop evaluating as soon as the value is known <!--s 417--> |
| `$mode pick.convert` | Added | Pick order of the arguments of `convert()` <!--s g222 507--> |
| `$mode pick.readnext` | Added | `readnext` keeps the id variable when it takes its `else` <!--s 418--> |
| `$mode pick.select` | Added | `selectv` moves a default list to its target <!--s g223--> |
| `$mode selectv` | Added | `select`, `selectv` and `sselectv` without `to`, and `readnext` without `from`, use the program's default select list variable <!--s 85--> |
| `$mode stdfil` | Added | the default file variable: file statements may be written without naming one <!--s 17--> |
| `$mode stdfil.shared` | Added | one default file variable for every program and subroutine of a command level <!--s g225--> |
| `$mode strict.equate` | Added | warns when a name given to `equate` or `$define` is also a statement or function name <!--s 582--> |
| `$mode time.ms` | Added | `time()` and `system(12)` return seconds since midnight to the millisecond <!--s 581--> |
| `$mode trap.unused.main` | Added | `trap.unused` for the program's own variables <!--s g227--> |
| `$mode write.delete.then.else` | Added | `write`, `matwrite` and `delete` take `then` and `else`; a trigger that refuses takes `else` <!--s 368 496--> |
| `no.query` on cataloguing | Added | the `basic` command, the `$catalogue` directive and the `catalogue` line of `$basic.options` take `no.query`, which stops the compiler asking before it removes an older entry <!--s 27 191--> |
| `open ... non.transactional` | Added | a write through that file variable is not undone by a rollback <!--s 64--> |
| `openseq` | Added | `creating` makes the file at once; `shared` lets several processes append; a block device can be opened <!--s 485 397 112--> |
| `option()` | Added | reads and sets the state of an option <!--s 224 473--> |
| `ospath()` | Added | keys `os$fullpathx` and `os$info` <!--s 293 432 233--> |
| `parse()` and `ttyget()` | Added | `parse()`, `sort.compare()`, `terminfo.ex()`, `ttyget()`, `ttyset`: split by a pattern; compare by a sort rule; a terminal capability; the terminal modes as an array <!--s g166 g183 g187 g190 g191--> |
| `phantom` statement | Added | starts a phantom from a program; the log name may be a variable <!--s 390 351--> |
| `precision inherit` | Added | takes the precision of the calling program <!--s 201--> |
| `@pstat` | Added | text a program leaves for `pstat` to show <!--s 492--> |
| `quotes()` family | Added | `quotes()`, `dquotes()`, `squotes()`: enclose every element of a dynamic array in quotes <!--s 11--> |
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
| substring assignment | Added | `s[3] = "xy"` overwrites the last three characters, and honours `pick.substr` for an element of a dynamic array <!--s 41 325--> |
| `swapmarks()` | Changed | returns the data as it is <!--s 238 g186--> |
| `trans()` family | Changed | `trans()`, `rtrans()`, `xlate()`: accept `a`, `s` and `c` items and an `l` link; a file that will not open takes the error action of the call <!--s 43 182 7--> |
| variable names | Changed | a name with two or more underscores together (`a__b`) is valid <!--s 336--> |
| `watch` | Changed | the debugger's `watch variable operator value` stops only when the condition is met <!--s 45--> |

## DATA

Data collections, JSON, XML, CSV and the verbs that import them.

| Name | Change | What |
|---|---|---|
| collection arrays | Added | `mat()`, `c{list, n}`, `ins ... as`, `del`, `inmat()` on an array |
| collection file verbs | Added | `ed`, `copy`, `copyp`, `compare.files`: work on a collection file; the post-write trigger no longer crashes the process |
| collection files | Added | `create.file name collection`; records are collections stored as JSON; `read` and `write` them whole; `ct` shows JSON <!--s 304--> |
| `collection()` and `c{name}` | Added | a collection is a set of named values read and written by name; `enumerate()`, `element.exists()` <!--s 311 518 529 339--> |
| `csv.mode` | Added | how `printcsv`, `writecsv` and `formcsv()` quote, with a delimiter, quote and escape character <!--s 173 200--> |
| `element` keyword in queries | Added | names an element of a collection file by its path, in a display list, `with`, `by`, `sum` and the like |
| `expand()` and links | Added | a link `"file:id"` is followed; `trans()` of an `e` item |
| file variable in a collection | Changed | a collection holding a file variable is written to a collection file as a null |
| `hu` conversion | Added | `oconv` and `iconv` escape and unescape |
| `indices` on `e` items | Added | a data collection element can be indexed; a query with `with` on it uses the index |
| `jboolean()` and `jtype()` | Added | `jboolean()`, `jnull()`, `jtype()`: true, false and null in collections, and the type of a value; a Boolean type <!--s 312--> |
| `jparse()`, `jbuild()` | Added | JSON text into a collection and back |
| operators on an element | Added | `+=`, `-=`, `*=`, `/=`, `:=` change an element in place |
| the debugger and collections | Added | `/c`, `/c{path}` and `dump c{sub} pathname` show and write a collection; diving in with `/*` no longer crashes <!--s 530--> |
| `xml` keyword for queries | Added | `list ... xml` writes the report as XML, with an optional DTD or schema <!--s g211 g202--> |

## FILES

File handling: opening, indexes, triggers, print files, sorting, sequential files.

| Name | Change | What |
|---|---|---|
| `analyse.file` | Changed | `statistics` shows a histogram of group utilisation <!--s 360--> |
| `analyse.index` | Added | every index with its number of values and spread <!--s g9--> |
| `catalog -name` | Added | a hyphen is a global catalogue prefix; `delete.catalog -name` removes it <!--s 217--> |
| `clear.file` | Changed | fixed: a `no.resize` file keeps its modulus <!--s 590--> |
| `configure.file ... reporting` | Added | shows how many records have been converted <!--s 172--> |
| `create.file` | Added | `comment`, `multifile` and a relative `pathname` kept relative in the VOC <!--s 383 522 278--> |
| `create.index`, `make.index` | Added | `no.case`: keys that differ only in case are one key; `deleting` replaces an index; a default location in `$index.path` <!--s 54 424 184--> |
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
| trigger on a read | Changed | fixed: a locally catalogued read trigger could end the process <!--s 317--> |
| `vocname` letters | Added | `r` opens a file read-only, `n` non-transactionally, `s` with forced writes, from field 6 of its VOC entry <!--s 197 380 102--> |

## QUERY

The query processor and the dictionary.

| Name | Change | What |
|---|---|---|
| `a;nocase` correlative | Added | makes the string operations of one correlative case insensitive <!--s 103--> |
| `absent.ignore` | Added | do not print the `not found` list for ids that are not in the file <!--s 25--> |
| `break.on "'lu'"` | Changed | the `l` is ignored when `u` is also given <!--s 40--> |
| `break.on "'n'"` | Added | starts a new page and numbers it 1 again <!--s 16--> |
| `by.exp` | Changed | more than one `by.exp` in the same association is sorted <!--s 572--> |
| `col.hdr.space` | Added | a blank line under the column headings of a tabular report <!--s 467--> |
| `csv 3` | Added | every item quoted, numbers too <!--s 26--> |
| dictionary expressions | Changed | `if` with a part missing, `fn` for a field, a format after a value, hyphens in names, divide by zero is zero <!--s 36 48 270 271 423 547 564--> |
| `for`, `from none` | Added | `search file for "text"`; `from none` ignores an active list 0 <!--s 190 378--> |
| `if` in a dictionary item | Added | field 8 of an `a` or `s` item may hold an `if` expression <!--s 104--> |
| `in`, `not.in` | Added | test a value against a saved list or a file record <!--s 94--> |
| `median`, `mode`, `range` | Added | figures at the end of a report and each breakpoint <!--s 231 g209--> |
| `$mode` in an `i`-type | Added | an `i`-type may begin with `$mode` for a few of the compiler modes <!--s 489--> |
| `no.page` | Changed | accepted on any query command <!--s 379--> |
| options | Added | `query.string.comp`, `query.str.comp.all`, `query.sort.no.case`, `default.mv`, `clear.select` <!--s 140 299 412 205 403--> |
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
| `invcase` | Added | `sd.conf` setting for the initial state of input case inversion <!--s 399--> |
| lock table | Changed | the time each lock was taken and each wait began is noted; more than 65,535 locks in a file work; a program that filled the table can be logged out <!--s 487 344 532--> |
| `numlocks` | Changed | range checked, 1 to 32767 |
| `phantoms=u,n` | Added | keeps user numbers for phantoms started with `user` <!--s 31 g296--> |
| process dump | Changed | shows the length of each string, the variables of objects and the environment <!--s 22 125 569 439--> |
| `pterm` keys | Added | `pterm erase`, `ctrl.filter`, `mark`: which key erases; control characters filtered; control keys that type the marks <!--s 155 253 254--> |
| `sd.conf` parameters | Added | `dhcache`, `lgnwait`, `maxrlock`, `pwdelay`, `userpool`: `sd.conf` parameters, each optional with the old fixed number as the default <!--s 90 46 313 106 551--> |
| `sortmem` | Changed | default 4096 <!--s 535--> |
| `status` | Changed | file times are in the user's time zone; field 27 is the file pathname <!--s 96 585--> |
| `system()` keys | Added | 14, 19, 20, 21, 33, 35, 45, 1016, 1036, 1037, 1040, 1045, 1047, 1048, 1049, 1051, 1062, 1065, 1066, 1067, 1071, 1073, 1083, 1086, 1088 <!--s 65 66 114 192 225 244 206 294 307 308 326 421 433 586 587 g252 g253 g254 g255 g256 g260 g261 g265 g266 g267 g270 g271 g274 g276--> |
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
| `copy.listp` | Added | the Pick form of `copy.list` <!--s 72--> |
| `ct` | Changed | `id.sup`, `num.sup`; lower case file names; the object code of a compiled dictionary item is not shown <!--s 242 347 373--> |
| `decatalog` | Added | deletes a local catalogue entry and its object code <!--s 576--> |
| `delete` | Changed | a record another user holds locked is reported and skipped <!--s 50--> |
| `delete.account` | Changed | not stopped by a file it cannot open when it looks for references <!--s 348--> |
| `delete.common all except` | Added | deletes every named common block but those listed <!--s 425--> |
| `ed` | Changed | `l` with no text as the first command works; marks typed in input; `ev` on a compound `i`-type; line numbers show positions in edit values mode; `spool` closes the printer; external commands; automatic ids <!--s 264 268 320 331 375 446 523 305--> |
| `fstat` | Changed | wider columns <!--s 55--> |
| `fstat.user` | Added | file activity of each session <!--s g44--> |
| `git` option | Added | a directory file keeps `.gitignore` and `.gitattributes` under their own names <!--s g238--> |
| `hot spot monitor` | Changed | counts opens, reads, writes and deletes of each program <!--s 491--> |
| `if` in a paragraph | Added | `exists`, `not.exists`, `in` and `not.in`, with `no.case` <!--s 28 230 426 476--> |
| inline prompts | Changed | largely case insensitive; may use quoted prompt strings <!--s 171 377--> |
| `k` entry in the VOC | Changed | fixed: a `k` entry over a locally catalogued program stopped with "Unable to load" <!--s 263--> |
| list merges | Changed | `list.union`, `list.inter`, `list.diff`, `merge.list` find a key without scanning, so large lists merge in seconds <!--s 414--> |
| `list.item` | Changed | numbers lines beyond 999 with as many digits as needed <!--s 349--> |
| `listdict` | Added | a dictionary in the form Pick systems use; `d` and `i` records too <!--s 10 75--> |
| `listu`, `who`, `pstat` | Changed | `!listu` too: show the account and the login name; `listu detail`; the blocking user and when a wait began <!--s 12 24 29 38 77 121 289 427 577--> |
| `logto reset all` | Added | discards all programs, menus and paragraphs at every command level <!--s 30--> |
| `map local`, `map no.page` | Added | list the locally catalogued programs; heading once <!--s 153 287--> |
| `move.list` | Added | the command form of `movelist` <!--s g62--> |
| `multisort` | Added | `!multisort` sorts several related lists by one of them <!--s 568--> |
| `option` words | Added | `catalogue.local`, `chained.select`, `command.level.locks`, `correlative.nocase`, `correlative.reuse`, `dir.dtm`, `dir.sel.omit.hidden`, `force.reload`, `git`, `inherit.mfile.path`, `inherit.ownership`, `keep.old.object`, `no.phantom.notify`, `numeric.exponent`, `paginate.on.heading`, `pick.ml.conv.mask`, `query.footer.pause`, `query.merge.print`, `spool.command`, `stacked.account`, `assoc.all`, `backslash.not.quote` <!--s 288 79 314 428 461 445 37 57 154 165 404 429 49 g230 g231 g232 g233 g237 g239 g240 g241 g242 g245 g247 g248--> |
| `phantom` | Added | `no.msg`, `data`, `log`, `group` and `user` options; `!phlog` gives a phantom's log record; a phantom started while SD is suspended gives back its place <!--s 87 137 364 483 31 385 280--> |
| phantom and terminal lists | Added | `list.phantoms`, `list.term.types`: the phantoms and no one else; the terminal types <!--s 381 g49--> |
| `private vocabulary` | Added | `$private.voc`: a file of commands searched after all other command sources <!--s 1--> |
| `profiler` | Added | records what the programs of a session do and where <!--s g66 g203--> |
| `redo` | Added | runs a command again and again, `times` and `every` <!--s 188--> |
| saved list verbs | Changed | `save.list`, `get.list`, `delete.list`: `keep`, `deleting`, `count.sup`, a default name, a name left out, `in file` <!--s 2 384 387 401 494--> |
| `selectindex` | Added | the command form of the statement <!--s 119--> |
| `set.queue`, `sp.assign` | Added | Pick style form queues kept in the account's `$forms` file; `sp.assign` alone shows the default printer's queue and `set.queue deleting` removes one <!--s g83 g88 18 189 502--> |
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

## New Features Unique to SD Core

Everything in this section is SD Core's own. None of it is on the openQM list, so none of it has a row in the
feature spreadsheet: the administrator's gates and the shared account, the screen library, the installer's additions and
the fixes to SD's own code. The sections above are the openQM items that were built, with the changes they made.

### Administration

| Name | Change | What |
|---|---|---|
| `bp-on` and `bp-off` | Added | per-account switch for saving a change to a program file (source or object code), and for compiling and cataloguing |
| `create.account` audit line | Changed | the audit line ends `gates=` with every access the command granted, or `gates=none` |
| `dict-on` and `dict-off` | Added | per-account switch for saving a change to a dictionary |
| `list.shared` | Added | SDSYS's list of the files of the shared account that an account with `shared.read` can open by name |
| `modify.account` | Changed | takes more than one action in a command (`modify.account fred sh-on os-on voc-on`), all carried out or none; no action at all prints the usage |
| new account defaults | Changed | a new account has no shell, no `os.execute`, no ssh, no API and no edit rights; SDSYS opens each, account by account |
| `restore.account` | Changed | fixed: no longer overwrites a different global program of the same name |
| `sd-on` and `sd-off` | Added | per-account switch: programs may reach files under the directory of any SD account the user could `logto` |
| `sh` and `os` switches | Added | `sh-on`, `sh-off`, `os-on`, `os-off`: per-account switches for the shell and for `os.execute`, off for a new account; they belong to the account, not to the Windows person |
| `shared` account | Added | a group account whose files every account opens by name, with no `logto` or pointer; made by the installer; its Windows group `sdg_shared` has no members |
| `shared-read-off` | Added | withdraws the shared account's files from one account (on for every account as delivered); `shared-read-on` gives them back |
| `shared-write-on` | Added | lets one account change the shared account's files (off as delivered); `shared-write-off` takes it away |
| `ssh` and `api` | Changed | a new account gets neither; `create.account user name ssh`, `api` or `both` and `modify.account` change it |
| `voc-on` and `voc-off` | Added | per-account switch for saving a change to a VOC |

### API and client library

| Name | Change | What |
|---|---|---|
| api server loop | Changed | fixed: a client that hung up at the wrong moment, or sent a false packet length, left its server process tied up |
| client library: `sdchecksum` | Added | a checksum computed on the client |

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
| `sdfix`, `sdidx`, `sdconv` | Changed | fixed several faults (see the changelog); `sdidx -m` says why it cannot make the directory |
| sort of equal or ordered keys | Changed | fixed: a long run of equal or already ordered keys took minutes; now a fraction of one |

### Installer

| Name | Change | What |
|---|---|---|
| group account folders | Changed | `group_accounts` is locked like `user_accounts`, and every group account's folder is set again on every install and upgrade; a folder that is really a link is skipped |
| SDNet groups and folder | Added | the groups `sdfiles` and `sdfileswrite`, with no members, and the folder `sd-net` (stored server logins), whose access list lets `sdusers` list it and add a sub-folder and nobody else in |
| shared account | Added | made by the installer: group `sdg_shared` with no members, and a directory open to `sdusers` with Modify; an existing account named `shared` that SD did not make stops the install before anything is changed; `make-shared.log` in the data folder says what was done |
| uninstall | Changed | removing SD with its data also removes the group `sdg_shared` |
| `upgrade_editgates` | Added | switches the three edit gates on once for every existing user account whose setting is blank, so no account loses what it had |
| `upgrade_gates` | Changed | copies once what `os.users` said into the account's `sh` and `os` settings, and fills only a blank setting, so a kept `no` stays |

### Screen library and terminals

The screen statement and its library, and what changed in the terminal handling around it. The library is Linux's code carried here; it has not yet been run on a Windows console.

| Name | Change | What |
|---|---|---|
| AccuTerm terminal types | Removed | the eleven `-at` terminal types and AccuTerm's escape sequences |
| `debugger` full-screen display | Added | on a terminal that reports its size and has an alternate screen the debugger takes the whole screen; F1 help, F4 the program's screen; a terminal without one (the `windows` type today) keeps the line-by-line debugger |
| immediate messages | Changed | `message ... immediate` is shown in a box over the alternate screen, or as lines and `Press return to continue` |
| `option debug.rebind.keys` | Removed | still accepted, no longer does anything |
| screen save and restore | Removed | `save.screen()` and `restore.screen`: still exist and do nothing the terminal could see |
| `screen` statement | Added | menus, dialogues and forms from BASIC; tabs, text areas, tables and trees; scroll bars and progress bars; the mouse |
| `sdterm` terminal type | Removed | with SDTerm and SDConsole, and the `term display` line about them |
| `term 120,36` at login | Removed | new accounts no longer carry it in their `login` paragraph |
| themes | Added | `mono` (the default), `classic` and `blue`; `screentheme=` in `sd.conf` chooses the default; a colour theme is refused where the terminal cannot show colour |
| window size | Changed | SD reads the terminal's window size at the start and when it is resized; `kernel(k$winsize)` answers it; `term w,h` holds until the next resize |

### SDNet

Files on another SD server. All of it is off as delivered. The client is Linux's, carried here; it is compiled and its
free checks pass, and it has not been run against another server.

| Name | Change | What |
|---|---|---|
| `files-on`, `files-off` | Added | per-account: the Windows group `sdfiles`, the files-only API login (files and nothing else); off for a new account; `sdapi` wins |
| `files-write-on`, `files-write-off` | Added | per-account: the Windows group `sdfileswrite`; without it a files-only login cannot write, delete, lock or clear; needs `files-on` first |
| `list.servers`, `delete.server` | Added | the administrator's list of defined servers, and removal of one <!--s g52 g26--> |
| `net-on`, `net-off` | Added | per-account NET switch: one of the four things that must all be true before a remote file opens (the switch, a defined server, your login on it, a VOC pointer) |
| `netwait`, `netreply` | Added | `sd.conf` settings, 1 to 3600 seconds, for a connection and a reply; a silent server is given up on <!--s 235 g291--> |
| `open.socket` | Changed | the fourth argument is the number of seconds to wait for the connection, zero for no limit of SD's own; it was the unused security context <!--s 174--> |
| remote files, a pointer | Added | a VOC entry whose first field is `n` points to a file on another server |
| remote files, cache | Added | a short record cache; `logto` closes the connections |
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
| uninstall | Changed | removing SD with its data also removes the groups `sdfiles` and `sdfileswrite`; removing a person removes their stored server logins |

### Security

Fixes that close a way round a gate, and what the gates now ask.

| Name | Change | What |
|---|---|---|
| api request 29 | Changed | fixed: it opened a file for any login once `netfiles` bit 2 was set; it now needs the account's NET switch (`net-on`), and a VOC pointer that leads out of the account needs the `os` switch |
| group account folders | Changed | `C:\ProgramData\SD\group_accounts` is locked like `user_accounts`; before, a group account whose own folder failed to lock kept the access every SD user has to the data tree |
| internal programs | Changed | the internal-mode bit in an object file is honoured only for an object from the global catalogue, which only SDSYS can write, or for the administrator; for any other object it is ignored |
| operating system paths | Changed | `dir()`, `select.dir`, `deleteseq` of a path, `setptr ... as pathname`, a print file made at a path and a VOC pointer out of the account each ask the account's `os` switch, and `sd-on` for another SD account; every session is held to it, the console included |
| print file refusal | Changed | outside the account: the message names the account instead of printing `%1` |
| `sh` command | Changed | no account may use pipes, redirection or chaining in an `sh` command |
| VOC pointers | Changed | an `f` pointer must lead into the account (or be what the stock VOC says), and a `q` pointer is followed only into an account the person could `logto` |

### System

| Name | Change | What |
|---|---|---|
| `sd -status` | Changed | fixed an overrun on a server that recorded no start time |
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
| Pick wildcards in `ne` | None | no change recorded <!--s 322--> |
| `qmbasic.warnings` | None | present already as `sdbasic.warnings` (`option w`) <!--s g251--> |
| `$qmcall` | None | already there as the `$sdcall` flag, which lets a restricted client session call a subroutine <!--s g212--> |
| `readv` fatal error | None | no change recorded <!--s 559--> |
| record cache and case | None | no change recorded <!--s 330--> |
| `set.date` | None | SD still has the command; nothing was withdrawn <!--s 78--> |
| the `u` format in a report | None | already wraps a long value as `t` and `l` do <!--s 531--> |
| the user limit reached | None | login prints message 1000 and exits cleanly <!--s 275--> |
| `update.account` | None | already there in W1.1-3 <!--s g102--> |
