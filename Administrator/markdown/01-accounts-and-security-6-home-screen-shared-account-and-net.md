Title: Accounts and Security: Home Screen, Shared Account and NET
Subtitle: set.tile, pins-on and the menu management page, the shared account, and the NET switch.

This page continues [Accounts and Security: Gates, Recovery, Transfer and
Start](01-accounts-and-security-5-gates-recovery-transfer-and-start.html).

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
  `terminal`, `keys`, `switch` and `signout`, and `recent`,
  which is not a tile but the **Recent group** of the home screen: the tiles the person
  started last, newest first, which they turn on themselves in the View menu (it is
  off as delivered). `set.tile account recent off` forbids it for the account: the
  group is not on the page, nothing is read or written for it, and the person cannot
  turn it on. **Sign out cannot be turned off**, and neither can the **Back** tile of
  a sub-menu page: a person must always be able to leave. Any other id is accepted
  and said not to be standard.
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

### The shared account: `shared-read-on`, `shared-read-off`, `shared-write-on` and `shared-write-off`

The installer makes one group account, named `shared`, and **the files in it can be
opened by every account by file name** — `open "inventory"` in any account finds
the file `shared` holds under that name, with no `logto` and no pointer in the
account's own VOC. Two per-account switches, in fields 13 and 14 of the register
record, decide who may. The full description, with the order of the checks and the
cautions, is its own page: [The shared account](13-the-shared-account.html).

| switch | delivered | words | what it allows |
|---|---|---|---|
| `shared.read` | **on, for every account** | `shared-read-off` / `shared-read-on` | opening the files of `shared` by name, and reading them |
| `shared.write` | off | `shared-write-on` / `shared-write-off` | saving, deleting and clearing records in them (a dictionary needs `dict-on` as well) |

**`shared.read` is the one switch in SD whose blank means ON.** It is only off when
the field says `no`: `shared-read-off` writes `no`, and `shared-read-on` writes
`yes`. A blank field — a new group or other account, and every account that
existed before the switch did — reads as on, so **nothing is withdrawn from an
existing account, and nothing needs to be run at an upgrade.** `shared.write` is
the other way: only `yes` is on. **Anything you place in `shared` can be read by
every account you have not taken the right from**, so put nothing there that is not
meant for everyone, and take the right from the accounts that should not have it
before you fill the account.

```
:modify.account fred shared-read-off
Account fred has shared.read no, shared.write no
:modify.account fred shared-write-on
Account fred has shared.read no, shared.write yes
```

`modify.account` *name* `shared-read-on` / `shared-read-off` / `shared-write-on` /
`shared-write-off` change one switch each and say where the account now stands,
both switches in one line. `create.account user` takes `shared-read-off` and
`shared-write-on` (the other two would only restate the delivered state). Asking
for what is already so changes nothing and says so.
Each change is written to the audit trail (`modify.account shared-read-off
account=fred`). A switch may be set on a group or other account, as `net-on` may;
**SDSYS is never a target**.

**It belongs to the account the person is in, like `net-on`:** it is read at
sign-on, again at `logto` into another account, and given back when `logto`
returns, and the API server reads it at every entry. `shared.read` is read when a
file is *opened*, so a file already open stays usable after you withdraw it,
until the person's next entry; `shared.write` is tested at every write.

**How SDSYS puts files in `shared`.** Sign in to Windows as SDSYS, `logto shared`, and make
files as in any account: `create.file`, `copy`, programs that write. The account's
directory, `C:\ProgramData\SD\group_accounts\shared`, gives SYSTEM and Administrators full
control and the group `sdusers` Modify, so every SD user's own process can read the
files through the kernel, and write them when it has `shared.write`. **Only SDSYS
enters `shared`**: its Windows group is `sdg_shared`, which has no members, so
`logto shared` and a Q-pointer to it are refused to everybody else. That is what
makes taking `shared.read` away a real wall for an account that has neither `sh` nor `os`.

**A maintainer who is not SDSYS** is made of two things: membership of the group,
`modify.account shared add` *name* (the Windows user can then `logto shared`),
and `shared-write-on` **on the account named `shared`**,
which lets those members write records there. Neither lets a maintainer change the
*structure* of a file — see the page for that. The switches on the account `shared`
decide what its members can do inside it; a blank means write off.

**What it does not do.** The verbs, sentences and programs of `shared` are not
shared; only data files and their dictionaries are. The administrator's own `open`
does not follow `shared` (reach it with `logto shared`). `shared` is not copied to
other servers. The name is reserved: `create.account` refuses it, and
`delete.account shared` is refused.

**Upgrading.** The installer makes `shared` when it is run, and keeps it when the
accounts are kept. **It stops before it changes anything if an account named
`shared` already exists that is not its own**, and names the register record: rename
that account by hand and run the installer again.

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

## Continued in

[Accounts and Security: Files-Only, AI and
Passwords](01-accounts-and-security-7-files-only-ai-and-passwords.html) —
files-on, files-admin-on, ai-on, modify.password and modify.account add and
delete.
