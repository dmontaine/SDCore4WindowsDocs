Title: Accounts and Security: Files-Only, AI and Passwords
Subtitle: files-on, files-admin-on, ai-on, modify.password, and who may enter an account.

This page continues [Accounts and Security: Home Screen, Shared Account and
NET](01-accounts-and-security-6-home-screen-shared-account-and-net.html).

### The files-only route: `files-on` and `files-off`

There are **two API routes, and the second is narrower.** `api` (the Windows
group `sdapi`) lets a person do everything the API offers: execute commands, call
cataloged subroutines, enter other accounts with `logto`, read and write
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
| 70 | a verb run on this server for the login (`analyze.file`, `configure.file`, `create.index`, `build.index`, `delete.index`, `disable.index`, `create.file`, `delete.file`): **only with `files-write-on` and `files-admin-on`** |
| 71 | `fcontrol`: **only with `files-write-on` and `files-admin-on`** |

| refused | request |
|---|---|
| 20 | call a cataloged subroutine |
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

### The AI: `ai-on` and `ai-off`

An account may send text to the AI provider you have chosen (the `ai` verb and the AI line of
the pages and editors) **only if the person is in the Windows group `sdaiusers`**:
`modify.account` *name* `ai-on`, `ai-off`, and `ai-on` in `create.account user`. **It is off for
every new account.** The installer turns it on only for the installing user's own account, and
only when its box *Open every access gate for your SD Core account* is ticked, because each request
is paid for by whoever holds the provider's key and sends the person's text off the machine. The
line printed is `Account fred has ai yes`, read back from the group. It stands alone (no other gate
is needed), is for accounts that belong to a person (a group account is refused), needs the person
to be in `sdusers`, and takes effect at the person's next request: the AI helper, the Windows
service `sd-ai`, reads the group each time, from the Windows user it sees at the other end of its
pipe. SDSYS has no gate and may always use the AI. The account's manifest records it as
`route.ai`, and `restore.account` gives it back. Which provider, model and key, what leaves the
machine, the security warning, and the page that does all of this, `tool.ai`, are in
[The AI Helper](21-the-ai-helper.html).

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

**That refusal is the point of the verb's design.** The older behavior set
the password from the prompt and threw the extra word away without a word,
so every visible sign said it had worked — while the password had already
reached SD's command stack, and a shell's history and process list if the
verb was reached from one. Refusing does not put it back, but it says so.

The prompts are hidden, and the account must already exist in
the register. **The rule is checked before the repeat is asked for**, and
there are up to three tries:

```
A password needs at least 8 characters, with a lower-case letter, an upper-case letter, a digit and a symbol.
New password:
ERROR: A password needs at least 8 characters, with a lower-case letter, an upper-case letter, a digit and a symbol.
That was attempt 1 of 3.
New password:
Repeat new password:
ERROR: Passwords do not match.  That was attempt 2 of 3.
```

A password that does not meet the rule is refused at once and is not asked for
again; one that does is asked for a second time, and a difference between the two
says *Passwords do not match.* Each failure names which it was and says which
attempt it was; the third ends the command with *ERROR: Password not changed.*
and nothing is changed. An empty line at *New password* leaves the password as it
was. `create.account user` asks the same way, with the same three tries, saying the
rule first and asking *Retype new password*; its failure lines carry no `ERROR: `
prefix.
**`modify.password` cannot be scripted**, by design.

**SDSYS's *Windows* sign-in password is a separate thing** — set once,
during installation, and changed afterward the ordinary Windows way, not
with this verb.

## Who may enter an account: `modify.account add` and `delete`

```
modify.account account add user
modify.account account delete user
```

**`add` and `delete` are the grant.** There is no separate `grant`, `revoke` or
`list.grants` verb: they were removed in 2.0-0, and `list.voc.removed` names
`modify.account` as what replaces them. **The grant is Windows group membership and nothing is written to the
account record.** Every SD account has a Windows group — `sdu_`*name* for a
user account, `sdg_`*name* for a group account — and entry to the account
**is** membership of that group. `add` puts a Windows user into that group and
`delete` takes one out.

| | |
|---|---|
| *%1 added to group %2* | `add` worked |
| *%1 removed from group %2* | `delete` worked |
| *%1 is already a member of group %2* | `add` for somebody who already has it; nothing changed |
| *%1 is not a member of %2* | `delete` for somebody who has not got it; nothing changed |
| *%1 is not a member of sdusers, not allowed* | the person is not a Windows user SD knows (`add` only) |
| *Unable to add user %1 to group %2 status: %3* | Windows refused the change |
| *SDRADMIN is the remote administration account* | `add` of `sdradmin`, which joins no group account |

**To see who is in an account,** read the Windows group: `tool.accounts` shows a
group account's members, and any account's group can be listed with `net localgroup sdu_`*name*
(`sdg_`*name* for a group account) or in Windows' own tools. The account's own user is a member
like any other. It is not a grant — creating the account put them there.

**A successful `add` or `delete` writes an audit record** to SD's audit
trail (`modify.account add account=`*name*` to=`*user* and `modify.account delete
account=`*name*` from=`*user*), stamped with the user and process that did it. The identity is
stamped by SD and is not passed in, so a caller cannot get it wrong or
forge it. Windows records the group change in its own security log as
well, and the two are independent records of the same act.

**`delete` is deliberately unguarded**: taking access away is always allowed.
**A change reaches the person at their next sign-in to Windows**, because
Windows fixes a person's groups when they sign in; a person you have just taken out keeps the account
until then.

## Continued in

[Account Maintenance](01a-account-maintenance.html) — clean.account,
update.accounts, [locked], config, set.date and delete.account.

[Differences from W1.0-0](12-differences-from-w1-0-0.html) — what changed
since the previous release, for an administrator upgrading into it.
