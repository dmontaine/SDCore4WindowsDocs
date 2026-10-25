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

**Say nothing and a user account gets `both`** (ssh and the API). Name
`ssh`, `api` or `none` to be narrower — an account meant to be reached only
with `logto` says `none` and means it.

> **It prompts for a password and `no.query` does not suppress that.**
> `no.query` covers the confirmation, not the credential — a password is
> never an argument anywhere in SD. **`create.account user` therefore
> cannot be driven from a script**, and a group account, which has no
> password, can.

**Every account gets the same VOC**, the whole of `newvoc` — there is no
tier to choose at creation. What it does *not* get automatically is
`sh`/`OS.EXECUTE` access: both default to off, and `modify.account`'s
`sh-on`/`os-on` grant them afterward (see below).

### Two settings that are easy to conflate

| | |
|---|---|
| `api` | says who may **connect** |
| `os-on` | says who may reach the **operating system** |

Holding the first has never implied the second. They are independent
settings and are checked in different places.

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
modify.account account suspended | unsuspended
```

**Every action except `add` and `delete` may be given together in one
command**, for example `modify.account fred sh-on os-on voc-on bp-on`. Every
word is read first and **if any is refused nothing is changed**: a word that is
not an action, two words that set one access to different states (`sh-on` with
`sh-off`, or `ssh` with `api`), or `add`/`delete` among other words — those take
a user name and stand alone. The words are then all carried out in a fixed order
whatever order you typed them (the remote routes, then the switches, then
`suspended`/`unsuspended`), each reported and audited as it would be on its own,
and a command of more than one ends with a line saying that every action was
carried out or which were not (the others are still done). With no action at all
the command prints its usage.

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
| **`os-on`** \| **`os-off`** | `OS.EXECUTE` and the screen editors |
| **`sd-on`** \| **`sd-off`** | may reach files under the directory of an account the person could `logto` (also allowed on a group account) |
| **`voc-on`** \| **`voc-off`** | may save a change to a VOC |
| **`bp-on`** \| **`bp-off`** | may save a change to a program file (source or object code), and compile and catalogue |
| **`dict-on`** \| **`dict-off`** | may save a change to a dictionary |
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
forms: it has no Windows user to hold the record.

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
