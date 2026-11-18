# SD Core for Windows - documentation

The documentation of **SD Core for Windows**, written in Markdown. The server
source is in the separate `SDCore4Windows` repository; nothing here is needed to
build SD, and nothing there is needed to build these pages.

## What is here

Five sets of documents, each in a `markdown/` folder (the source); the `html/`
and `pdf/` folders beside it are generated.

| Set | For | Contents |
|---|---|---|
| `GettingStarted/` | everyone | installing SD Core on Windows, running it, accounts and security, what differs from OpenQM and from SD Core for Linux, and moving programs over from other MultiValue databases |
| `User/` | programmers and users | SD BASIC by subject, SD TCL by subject, the VOC and dictionaries, files, standard subroutines, the client API, the terminal screen library, a tutorial with worked programs, the glossary and the generated syntax cards (`94` SD BASIC, `95` SD TCL) |
| `Administrator/` | the administrator | accounts and access gates, sessions and locks, operating system access, encryption, remote access, system limits, configuration, installation and the service, the installed scripts, restricted commands, known limits, SDNet, the shared account, the master files, the `sdfix`, `sdidx` and `sdconv` tools, moving an account to another machine, giving an AI agent an account of its own, the AI helper, the audit trail, remote administration over ssh, and scheduled jobs. Everything in it is administrator-only or unavailable to an application, so an administrator can withhold the whole set |
| `TUIGuide/` | programmers, from the administrator's documents | *SD Text User Interface - Programmer's Guide*: building a full-screen page of your own in SD BASIC with the public `!tk` routines and `tkpub.h` - the shape of a program, the window and its floor, the key table and menus, the finder, the confirm box, the form, the pick lists, the output pane, and how a page uses the `screen` statement with the routines - with five worked example programs and a reference of every routine. A document of its own, with its own page numbers and its own book |
| `Changes/` | everyone upgrading | what was added, changed and removed in this version, by area |

The sets do not link to each other, because each is handed out on its own. Where
a page in another set is worth naming, it is named in words.

### Page numbers

A number with a letter after it is the second half of a long page (`04` and
`04a`); pages are kept to about 14,000 characters so a reader moves between
pages rather than scrolling through one. `00a` is the copyright and license
page, which comes first in every set; `00b` is the introduction. The syntax
cards sit at the end (`94` and `95`) so they can grow without renumbering
anything.

The copyright and license block appears in full once per set, on `00a`; every
other page carries a one-line footer with the product, version, copyright and
license name.

## Reading the pages

`start-docs.cmd` serves the pages on `http://localhost:8123/` and opens
`index.html` in a browser (it needs Python; close its window to stop it):

```
start-docs.cmd
```

## Building the HTML

From the root of this repository, in PowerShell:

```
pip install markdown
python tools\mkdoc.py --in GettingStarted\markdown --out GettingStarted\html
```

`tools\mkdoc.py` renders each Markdown page to one self-contained HTML file (the
style is embedded, so a page can be copied anywhere). `tools\add_nav.py` adds the
previous/next links and checks that each set has its license page first, and
`tools\mkbook.py` joins a set into one book. `tools\mkpdf.ps1` makes the PDF of
a rendered page and needs Edge or Chrome, which every supported Windows machine
has. The generated pages are not tracked; the Markdown is the source.

`tools\release.ps1` does all of it for a release: it renders whatever changed,
refuses if any generated page is older than its Markdown, and zips the result
(`-Set` does one set, `-Force` renders everything, `-NoZip` stops before the zip).

The syntax cards are generated from SD itself and are not edited by hand:

```
python tools\mksyntax.py <SDCore4Windows>\sdb_ai\sd64\sdsys\gpl.bp\bcomp User\markdown\94-sd-basic-syntax.md Administrator\markdown\10-sd-basic-restricted-commands.md
python tools\mktclsyntax.py <SDCore4Windows>\sdb_ai\sd64\sdsys User\markdown\95-sd-tcl-syntax.md
```

`tools\checklinks.py`, `tools\docmap.py` and `tools\tclmap.py` check the links
and that every SD BASIC name and TCL verb is documented.

`tools\` also holds the PowerShell programs (`sdtcl.ps1`, `sdprobe.ps1`,
`sdprobe2.ps1`, `sdcompile.ps1` and `sddebug.ps1`) that run something inside a
real SD session, with the BASIC they run in `tools\probes\`; they are how the
pages were measured and are not needed to read or build them.

## License

See `GettingStarted/markdown/00a-copyright-and-licence.md`.
