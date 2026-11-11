Title: The Master Files
Subtitle: How the administrator manages every account's VOC entries, dictionary items and programs from SDSYS, in the account each one belongs to: the page tool.entries, its lists, the pointer rule, and editing and deleting a record.

**The administrator manages every account's VOC entries, dictionary items and programs from one
page, `tool.entries`, and each one is changed in the account it belongs to.** Nothing is copied: the
page reads the accounts' own files, and an edit, a delete or a compile happens on the real
record, in its own account. That is the purpose of the master files: most accounts can be locked out
of editing their own VOC, dictionaries and programs (the edit gates `voc-edit`, `dict-edit` and
`bp-edit`), and the administrator does that work for them.

The page continues in [The master files: programs and global changes](19a-the-master-files-programs.html)
(compiling, `G` and `U`), and the command it runs inside an account is
[run.in](19b-run-in.html).

> **What lets SDSYS write into an account.** An SDSYS session runs as an elevated Windows
> administrator, and every account directory gives the Administrators group full control (with
> SYSTEM and the account's own group). So SDSYS can write inside every account; there is no grant to
> make and none to take away, and the page's SDSYS column always says `yes`. That is also why the
> page and `run.in` are careful about what of the account's own runs while they work in it (see
> [run.in](19b-run-in.html)): anything of the account's that ran in that session would run with the
> administrator's token.

## The entries of every account by pointer: `tool.entries`

**`tool.entries`** is the page that looks at the accounts' own files and copies nothing: it is in the SDSYS VOC only and
refuses anyone else before it reads anything. **It lists the VOC entries, the dictionary items and
the programs, and it edits, deletes and compiles each in the account it belongs to** (below).

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
programs are on the [next page](19a-the-master-files-programs.html)). The terminal is
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

## What it does not do

* **It does not change what a pointer points at from another account.** A pointer record is the
  account's own record and is edited like any other; its target is edited in the account it lives
  in, SDSYS's included.
* **It does not remove a catalog entry when it deletes a program.** The entry is the account's;
  `run.in` *account* `delete.catalog` or `decatalog` removes it.
* **It does not debug.** `B` says it is not built on Windows: `run.in` has no `debug` here (see
  [run.in](19b-run-in.html)). Debug a program in its own account.
* **It does not see a change made outside SD** any differently from SD itself: the page reads the
  accounts' files when it is asked to, so a change made in Windows is simply there at the next read.
