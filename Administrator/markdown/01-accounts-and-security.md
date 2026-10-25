Title: Accounts and Security
Subtitle: Making and changing accounts, passwords, and who may enter an account.

These are the verbs that decide **who may use this installation and what
they may do with it.** They are SDSYS's set — not in any other account's
VOC at all — and almost all of them need more than the verb before they
will do anything.

> **This document is separate so that it can be withheld.** Everything in
> the administrator set describes verbs an ordinary account does not have
> and cannot run. It is a complete set on its own and **links to nothing
> outside itself**, so that handing somebody the user documentation without
> this never leaves them at a page that is not there. Where a user-set page
> is worth naming, it is named in words rather than linked.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Read this before anything else: being SDSYS is the whole of it

**Having the verb is not having the right to use it — but there is only one
gate now, not two.** SD Core used to check a VOC tier and elevation
separately; the tier is gone. Every verb on this page is refused outright
to any session that is not actually SDSYS, whether or not that session is
elevated:

```
:list.grants don
Command requires administrator privileges
:delete.account sdsys
Command requires administrator privileges
:modify.password sdsys
Command requires administrator privileges
```

**Every one of those refusals came before the command was looked at.**
`delete.account sdsys` would have been refused anyway — you cannot delete
`SDSYS` — and it never got that far.

**Being SDSYS means having signed in to Windows as the account named
`sdsys`**, made once by the installer, and nothing else. Being a Windows
administrator grants nothing by itself — an elevated session in an ordinary
account is still an ordinary account. **Start SD by signing in to Windows
as SDSYS and running it elevated.** The three verbs on this page that do
*not* require this are `clean.account`, `config` and `update.accounts`, and
each of them acts only on the account you are already standing in or on
your own session.

## Making an account: `create.account`

```
create.account user <name> {ssh | api | both | none} {sh-on} {os-on} {voc-on} {bp-on} {dict-on}
                           {net-on} {files-on} {files-write-on} {files-admin-on} {shared-read-off} {shared-write-on} {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

| | |
|---|---|
| **`user`** | an SD account **and** a Windows local account to sign in as |
| **`group`** | a shared workspace with no Windows account, reached only with `logto` |
| **`other`** | an SD account over a directory you name |

**A new user account starts with every door shut** (but one: it can read the
files of the `shared` account, [The Shared Account](13-the-shared-account.html),
and not write them). Say nothing and it has no ssh, no API, no `sh` and no
`OS.EXECUTE`, it cannot save a change to a VOC, a program file or a
dictionary, it has no right to use a server defined for SDNet, and no
files-only login; you open each one by naming it. `ssh`, `api` or `both` give
the remote routes (`none` is the default and is accepted so that a script can
say so); `files-on` gives the narrower files-only API route (below, *The
files-only route*); `sh-on` and `os-on` give the two operating-system switches,
and they are independent, so `sh-on os-on` gives both and neither cancels the
other; `voc-on`, `bp-on` and `dict-on` give the three edit switches (below),
each on its own; `net-on` gives the SDNet switch (below). Two words go the
other way, because the `shared` account is open to every account unless you say
otherwise: `shared-read-off` takes away the right to read its files and
`shared-write-on` gives the right to write them. (The two words that restate the
defaults, `shared-read-on` and `shared-write-off`, are for `modify.account`
only.) **This is the setting SD is delivered with, on purpose: it is the
tighter one, and you loosen it for the accounts that need it, one at a time** —
the same words change an account later in `modify.account`, below. (Before 25
October 2026 a new account was given both remote routes and the person's shell
came from a file, `os.users`; neither is so now.) When it has made the account
SD says where it stands:

```
fred has no remote access: not ssh, not the API
Account fred has SH no, OS.EXECUTE no
Account fred has VOC.EDIT no, BP.EDIT no, DICT.EDIT no
Account fred has NET no
Account fred has files no
Account fred has shared.read yes, shared.write no
```

(Two more lines, for `files-write` and `files-admin`, follow the `files` line;
the remote-route line is the one for the words you gave.)

**A group account and an `other` account have no Windows user of their own,
so `sh-on` and `os-on` are refused for them** — "is a group account and has
no Windows user, so it has no shell to permit". A shell is a fact about a
person, and a group account is not one.

> **It prompts for a password and `no.query` does not suppress that.**
> `no.query` covers the confirmation, not the credential — a password is
> never an argument anywhere in SD. **`create.account user` therefore
> cannot be driven from a script**, and a group account, which has no
> password, can.

**Every account gets the same VOC**, the whole of `newvoc` — there is no
tier to choose at creation. What differs from one account to the next is what
it is *allowed to do* with the verbs it has: its remote routes and its
switches are per-account settings, all off until you turn them on (the exception
is reading the shared account). **SDSYS is the exception and it is not a
setting** — it is never refused by these switches.

**The audit trail records what was granted.** The line `create.account` writes
ends with `gates=`, the words of the sentence that grant or withdraw an access,
in the program's fixed order, or `gates=none`:

```
create.account account=FRED type=user gates=ssh,api,sh-on
```

(The words up to `type=` are as they always were; the account name is in upper
case here.)

### Two settings that are easy to conflate

| | |
|---|---|
| `ssh`, `api`, `files-on` | say who may **connect**, and by which route |
| `sh-on`, `os-on` | say who may reach the **operating system** |

Holding the first has never implied the second. They are independent
settings and are checked in different places. **ssh alone does not give a
shell**: every ssh session is forced into `sd`, so what the person can do is
what SD lets them do — and an account without `sh-on` gets no shell from SD.

### The operating-system switches: `sh-on` and `os-on`

Two independent switches, kept per account in the register (fields 7 and 8).
**Both are off for a new account** and SDSYS turns each on with `modify.account`
(below). An account with neither is still a full SD user: it runs programs,
opens every file its VOC names, builds indexes, runs queries — everything that
stays inside SD.

| | |
|---|---|
| **`sh-on`** · `sh-off` | the `sh` verb and `!` (see [Operating System Access](03-operating-system-access.html)) |
| **`os-on`** · `os-off` | `OS.EXECUTE` in a BASIC program, the screen editors `edit` and `micro`, the embedded Python, **and reaching an operating-system file or directory by its path outside the account's own directory** |

**This changed on 25 October 2026.** The grant used to be a record in the file
`os.users`, keyed by the Windows login name, so it followed a person into every
account they entered; it is now two fields of the account's own record, so it
follows the account, and `os.users` is no longer read. And the limit on paths
used to bind only a session that arrived over the network: **a person at the
console is held to it now too.**

That last clause of the table is the one that is easy to miss. Without
`os-on` an account can still open every file it reaches **through its VOC** —
dictionaries and other SD files included — and anything inside its own
directory, **provided the VOC pointer leads somewhere it may go** (see *VOC
pointers*, below). What it cannot do is name another account's directory, the
system directories, or a path that climbs out of its own with `..`, in any of
these:

| | without `os-on` |
|---|---|
| `OPENSEQ` and `OPENPATH` with a path | status 3035, so `OPEN ... ELSE` works as before |
| `DIR()` and the `select.dir` verb | refused (the verb says why) |
| `DELETESEQ` of a bare path | refused; the file is left alone |
| printing into a file by path (`setptr ... as pathname`, `SETPU`, or a `$hold` print name that climbs out with `..`) | refused |

`..` is resolved before the test, so it does not get round it, and a path inside
the account's own directory always works. Three more places are open to an
account without the switch: the shipped SDSYS entries that every VOC names
(**read only**) and the directories the administrator listed in `NETDIRS`
(read and write; see [SD Admin Configuration](07-sd-admin-configuration.html)).

**SD says no in words.** `sh` gives "*name* is not permitted to use the
operating system shell", `OS.EXECUTE` gives "*name* is not permitted to use
OS.EXECUTE", and the path routes give "*name* has no OS access, so a file or
directory outside its own account cannot be reached by pathname (SDSYS can give
it: `modify.account` *name* `os-on`)" (message 12185). **SDSYS is never
refused.**

**The upgrade keeps what the old file said.** The installer's `upgrade_gates`
step copied, once, what `os.users` said about each user account's Windows user
into that account's two fields (`yes` for `yes`, `no` for anything else and for a
user with no record; group and other accounts are left blank, which reads as
no), and fills only a field that is blank, so an administrator's later `sh-off`
is not turned back on by the next install. The file stays on disk, unread.

### The third switch: `sd-on`, other SD accounts' directories

`os-on` is wide: it reaches any path. `sd-on` is the narrow version, for an
account that has to read or write the **data** of a neighbouring SD account
(a shared reports folder, a hand-over directory) without being given the
whole machine. It is **off for a new account**, and `modify.account` *name*
`sd-on` / `sd-off` turns it on and off. It may be set on a group account
(`sh-on` may not).

With `sd-on`, the path routes in the table above also accept a path under the
directory of any SD account **the user could `logto`**: the account's Windows
group (`sdu_`*name* or `sdg_`*name*) is one the user belongs to, and the
account is not suspended. Reading and writing are one switch. Two things stay
shut:

- **The other account's VOC** (`voc`, `voc.dic` at the top of its directory)
  is never reachable this way; the account's own VOC is, as always.
- Any directory that is not an SD account's still needs `os-on`.

**SDSYS is not affected** — it is never refused. `os-on` implies `sd-on`.
The setting lives in field 9 of the register record and is not carried by an
account archive, so a restored account starts with it off.

### The edit switches: `voc-on`, `bp-on` and `dict-on`

Three more per-account switches, in fields 10 to 12 of the register record,
say whether the person who signed on to the account may **save a change** to
a VOC, to a program file, and to a dictionary. Reading is never stopped. **All
three are off for a new account**, and `modify.account` *name* `voc-on` /
`voc-off`, `bp-on` / `bp-off` and `dict-on` / `dict-off` turn each one on and
off. `create.account user` takes `voc-on`, `bp-on` and `dict-on`. After a
change SD says where the account now stands (if the switch already had the
value asked for, SD says only that the account already had that access and
that nothing changed):

```
:modify.account fred bp-on
Account fred has VOC.EDIT no, BP.EDIT yes, DICT.EDIT no
```

**Which files.** A file is known by the name of the file that is **open**, not
by the name that was typed, so a Q-pointer to somebody's VOC is caught:

| | |
|---|---|
| **a VOC** | a file called `voc` |
| **a dictionary** | any file whose name ends in `.dic`. `voc.dic` is the dictionary of the VOC, so it is a dictionary, not the VOC |
| **a program file** | `bp`, `bp.out` (the object code), or any name ending in `.bp` or `.bp.out`; the private catalogue directory (`cat`, or whatever `$private.catalogue` names) counts as one |

Capitals do not matter.

**What stops.** A program's `WRITE`, `WRITEV`, `DELETE` and `CLEARFILE` of
such a file is refused with a message that names the missing switch (messages
12410 to 12412), or sets the `ON ERROR` status. The verbs and statements that
change a file the person names ask the same question first, before they lock or
change anything, and give the reason: `sed`, `ide` and `ced` show it in their
message line, and every other verb prints it and stops. They are `ed`, `edit`,
`copy` and `copyp` into the file or moving records out of it, `delete`,
`clear.file`, `cname` of a record, `delete.file` of a program file or of a
dictionary on its own, `fixdir`, `format`, `map file`, `sp.view` (the X key that
deletes an item), `set.trigger` when it installs or removes a trigger,
`copy.list` into the file or with `deleting` from it, `delete.list ... in`,
`get.list ... deleting in`, `save.list ... in`, `sort.list ... from`,
`reformat ... to`, `list ... pageseq`, a delimited report written `to` a
pathname, `cd data`, `generate`, `como on ... in`, and the `.s` and `.d`
stack commands on an existing VOC record. `create.file` naming a file that
already exists (adding a part to a multifile, or converting a single file to a
multifile) is asked too; making a new file is not. `cname` will not take a
program file out of its name, or put a file under one, for a person without the
switch, so a rename is not a way round. `OPENSEQ` in such a place opens the file
for reading only and cannot create one; `DELETESEQ` and a print file made there
are refused. For these operating-system routes the name of the record or file
being made counts only when it is itself a directory or anything but a plain
file, so a plain file called `sample.bp` in an ordinary directory is not held
back, while a file inside the directory `bp` is. Over the API a client's
writes, deletes and file clears are held to the same rule.

**Compiling is held by `bp-on` too.** Without it `basic`, `catalog`,
`delete.catalog` and `decatalog` are refused (message 12413), because
compiling is how a source becomes code that runs: otherwise source could be
copied into any file and compiled there.

**`logto` does not change them.** The switches are those of the account the
person **signed on** to (over the API, the account first entered). A person
with a switch on keeps it in another account; a person without it does not
gain it there. A change takes effect the next time the person signs on. Unlike
`sh-on`, `os-on` and `sd-on`, the three edit switches are read at sign-on
only, not again at `logto`.

**What is not stopped.** What SD writes as a side effect of an ordinary
command — a new pointer made by `create.file`, a new saved sentence, a
compiled I-type, the command stack — and anything done from the shell by an
account that holds `sh-on` or `os-on`. The operating-system routes above
(`OPENSEQ`, `DELETESEQ`, print files) are not looked at for an account that
holds `os-on`, when the path is outside the account's own directory: `os-on`
already trusts it with the whole machine. The switches are about changing
these files by hand or by program, not a replacement for the operating-system
switches above.

**`$private.voc` and `$voc.parser` are not guarded by `voc-on`** when they
point at a file that is not called `voc`: the switches look at the name of the
file being written, so a private vocabulary called `zzpv` is an ordinary data
file, and an account with all three edit switches off could add and replace
commands in it once you had pointed `$private.voc` at it. Keep such a file where
only the people you mean can write it. The two records themselves are VOC
records, so writing one needs `voc-on`. (Linux ran this on 18 October 2026; it
has not been run on Windows. See the User set's page on the private vocabulary
and parser.)

**Internal programs run only from the global catalogue.** The gates on files
and on operating-system paths do not apply to a program compiled in *internal
mode*, which SD's own commands are. That mark is a bit in the program's own
object file, and SD used to believe it wherever the object came from, so a
user who could put an object file where SD would run it could set the bit and
skip every gate. SD now honours the bit only for an object from the global
catalogue, which only SDSYS can write, or for the administrator; for any other
object the bit is cleared when the object is loaded. SD's own commands are all
in the global catalogue and are unaffected; a program that SDSYS compiled in
internal mode into a user's account runs there as an ordinary program.

**SDSYS is never refused.** `modify.account` refuses SDSYS as a target, so
there is nothing to set for it.

**Group and other accounts.** The three words are accepted for a group or
other account. Because `logto` does not reload them, they decide only for a
session that signs on to that account itself. The upgrade leaves group and
other accounts off on purpose; where members need to save to a VOC, a program
file or a dictionary there, SDSYS gives it with `modify.account` *name*
`voc-on` / `bp-on` / `dict-on`.

**On an existing machine.** The installer's `upgrade_editgates` step switches
all three on, **once**, for every *user* account in the register whose field is
blank, so that no such account loses what it had; group and other accounts,
and accounts made afterwards, start with all three off. The installing user's
own account is made with all three off like any other. The switches are kept
in the account archive (`edit.voc`, `edit.bp`, `edit.dict`), but
`restore.account` gives them back only to an account it has to create; an
archive from before the switches existed carries none and gives none.

### VOC pointers: where a file pointer may lead, and which Q-pointers are followed

**A VOC pointer is a way to name a file, so it is held to the same rule.** An
account can write a pointer into its own VOC with `ed`, or make one with
`create.file ... pathname`, and a Q-pointer is what `set.file` makes into
another account. For everybody but SDSYS:

| | |
|---|---|
| **a file pointer (F-type)** | must lead **inside the account's own directory**, or be **the pointer SD itself put in the VOC** (the stock entries of `newvoc`). An account that holds `os-on` may go anywhere its Windows user can. Anything else is refused with status 3035 |
| **a Q-pointer** into a **registered account** | is followed only if the user **could `logto` that account**: a member of its Windows group, and the account not suspended — `logto`'s own test — **whether or not the account holds `os-on`** |
| **a Q-pointer** that **names a path** | is an operating-system path, and the `os-on` question |

So `set.file` into somebody else's account works only for a user who may enter
that account, and a hand-made pointer at a system directory or another
account's directory is refused unless the account holds `os-on`. A refused
open takes the `ELSE` branch with status 3035, like any other refusal here.
**SDSYS is never refused.** The accounts that existed at an upgrade hold what
`os.users` gave them (above), so an account that had `os-on` keeps its own
pointers; the Q-pointer rule applies to every account. The API's request 29,
"open an SDNet file", asks the same question of the account named in the
request ([SDNet](12a-sdnet.html)).

### What `os-on` actually costs

Granting `os-on` to any account is a larger decision than it looks.

**That account reaches the operating system over the API as well as
locally** — and over the API the session's process token is LocalSystem.
On an ordinary account with both `os-on` and API access, a remote API
connection makes the operating system report the session as
`nt authority\system`.

This is accepted behaviour rather than a defect, and it follows from the
way SD's listener creates a session — it is unrelated to the account's own
identity, which is why it is stated here rather than assumed. It is stated
here because it is not something a reader should have to discover: `os-on`
on an account with API access gives that account the operating system, as
LocalSystem, from any machine that can reach the API port.

The full account of what creating a user account does to Windows — the
groups, the disabled-then-enabled login, the console denial — is in the SD
Core for Windows release documentation, under *Accounts*, and is not
repeated here.

## Changing one: `modify.account`

```
modify.account account add | delete  user.name
modify.account account ssh | api | both | none
modify.account account sh-on | sh-off
modify.account account os-on | os-off
modify.account account sd-on | sd-off
modify.account account voc-on | voc-off | bp-on | bp-off | dict-on | dict-off
modify.account account shared-read-on | shared-read-off | shared-write-on | shared-write-off
modify.account account net-on | net-off
modify.account account files-on | files-off | files-write-on | files-write-off | files-admin-on | files-admin-off
modify.account account start-menu | start-terminal | start-default
modify.account account pins-on | pins-off
modify.account account suspended | unsuspended
```

**More than one action in a command** (from 25 October 2026). Any number of the
words above except `add` and `delete` may follow the account, in one command:
`modify.account fred sh-on os-on voc-on bp-on`. SD reads every word first and
then carries out all of them, or none of them:

* **An unknown word, two words that set one access to different states, or
  `add` / `delete` among other words refuses the whole command before anything
  is changed**, and the refusal names the word: `sh-on` with `sh-off`, `ssh`
  with `api` (say `both`), `files-off` with `files-write-on`, and
  `files-admin-on` with `files-off` or `files-write-off` are the conflicts.
* **The words are carried out in one fixed order whatever order they were
  typed:** the route words, then `sh`, `os`, `sd`, the three edit switches and
  `net`, then the files words (`files-on` before `files-write-on`, which needs
  it, and that before `files-admin-on`), then the shared-account words, the
  start and pins words, and the suspension last. Each is reported and audited
  exactly as if it had been given alone.
* **A command of more than one action ends with a line** saying which were
  carried out, and if one could not be (a refusal such as `sh-on` on a group
  account, or a Windows group change that failed) the others are still carried
  out and the line names the one that was not (messages 12798 and 12799).

```
:modify.account fred os-on sh-on
Account fred has SH yes, OS.EXECUTE no
Account fred has SH yes, OS.EXECUTE yes
Account fred: 2 actions carried out: sh-on, os-on
:modify.account fred sh-on sh-off
sh-on and sh-off set the same access to different states, and nothing was changed: give one of them
:modify.account fred voc-on bogus
bogus is not a modify.account action, and nothing was changed: give modify.account with an account and no action to see them
```

(These lines are the messages' texts and the order of the work; they were
produced on Linux and have not been run on Windows.) `add` and `delete` take one
user name and stand alone: among other words, or with a word after the user
name, they are refused with the message *add and delete take a user name and
stand alone, and nothing was changed: ...*. The same word twice is one action.
Before this release a word after the first was read by nobody: `voc-off bp-off`
did the first and said nothing of the second. With no action at all the
command prints its usage.

### `suspended`/`unsuspended` is a state, not a tier

**Nothing about the account moves except the one field.** No Windows
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless of the field. Three doors refuse a suspended account:
signing in, `logto`, and the API.

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`sh-on`** \| **`sh-off`** | the `sh` verb and `!` |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`sd-on`** \| **`sd-off`** | may reach files under the directory of an account the person could `logto` (also allowed on a group account) |
| **`voc-on`** \| **`voc-off`** | may save a change to a VOC (see *The edit switches*) |
| **`bp-on`** \| **`bp-off`** | may save a change to a program file (source or object code), and compile and catalogue |
| **`dict-on`** \| **`dict-off`** | may save a change to a dictionary |
| **`start-menu`** \| **`start-terminal`** \| **`start-default`** | where a session on a terminal starts: the home screen, the command prompt, or the system default (see *Where a session starts*) |
| **`pins-on`** \| **`pins-off`** | may add its own programs to the home screen (see *What the home screen shows*) |
| **`shared-read-on`** \| **`shared-read-off`**, **`shared-write-on`** \| **`shared-write-off`** | open, and write, the files of the shared account by name (blank read means on, blank write means off; see [The Shared Account](13-the-shared-account.html)) |
| **`net-on`** \| **`net-off`** | may use SDNet: open a file on another SD server (see [The NET switch](#the-net-switch-net-on-and-net-off)) |
| **`files-on`** \| **`files-off`**, **`files-write-on`** \| **`files-write-off`**, **`files-admin-on`** \| **`files-admin-off`** | may log in over the API for files only, and, with the second pair, change files there, and, with the third, administer them there (see [The files-only route](#the-files-only-route-files-on-and-files-off)) |
| **`add`** \| **`delete`** *user* | put a Windows user in, or out of, the account's group |

**The first group is absolute and the second is not.** `ssh`/`api`/`both`/
`none` are four names for one state, so whatever is not named is
withdrawn. `sh-on` and `os-on` are two independent switches over two
separate settings, so **`sh-off` says nothing about `OS.EXECUTE`** and
leaves it alone.

**Every keyword on this page refuses `SDSYS` as the target account,
outright, before the keyword itself is even read** — *"Remote access is
never available to SDSYS"* is the message whatever you asked for. SDSYS's
own routes are not a setting; see [Read this before anything
else](#read-this-before-anything-else-being-sdsys-is-the-whole-of-it). A
group account is refused too, for the `sh-on`/`sh-off`/`os-on`/`os-off`
forms: it has no Windows user, and a shell is a fact about a person.

After `sh` or `os` SD says where the account **now** stands, both fields at
once, so that a command that did only what it named is plain to see:

```
:modify.account fred sh-on
Account fred has SH yes, OS.EXECUTE no
:modify.account fred os-on
Account fred has SH yes, OS.EXECUTE yes
:modify.account fred sh-off
Account fred has SH no, OS.EXECUTE yes
```

Asking for what is already so changes nothing and says so ("fred already had
that access; nothing changed"). A route word reports the route in the same way
("fred has no remote access: not ssh, not the API").

**A change takes effect the next time the account is entered.** The setting is
read when a session signs in, and for `sh`, `os`, `sd`, `net` and the two
`shared` switches again when it `logto`s into the account (the three edit
switches are read at sign-on only), so a session already open keeps what it
started with. To take a grant away from somebody who is signed in now, change
the setting and then end their session.

**Every one of these words is written to the audit trail** (`modify.account
sh-on account=fred` and its siblings), in lower case.

**Upgrading keeps what accounts have.** The installer's `upgrade_gates` step
copies `sh` and `OS.EXECUTE` into the register once, from what `os.users` said
(see *The operating-system switches*); `upgrade_editgates` switches `voc-on`,
`bp-on` and `dict-on` on, once, for every user account whose field is blank.
Ssh and the API are left exactly as they were. Group and other accounts are
left off on purpose. **`net-on` is not part of it**: nothing used SDNet before,
so every existing account has it off. **The `shared` switches are not part of it
either**: a blank field already reads as `shared.read` on and `shared.write`
off, which is how they are delivered. **Neither is `files-on`**: the `sdfiles`
group is made empty, and nobody is in it until you say so. You can then turn
them off one account at a time, and a later install does not turn them back
on. Only accounts made after the upgrade start with everything off.

### Every account against every gate: `tool.gates`

```
tool.gates
```

**The gate matrix** is a full-screen page for the administrator (SDSYS's VOC only;
it is refused, before anything is read, to anyone else: in every other account the
same verb is the account holder's read-only "what my account may do" page,
described in the User set under *What this account may do*). One row for each
registered account but SDSYS, one column for each gate the system has, in the
order `modify.account` carries them out: `ssh api sh os sd voc bp dict net sh-rd
sh-wr files f-wr f-adm sock`. A cell says **ON**, **off**, a **dash** (the gate
does not apply to this kind of account: ssh, api and files are routes for a
person, and a group or other account has no Windows user of its own) or **plan**
(not built yet; sockets). A star after a cell is a change you have queued; the
cell shows the state it would have. Under the matrix a box says, for the cell
under the cursor, what the gate is: its two words, what ON allows, what OFF still
allows, when a change reaches the person, whether it reaches beyond SD and what it
is as delivered. A second box lists the accounts that have a gate on which reaches
beyond SD, and a third the live sessions of the account under the cursor.

| Key | What it does |
|---|---|
| arrows, a click | move over the cells |
| Enter or the space bar | queue the opposite state for the cell; again takes it back |
| R | run the queued changes of the account on the cursor's row |
| U | drop them |
| T | queue OFF for every gate of that account that is off as delivered and on now |
| F | change which accounts are shown: all, accounts of persons, accounts with a gate on that reaches beyond SD |
| F5 | read the machine again (a queued change is kept) |
| F1, `?`, a click on the `[?]` | explain the matrix |
| Ctrl-Q | leave |

**The page writes nothing itself.** The queued changes of one account become ONE
command, `modify.account name word word ...`, shown with its effect in a box that
is answered Run or Cancel (Enter alone is Cancel). The verb reads every word
before it changes anything, so a conflict is refused whole. After the command the
page reads the machine again and shows the verb's own words, so a cell changes
because the system changed, never because the page said so. Every change is
audited by the verb as if you had typed it.

* **There is no key that queues everything ON.** **T** is the only "all": it
  queues OFF for what is on and off as delivered (`shared-read`, which is on as
  delivered, is left alone).
* **Turning ON a gate that is off as delivered says so**, and says that leaving
  it off is the tighter choice. **Turning ON a gate that reaches beyond SD**
  (ssh, api, sh, os, sd, net, files, files-write, files-admin) **asks for the
  account's name to be typed**; turning anything OFF does not.
* **ssh and api are one setting** in the verb: the words `ssh`, `api`, `both` and
  `none` SET the pair. The page therefore sends the one word that gives the pair
  of states you queued, and its box says which.
* **files-write needs files, and files-admin needs files-write.** A queue that
  breaks that is refused by the page before the box opens, and the verb refuses
  it again.
* **A group or other account cannot have `sh` or `os`:** the verb refuses them in
  both directions. The page says so instead of queueing them.
* **A change does not reach a session that is already running.** The box says when
  it reaches the person: the next sign-on (voc, bp, dict), the next account entry
  (sh, os, sd, net, shared), the next login (ssh, api, files).
* **Home-screen settings are not gates and are not on this page:** `pins-on` /
  `pins-off` and the three start words are managed on the menu management page
  (`tool.menus`, below).

*Not run on a Windows console yet.* The page is Linux's, carried here and
compiled; it needs a window of at least 140 columns by 43 lines.

### Where a session starts: `start-menu`, `start-terminal`, `start-default` and `set.start.default`

A session on a terminal starts either in the **home screen** (a screen of tiles:
the account's tools, a terminal, switch account and sign out; the User set has the
page *The Home Screen*) or at the **command prompt**. **You decide, account by
account**, and you decide what an account with no setting of its own does:

```
modify.account fred start-terminal       fred starts at the prompt, whatever the default is
modify.account fred start-menu           fred starts in the home screen, whatever the default is
modify.account fred start-default        fred follows the default (the register field is made empty)
set.start.default terminal               accounts that follow the default start at the prompt
set.start.default menu                   ... or in the home screen
set.start.default                        says which it is now
```

* **The default is `menu` as delivered.** `set.start.default` writes the word to the
  file `start.default` in the `sdsys` directory; the file is absent until you use the
  verb, and absent means menu.
* **EVERY EXISTING ACCOUNT HAS NO SETTING OF ITS OWN**, so after an upgrade each
  follows the default and starts in the home screen. To keep the old start for
  everyone, run `set.start.default terminal` (as SDSYS); to keep it for some,
  `modify.account name start-terminal`.
* The setting is **field 16** of the account's register record. `modify.account`
  writes it; it applies at the person's next sign-on, and when they type `logto` at
  the prompt to enter the account. It may be set on any kind of account.
* **It is not a wall.** Starting in the home screen confines nobody: its *Terminal*
  tile gives the ordinary command prompt (and `exit` comes back).
* The screen is never given to a session that cannot use it: a window under 140 by
  43, a session with no terminal (a pipe, a phantom), an API server, or a `logto`
  that a program ran with `execute`. Scripts and scheduled jobs are unchanged.
* `modify.account` says `Account fred starts at: menu` (or `terminal`, or `system
  default`) and `fred already starts that way; nothing changed` when the word is the
  one already set. It is audited as `modify.account start-menu account=fred`, and
  `set.start.default menu` as `set.start.default menu`.
* `create.account` does not take the words: make the account, then use
  `modify.account`.

### What the home screen shows: `set.tile`, `pins-on` and the menu management page

```
tool.menus
```

**Menu management** is a full-screen page for the administrator (SDSYS's VOC only;
it is also a tile on the administrator's own home screen). It lists every account
but SDSYS with where it starts, whether it may add its own programs, and the tiles
turned off for it; for the account you select it shows the standard tiles with `[x]`
on and `[ ]` off, and a box that says in plain words what the settings mean. **It
writes nothing itself:** every change is the command it will run, shown with its
effect in a box you answer *Run* or *Cancel* (Cancel is the button Enter chooses),
run by the same verbs you can type, and the line under the page is the verb's own
answer. **Every setting has a `[?]` at the end of its row** (and one on the accounts
list and on the system default): F1 or `?` on the selected row, or a click on the
`[?]`, opens a box that says what the setting means. The text is the record of that
setting in the file `context.help` of the shared account. **`load.help`, run by
SDSYS, fills that file from the `helptext` directory of the SD system directory**
(it replaces the shipped records and keeps any you added under another id); the
Windows installer does not run it yet, so run it once after an install or an
upgrade, or a `[?]` finds no text.

```
set.tile                          says which tiles are off, one line for each account that has any
set.tile account tile off         turn a tile off for that account
set.tile account tile on          turn it on again
modify.account account pins-on    the person may add their own programs to their home screen
modify.account account pins-off   they may not (the delivered state)
```

* **Tiles are on as delivered and are turned off one account at a time**; there is
  no setting for every account. The standard tile ids are `editor`, `ide`, `ced`,
  `terminal`, `keys`, `switch` and `signout`. **Sign out cannot be turned off**: a
  person must always be able to leave. Any other id is accepted and said not to be
  standard.
* The setting is **field 17** of the account's register record (tile ids separated by
  spaces). A tile that is off is not on the page, its menu entry cannot be chosen, and
  a group with no tile left has no heading. It takes effect when the home screen is
  next built (sign-on, F5, Switch account).
* **The Terminal tile off is a wall for an account that starts in the home screen**:
  the screen never leaves the person at the command prompt, whatever ends it, and signs
  them out instead (a window too small to take the screen ends the session after the
  message). An account that starts at the prompt (`start-terminal`) keeps it. **It is a
  wall only for the prompt the screen gives**: the programs behind the other tiles are
  the account's own, so an account that is to be kept to the screen should have the
  editor, IDE and record editor tiles off as well, and a command that gives a shell
  needs `sh-on`, which is off as delivered.
* **`pins-on` is off as delivered.** An account that has it gets a group *My programs*
  on its home screen and the verb `my.menu`, with which the person adds **their own**
  programs (a label and a command they could type at their prompt): they manage only
  their own list, never the standard tiles, and a program of theirs adds no access. It
  is **field 18** of the register record, and the administrator always may. `pins-off`
  hides the group and `my.menu` refuses; the list stays in the person's file.
* `set.tile` says `Tile ide is now off for fred` (and `... was already off ...; nothing
  changed`) and is audited as `set.tile off tile=ide account=fred`; `modify.account`
  says `Account fred may add its own programs to the home screen: yes`.

*Not run on a Windows console yet.* The home screen and its pages are Linux's, carried
here and compiled.

### The NET switch: `net-on` and `net-off`

One more per-account switch, in field 15 of the register record, for **SDNet**:
files held on another SD server, which an account opens from its own VOC through
an `N` pointer (see [SDNet](12a-sdnet.html)). It is the permission an account needs before it
may use a server, and **it is off for a new account**. `modify.account` *name*
`net-on` / `net-off` turns it on and off, and `create.account user` takes
`net-on`. After a change SD says where the account stands:

```
:modify.account fred net-on
Account fred has NET yes
```

**The switch is what lets an account open a remote file.** An account without it
is refused before anything is dialled. It is checked at every sign-on. A blank
field, and every account that existed before the switch did, count as off:
**there is no upgrade step**, and those accounts cannot use SDNet until SDSYS
turns the switch on, which is the delivered state. The change is written to the
audit trail (`modify.account net-on account=fred`). The administrator (SDSYS) is
exempt from the switch.

**Having the switch is not enough.** An account must also be named in the
*allowed accounts* of the server it wants, and SDSYS puts it there with
`set.server ... accounts` ([SDNet](12a-sdnet.html)). Two lists, both empty
until SDSYS writes to them: the switch says the account may use SDNet at all,
the list says which servers it may use. The same switch guards the API's request
29, "open an SDNet file" (see [SD Admin Configuration](07-sd-admin-configuration.html)).

### The files-only route: `files-on` and `files-off`

There are **two API routes, and the second is narrower.** `api` (the Windows
group `sdapi`) lets a person do everything the API offers: execute commands, call
catalogued subroutines, enter other accounts with `logto`, read and write
sequential files, and work with files. **`files-on` (the Windows group `sdfiles`)
lets a person log in over the API and do files and nothing else.** It exists so
that a login kept for SDNet (see [SDNet](12a-sdnet.html)) never needs `sdapi`: the
other server's administrator gives that login `sdfiles`, and whoever steals the
stored login can open and read files on that server and cannot run a command
there. **Changing files there is a further permission, `files-write-on` (the
Windows group `sdfileswrite`)**, given separately and off for a new account, and
**administering them there - configure, index, create and delete a file, the file's
counter - is a third, `files-admin-on` (the Windows group `sdfilesadmin`)**, off for every
account (below, *Administering files: `files-admin-on`*).

**Off for a new account, like every other door.** `create.account user` takes
`files-on`, `files-write-on` and `files-admin-on`; `modify.account` *name* `files-on` / `files-off`,
`files-write-on` / `files-write-off` and `files-admin-on` / `files-admin-off` turn them on and off. Membership of the
group *is* the route, as membership of `sdapi` is for `api`, so there is no field
for it in the register. After a change SD says where the account stands, **read
back from the group** rather than taken from the request:

```
:modify.account fred files-on
Account fred has files yes
:modify.account fred files-write-on
Account fred has files-write yes
```

`files-write-on` for a person who is not in `sdfiles` is refused ("Account fred
does not have FILES access, so it cannot be given FILES-WRITE: use files-on
first"), because the group on its own gives nothing. `files-off` takes the groups
above away first (administration, write), then `sdfiles`, and reads each back; if a
removal fails SD says so and stops, leaving the person with the lower access and
never a higher one without it. `files-on` takes a leftover `sdfileswrite` or
`sdfilesadmin` membership away before it adds `sdfiles`, and stops with the same
message if it cannot. The change is written to the audit trail (`modify.account
files-on account=fred`). The three groups are made, empty, by the installer (its
`sync-route-groups.ps1`), and removed by an interactive uninstall.

**The rules, in the order the login applies them.** The API server decides at the
end of the login, after the password has been proved:

1. The person must be in `sdusers`, as for every route.
2. A member of **`sdapi` has the whole API, whether or not they are also in
   `sdfiles`: `sdapi` wins.**
3. Otherwise a member of **`sdfiles`** is let in **files only**. On Windows the
   session that serves the connection works this out for itself from the groups
   when it starts, and the mark is never cleared for the life of the connection.
4. A person in **neither** group is refused exactly as before, with the reason
   `not a member of sdapi or sdfiles` in the audit trail. If the groups cannot be
   read the login is refused, not guessed.
5. SDSYS is exempt from both groups by name and keeps the doors it has always
   had; it is never made files-only.

**What a files-only session may ask for.** One function, `!apifilesok`, decides, and
it is an *allow list*: a request number that is not in it is refused, including a
number this release has never heard of.

| allowed | request |
|---|---|
| 1, 2 | quit; get the text of the last error |
| **3, once** | set the account. The first one, which is the entry to an account after login, is allowed; a later one would be a `logto` and is refused |
| 4, 5 | open a file; close it |
| 6 | read |
| 7 to 10 | the locking reads (`readl`, `readlw`, `readu`, `readuw`): **only with `files-write-on`** |
| 11 to 15 | select; read the next id; clear a select list; read a saved list; release a lock |
| 16 to 19 | write; write and keep the lock; delete; delete and keep the lock: **only with `files-write-on`** |
| 26 | select on an index. Allowed because it is a select, with 37 to 39 |
| 30 to 34 | lock a record; clear a file; lock and unlock a file; ask whether a record is locked (the answer names the holder by user number): **only with `files-write-on`** |
| 35, 36 | list the indices |
| 37 to 39 | select a list; select by an index value; select by an index key |
| 40, 41 | file information; read one field (a `readv` that takes a lock is a change and needs `files-write-on`) |
| 42 to 45 | set the left or right end of an index range (`setleft`, `setright`), and select within it (`selectleft`, `selectright`) |
| 46 | the mark mapping |
| 49 | the server's revision |
| 68, 69 | `write` and `writeu ... creating.seqkey` (the file's own counter gives the id): **only with `files-write-on` and `files-admin-on`** |
| 70 | a verb run on this server for the login (`analyse.file`, `configure.file`, `create.index`, `build.index`, `delete.index`, `disable.index`, `create.file`, `delete.file`): **only with `files-write-on` and `files-admin-on`** |
| 71 | `fcontrol`: **only with `files-write-on` and `files-admin-on`** |

| refused | request |
|---|---|
| 20 | call a catalogued subroutine |
| 21, 22, 23 | execute a command; respond to its prompt; end it |
| 24, 25 | the other logins |
| 27, 28 | enter and exit a licensed package (not supported by any route) |
| 29 | open a file on another SDNet server |
| 47, 48 | the SCRAM login itself, which is only possible before the session is logged in |
| 50, 51 | read a variable; `system()` |
| 52, 53 | `trans()` |
| 54 | transactions |
| 55 to 60 | evaluate and the conversions |
| 61 to 67 | sequential files |
| 0, 72 and above, anything else | no such request here |

A refused request is answered with "This login is for files only: request *n* is not
allowed" (a change or lock without the write group: "This login cannot change or
lock files here: ask the administrator for files-write-on (request *n*)"), **the
request is not carried out**, and a line goes to the audit trail
(`api refused request=16 route=sdfiles write=off admin=off user=fred`; a login by this route
is `api login route=sdfiles write=on admin=off user=fred`, with `admin=on` for a person in
`sdfilesadmin`; the `admin=` word is new in this release, and before it the lines ended
`write=on user=fred`). The connection stays open.

### Administering files: `files-admin-on` and `files-admin-off`

A files-only login may configure a file, build and delete its indices, create and delete a file,
and set or take the file's counter (`WRITE ... CREATING.SEQKEY`, `FCONTROL`) **only if the person
is in both `sdfileswrite` and the Windows group `sdfilesadmin`**: `modify.account` *name*
`files-admin-on` (needs `files-on` and `files-write-on` first, else "Account fred does not have
files-write, so it cannot be given files-admin: use files-write-on first", message 12531),
`files-admin-off`, and `files-admin-on` after `files-on` and `files-write-on` in `create.account
user` (without them it is refused the same way, before anything is made). **It is off for every new
account, and nothing in the installer turns it on.** The line
printed is `Account fred has files-admin yes`, read back from the group. A group account or an
`other` account is refused as it is for `files-on`.

The three groups are a chain, `sdfiles` < `sdfileswrite` < `sdfilesadmin`: `files-write-off` and
`files-off` take the higher groups away first (administration, write, files), each removal read
back, and a failure half way reports the removals that did happen (`Account fred has files-admin
no`, and the audit line `modify.account files-admin-off account=fred`) before it reports the
failure. `files-on` and `files-write-on` take a stray higher membership away before they add. Two
words that ask for opposite things in one command are refused with message 12796 and nothing is
changed (`files-admin-on` with `files-off` or with `files-write-off`, and `files-write-on` with
`files-off`). What the permission allows, what the server checks and how it is audited is in
[SDNet](12a-sdnet.html), *The administration group*. A refused request is answered "This login
cannot administer files here: ask the administrator for files-admin-on (request *n*)" (message
12529) and nothing is carried out. The account's backup manifest records the membership as
`route.files.admin`, and `restore.account` gives it back only to an account that is in `sdfiles`
and `sdfileswrite`.

**What is not changed.** Everything else about the session applies as it does to any
other: the account must be entered, the account's own switches (the OS-access
gate, the three edit switches, the NET switch) are loaded and enforced, `SDCLIENT` in
`sd.conf` still decides whether a client may open the files it names, and the
API listener must be on (`remote.api`). **`sdfiles` alone is a read-only route.**
`modify.account fred none` takes away `ssh` and the API and not the files-only
login; withdraw it with `files-off`. `sdapi` is never touched by `files-on` or
`files-off`.

**Not run on Windows yet.** The route is carried from SD Core for Linux and compiled;
no files-only login has been made against a real Windows installation.

## Passwords: `modify.password`

```
modify.password {account}
```

With no account name it changes **your own**, and asks for the current
password first. With one, from SDSYS, it changes that account's — any
account, including SDSYS's own — and does not ask for the old password: an
administrator resetting a forgotten password does not know it.

**The password is never an argument, and a trailing token is refused rather
than ignored:**

```
:modify.password don hunter2
A password is never given on the command line; modify.password prompts for it
```

**That refusal is the point of the verb's design.** The older behaviour set
the password from the prompt and threw the extra word away without a word,
so every visible sign said it had worked — while the password had already
reached SD's command stack, and a shell's history and process list if the
verb was reached from one. Refusing does not put it back, but it says so.

The prompts are hidden, asked twice, and the account must already exist in
the register. **`modify.password` cannot be scripted**, by design.

**SDSYS's *Windows* sign-in password is a separate thing** — set once,
during installation, and changed afterward the ordinary Windows way, not
with this verb.

## Who may enter an account: `grant`, `revoke`, `list.grants`

```
grant account to user
revoke account from user
list.grants account
grant account              the same as list.grants
```

**The grant is Windows group membership and nothing is written to the
account record.** Every SD account has a Windows group — `sdu_`*name* for a
user account, `sdg_`*name* for a group account — and entry to the account
**is** membership of that group. These three verbs edit that group and
read it back.

| | |
|---|---|
| *There is no Windows account named %1* | `grant` to somebody who does not exist |
| *%1 is already a member of group %2* | `grant` to somebody who already has it |
| *%1 has not been granted account %2* | `revoke` from somebody who has not |
| *Account not registered in ACCOUNTS file* | the account name is not one of SD's |
| *Account %1 has no Windows group recorded* | a record predating the group model; it is **refused, not guessed at** |

**The account's own user is listed like any other member.** It is not a
grant — creating the account put them there — but hiding it would make the
listing disagree with the Windows group it is reporting.

**A successful `grant` or `revoke` writes an audit record** to SD's audit
trail, stamped with the user and process that did it. The identity is
stamped by SD and is not passed in, so a caller cannot get it wrong or
forge it. Windows records the group change in its own security log as
well, and the two are independent records of the same act.

> **`modify.account` *account* `add`/`delete` *user* makes the same group
> change and writes no audit record.** Prefer `grant` and `revoke` when
> there is a choice: they say what they mean and they leave a trail.

## Continued in

[Account Maintenance](01a-account-maintenance.html) — clean.account,
update.accounts, [locked], config, set.date and delete.account.

[Differences from W1.0-0](12-differences-from-w1-0-0.html) — what changed
since the previous release, for an administrator upgrading into it.
