Title: SD Core for Windows - Introduction and Getting Started
Subtitle: What a multivalue database is, what SD is, the four components, and your first session.

This page orients you to SD Core for Windows: what a multivalue database is,
where SD came from, what the pieces are, and how to take your first steps. It
is the only page in this set that assumes nothing.

## What is a multivalue database?

A multivalue database stores data in records made of **fields**, where
each field can hold **more than one value** — and each value can hold
**more than one subvalue**. A single field in a customer record can
therefore carry every phone number the customer has, without a separate
table or a join.

The model was designed by Dick Pick in the 1970s as the Pick Operating
System. It has been through PI/open, UniVerse, Unidata, D3, jBASE,
QM, and ScarletDME — and SD is one of its direct descendants.

The three delimiters that make it work are **field marks**, **value
marks** and **subvalue marks** — control characters that separate the
levels inside a single string. A dynamic array in SDBasic is a string
that carries these marks, and the angle-bracket forms (`a<f,v>`), `ins` and
`del` work on them directly.

## What SD is

SD Core for Windows is built from upstream `sdb64`, a MultiValue database
with elements found in the main SD version and in ScarletDME. ScarletDME
was a fork of the original GPL release of OpenQM 2.6.6.

**That lineage matters when you go looking for documentation.** Not all
the features of the *commercial* OpenQM 2.6.6 were in the GPL release,
and no documentation specific to the GPL version was ever released. The
OpenQM 2.6.6 documents can be used as a reference, but SD Core has
additions, changes and deletions — of features, of structure, of
security and of commands. This documentation set covers those changes.

If you have used OpenQM, or upstream `sdb64`, much of SD Core will still be
familiar: the same data model, the same query processor, the same
BASIC.

**SD Core for Windows is Windows only.** SD Core for Linux is a separate
product, built to behave the same way for the people who use it, and this
is not a build of it.

SD Core is free software under the GNU General Public License v3. `config gpl`
displays the license and `config contrib` the list of contributors. The
installer carries compiled binaries; the source is a separate download.

## The four components

| | |
|---|---|
| **The command processor (TCL)** | reads what you type at the `:` prompt and dispatches it to a verb, a program, a paragraph or a query |
| **The query processor** | runs `list`, `select`, `count`, `sort` and the rest — the reporting language |
| **SDBasic** | the programming language: a compiled BASIC with dynamic arrays, file I/O, and the multivalue string functions |
| **The SDClient API** | a C client library (`sdclilib.dll`) that lets an external application connect to SD, read and write records, execute commands and call subroutines |

## Signing in

```
sd
```

You land in **the SD account with your own name**. Nothing asks for a
password — Windows has already authenticated you. SD asks Windows who
you are.

If `sd` answers *Account ... not in register*, you are in the wrong
account or your group membership has not taken effect yet. If it
answers *not registered for SD use*, you are not in the `sdusers`
group.

> **You must sign out and back in after being added to `sdusers`.**
> Windows fixes group membership when you sign in. Until you get a new
> logon token you cannot read the data tree at all, and the symptom
> looks like a broken install.

SD is already running. It is a Windows service — **String Database (SD)**
— and Windows starts it at every boot. You do not type `sd -start`.

## Your first file and record

```
create.file customers
ed customers 1001
```

`ed` is the line editor, and it needs nothing installed. In `ed`: `i`
to insert, type your lines, a full stop on its own line to stop
inserting, then `fi` to file and exit.

`sed` is a full-screen editor that runs inside SD, with drop-down menus and
color for SD BASIC that you turn on when you want it; any account may use it.
An account can also use `edit` (Microsoft Edit, a full-screen editor) or
`micro` (a full-screen editor with syntax highlighting) once the administrator
has given it the `os-on` switch; a new account does not have it.

```
list customers
count customers
```

Commands are lower case now. Typing `LIST` still works — SD tries what you
typed, then lower case, then upper, and finally with any hyphens changed to
dots, so `clear-select` reaches `clear.select` too.

## Writing a program

A program lives in a `bp` file — a directory file, which is an ordinary
Windows folder with one file per program. You can write it in `ed`,
in `edit`, in `micro`, or in any text editor you like (Notepad, VS Code,
etc.) — the folder is on disk at:

```
C:\ProgramData\SD\user_accounts\<account>\bp
```

A new account must be given `bp-on` by SDSYS before it can save a program in
`bp` or compile it, and `os-on` as well before it can use `edit` or `micro`.

Compile and catalog it from inside SD:

```
basic bp myprog
catalog bp myprog
```

Then run it by name:

```
myprog
```

## Becoming an administrator

**There is no `logto` route to it.** SDSYS, the one administrator account,
is reached only by signing in to Windows as the `sdsys` account itself and
starting `sd` elevated — a fresh session, not a command typed from inside
one you already have. `logto sdsys` is refused outright to every other session,
whatever its elevation; only a session that started in SDSYS can use it, to
come back from an account it visited.

**This needs the console, or a remote desktop or remote-control product
installed as a service** — something Windows can draw a UAC consent prompt
on. Over an ordinary ssh session there is no such screen, and in any case
SDSYS itself has no ssh route to arrive over.

## What is not in SD Core for Windows

The following were in OpenQM, in ScarletDME, or in upstream `sdb64`, and
are not in SD Core for Windows:

| Gone | Why |
|---|---|
| The old SDNet (`server;file` in a VOC entry) | Not provided, and a name with a semicolon in it stays unresolved. SDNet takes its place: it is off until the administrator turns it on, and it opens a file on another SD server through an `N` entry in the VOC (the *Administrator* set's *SDNet* page describes it). The API is the other way to reach another SD server |
| Embedded Python (a Python interpreter loaded into `sd.exe` itself) | Gone permanently - `sd.exe`'s MSYS2 runtime cannot safely share a process with Python. Calling Python **from** a BASIC program is not gone: it runs as a separate helper process instead - see *SD BASIC - Python Integration* |
| `sdlnxd` daemon | Linux-only; the Windows service replaces it |
| `ENCRYPT.FIELD` verb | Removed; `sdencrypt()` and `sddecrypt()` in SDBasic, with `sdkey()` for the key, and the `XE` conversion are the supported route |
| `update.record`, `modify` editors | Gone; use `sed`, `edit`, `micro` or `ed` |
| PROC language | Removed; use paragraphs instead |
| `SET.LANGUAGE`, `LOAD.LANGUAGE` | Removed; SD Core is English only (NLS, for currency and separators, is kept) |
| Unattended install | Not supported; the installer asks questions and sets passwords that cannot be scripted around |
| Multi-user Remote Desktop | Not supported; accounts SD creates are denied the console and RDP |

## Document conventions

| | |
|---|---|
| **bold** | a word typed as it stands |
| *italics* | something you supply |
| braces `{ }` | an optional part |
| `code` | a command, a function name, or something you type |
