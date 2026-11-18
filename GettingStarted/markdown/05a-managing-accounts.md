Title: Managing accounts
Subtitle: Group accounts, sharing one, changing an account afterwards, and deleting it.

This page continues [Accounts](05-account-types.html).

## Group accounts

A group account is a shared workspace with **no Windows account and no
sign-in of its own**. It is how you keep separate work separate, and it is
the one kind of account that needs no way in from outside — which makes it
the only extra account available on a machine with no ssh server and no API.

```
create.account group payroll
modify.account payroll add fred
```

Reach it with `logto payroll`, or through an F pointer.

## Sharing a user account

```
modify.account <account> add    <user>
modify.account <account> delete <user>
```

**Both are SDSYS's, like every other administration verb** — they are
not in an ordinary account's VOC at all, so typing them anywhere else says
the verb is not recognized, not that you lack permission for it. (`grant`,
`revoke` and `list.grants` were removed in 2.0-0: these two do what the first
pair did, and there is no verb that lists who is in.)

**Read this twice, because it is the most confusing part of how SD controls
access.** Entry to an account is membership of the Windows group named in
the account's record, and **Windows fixes group membership when you sign
in**. So:

- a grant does not reach the person until they sign out of Windows and back in;
- and **somebody you have just removed keeps the account until they do the
  same.**

**To see who is in an account,** read its Windows group: `net localgroup
sdu_`*name* (`sdg_`*name* for a group account). The account's own user is
always there and is not a grant.

> From an ordinary account the register is reached as `sd.accounts`, not
> `accounts` — `list sd.accounts`, `ct sd.accounts fred`. There is no tier
> column any more; the register's only state field is the suspension.

## Changing an account afterwards

```
modify.account <account> add | delete <user>
modify.account <account> ssh | api | both | none
modify.account <account> sh-on | sh-off
modify.account <account> os-on | os-off
modify.account <account> voc-on | voc-off
modify.account <account> bp-on | bp-off
modify.account <account> dict-on | dict-off
modify.account <account> files-on | files-off
modify.account <account> suspended | unsuspended
```

**All of them are SDSYS's**, the same as `create.account` and `delete.account`
— run from anywhere else, `modify.account` is not in the VOC at all.

### Suspending and unsuspending

**Nothing about the account moves except the one field.** No Windows
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless, so there is nothing left to add back. See
[Suspended](05-account-types.html#suspended-a-state-not-a-tier).

**You cannot suspend your own account, or the one you are standing in.**

### The remote routes

**The keyword says what the access is, not what to add.** So

```
modify.account fred api
```

gives Fred the API **and takes ssh away**. If you want both, say `both`. The
message afterwards always names both routes, so you can see what you have
left him with.

### Remote access, `sh` and `OS.EXECUTE`: four switches, all off for a new account

**A new user account can sign in to nothing from outside and cannot reach
the operating system from inside SD.** SDSYS opens each door for the
accounts that need it, one at a time:

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | who may connect. Absolute: `api` takes ssh away. These four words leave `files-on` alone |
| **`files-on`** \| **`files-off`** | the files-only API route: a login that may work with files and do nothing else. Off for a new account; reported as "Account fred has files yes"; reaches the person at their next login. `api` wins when the account has both |
| **`sh-on`** \| **`sh-off`** | the `sh` verb |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE` in a program, `edit`, `micro`, the embedded Python, and files or directories of the operating system named by their path outside the account's own directory |

`sh-on` and `os-on` are independent, so `sh-off` leaves `OS.EXECUTE` alone;
each reports where the account now stands ("Account fred has SH yes,
OS.EXECUTE no"). **A change reaches the account the next time it is
entered.** Without `sh-on` the verb answers "*name* is not permitted to use
the operating system shell"; without `os-on`, "*name* is not permitted to use
OS.EXECUTE" or "*name* has no OS access, so a file or directory outside its
own account cannot be reached by pathname". See the *Administrator* set's
*Accounts and security* chapter, which says what each switch covers and what
`os-on` costs on an account that is also reachable from outside. Any number of
words may be given in one command (`modify.account fred sh-on os-on voc-on`);
SD reads them all first and does all of them or none.

### Saving changes to a VOC, a program file or a dictionary: three more switches

Three more switches, also off for a new account, say whether the person
may **save a change** to a VOC, to a program file (and compile or catalog)
or to a dictionary. Reading is never stopped:

| | |
|---|---|
| **`voc-on`** \| **`voc-off`** | saving a change to a VOC |
| **`bp-on`** \| **`bp-off`** | saving a change to a program file (`bp`, `bp.out`, or any name ending `.bp` or `.bp.out`), and the `basic`, `catalog`, `delete.catalog` and `decatalog` commands |
| **`dict-on`** \| **`dict-off`** | saving a change to any dictionary (a file whose name ends `.dic`) |

After a change SD says where the account now stands ("Account fred has
VOC.EDIT no, BP.EDIT yes, DICT.EDIT no"); when the switch already had the
value asked for, it says only that the account already had that access. The
account the person **signed on** to decides, so `logto` neither gives nor takes
the switch (and, unlike `sh-on` and `os-on`, it is read at sign-on only), and a
change reaches the person the next time they sign on. A refusal names the
switch: "A program file can only be changed by an account that has bp.edit
(SDSYS can give it: modify.account *name* bp-on)". The editors `sed` and `ide`
show that in their message line; every other verb prints it.

When the installer is run over accounts that already exist, the upgrade
switches all three on, once, for the *user* accounts in the register. Group and
other accounts are left off on purpose, and a member who signs on to one
directly (`sd -A`*name*, a batch job, or the API) gets that account's own
switches, so give them there with `voc-on`, `bp-on` and `dict-on` where members
need them. `restore.account` gives the switches back only to an account it has
to create; an existing account keeps what it has. See the *Administrator* set's
*Accounts and security* chapter for which files and which commands are covered,
and for what is not stopped.

**`modify.password` changes a password.** Every account has a password
from the moment it is made, so there is nothing to *set* for the first time.
Run with no argument it changes your own; SDSYS may change any account's,
naming it — see [Administrator commands](06-administrator-commands.html).

## Deleting an account

**`delete.account`** **asks once, then removes everything.** The single
question names exactly what will go, including the Windows account when
there is one to remove.

**It will not delete a Windows account SD did not create.** The question
uses shorter wording in that case rather than promising something it will
not do.

## `sdusers` membership needs a fresh logon

Same reason as a grant, above. After being added to the group, sign out of
Windows and back in, or you cannot read the data tree at all — and the
symptom looks like a broken install rather than a permissions problem.
