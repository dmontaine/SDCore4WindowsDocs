Title: Programs: find.program, Dictionaries and the IDE
Subtitle: Which copy of a program will run, formatting source, compiling dictionaries, named common blocks and the IDE.

This page continues [SD TCL - Programs and the
Catalogue](24-sd-tcl-programs-and-the-catalogue.html).

## Which copy will run: `find.program`

```
find.program name {detail}
```

For the case where the system seems to run the wrong version of a program
because it is catalogued in more than one place. It looks in the three places a
program is loaded from, **in the order they are searched** — the local catalogue
(a VOC entry that points at the object file), the private catalogue (the
account's `cat` directory, or the directory `$PRIVATE.CATALOGUE` names) and the
global one — and reports every one that has it:

```
Program is in the local catalogue
   Compiled 10/15/26 20:56:03
   Subroutine with 2 arguments
Program is in the private catalogue
   Compiled 10/14/26 09:12:40
   Subroutine with 2 arguments
```

The kind is *Program*, *Subroutine with n arguments*, *Function with n
arguments* or *Class module*. `detail` adds the object code size in bytes and the
flags of the object (`internal`, `debug`, `recursive`, `trusted`, `case sensitive`,
`sdcall`). **SD's object code carries no compiler version and no source
pathname, so those two lines of openQM's `detail` are not there.** A name found
nowhere is *xx is not catalogued*. The name is looked for as typed; a global
program is named with its prefix (`!acc_hold`, `$listphan`).

## Formatting source

```
format {file} {record} {case}
```

`format` rewrites a BASIC source record with standard indentation. **It says
nothing at all when it succeeds** — no output is the success case, which is
worth knowing before you go looking for a confirmation that never comes. `case`
additionally applies case conversion.

With no record name it uses the active select list.

## Compiling dictionaries

```
compile.dict {dict | data} file {i-type}... {no.query} {no.page}
compile.dict local
compile.dict all
```

It compiles the I-type entries in a dictionary; with no names it does all of them, or uses
the active select list if there is one.

| | |
|---|---|
| **`compile.dict local`** | every dictionary in the account |
| **`compile.dict all`** | every dictionary visible from the account |

Compiling a dictionary is a performance step, not a correctness one: it is what
a query using those entries runs against.

## Named common blocks

```
list.common {all} {detail}
delete.common name
```

```
No named common blocks present
```

Named common survives between programs in a session, and `list.common` is how
you see what is holding memory. `all` additionally shows the system blocks and
is internal-only. `detail` puts the name of the program that created each block
beside its name, which helps when two programs disagree about the size of a block:

```
list.common detail
SCREEN.DATA  show.screen
SYS.FILES    myprog
```

The names are sorted on their own; the program is the one that executed the
`common` statement first, in this session.

## One screen for the lot: `ide`

```
ide {file record}
```

Opens a full-screen environment for BASIC programs and the other text records
of an account, built on the screen library. `ide file record` starts on that
record. It needs a terminal and **stops in a phantom**. It runs inside SD, so it
needs no operating-system permission.

> **Not run on Windows yet.** The IDE is SD Core for Linux's program, carried
> here unchanged and compiled (25 October 2026); nothing on this page has been
> seen on a Windows console.

| part | what it is |
|---|---|
| menu bar | the top row; F10 or Esc opens it, and a click on a title opens that menu (a click on the bar beside the titles does nothing) |
| tree | the account's files on the left. Return on a file lists its records (the first 2000), and Return again closes the list. Return on a record opens it. A letter jumps to the next entry that starts with it |
| editor | on the right, a tab for each open record. **While it has the focus the character at the cursor is shown in the highlight style** (as well as the terminal's own cursor being put there), so the place shows on a terminal that draws its cursor poorly. It is the text area `screen memo` uses, so its keys are `memo`'s: selection, cut, copy and paste, undo and redo, find, line numbers. Text is coloured as SD BASIC, C, Python, JSON, shell or Markdown by the file and record name. **A horizontal scroll bar runs along its bottom row** (`<` and `>` at the ends, a thumb as long as the visible part is of the longest line; none to speak of when every line fits); clicking an arrow scrolls 8 columns and clicking the track a page |
| table | under the editor: the compiler's errors, or search results |
| pane marks | **`[*]` or `[-]` in the top right corner of each pane that can have the keyboard**: the files (on the frame above the tree), the editor (on the frame above it), the tab strip (at its right end) and the messages (at the right end of their bar). `[*]` is on the pane that has the keyboard, `[-]` on the others; Tab moves it round in that order |
| status line | **the pane that has the focus** first, in brackets (`[Files]`, `[Tabs]`, `[Editor]`, `[Messages]`: Tab goes round them in that order), then the record, the cursor's line and column, and a star when there are unsaved changes |

| key | |
|---|---|
| F7 | save and compile; the compiler's lines go in the table. Return on one goes to its line, F4 to the next |
| F8 | compile and catalogue |
| F5 | compile and run |
| F9 | compile with debugging and run the debugger |
| F2 · Ctrl-S | save the record |
| Ctrl-R | find a text in every record of the file the tree is on (the first 2000 records, 500 lines), listed in the table; Return opens the record at the line |
| F11 | find in all the records of a file |
| Ctrl-E · Go, Edit in SED | edit the record in [SED](27a-sd-tcl-sed.html) and come back (below) |

Run and debug give the terminal to the program and come back to the IDE when
you press Return. **Nothing runs if the compile failed.** If somebody else has
changed a record since the IDE read it, saving asks before it overwrites;
closing a record, or leaving, with unsaved changes asks whether to save. **If the
IDE's input ends** (a pipe that has been used up; a terminal does not end like this)
it leaves at once and asks nothing, so unsaved text is not saved. Saving a record
of a program file, and compiling, ask the account's edit switches (`bp-on`; see the
Administrator set's *Accounts and Security*), and say which is missing.

**Ctrl-E hands the record to SED, and SED's save brings you back.** SED edits the
record on disk, so a record with unsaved changes is saved first: the IDE asks *Save
them, then edit in SED?* and **Cancel** leaves everything as it was. In SED you work
as you always do; **the first successful save ends the edit** and the IDE comes
back with the new text in the editor, the compile errors forgotten (they named
lines of the old text) and a line in the status bar, *Back from SED: bp prog is
saved*. Leaving SED without saving (Ctrl-Q) brings you back too, with the record as
it was, and a record that someone else holds locked opens in SED **read only**, with
SED's own message, as it does from the command line. There is no *press Return*
pause on the way back, which Run has because a program may have written something
to read. Ctrl-E is the editor's *end of row* key in other programs that use
`screen memo`; in the IDE it belongs to this and **End** ends a row.

The other keys follow [SED](27a-sd-tcl-sed.html) where the two do the same:
Ctrl-Q quits, Ctrl-L goes to a line, Ctrl-X, Ctrl-C and Ctrl-V cut, copy and
paste, Ctrl-Z and Ctrl-Y undo and redo, Ctrl-F finds forward and Ctrl-B
backward (Return on the question repeats the last text), Ctrl-R replaces a text
through the record and Ctrl-W writes the text to another record. In the text
area of every program that uses `screen memo`, a word back and on are
Ctrl-P and Ctrl-U; Ctrl-B and Ctrl-F are SED's find keys.

On a terminal that says it is UTF-8 the frame, menus and scroll bars use
line-drawing characters; elsewhere `+ - |`. The colours are the blue theme.

**What it does not do:** it does not lock records while they are open (the check
at saving is what protects against a second editor), has no replace across
records, no project files and no completion.

**The IDE is laid out for 140 columns by 42 lines or more**; a bigger window is
used whole. **A window smaller than 140 by 42 when the IDE starts is refused**, in
words (*IDE needs a window of at least 140 columns by 42 lines; this one is 100 by
30*), and nothing is drawn; `ed` is the editor for a small window. The window
measured is the one on the screen, or the display `term w,h` gave if that is
smaller. If the window is made smaller while the IDE runs, the layout does not
shrink with it: the IDE shows the **upper left corner** of its 140 by 42 layout and
nothing past the edge, and draws the whole layout again when the window is made
bigger. While the cursor of the editor, the tree or a question is **off the
screen** the IDE does not take keys, because you would be typing where you cannot
see: a warning in reverse video fills the upper left, every key is thrown away, the
warning goes by itself when the window is big enough, and **Ctrl-Q, then y** leaves
the IDE without saving. [SED](27a-sd-tcl-sed.html) describes all of it; the IDE and
[CED](27b-sd-tcl-ced.html) behave the same way.

## The two that are not like the others

**`generate`** builds `$include` token definitions from a dictionary. **It is
interactive** — it asks for the token type, the prefix and several other
things — so it cannot be driven from a script.

**`debug`** runs a program under the debugger, taking the same arguments as
`run`. It needs a terminal and **refuses inside a phantom** with *"Cannot debug
program in a phantom process"*. The debugger itself is covered in
[SD Basic - Debugging](17-sd-basic-debugging.html).

## Who has these verbs

**Every account has all of them now**: `format`, `list.common`, `basic`,
`catalog`, `compile.dict`, `debug`, `delete.catalog`,
`delete.common`, `find.program`, `generate`, `map`, `run`.

**Running a catalogued program never needed any of these anyway** — a
catalogued name runs by being typed, with no VOC record of its own — so an
application deployed this way was always reachable regardless of what
verbs an account had.

## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Debugging](17-sd-basic-debugging.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).
