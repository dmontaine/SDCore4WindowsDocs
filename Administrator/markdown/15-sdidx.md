Title: sdidx, the Index Relocation Tool
Subtitle: Reporting where a hashed file's indexes are kept, moving them to another folder or back, pointing a file at indexes you have moved yourself, and deleting them: every option, and what each does to the disk.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

An index on an SD hashed file lives in an extra file beside the data, `%2` for
the file's first index, `%3` for the next, up to 32 in all. Normally it sits in
the data file's own folder. An index can instead be kept in another folder,
**relocated**, which is how an index is put on a faster or larger disk. The data
file's header records where. `sdidx` is the stand-alone program that reads and
changes that record and moves the files. It works on the files on disk, not
through SD.

You can relocate an index at creation from SD: `create.index` *file* *field*
`pathname` *path*. `sdidx` is for everything after that, and for the case where
SD is not running.

## The short version

```
sdidx -q C:\ProgramData\SD\user_accounts\acct\orders      # where are its indexes?
```

* **Copy the file's whole folder first if you use `-m` or `-d`**
  (`Copy-Item -Recurse` in PowerShell). `-m` deletes the old index files
  afterwards and `-d` deletes indexes. Neither can be undone.
* **Give full paths, for the data file and for the index folder.** Either
  slash will do. A relative index path given to `-m` or `-p` is made absolute
  from the current folder before it is stored, as `C:\...`. A path longer than 255 characters, which
  the file header cannot hold, is refused: `Path is too long (the limit
  is 255 characters)`, status 1.
* **Close the file in every session first.** The program refuses if the file is
  open within the running SD: see below. **It refuses nothing if SD is not
  running**, because it has nothing to ask.
* If `-m` or `-d` cannot delete an old index file it says so and exits 1; it
  does not say "moved" or "deleted" over a file that is still there.

## Where it is and who can run it

`C:\Program Files\SD\usr\bin\sdidx.exe`. Type that, or just `sdidx` if SD's
program folder is on the system PATH (`append.sd.path`, in the remote access
page of this set). **It opens the file's `%0` for read and write even to answer
`-q`**, so you need write access to the file even to ask where its indexes are
(on a copy whose `%0` is read-only, `-q` prints *Cannot open
data file [13]* and exits 1). Inside an account those with write access are the
account's own SD user (`sdu_` and the account name), Administrators and SYSTEM.

The files `-m` creates take the permissions of the folder they are made in, as
any new file does on NTFS, and belong to whoever ran the program. Check the new
folder with `icacls` after moving an account's indexes to another disk, so that
the account's user can still write there.

It needs no configuration file and takes no option other than the mode.

## The command line

```
sdidx -d datapath             delete the indexes
sdidx -m datapath {akpath}    move the indexes to akpath (or back, if omitted)
sdidx -p datapath {akpath}    set the index path in the header, move nothing
sdidx -q datapath             report where the indexes are
sdidx datapath                the same as -q
```

Give exactly one mode. Letters are not case sensitive, and only the second
character of a word is read, so `-qx` is `-q`. Anything else, two modes,
an extra argument or no path prints the five usage lines above and exits 1. A
**datapath** is the Windows path of the file's folder, not an SD file name. A
path that does not exist, or is not an SD hashed file, gives *Cannot open data
file [2]* and exit 1.

Every run prints the banner. Success exits 0; any failure exits 1.

### `-q`, report
```
> sdidx -q C:\sdi_demo\orders
Indices are not relocated
> sdidx C:\sdi_demo\plain
File has no indices
> sdidx -q C:\sdi_demo\orders          (after a move)
Index directory is C:\sdi_demo\a\b\orders.idx
```

The three answers are the only ones. It changes nothing. (The word is
*directory* in the program's own output.)

### `-m`, move
```
> sdidx -m C:\sdi_demo\orders C:\sdi_demo\a\b\orders.idx
Moving index subfile 2
Indices have been moved
```

What it does, in order: refuses if the file is open in SD; stops with
*Indices are already at this location* if `akpath` is where they are; checks that
each index file really belongs to this data file (it compares a creation stamp in
both headers, and says *Index subfile n does not appear to belong to the data
file* or *Incorrect magic number* if not); refuses with *`akpath` already exists*
if the target is there; creates the target folder, **and any missing
parents** (`a\b\orders.idx` is made from nothing); **copies** each index
file to the new place; writes the new path into the data header; **then deletes
the old index files.** If it stops before the header is written, the copy at the
target is left behind and the file is as before.

* **With no `akpath`, it moves the indexes back** into the data file's own
  folder and clears the path in the header.
* **Only the index files are deleted from the old place**: the `%2`,
  `%3` ... that the header lists, and nothing else. If the indexes were in a
  relocated folder, that folder is removed afterwards **only if it is then
  empty**; if it holds anything else (a file named `note-from-admin`, say) the
  folder and the file stay, and the program says `path holds other files and has
  been left`.
* If an old index file cannot be deleted the program says `Cannot delete path
  [n]`, then `Indices have been moved, but the old index files could not all be
  deleted`, and exits 1. The move itself is complete: the header names the new
  place.
* It needs room for a second copy of the indexes while it moves them.
* **If the target folder cannot be made, it says so and changes nothing.** It
  prints `Cannot create directory` *akpath*`:` and the reason on standard
  output, and ends with status 1. The reason is the operating system's, or *a file
  of that name exists* when a component of the path is a file. *akpath* in the
  message is the whole path as you typed it, not the component that failed, and
  the indexes and the header are where they were.

### `-p`, point
`-p` writes the path into the header and moves nothing. Use it when you have
moved the index files yourself (or restored them elsewhere) and only the header
is out of date.

* It checks that the folder exists and is a folder (*does not exist*, *is not a
  directory*), and that **every index the header lists is in it and belongs to
  this file**. A folder without the index files gives *Cannot open index subfile
  2 [2]*.
* **On success it says what `-q` would now say**: `Index directory is
  C:\sdi_demo\byhand`, or `Indices are not relocated` when `akpath` is omitted.
  A failure to write the header is reported and exits 1.
* Omit `akpath` to say "the indexes are in the data file's folder".
* It does not know about accounts. It will point a file at any folder you can
  write, inside the account or not.

### `-d`, delete
```
> echo y | sdidx -d C:\sdi_demo\o4
Delete the index files in C:\sdi_demo\o4.idx (Y/N)? All indices deleted
```

The result is a file with no indexes: the header's index map is cleared. To get
the indexes back you create them and build them again with `create.index` and
`build.index`.

* If the indexes are relocated and the folder exists, it asks `Delete the index
  files in path (Y/N)?` and, on `y`, deletes **the index files the header
  lists** and then the folder if that leaves it empty. Anything else in the
  folder stays, and the program says so (the same rule as `-m`).
* **Answering `n` stops the program**: it prints `Indices not deleted`,
  exits 1, and changes nothing: the header is as it was and `-q` still names the
  folder.
* **If standard input ends at the question, it is taken as `n`**: the
  program prints `End of input` and `Indices not deleted` and exits 1.
* With indexes in the data file's own folder there is no question. It deletes
  the files and clears the map. If a file cannot be deleted it says so, clears
  the map anyway, and exits 1 with `The indices are removed from the file, but
  some index files could not be deleted`.

## The check that SD does not have the file open
`sdidx` attaches to SD's shared memory when SD is running and looks through the
table of open files for the data folder's resolved path. If it finds one in use
it prints *File is currently open within SD* and exits 1, for every mode, `-q`
included; `-q` succeeds once the session has ended.

**The comparison ignores case, as NTFS does**: `...\user_accounts\Don\x`
and `...\don\x` are the same file, and the first is refused as readily as the
second. **That is all it does. It does not look for a file held by another
program, by `sdfix` or by `sdconv`, and when SD is not running it checks
nothing.** Stop the service (`Stop-Service SD`) if you must be sure; see
*Installation and the service*.

## What it will not do

* It does not check, rebuild or repair an index. Use `sdfix` to check one
  ([sdfix](14-sdfix.html)) and `build.index` to rebuild it.
* It does not take a backup, and does not warn before it deletes.
* It does not stop other programs using the file, and does not check the file is
  open anywhere except within SD.
* It does not change an index's definition, only where its files are. It cannot
  move one index and leave the others.
* It does not work on directory files, sequential files or other things that are
  not SD hashed files.
