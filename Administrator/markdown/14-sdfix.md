Title: sdfix, the File Check Tool
Subtitle: Checking a hashed file's structure on disk, repairing what it can, recovering space and clearing dead space: when to run it, every option, and what it does to the file.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

`sdfix` is a stand-alone program, not an SD command. It reads and, with the
right options, **rewrites the files of an SD hashed file** directly on disk,
without going through SD. Use it when you suspect a file's structure is
damaged (after a crash, a full disk, a restore from a bad copy), or to give a
file back disk space it no longer needs. It has no effect on a file that is
sound.

> **How this page was made.** Everything here was read from `sdfix.c` and run on
> scratch copies of a small file under `C:\sdi_demo`, with the program as built
> from the `Dev` branch of SD Core for Windows (the banner reads `SDFIX
> W1.1-3`). Each result is marked *run* (the damage was made and the output is
> real) or *source* (read from the code, not provoked). It was run from an
> ordinary, not elevated, prompt; not on a file owned by another user.
>
> **Written 19 October 2026.** The tool had faults, found by running it and fixed
> (see the end of [sdfix: what it checks and
> repairs](14a-sdfix-checks-and-repairs.html)). This page describes the program
> as fixed. A copy built before that day behaves as the old lines there say.

## The short version

```
back up the file, close it everywhere (or stop SD), then:
sdfix C:\ProgramData\SD\user_accounts\acct\orders      # a check; changes nothing
```

* **Take a copy of the file first, whatever the options.** The file is a folder
  holding `%0` and `%1` (and `%2` onward for indexes); copy the whole folder with
  `Copy-Item -Recurse`. `-F`, `-R` and `-Z` write into the file and none of them
  can be undone.
* **`sdfix` refuses a file that SD has open** (*run*): `File is currently open
  within SD`, `Status: 1`, and it reads nothing. It looks in the running SD's
  table of open files for the file's resolved path, ignoring case as NTFS does,
  so a different spelling, a junction or a trailing slash makes no difference,
  and it does so for every option, a plain check included. **It checks nothing
  when SD is not running**, and it cannot see a file held by another program,
  `sdidx` or `sdconv`. Close the file in every session, or stop the service
  (*Installation and the service* gives the commands).
* **A plain `sdfix file` is safe to run** on a file that nobody has open. It
  reads. The one exception is `-Z`, which writes (see below).
* **"Status: 0" does not mean the file is sound.** It means the program ran. A
  file full of errors still ends `Status: 0`.

## Where it is and who can run it

`C:\Program Files\SD\usr\bin\sdfix.exe`. Type that, or just `sdfix` if SD's
program folder is on the system PATH (`append.sd.path`, in the remote access
page of this set). The program opens the file's subfiles for read and write:
**you need write access to them**, even for a check. Without it the file is
reported as *No SD hashed files found matching given name(s)* (*run*: a copy
whose `%0` was marked read-only), which is easy to misread as "not an SD file".
Inside an account the users with the right are the account's own SD user (`sdu_`
and the account name), Administrators and SYSTEM (*run*: `icacls` on an
account's folder).

The files `-R` writes (a new overflow subfile, `%1`, renamed into place) take the
permissions of the folder they are in and belong to whoever ran the program
(*run*: after `-R` inside an account the file's permissions and owner were
what they had been). The account's own user keeps its access.

It reads the configuration file named by the environment variable `SD_CONFIG`
or else `C:\ProgramData\SD\sd.conf`, and **stops with "*path* not found" if it
cannot read it** (*run*). The only item it looks at is `DEBUG` (see Interactive
mode).

## The command line

```
sdfix {options} pathname ...
```

A pathname is the file's folder, as a Windows path, not an SD file name and not
a VOC entry. Options start with `-`, may be joined in one word (`-BF`), and are
not case sensitive. Several files may be named; each is processed in turn. A
path that is not an SD hashed file is skipped, with only the line `SDFIX
processed: name   Status: 1`, and if none was found the program says *No SD hashed
files found matching given name(s)* (*run*).

| Option | What it does |
|---|---|
| `-C` | Check the file. This is the default when no other mode is given. |
| `-F` | Check, and **fix every error it knows how to fix, without asking.** Not combinable with `-Q`. |
| `-Q` | Check, and **ask `Fix?` at each error it knows how to fix.** Answer `y` or `n`. Not combinable with `-F`. |
| `-R` | Recover disk space: shrink the primary subfile and rewrite the overflow subfile with the free blocks squeezed out. **Not combinable with `-F` or `-Q`** (*run*): `-r cannot be combined with -f or -q: run the fix first, then -r on its own`, status 1, and the file is not touched. Add `-C` or `-Z` to make it check first. |
| `-Z` | Clear the dead space at the end of each group (implies `-C`). **Writes to the file.** |
| `-B` | No progress bar. Use it when you log or redirect, since the bar is drawn with carriage returns. |
| `-V` | Verbose. Changes the output of `-R` only (a line for every block it moves); it does nothing to a check. Not listed in the usage text. |
| `-L` | Log everything the program prints, except the banner, to `sdfix.log` in the current folder. |
| `-Lname` | The same, to the file `name`. The rest of the word is the name, so put `-L` last in a joined word (`-BLcheck.log`). An existing log is overwritten. |
| `-I` | Interactive mode. Refused unless the configuration file sets `DEBUG` with bit 2 on. Not listed in the usage text. See below. |

The usage text printed for a bad option names only `-F`, `-L`, `-Q`, `-R` and
`-Z`; `-B`, `-C`, `-V` and `-I` work but are not listed. *Run.*

**Exit status.** The program's status is 0 if every pathname could be processed
and **1 if any of them could not**: it was not a hashed file, was open in SD,
could not be opened, had a path too long for its index subfile names, or its
overflow subfile had a wrong magic number (*run*: a missing file followed by a
good one ended 1, and the good one was still checked). Finding and even fixing
errors gives 0. Each file also prints a line ` SDFIX processed:  name   Status: n`.

**A path of 252 characters or more is refused** (*run*): `The path is too long:
the name of the last index subfile does not fit in 255 characters`, `Status: 1`,
and nothing more is read. The check looks for index subfiles under all 32
possible names, and with a path this long the names of AK 8 and up do not fit.
(Windows itself will not make a folder of that length without long paths
enabled; an account's files are nowhere near it.)

### Paging, and what happens when input runs out

Output stops every 24 lines with *Press return to continue...* (*run*; the
program reads standard input one character; `q` quits, `s` stops paging). The
`Fix?` and *Dump and rebuild* questions also read standard input.

**If standard input ends while `-Q` is asking `Fix?`, the end of input is taken
as `n`** (*run*): the program prints `Fix? N (end of input)`, repairs nothing, and
carries on with the check without waiting for any further answer. At the *Press
return* pause the end of input means "stop paging". To answer the questions from a
script, pipe the answers, one character each: `'Y' | sdfix -B -Q file` repaired a
file and `'N' | sdfix -B -Q file` did not (*run*, PowerShell; the line end it adds
does no harm). PowerShell has no `<`: for "input that ends" use `$null |
sdfix ...` or `cmd /c "sdfix ... < NUL"`. If the output is long enough to page,
start the answers with `s`.

## A check, with nothing wrong *(run)*

```
> sdfix -B C:\sdi_demo\plain
[ SDFIX W1.1-3   Copyright, Ladybridge Systems, 2007.  All rights reserved. ]

Processing C:\sdi_demo\plain
Checking file header...
Checking data groups...
Checking free chain...
Checking for unreferenced blocks...
0 overflow blocks allocated, 0 on free chain
 SDFIX processed:  C:\sdi_demo\plain   Status: 0
```

Without `-B` a row of asterisks, the progress bar, is redrawn on one line (with
carriage returns) after *Checking data groups...*. A file that has indexes adds
*Checking AK 0*, *Checking AK free chain* and *Checking I-type chain*.

## Fixing errors *(run)*

A scratch file was damaged so that its minimum modulus and its header record
count were wrong. A check reports them and changes nothing:

```
Minimum modulus is invalid (1645215744)
Record count error: Actual 000000000040, file header (adjusted) 000117440511
```

With `-Q`, answering `n` and then `y`:

```
Minimum modulus is invalid (1645215744)
Fix? N
Record count error: Actual 000000000040, file header (adjusted) 000117440511
Fix? Y
   Corrected by updating header
```

The first error is still there on the next run; the second is gone. `-F` does
the same for every error, with no questions (`Corrected by resetting to 1`). Which
errors can be fixed, and how, is on the next page of this set, [sdfix: what it
checks and repairs](14a-sdfix-checks-and-repairs.html). That page also covers the
dump-and-rebuild of mis-hashed groups, interactive mode, and the faults in the
tool that were found while writing these pages and fixed.

## Recovering space with `-R` *(run)*

A file that once held 3,000 records and now holds 305 keeps all the disk it
grew to: `%0` was 2,668,544 bytes and `%1` 1,247,232.

```
> sdfix -B -R C:\sdi_demo\big
Processing C:\sdi_demo\big
Recovering space
Overflow subfile contracted to 231424 bytes
 SDFIX processed:  C:\sdi_demo\big   Status: 0
```

Afterwards `%0` was 432,128 bytes and `%1` 231,424, and a check was clean. The
file was put back in an account and read through SD: `COUNT` found the 305 records
and a `SELECT` found the five long ones.

**`-R` rewrites the file in place and is the most dangerous option.**

* It first empties the file's free chain in the header, then rewrites the
  primary subfile's links group by group. From that point the old overflow
  subfile no longer matches the primary subfile. If the run stops part way (a
  full disk, a kill, a power cut) the program says *The original file is no
  longer usable* if it notices, and **the only remedy is your copy.**
* It does not touch the index subfiles. The source says they were too hard to
  shrink, so an indexed file keeps its index sizes.
* It does not check the file first unless you also give `-C` (or `-Z`), and
  `-F` and `-Q` are refused alongside it. **Run a check, and `-F` any errors in
  a separate run, before you recover space**, not after.

## Clearing dead space with `-Z` *(run)*

When a record is deleted or shortened, the bytes after the used part of a block
keep their old text. `-Z` zeroes them. It does not change a record. It makes a
file compress better and stops old text lingering in a backup, and the file
works the same without it.

```
> sdfix -B -Z C:\sdi_demo\big-z
...
Dead space cleared in 7 block(s)
...
> sdfix -B -Z C:\sdi_demo\big-z
Dead space cleared in 0 block(s)
```

It walks the groups in the primary subfile and the overflow blocks chained from
them. It does **not** clear free overflow blocks (those on the free chain), and
it does not visit the blocks that hold a large record's data (source, not
provoked). Unlike a plain check it **writes**, so back up and close the file
first, as for `-F`.

## Writing it down

Give `-L` when a run matters, so there is a record:

```
sdfix -B -F -Lfix-20261019.log C:\ProgramData\SD\user_accounts\acct\orders
```

The log has everything but the banner and the progress bar, and the lines
` SDFIX processed:  name   Status: n`. *Run*: `-Lfix-demo.log` made that file in
the current folder.
