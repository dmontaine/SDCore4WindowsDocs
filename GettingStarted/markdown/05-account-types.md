Title: Accounts
Subtitle: Ordinary accounts, SDSYS, Suspended and Group — what each one may do, and how to make one.

**Every ordinary account gets the same VOC.** There are no capability tiers:
the only privileged account is SDSYS. An account you create gets every verb there is, the same set SDSYS has for running applications and
building them. What it does **not** get is administration — that is not a
verb an account can be given, it is a separate account.

**Suspended** is a state, not a tier — it denies entry and nothing else. Group
accounts are a different thing again: a shared place, not a person.

## SDSYS is the only administrator

**SDSYS is a single Windows account made by the installer, not something
`create.account` can produce.** Administering SD — creating, deleting or
granting accounts, changing system-wide state, reaching another account's
files without a grant — means signing in to *Windows* as SDSYS and running
`sd`, elevated. Signed in as SDSYS, the Start menu's **SD** asks Windows for
that elevation itself: Windows shows its consent prompt and SD opens in SDSYS;
declined, SD says SDSYS needs an elevated session and stops. Being a Windows
administrator grants nothing by itself: the
account that ran this installer is an ordinary account like any other once
setup finishes, and **elevating a session does not make it SDSYS**.

The reasoning is in the *Administrator* set's *Accounts and security* chapter.

**SDSYS's Windows sign-in password** is asked for once, during installation,
in the window that appears after the wizard closes — that is what you type
at the Windows login screen to reach it at all, and changing it afterward is
an ordinary Windows administrative action, not an SD verb. SDSYS also has its
own SD credential (`modify.password`, run from within an SDSYS session,
changes its own). That credential secures nothing remote unless the
administrator opens a door for it: `remote.api` and `remote.ssh` give SDSYS no
route, and its API door from another computer (`remote.sdsys api on`) is shut as
delivered — see [Reaching the operating system](06-administrator-commands.html).

## Creating an account

```
create.account user <name> {ssh | api | both | none} {sh-on} {os-on} {voc-on} {bp-on} {dict-on} {files-on} {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

**Creating an account needs an elevated SDSYS session.** Creating a Windows
account needs an elevated token, and only SDSYS carries the identity that
makes an elevated session mean anything to SD — see
[SDSYS is the only administrator](#sdsys-is-the-only-administrator) above.

### A new account starts with every door shut

**A new user account has no ssh, no API, no `sh` and no `OS.EXECUTE`, and it
cannot save a change to a VOC, a program file or a dictionary,** until
SDSYS turns each one on. SD is delivered with the tighter setting and the
administrator loosens it, account by account, for the people who need it:

| word | gives the account |
|---|---|
| `ssh` · `api` · `both` | the remote route(s). `none` is the default: an account with `none` is reached only with `logto`, from inside another session |
| `files-on` | the files-only API route: an API login that can open, read, write and select from files and do nothing else (no commands, no subroutine calls, no `logto`). `api` gives the whole API and wins when an account has both |
| `sh-on` | the `sh` verb |
| `os-on` | `OS.EXECUTE`, `edit`, `micro`, the embedded Python, and files or directories of the operating system named by their path outside the account's own directory |
| `voc-on` | saving a change to the account's VOC |
| `bp-on` | saving a change to a program file (`bp`, `bp.out`, `*.bp`, `*.bp.out`), and compiling and cataloging. A new account needs it before it can save or compile its first program |
| `dict-on` | saving a change to a dictionary (a file whose name ends `.dic`) |

`sh-on`, `os-on` and the three edit switches are independent of each other
and of the routes. The same words change an account afterwards in
`modify.account` — see [Managing accounts](05a-managing-accounts.html), which has a
section on the edit switches. **No new account is an
exception — not even the one the installer creates for whoever installed SD on a
fresh machine** (see [Installing SD Core](01-installation.html#what-you-are-asked)); the accounts that keep
their shell, `OS.EXECUTE` and edit rights are the user accounts that already
exist when the installing user upgrades.

**If the machine has no ssh server, `ssh` and `both` still make the account,
and the command warns that it cannot sign in over ssh until one is installed; if
it has no API listener, `api` and `both` warn the same way** (turn it on with
`remote.api on`). The grant is already in place and takes effect then. SDSYS's own
remote doors are not among these words: `remote.sdsys on` opens remote administration for the
separate account SDRADMIN over ssh, and `remote.sdsys api on` *address* opens SDSYS's API login
for a listed address; both are shut as delivered. The test
is made against the machine when you type the command. See
[Installing SD Core](01-installation.html#what-you-are-asked).

### What creating a user account actually does

| | |
|---|---|
| Makes a Windows local account | created disabled, then enabled when the password is set |
| Creates the group `sdu_<name>` | and writes it to the account record |
| Joins `sdusers` | which is what grants access to the data tree |
| Joins `sdsshonly` | this is what denies the console and Remote Desktop — every ordinary account gets it; only SDSYS's own Windows account does not |
| Joins `sdssh` and/or `sdapi` | to match the route keyword — see below |
| Prompts for a password | in SD, masked; it never goes on a command line |

**A user account cannot be created without a password.** Refusing the prompt
creates nothing at all.

**`sdssh` and `sdapi` govern the ssh and API doors specifically, separately
from `sdsshonly`.** An account with route `none` still joins `sdsshonly` like
every other ordinary account — that denies the *Windows* console
and Remote Desktop, and has nothing to do with ssh — it simply also has
neither `sdssh` nor `sdapi`, so it has no remote door of any kind and can
only be reached with `logto`. A third group, `sdfiles`, is a narrower API route
that reaches files and nothing else; the `files-on` and `files-off` words make
and take it away, and `ssh`, `api`, `both` and `none` leave it alone. One more
group works the other way round: a Windows user that `create.account` makes is
put in `sdsshnokey`, and its members are offered no ssh key sign-in (only the
password), until `modify.account` *name* `ssh-key-on` takes the user out; see
[ssh access](08-ssh-access.html).

### What every account can do

**Every verb, from the moment it is created.** Compile, catalog, edit,
define files and indexes, run the bulk record editors, inspect processes —
none of that is withheld. What an account cannot do is administer: create,
delete, or suspend another account; change system-wide configuration. And
reaching the operating system — the `sh` verb, `OS.EXECUTE`, `micro`,
the embedded Python, a file or directory of the operating system
by its path outside the account's own directory — takes the switch above:
see
[Security and the operating system](12a-security-and-the-operating-system.html#the-shell-and-operating-system-access-are-per-account-switches).
Saving a change to a VOC, a program file or a dictionary takes the account's
`voc-on`, `bp-on` or `dict-on` switch, which SDSYS turns on account by account;
see [Managing accounts](05a-managing-accounts.html#saving-changes-to-a-voc-a-program-file-or-a-dictionary-three-more-switches).

> **The VOC is the same for every ordinary account and is not the wall.**
> What stops one account reaching another's data is the operating system's
> own file permissions and the ssh confinement, and — for the verbs and
> statements that name an operating-system path — the account's `os-on`
> switch. See the *Administrator* set's *Accounts and security* chapter.

## The `shared` account

**One group account, named `shared`, exists on every installation.** The
installer makes it; you do not create it, and nobody can create or delete an
account of that name. **Its data files can be opened by every account by
file name** — `open "inventory"` finds the file `shared` holds under that
name, with no `logto` and no pointer in your VOC — unless your own account
already has an entry of that name, which always wins.

**Reading is on for every account; writing is off.** Two per-account
switches, `shared-read-on` / `shared-read-off` and `shared-write-on` /
`shared-write-off`, are SDSYS's to change. Without `shared-write-on`, an
attempt to save, delete or clear a record in a shared file is refused, and
changing the *structure* of a shared file (clearing it, configuring it,
indexing it, deleting it) is SDSYS's alone, at a terminal on the machine.
The verbs, programs and catalog of `shared` are not shared: only its data
files and their dictionaries. **Nobody but SDSYS signs on to `shared`.**
Because every account can read it, put nothing there that is not meant for
everyone.

## Suspended — a state, not a tier

**A suspended account cannot be entered.** It is for an account that should
stop working for a while — somebody on leave, a login being looked into —
and it is refused at all three ways in:

| | |
|---|---|
| ssh, or the console | `Account FRED is suspended` |
| **`logto`** from another account | `Account FRED is suspended` |
| the API | `User not allowed in requested account` |

The API wording is deliberately the same one it gives for an account that
does not exist and for one you are not granted, so the API cannot be used to
find out which accounts exist or what state they are in.

**It takes nothing away, which is why lifting it is free.** The VOC is left
exactly as it is and no Windows group membership moves — suspending sets one
field and unsuspending clears it. Suspending is not a substitute for
deleting: it is reversible on purpose. See
[Changing an account afterwards](05a-managing-accounts.html#changing-an-account-afterwards).

**SDSYS can still `logto` into a suspended account.** That is deliberate —
looking at a suspended account is the usual reason to have one. **What a
suspension denies is the account's own user.**

## Continued in

[Managing accounts](05a-managing-accounts.html) — group accounts, sharing
one, changing an account afterwards, and deleting it.
