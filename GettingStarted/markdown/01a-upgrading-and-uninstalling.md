Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html).

## Upgrading

**Installing a new release over an existing one updates your database.**

| Replaced | Kept, and not touched |
|---|---|
| the catalog and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalog |
| the messages and include records | which Windows users are linked to which SD accounts |
| the VOC templates and library routines | the commands each account may run |
| the SDSYS `BP` programs | your print queue and held reports |
| terminfo, the license, the contributor list | everything under your own accounts, and `sd.conf` |

Anything SD created while it was running — your VOC included — is left exactly
as it is.

**The dictionaries are brought up to date for you.** Upgrading reapplies the
dictionary definitions the release ships: it adds and updates the entries SD
ships and leaves alone any you added. If that step cannot run, the installer
says so at the end rather than finishing quietly, and `upgrade-dicts.log` in
`C:\ProgramData\SD` says what happened.

**Every account's VOC is brought up to date for you.** The installer runs
`update.accounts all`, which walks every registered account, so a command this
release adds can be typed in accounts that already existed.
**Your files are converted to case-insensitive record ids for you.** Every
file `create.file` makes now treats ids as one whatever the
case (see [Lower case](11-lower-case.html)), and an upgrade keeps your existing
files, which were built case sensitive. So the upgrade walks every registered
account, **naming each one as it goes** (*Account fred*), reads each file its VOC
names first, and converts it only if no two of its ids differ only by case, so a
conversion cannot lose a record. **`nocase-upgrade.log`** in `C:\ProgramData\SD`
holds the whole walk. A file is **left exactly as it was** and named in the log when:

- it holds two ids that differ only by case (rename or delete one of each pair);
- it has alternate key indexes (*File has indices, so convert it by hand*);
- it lies outside its account's directory, or under SDSYS (the log says how many,
  and each is converted by its owner with `configure.file no.case`);
- its work file could not be made or cleared (the file is named, so it can be
  found).

**SDSYS's own files are left as they are**: the walk does not go into SDSYS at all.
When any file was left, the installer's closing box says so
(*Some files were not converted to case-insensitive record ids*, with the log's
name) and the step ends with a warning, not a failure; a file that could not be read
or rebuilt is a failure and the box says so. Whatever was left keeps working: ids are
still found typed in any case.

**The parameters SD no longer has are taken out of a kept `sd.conf` for
you.** SD refuses to start on a name it does not recognize, so when you install
over a kept `sd.conf`, the installer removes each line that names a parameter
this release dropped (`APILOGIN`, `CODEPAGE`, `CREATUSR`, `EXCLREM`,
`FILERULE`, `FIXUSERS`, `GDI`, `INVCASE`, `JNLDIR`, `JNLMODE`, `PORTMAP`,
`RINGWAIT` and `TXCHAR`) before anything starts SD, and writes which to the
installer's own setup log. A configuration file you copy in by hand from an
older installation needs the same done to it; see *Configuration* in the
Administrator set.

To refresh one account by hand afterwards, `update.accounts` in that account
updates it and offers the rest.

Two limits are worth knowing before you rely on it.

> **The VOC update removes only what is on SD's deletion list.** A record
> that a release withdraws is taken out of an account only if it is on the
> list and is still the record SD shipped, and a copy is saved first
> (`restore.voc` puts it back). Anything else the update leaves alone, and a
> record you marked `[locked]` is kept — a locked verb excepted.

> **A record you have customized can be held back on purpose.** Put `[locked]`
> in field 1 after the type code and the update leaves that record alone,
> naming it in a message so you know what was withheld — and therefore which
> corrections this release made that you have not taken. Verbs are the
> exception: a locked verb is updated anyway, and you are told which. The
> administrator documentation covers it under *Accounts and security*.

### An upgrade keeps what accounts could do with the shell and the operating system

**A new account now starts with `sh` and `OS.EXECUTE` off** (the `sh-on` and
`os-on` switches), and so does the right to save a change to a VOC, a program file
or a dictionary (`voc-on`, `bp-on`, `dict-on`). But accounts made before those
switches existed have always had all of it, so when you kept your accounts the
installer copies the old `os.users` list into the switches, **once**, and switches
the three edit switches on for every user account; ssh and the API are left as
they were. Turn any of them off for an account whenever you like with
`modify.account` *name* `sh-off` / `os-off` / `voc-off` / `bp-off` / `dict-off` —
**a later install does not turn them back on.** Accounts you make after the
upgrade start with everything off. The Administrator set's *Installation* page
has the details, including what to do if the installer says it could not carry
them forward.

**The installer makes the `shared` account** (a group account whose data files
every account can open by file name; see [Accounts](05-account-types.html#the-shared-account)),
just after the account for the installing user and before the accounts you kept are
brought up to the release. If you kept your accounts, the one you had is kept. Every
account, new or existing, can read the `shared` account's files and none can write them,
until SDSYS says otherwise with `shared-read-off` and `shared-write-on`; nothing is
written to your existing accounts for that.

**The installer stops, before it changes anything, if an account named `shared`
already exists that is not SD's own.** The name is reserved. It names the account's
register record, and you rename that account by hand and run the installer again.

### Setup refuses a data folder that has a system folder and no accounts

If `C:\ProgramData\SD` holds a `sdsys` folder but its account register
(`sdsys\accounts`) has no account in it, an earlier install or removal did not
finish, and installing over it would make no accounts and report success. Setup
stops before it copies anything and says so: *"The data folder ... has a system
folder and no accounts, so an earlier install or removal did not finish."*
**To correct it, delete `C:\ProgramData\SD`, or restore it from a backup, and run
setup again.** A machine with no data folder, and a folder with at least one
account, are not affected.

A plain delete can stop on `C:\ProgramData\SD\ai\keys`: that folder is locked to
the AI service and SYSTEM, so even an administrator is refused. Take ownership
first, in an **elevated** PowerShell:

    takeown /f C:\ProgramData\SD /r /d y
    icacls C:\ProgramData\SD /grant *S-1-5-32-544:(OI)(CI)F /t /c /q
    Remove-Item C:\ProgramData\SD -Recurse -Force

`*S-1-5-32-544` is the Administrators group.

## Uninstalling

It is the standard Windows uninstall — Settings ▸ Apps, or `unins000.exe`.

**The default does not touch your accounts, the database or the
configuration.** Inno removes only what it installed and only removes a
directory if it is empty, so everything the running system created is invisible
to it.

**Removing the data is a separate, opt-in prompt** that defaults to keeping it,
and says exactly what it destroys and where. **A silent uninstall never
deletes the database**, whatever the prompt would have offered.

**The administrator's scheduled jobs are removed either way**: every SD task
in Task Scheduler and its definition, since a task left behind would name a
program that is gone.

**The uninstaller does not remove OpenSSH.** It may predate SD or be in use by
something else. It does restore `sshd_config`, keeping the original as
`sshd_config.before-sd` — but it deliberately does **not** widen the firewall
rule back, because restoring it would mean opening a port on the way out.

**The uninstaller removes the SD Core API's own firewall rule, and a reinstall
puts it back as it was if you kept `sd.conf`.** Before the rule goes, the
uninstaller notes whether it let other computers in (one value in the registry,
`HKLM\SOFTWARE\SD\SetupNotes`, which only an administrator can write). If it did,
and `sd.conf` is still there with the API switched on, the next install makes
that open rule again, and says so on the closing page. **An API that was closed
stays closed.** The note is removed by that install, and by any uninstall that
leaves no `sd.conf`; a silent uninstall keeps `sd.conf` and so keeps the note.
Change the setting at any time with `remote.api`.

**A reinstall over a kept `sd.conf` does not ask who may reach ssh.** The three
"let other computers on your network connect to this one over ssh" boxes are not
shown. An ssh server that was already here keeps its firewall rule exactly as it
was: open stays open, closed stays closed. A server the install adds itself is
reachable from this computer only, as on a new machine; `remote.ssh` changes it
afterwards. The "Install the OpenSSH server" box is still shown, and ssh is
still limited to SD's accounts.

## Continued in

[Your first thirty minutes](02-first-run.html) — install to a second user
signing in, in eight steps.

[Differences from W1.0-0](01b-differences-from-w1-0-0.html) — everything
that changed since the previous release, and what an upgrade might break.
