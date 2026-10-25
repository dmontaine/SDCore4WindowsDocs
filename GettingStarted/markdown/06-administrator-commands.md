Title: Administrator commands
Subtitle: The verbs only SDSYS has, and how to use them.

**These verbs are not in an ordinary account's VOC at all.** SD Core used to
give an *administrator-tier* account a larger VOC than a *programmer*
account's; that model is gone. Every ordinary account now gets the same VOC
— see [Accounts](05-account-types.html) — and administration is not a verb
an account can be given. It is SDSYS, a single Windows account the installer
makes, reached by signing in to Windows as SDSYS and running `sd`, elevated.
Typing one of these verbs from any other account says it is not recognised,
not that you lack permission for it.

## Accounts

```
create.account  user <name> {ssh|api|both|none} {sh-on} {os-on} ...
create.account  group <name>
delete.account  <name>
modify.account  <name> add|delete <user>
modify.account  <name> ssh|api|both|none
modify.account  <name> sh-on|sh-off|os-on|os-off
modify.account  <name> suspended|unsuspended
update.accounts {all}
clean.account
```

Covered in full in [Accounts](05-account-types.html) and
[Managing accounts](05a-managing-accounts.html). The points worth repeating
here:

- **A new user account starts with every door shut.** Say nothing and
  `create.account user` gives it no ssh, no API, no `sh`, no `OS.EXECUTE`; you
  name each thing it is to have (`ssh`, `api` or `both`, `sh-on`, `os-on`, ...).
- **`modify.account` says what the access *is*, not what to add.**
  `modify.account fred api` takes ssh away.
- **`modify.account` takes several actions in one command**
  (`modify.account fred sh-on os-on`); it reads them all first and does all of
  them or none.
- **`suspended`/`unsuspended`** is a state, not a tier — nothing about the
  VOC moves either way, because every account's VOC is the whole of `newvoc`
  regardless.
- **`update.accounts`** only ever adds VOC records it finds missing, from a
  release that shipped verbs the account was created before. Since every
  account already has the whole VOC, this now matters only after an
  *upgrade* — a fresh account never needs it.

**`clean.account`** tidies an account's workspace. **`update.accounts`** is
the one you run in each account after upgrading SD.

## Grants

```
grant       <account> to   <user>
revoke      <account> from <user>
list.grants <account>
```

**A grant or a revoke does not take effect until the person signs out of
Windows and back in.** Entry to an account is Windows group membership, and
Windows fixes that at logon. **Somebody you have just revoked keeps the
account until they get a new token.** Both verbs print the reminder every
time.

## Passwords

```
modify.password {<account>}
```

**A password cannot be typed on the command line.** **`modify.password`**
refuses one given as an argument. A password on a command line is visible to
any local user through Task Manager or `Get-CimInstance Win32_Process`, so
SD prompts for it instead, masked.

Run with no argument it changes your own; from SDSYS, naming an account
changes that account's — every account, including SDSYS's own. The password
matters for **API logins only**. Console and ssh logins ask for nothing —
see [Security](12-security.html).

**SDSYS's *Windows* sign-in password is a different thing entirely** — set
once, during installation, and changed afterward the ordinary Windows way,
not with this verb. See [Accounts](05-account-types.html#sdsys-is-the-only-administrator).

## Locks and sessions

```
lock / unlock
list.locks / clear.locks
listu / list.readu
logout
```

**`unlock` is the one to know about.** It clears a record lock left behind
by a session that died holding one. Without it the only way to release such
a lock is to stop and restart SD, which disconnects everybody.

**`listu`** and **`list.readu`** report sessions and read locks; **`logout`**
ends another session.

## System state

```
config
set.date
```

**`config`** reports the configuration parameters in force.

## The remote doors

```
remote.api on | local | off
remote.ssh on | off
ssh.server ...
append.sd.path ...
```

These four set up the machine's own remote-access surface rather than any
one account's — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html) for what each one does.

## The shell escapes — `sh` and `!`

**Who may use `sh` is a switch on each account, not a matter of elevation.**
`sh` and `!` are in every ordinary account's VOC; whether they *do* anything is
a separate permission, **kept in the account's own record and off for a new
account.** (Until 25 October 2026 it was a record per person in a file,
`os.users`; that file is no longer read.)

### How you grant it

**Four keywords on `modify.account` do it:**

```
modify.account fred sh-on      the sh verb and ! at the prompt
modify.account fred sh-off
modify.account fred os-on      OS.EXECUTE, the edit and micro editors, Python,
                               and files outside the account's own directory
modify.account fred os-off
```

**They are four switches over two fields**, not four names for one state,
so `sh-off` leaves `OS.EXECUTE` alone — and the verb prints the resulting
state, both fields, every time (`Account fred has SH yes, OS.EXECUTE no`).
**Both default to off**, for every account `create.account` makes, and
`create.account user fred sh-on os-on` gives them at creation.

**The switch follows the account, not the person.** It is read when a session
signs in or `logto`s into the account, so a change reaches the account the next
time it is entered; to take a grant from somebody who is signed in now, change
it and end their session.

| What you want an account to have | `sh-on` | `os-on` |
|---|---|---|
| nothing outside SD | off | off |
| the editors and `OS.EXECUTE`, but no shell at the prompt | off | on |
| a shell, but programs may not shell out | on | off |
| both | on | on |

### SDSYS always has both, from any session

**SDSYS reaches `sh`, `!`, `OS.EXECUTE`, `edit` and `micro` whatever the
register says** — the same identity check that gates administration (see
[Accounts](05-account-types.html#sdsys-is-the-only-administrator)) grants
this too. **`modify.account sdsys` is refused outright, for every action,
not only these four** — *"Remote access is never available to SDSYS"* is
the message whatever you asked for, because the refusal comes before the
action is even parsed: SDSYS is outside this verb's reach entirely, not
only for the routes the wording names.

### Both switches are enforced

`OS.EXECUTE` used to be unchecked entirely, so **any account that could
write a program had the operating system** and the **`sh`** restriction
could be walked around by anyone able to type BASIC. `os-on` is what decides
whether `OS.EXECUTE` may run. The refusal reads *`<name>` is not permitted to
use OS.EXECUTE*; the one for `sh` reads *`<name>` is not permitted to use the
operating system shell*.

```
no switch         sh refused    OS.EXECUTE refused
sh-on only        sh RUNS       OS.EXECUTE refused
os-on only        sh refused    OS.EXECUTE RUNS      <- programs may shell
                                                          out; the person at
                                                          the prompt may not
SDSYS             sh runs       OS.EXECUTE RUNS
```

SD's own system programs are exempt, so **`create.account`** and the
**`sh`** verb work as before.

### Two rules that go with it

**No account gets a pipe, a redirect or a chain at the prompt.** `sh` and `!`
refuse a command that holds `;`, `|`, `&`, `$`, a backquote, `<`, `>` or a
newline — for every account, SDSYS included, switch or no switch. A bare `sh`
is refused too. Write the work into a script and run the script:
`sh powershell -File .\nightly.ps1`. (Until 25 October 2026 a person on the
`os.users` list could type `sh dir | more`; nobody can now.)

**`os-on` is also what lets an account name a file outside its own
directory.** Without it, opening a file by its path, `dir()`, `select.dir`,
`deleteseq` of a path and a print file made at a path are refused anywhere but
the account's own directory (and the shipped SDSYS entries, read only, and the
directories listed in `NETDIRS`). That holds at the console as well as over the
network. `sd-on` is the narrower switch that reaches the directories of other
SD accounts the person could `logto`.

### Over the API

**An API session is held to the same switches**: the API server reads the
account's `sh-on` and `os-on` when it enters the account. An account with
`sh-on` and the API route therefore has a shell behind its credential, from
wherever the API port is reachable — which is why both default to off. SDSYS has
no API route to arrive over in the first place — see
[API access](09-api-access.html).

## The full list

**`create.account`** · **`delete.account`** · **`modify.account`** ·
**`update.accounts`** · **`clean.account`** · **`grant`** · **`revoke`** ·
**`list.grants`** · **`unlock`** · **`config`** · **`listu`** ·
**`list.readu`** · **`list.locks`** · **`clear.locks`** · **`lock`** ·
**`logout`** · **`set.date`** · **`remote.api`** · **`remote.ssh`** ·
**`ssh.server`** · **`append.sd.path`**

**`sh`, `!` and `modify.password` are not on this list** — every account
has them; what SDSYS has that an ordinary account does not is the
right to run `sh` whatever the register says and the right to name a different
account with the third.
