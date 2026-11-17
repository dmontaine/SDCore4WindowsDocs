Title: The Master Files
Subtitle: How the administrator manages every account's VOC entries, dictionary items and programs from SDSYS, in the account each one belongs to: the page tool.entries, its lists, the pointer rule, editing and deleting a record, programs, global changes, and run.in.

**The administrator manages every account's VOC entries, dictionary items and programs from one
page, `tool.entries`, and each one is changed in the account it belongs to.** Nothing is copied: the
page reads the accounts' own files, and an edit, a delete or a compile happens on the real
record, in its own account. That is the purpose of the master files: most accounts can be locked out
of editing their own VOC, dictionaries and programs (the edit gates `voc-edit`, `dict-edit` and
`bp-edit`), and the administrator does that work for them.

> **What lets SDSYS write into an account.** An SDSYS session runs as an elevated Windows
> administrator, and every account directory gives the Administrators group full control (with
> SYSTEM and the account's own group). So SDSYS can write inside every account; there is no grant to
> make and none to take away, and the page's SDSYS column always says `yes`. That is also why the
> page and `run.in` are careful about what of the account's own runs while they work in it (see
> *Running one command inside an account*, below): anything of the account's that ran in that session would run with the
> administrator's token.

## The entries of every account by pointer: `tool.entries`

**`tool.entries`** is the page that looks at the accounts' own files and copies nothing: it is in the SDSYS VOC only and
refuses anyone else before it reads anything. **It lists the VOC entries, the dictionary items and
the programs, and it edits, deletes, compiles and debugs each in the account it belongs to** (below).

```
tool.entries
```

*Accounts* (left) lists every registered account but SDSYS with **the gates it holds**, shown as
`v d b` or a dash: `voc-edit`, `dict-edit` and `bp-edit`, the rights to save a change to its VOC,
its dictionaries and its programs. A dash is what locks an account out of its own files; an
administrator is not held to them. The next column says whether SDSYS can write inside the account
from outside SD (always `yes` here, above), and the last whether the account is suspended.
*Entries* (right) lists the VOC of the account under the cursor, in name
order, with each entry's type and what it points at; **`K` switches to the dictionary items** of
the files its VOC points at (the dictionary path of each file pointer), each with its file, id,
type and column heading, **and again to the programs**: the program files of the VOC (a directory
file named `bp`, or ending `.bp`, or with a `.out` file beside it, as `tool.catalog` finds them) and
the record of each, with **Built**, which says `yes` when the compiled program is in the `.out` file
under the same name and `-` when it is not. The `.out` file is the one the VOC names, or else the
one beside the program file. A third `K` is back at the VOC. Under the two lists the entry under the
cursor is shown field by field.

**The VOC of an account is read when the cursor comes to the account**, from the account's own
file by the pathname the register gives, so a system with many accounts is not read as a whole.
`/` keeps the entries whose id holds a part you type; in the dictionary items it also looks in the
column heading, so `/ first name` finds the items headed "First Name" whatever they are called.
**`F` finds a part of an id, or of a heading, in the VOC or the dictionaries of every account**: it
reads them all, so it runs only when you ask, and the box then lists the hits with their accounts;
Enter on a hit goes to that entry in its account. Esc takes the find and the filter off, F5 reads
again, F6 or Shift-F6 changes box, F1 or `?` explains the box. An account whose VOC cannot be opened is
listed and says so. At most 3,000 entries or hits are listed, and the page says when there were
more.

**A pointer is not followed to change what it points at.** A `>` in the second column marks a
pointer whose target lies **outside the account being listed**: a file pointer whose data or
dictionary is in another directory (the shipped ones lead to `@SDSYS/voc.dic` and the like), a
Q-pointer to another account, a remote item, a program file that lies outside the account. A path
is the account's when it is relative; a drive letter with either slash, or a leading slash, makes
it absolute. The test is the kernel's own, so `..` does not make a path look inside. For a VOC entry
the pointer is the account's own record and is edited like any other (change `@SDSYS/voc.dic` to
another directory, and it is changed); what it points at is never edited from this page. A
dictionary item marked `>` lives in another account's dictionary, SDSYS's included, and is only read
through this account's pointer: it is edited in the account it lives in.

## Editing a record: `E` and `N`

**`E` edits the record under the cursor and `N` makes a new one, in the account it belongs to.** In the
VOC view they edit **VOC entries only**: the record of the VOC, as text, never the file a pointer
leads to. In the dictionary view they edit **dictionary items only**, as the item form (the
programs are described under *Programs: `E`, `N` and `C`*, below). The terminal is
given to the editor on that one record and comes back to the page when the editor ends; `N` asks the
id first (for an item, the dictionary is that of the file the row under the cursor belongs to). An
account with `voc-off`, `dict-off` or `bp-off` is edited all the same, because an administrator is
not held to those gates; that is what they are for. A suspended account is edited too: SD lets
the administrator follow the pointer into it. For the length of the edit SDSYS's VOC holds
one temporary file pointer, `zm`*user number*`.`*account*`.`*file*, which holds the path the page
has just checked and lets the editor reach that file; the page takes it away when the editor ends.
It is not a Q-pointer into the account's VOC: that would be followed again each time the editor
opens the file, after the check, and an account allowed to write its VOC could repoint the file in
between. If the session is killed inside the editor the pointer stays, and the page takes it away
the next time it starts in a session with the same user number.

**The rule is asked before anything is made.** At the keypress the page reads the register and the
account's own VOC again (the list may be old) and asks the kernel whether the file to be edited
lies inside the account, and then asks it again of what the pointer opens, the file's two
subfiles included, and that file must be a hashed file. A dictionary that lies
outside the account is refused with its reason (`the dictionary of zeesc lies outside ze1: it is
edited in the account it lives in, not from here`), so a VOC pointer written `..\other\dict.dic`
and the shipped system dictionaries cannot be edited from
another account's row; nothing is written, no pointer is made and the audit trail has no line. The
pointer record itself is the account's own record and is edited like any other: a Q-pointer that
leads to another account can have its text changed, and the other account is not touched. The
editor is a general editor; the page decides what it is given first, not what the person opens
next inside it.

Each edit that reaches the editor writes one line to the audit trail, for example
`master edit account=ZE1 kind=voc file=voc id=zzonly1 new=0` (`kind=dict` and the file's name for an
item, `new=1` for `N`); the page's other line is `tool start app=tool.entries`.

## Deleting a record: `D`

**`D` deletes the record under the cursor**, a VOC entry in the VOC view or a dictionary item in the
dictionary view, in the account it belongs to. It goes the same way as `E`: the register and the
account's VOC are read again, the rule above is asked, and the file is reached through the same
temporary pointer and judged again with its subfiles, so an item of a dictionary that lies outside
the account is refused with its reason before anything is shown. The record is then read with its
update lock: a record another session holds (someone editing it) is refused, `zz1 in the VOC of ACME
is locked by user 12 (an editor holds it): it is not deleted`. Otherwise a box titled `Delete this
record?` names the record, the account and the file's path; `Cancel` is the default, and `Run` asks
for the record's id to be typed. Only the exact id deletes it; Cancel, Esc or a different id leave
it where it is (`nothing was run`). The page deletes that one record itself, through the file it
judged, and runs no command. A delete writes one line to the audit trail, for example
`master delete account=ZE1 kind=voc file=voc id=zzdel1`.

**`D` in the programs view deletes the program and its compiled program.** It goes the same way: the
program file and the program's own file must lie inside the account, the program is read with its
update lock, and its id is typed in the box. The compiled program is found by its name, as the
Built column finds it: the record of the same name, in lower case, in the `.out` file the account's
VOC names for the program file (`bp.out` for `bp`), or else in the `.out` file beside the program
file. The same rule holds for it: when that `.out` file, or the compiled program's own file, lies
outside the account the whole delete is refused with
its reason (`the compiled programs of zeob.bp lie outside ZE1: zwob is deleted in the account they
live in, not from here`), before the box and before anything is deleted. The box names the
compiled program, or says there is none; the page deletes the program, then its compiled program,
through the files it judged, and runs no command. **A catalog entry of the program is left**: it
is the account's (a private catalog holds its own copy, so the program can still be run by its
catalog name), and the box says so; remove it in that account, for example
`run.in ze1 delete.catalog prog` for a private catalog entry or `run.in ze1 decatalog prog` for a
local one. The audit line is `master delete account=ZE1 kind=bp file=bp id=prog object=deleted`
(`object=none` when there was no compiled program, `object=failed` when the `.out` file refused the
delete).

## Programs: `E`, `N` and `C`

**In the programs view, `E` and `N` open the program in the editor and `C` compiles it, in the
account it belongs to.** `E` and `N` go the same way as for a VOC entry: the program file must lie
inside the account (a program file reached through a pointer to another account, marked `>`, is
refused), and so must the program's own file. The temporary pointer reaches the program file's data
only. The editor is told which account the program belongs to, so its **Compile** (F8) and
**Compile and catalog** (F9) do not run BASIC in SDSYS through the pointer: they run
`run.in` (see *Running one command inside an account*, below) in that account, so the object goes into the account's own `bp.out`, a
`$catalog` line in the source is not acted on, and the catalog is the account's. Its **Debug** (F7, and Debug from the first line) compiles the
program for the debugger and runs the debugger in that account, the same way (`run.in … basic …
debugging`, then `run.in … debug …`), and the breakpoints marked in the editor's gutter are handed to
that debugger as they are for any program (F7 runs on to the first of them, and the lines that
still have a breakpoint come back to the editor); **Run** is refused in the editor (run it in its account).

**`C`** on the page compiles the program under the cursor the same way and shows what the compiler
said in a box; the Built column follows. The page writes `master edit account=ZE1 kind=bp file=bp
id=prog new=0` for an edit and `master compile account=ZE1 file=bp id=prog result=ok` (or `failed`)
for `C`; `run.in` writes its own `run.in begin` and `run.in end` lines for each compile. A compile
that `run.in` refuses (a command word that is not SD's own entry in that account, a file outside the
account, a file with a trigger, a `$execute` line in the source) shows the refusal in the same box.

**`B`** on the page debugs the program under the cursor the same way: a compile that fails is shown
as `C` shows it and nothing is debugged; otherwise the terminal goes to the debugger, and when it
ends the page asks you to press Enter and comes back on the same program. The page writes `master
debug account=ze1 file=bp id=prog`.

## A global change of every row shown: `G`, and `U` to put it back

**`G` makes one change to every row the page shows, in every account the rows come from.** The rows
are exactly those on the screen: the hits of a find (`F`, every account) or the entries a filter
(`/`) keeps in the account under the cursor. A filter or a find must be on, and a list cut short at
the page's limit is refused (narrow it until every row is shown). `G` asks what to change:

- **VOC entries and dictionary items**: the field, by its number (1 to 500) or, for a dictionary
  item, the word `heading` (field 4 of a D, I, E or L item; an item of another type is refused for
  having no heading), then `S` to set the field to a value or `R` to replace a text in it with
  another (an empty replacement takes the text out).
- **Field 1 is the type of the record** (a VOC entry's V, F, Q, PA ...; a dictionary item's D, I,
  PH ...), and changing it turns a verb or a pointer into something else. `G` therefore changes it
  on **one record only**: when more than one record is shown it is refused before the box
  (`field 1 is the type of the record: G changes it on one record only, and 3 are shown ...`), and
  on a single record the box carries a **WARNING** line with the old and the new type (`"X" ->
  "PA"`). Cancel is still the default, and `U` puts field 1 back like any other field (field 1 is
  excluded from batch actions and allowed on a single item with a confirm warning).
- **Programs**: a text to replace in the source and what replaces it. Each program changed is then
  compiled again **in its own account** through `run.in` (as `C` does), and is counted as failed
  when the compiler does not say it compiled.

The texts are printable characters only, up to 120 of them. **One box** (titled *Update these
records?*) then shows the change, and each account with how many records would change, the first
ids, how many are as they are already and how many would be refused, with the first reasons. **Run
or Cancel is all it asks** (Cancel is the default): no name or count is typed. This is looser than
`D`, which asks for the id; it is deliberate, and
it is how the page is delivered.

Run writes **account by account**. Each account is judged again (it must still be in the register),
and each file by **the pointer rule** before it is opened for writing: the path, what the kernel
opened, and the two parts of a hashed file must lie inside the account (a program's own file too). A
row whose file lies outside the account it is listed under - the dictionary of `@SDSYS/voc.dic`,
another account's file reached through a pointer, a path written with `..` - is **refused**, in the
box and again at the write; its target is never written. Each record is read with its update lock
(a record another session holds is refused) and must still be what the box read (one changed since
is refused). **A refusal or a failure is counted and the run goes on**, in that account and in the
next. A box then shows, for each account, how many records were changed, refused and failed, with
the first reasons; the audit trail gets one line per account:
`master global account=ZE1 kind=dict changed=2 refused=3 failed=0` (`kind=voc`, `dict` or `bp`).

**`U` puts the last global change back.** Before each record is written, the record as it was is
kept in `&entries.undo&`, a file of SDSYS's own account; the first time, a box shows the command
that makes it (`create.file &entries.undo&`) and nothing is changed unless it is made. It holds the
last run only: a new run replaces it. `U` (offered while there is a run that has not been put back)
shows a box titled *Put these records back?* (Run or Cancel) and then puts back each record **only
if it is still exactly what the run wrote**; a record edited since is left as it is and counted,
never overwritten, and so is one that has gone or that another session holds. The pointer rule is
asked again, and a program put back is compiled again in its account. The audit trail gets
`entries undo account=ZE1 records=2` for each account. When nothing was held, refused or failed the
run is marked put back and `U` is no longer offered.

The AI line of the page is not offered `G` or `U`.

## Running one command inside an account: `run.in`

A program is compiled and cataloged in its own account: its VOC, its private catalog, the files its
I-types translate through. An account that is locked out of its own programs (`bp-off`) cannot do
that, so the administrator does it for the account. `tool.entries` (described
above) and the editor it opens use it for every compile.

```
run.in acme basic bp prog
run.in acme basic bp prog debugging no.query
run.in acme catalog bp prog local no.query
run.in acme decatalog prog
run.in acme delete.catalog prog local
run.in acme compile.dict cust total
run.in acme debug bp prog
```

The verb is in the SDSYS VOC only and refuses anyone else ("Command requires administrator
privileges"). It runs **one** command from the list above, in a **registered** account (never
SDSYS itself, never a path), and **it is back in SDSYS when the command ends**. That includes a
command that aborts, a break and a run-time error: the session is put back before anything else
happens and says so ("run.in: the command did not finish; the session is back in account acme").
Without this an administrator would be left in the account, with the command's reach, until typing
`LOGTO SDSYS` (the administrator's way back by hand; it is refused to every other session).

### Debugging a program in another account: `run.in` *account* `debug` *file* *program*

The program does not run in your session. An SDSYS session's token is elevated for the whole session, so on
Windows the SD service starts **a separate SD process of that account** for it, as the local Windows account
`sdrunin`, with the account's own group and `sdusers`, no privileges and no administrator rights. It has no shell,
no `os.execute` and no edit gates, and cannot start another process. The debugger appears in your window; while the
program runs, its screen and keyboard are your window's. A resize of your window while it runs does not reach it.
If the run cannot start, SD says why (message 12599).

The installer creates the local account `sdrunin`; nobody can sign in as it, and uninstalling removes it.

> **Security warning.** The program can do whatever a session of that account can do, including changing that
> account's files. Its output goes to your elevated window as it writes it, as it would on Linux, so a program
> written to deceive can draw anything there. Do not type passwords or other secrets into it unless you trust its
> code. The debugger's AI command is not available for these runs: the program's text is not trusted in an elevated
> session.

### What it checks before it changes anything

The account and every name are one plain word (a-z, 0-9, dot, dash and underscore, a letter or digit
first, at most 64 characters, and not a word SD reads as an option); each option is on that
command's own list and is given once; the first name of `basic`, `catalog` and `compile.dict` is a
file in **that account's** VOC. **The command SD runs is built from those words and is never the
text you typed.** **`basic` is always given `no.catalog`**, so a `$catalog` directive in the
account's source (or in a file it includes, or in its `$BASIC.OPTIONS`) is not acted on: without
it, compiling the source as the administrator would catalog it as the administrator, in the global
catalog if the directive says `global`. To catalog a program of an account, say so:
`run.in acme catalog bp prog`. `run.in` does not start the account's `login` paragraph (it would
run with the administrator's rights), and it does not nest.

### The command does not run as the administrator

The account's files, VOC and programs are written by the account's user, so nothing in them is
trusted. For the command itself the administrator flag is **off**, only the edit gate the command
needs is on (`bp-edit` for `basic`, `catalog`, `decatalog` and `delete.catalog`, `dict-edit` for
`compile.dict`), and `sh` and `os.execute` are off whatever the account's own switches say.
Everything is put back when the command ends, the flag last. So `run.in acme catalog` with a
`global` request is refused, as it would be for the account.

**The words must be SD's own.** The command word and every option word (`no.catalog` included)
must be, in that account's VOC, exactly the entry SD ships: the record of the same name in
`newvoc`, its type letter and everything after the description. An account that has changed or
removed one (its own `basic`, say) is refused before anything happens, and before anything is
kept or changed: *run.in: basic is not SD's own entry in the VOC of account acme (it is missing or
was changed there); nothing was run*. Put SD's own entry back in that account's VOC and try again:
`update.accounts` does it, since it adds a shipped entry that is missing and rewrites one that differs
from the record of the same name in `newvoc` (it asks first where the type letter differs, and keeps an
entry whose description says `[LOCKED]` unless it is a verb). **An account whose VOC has no `no.catalog` keyword** (one made before the keyword
existed and not updated since) is refused for `basic` until its VOC has it.

**On Windows that is not the whole of it.** An SDSYS session's own Windows token is elevated for the
whole session, and turning SD's flag off does not change it. So anything of the account's that ran
during the command, and any file it read, would have the elevated administrator's reach. So, once
it is in the account and before the command runs, `run.in` also refuses:

* **a file the command writes that lies outside the account**: the named file's data and dictionary,
  the `.out` file of `basic` and `catalog`, and the private catalog of `catalog`, `decatalog` and
  `delete.catalog`. A path must be relative, with no `..`, no `@` token and no drive, and what of
  it exists is asked of the kernel (which resolves it as an open would). A VOC entry could
  otherwise point the compile's output at SDSYS's own files, which this session can write. `bp.out
  in account ACME names a path outside the account; run.in did not run the command`.
* **a file the command opens that has a trigger**: the VOC, the named file and its dictionary, the
  `.out` file and the private catalog. A trigger is a program found in the account's own catalog,
  and it would run in this session. `bp in account ACME has a trigger function; run.in did not run
  the command`.
* **a `$execute` line in the source it compiles.** The compiler runs the command a `$execute`
  directive names while it compiles; under `run.in` it refuses it instead, and the compile fails
  with `$execute is refused in a compile started by run.in: it would run a command from the
  administrator's session`.

And while the command runs:

* **an include file or a dictionary outside the account.** A `$include` (or `include`), `$dict` or
  `file` that leads outside the account's own directory, through a pointer in its VOC, fails the
  compile: `... is outside the account: a compile started by run.in reads include records and
  dictionaries in the account and syscom only`. SD's own `syscom` headers are still found.
* **a Q-pointer out of the account.** A Q-pointer, or the *account*`:`*file* form, leads only into
  the account the command runs in.
* **`logto`.** `logto is refused while run.in is running a command in account acme`.

Each refusal writes `run.in refused account=ACME reason=...` to the audit trail (a refused word
also gives `word=`).

**What it does not cover:** a source that includes a record from another of the account's own files
reads that file too, and a read trigger on that file would run. The files a command reads by a name
in the source are not listed in advance.

### The audit trail

Every use writes `run.in begin account=… command=…` and `run.in end account=…` (or
`run.in revert account=… reason=abort`) to the audit trail, and a refusal writes `run.in refused …`
with the reason.

## What it does not do

* **It does not change what a pointer points at from another account.** A pointer record is the
  account's own record and is edited like any other; its target is edited in the account it lives
  in, SDSYS's included.
* **It does not remove a catalog entry when it deletes a program.** The entry is the account's;
  `run.in` *account* `delete.catalog` or `decatalog` removes it.
* **It does not see a change made outside SD** any differently from SD itself: the page reads the
  accounts' files when it is asked to, so a change made in Windows is simply there at the next read.
