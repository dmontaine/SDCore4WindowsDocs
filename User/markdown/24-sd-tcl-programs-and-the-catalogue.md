Title: SD TCL - Programs and the Catalogue
Subtitle: Compiling SD BASIC, running it, and giving it a name you can type.

Getting from source to something you can type is three steps: **compile it, put
it in a catalogue, then call it by name.** Only the first is compulsory.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

> **Every listing on this page was produced by running it**, on SD Core for
> Windows W1.0-0, against a two-line program in an account's `bp` file.

## Compiling

```
basic {file} record
```

The file defaults to `bp`. What comes back names the file and record, then the
error count:

```
basic bp zzprog
```

```
Compiling bp zzprog
WARNING: Final END statement is missing
0 error(s)
Compiled 1 program(s) with no errors
```

**A warning is not an error and the program still runs.** The line above is a
warning, the count says `0 error(s)`, and that program ran. **Read the count,
not the presence of output.**

`@system.return.code` is the number of programs compiled, and negative on a
fatal error.

**`basic ... no.catalog` compiles and catalogs nothing.** A `$catalog` line in
the source or in a file it includes, or a `CATALOG` line in the `$BASIC.OPTIONS`
record, makes the compile catalog the program as well; with `no.catalog` none
of them is acted on, and the compile says so
(`zzprog compiled; its catalog directive was not run (no.catalog)`). The
administrator's `run.in` always gives it to the `basic` it runs, so compiling an
account's source for it cannot put that account's code in the global catalog.

**The object code goes into `bp.out`**, a separate file beside `bp`, one record
per program. **Its name is lower case even when the source record is not** —
a source record `ZZPROG` compiles to an object record `zzprog`. That is this
port's naming, and it is worth knowing before you go looking for the object by
the name you typed.

## Running without cataloguing

```
run {file} record
```

```
run bp zzprog
```

```
ZZPROG OK
```

`run` needs the file and record name every time. It is what you use while you
are still writing the thing.

## The catalogue is what gives a program a name

```
catalog {file {call.name}} {program | *} {local | global | pcode} {no.xref}
```

Catalogue it and the name becomes a command:

```
catalog bp zzprog
zzprog hello
```

```
ZZPROG added to private catalogue
ZZPROG OK
```

**The program sees the whole command line.** `@sentence` in the program above
read `zzprog hello`, so arguments arrive as typed and the program parses them
itself.

**A program run by its catalogue name takes `lptr` and `no.page` as `run`
does.** The words stay in the sentence for the program to see. A word in
quotation marks is not a keyword. This applies to a catalogue name only, not to
the name of a VOC verb.

### Three catalogues, and they are not the same

| | |
|---|---|
| **private** | the account's own. The default when no keyword is given |
| **local** | a VOC entry in the account, so the name works only there |
| **global** | `gcat` in the system account — **every account sees it** |

**Global cataloguing requires administrator privilege, and on this port that
means an elevated session.** Without it you get *"Command requires
administrator privileges"*. **The same gate applies to an implicit global
catalogue** — one chosen by a `!`, `_` or `$` prefix on the call name
rather than by the `global` keyword — so the prefix is not a way round it.
The prefix characters `*` and `-` were removed in 1.2-0: `catalog bp *name` and
`catalog bp -name` are refused.

Private and local cataloguing need none of this and work in a programmer's own
account.

**`catalog ... local` asks before it overwrites.** When the VOC already holds a
local catalogue pointer under that name and it points at a different object
file, you are asked first (Return is no). `no.query` goes ahead without asking,
and cataloguing the same file again does not ask.

### Seeing and removing

```
map {all} {lptr {n}} {file {name}}
```

```
System catalogue map at 23:12:07 on 26 Aug 2026                    Page 1
  Catalogue name..................  Compiled.  Time....  ...Obj  ..Xref  ..Size
  ZZPROG                            26 Aug 26  23:12:07     189       6     195
                                                                Total:      195
```

`Obj` and `Xref` are the object-code and cross-reference sizes in bytes, and
`Size` is the total. An empty one says so:

```
Catalogue is empty
```

```
delete.catalog name... {global | local}
```

```
ZZPROG deleted from the private catalogue
```

```
decatalog {file} name ...
```

**`delete.catalog ... local` removes only the VOC entry**, and leaves the object
code it pointed to lying in the account's object directory. **`decatalog` removes
both** — the local catalogue entry and the compiled program it names:

```
catalog bp zzdocprog local
decatalog zzdocprog
```

```
zzdocprog added to local catalogue
zzdocprog deleted from the local catalogue
```

Several names may be given. A name that is not in the local catalogue is said so
(*zzdocprog is not in the local catalogue*) and the rest are still done; an object
file that cannot be deleted is reported as *Cannot delete the object code* and
the entry is gone all the same. A file name in front of the program name is
accepted and ignored, because the entry already holds the object's pathname.
`decatalog` works on **local** entries only — a private or global catalogue entry
is removed with `delete.catalog`.

> **`map` also takes a `file` option**, which writes the map to a file instead
> of the screen. **It asks before overwriting** — *"File xx will be cleared and
> overwritten. Continue (Y/N)?"* — so it is not usable from a script driving SD
> down a pipe.

## Continued in

[Programs: find.program, Dictionaries and the
IDE](24a-sd-tcl-find-program-dictionaries-and-the-ide.html) — find.program,
formatting source, compiling dictionaries, named common and the IDE
