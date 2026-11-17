Title: Accounts and Security: Changing One Account
Subtitle: modify.account and its keywords, suspended and unsuspended, and the accounts on one screen.

This page continues [Accounts and Security: The Edit
Switches](01-accounts-and-security-3-edit-switches.html).

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
modify.account account ai-on | ai-off
modify.account account xfer-on | xfer-off
modify.account account start-menu | start-terminal | start-default
modify.account account pins-on | pins-off
modify.account account suspended | unsuspended
```

**More than one action in a command.** Any number of the
words above except `add` and `delete` may follow the account, in one command:
`modify.account fred sh-on os-on voc-on bp-on`. SD reads every word first and
then carries out all of them, or none of them:

* **An unknown word, two words that set one access to different states, or
  `add` / `delete` among other words refuses the whole command before anything
  is changed**, and the refusal names the word: `sh-on` with `sh-off`, `ssh`
  with `api` (say `both`), `files-off` with `files-write-on`, and
  `files-admin-on` with `files-off` or `files-write-off` are the conflicts.
* **The words are carried out in one fixed order whatever order they were
  typed:** the route words, then `sh`, `os`, `sd`, the three edit switches,
  `recovery`, `xfer` and `net`, then the shared-account words, then the files words
  (`files-on` before `files-write-on`, which needs it, and that before
  `files-admin-on`), then `ai-on` / `ai-off`, the start and pins words, and the
  suspension last. Each is reported and audited
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

`add` and `delete` take one
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
signing in, `logto`, and the API. **Suspending prints two lines**, *Account fred
is now suspended* and *Nothing on Windows has changed: fred keeps its Windows
account, its password and every group it belongs to, including any administrator
rights it had.* A `logto` refused for a suspended account is audited with
`reason=suspended`.

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`sh-on`** \| **`sh-off`** | the `sh` verb |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`sd-on`** \| **`sd-off`** | may reach files under the directory of an account the person could `logto` (also allowed on a group account) |
| **`voc-on`** \| **`voc-off`** | may save a change to a VOC (see *The edit switches*) |
| **`bp-on`** \| **`bp-off`** | may save a change to a program file (source or object code), and compile and catalog |
| **`dict-on`** \| **`dict-off`** | may save a change to a dictionary |
| **`start-menu`** \| **`start-terminal`** \| **`start-default`** | where a session on a terminal starts: the home screen, the command prompt, or the system default (see *Where a session starts*) |
| **`pins-on`** \| **`pins-off`** | may add its own programs to the home screen (see *What the home screen shows*) |
| **`shared-read-on`** \| **`shared-read-off`**, **`shared-write-on`** \| **`shared-write-off`** | open, and write, the files of the shared account by name (blank read means on, blank write means off; see [The Shared Account](13-the-shared-account.html)) |
| **`net-on`** \| **`net-off`** | may use SDNet: open a file on another SD server (see [The NET switch](01-accounts-and-security-6-home-screen-shared-account-and-net.html#the-net-switch-net-on-and-net-off)) |
| **`files-on`** \| **`files-off`**, **`files-write-on`** \| **`files-write-off`**, **`files-admin-on`** \| **`files-admin-off`** | may log in over the API for files only, and, with the second pair, change files there, and, with the third, administer them there (see [The files-only route](01-accounts-and-security-7-files-only-ai-and-passwords.html#the-files-only-route-files-on-and-files-off)) |
| **`ai-on`** \| **`ai-off`** | may use the AI the administrator has chosen: the `ai` verb and the AI line of the pages and editors (see [The AI](01-accounts-and-security-7-files-only-ai-and-passwords.html#the-ai-ai-on-and-ai-off)) |
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
else](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it). A
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

### The accounts on one screen: `tool.accounts`

```
tool.accounts
```

A full-screen page in SDSYS's VOC only (a window of 140 columns by 43 lines or more; in a bigger window this page, like every
administrator page, uses the whole window, with more rows and wider boxes, and follows a resize). The list is every
registered account but SDSYS: its name, its kind (user, group or other), whether it is suspended, **the
gates that are on for it** (read the way `tool.gates` reads them: the register and the Windows groups) and
how many sessions are signed on in it. The box at the foot shows the account under the cursor: its path,
its Windows user and group, its routes, a group account's members, the gates that are on and who is signed
on in it. **The gate switches are `tool.gates`'s, not this page's**: a new account has every gate off, as
the verb makes it.

| Key | Runs |
|---|---|
| `S` | `modify.account name suspended`, or `unsuspended` when the account is suspended already |
| `A` | `modify.account group add user`, on a group account, for the Windows user you type |
| `R` | `modify.account group delete user`, taking one away |
| `C` | `create.account group name no.query`, `create.account other name path no.query` (the path written with forward slashes, such as `C:/Data`), or `create.account user name {none\|ssh\|api\|both}` |
| `X` | `delete.account name no.query`, from one dialog where you type the account's name and press Run |

Each shows its command and what it does in a box answered Run or Cancel, **and Cancel is what Enter
chooses**. The verbs ask for the administrator again and write their own audit lines; the page runs
nothing else. **`/`** goes to the next account whose name holds a text you type (any case; it goes
round to the top): the letters are this page's commands, so `/` is how you find an account by typing.
**One of them is not run through the page**: creating a user account hands the terminal to the verb,
because `create.account user` asks for the new person's password at a prompt of its own that shows
nothing; nothing typed there passes through the page, and when the verb ends the page takes the screen
again and shows what is registered now. **`X` is one dialog, not a box**: you type the account's name and
press Run; the page then runs `delete.account name no.query`, since the dialog has asked. It asks no
`remove.home` question: `delete.account` removes the profile of a Windows user SD made in any case. In the
create dialog the kind and the doors are chosen from a row of words (Left, Right or the space bar), not
typed. A suspended account is refused by LOGIN, ssh and the API; sessions
already signed on in it keep running until they end; nothing changes in Windows, so lifting the suspension
costs nothing. `F5` reads everything again, `F1` explains the page and `Ctrl-Q` leaves. Opening the page
writes the audit line `tool start app=tool.accounts`.

## Continued in

[Accounts and Security: Gates, Recovery, Transfer and
Start](01-accounts-and-security-5-gates-recovery-transfer-and-start.html) —
tool.gates, recovery-on and recovery-off, xfer-on and xfer-off, and the start
words.
