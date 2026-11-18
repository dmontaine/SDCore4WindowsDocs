Title: Accounts and Security: The Other Keywords
Subtitle: The recovery copy, file transfer, where a session starts, and the other modify.account words.

This page continues [Accounts and Security: Changing One Account](01-accounts-and-security-6-modify-account.html).

### The other keywords

| | |
|---|---|
| **`ssh`** \| **`api`** \| **`both`** \| **`none`** | what the account's remote access **is**. Absolute: `api` takes ssh away |
| **`ssh-key-on`** \| **`ssh-key-off`** | ssh sign-in with a key, for a user account whose Windows user SD made (see [Signing in over ssh with a key](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html#signing-in-over-ssh-with-a-key-ssh-key-on-and-ssh-key-off)). **Off as delivered**; independent of `ssh`: the account still needs its ssh route |
| **`sh-on`** \| **`sh-off`** | the `sh` verb |
| **`os-on`** \| **`os-off`** | `OS.EXECUTE`, the screen editors, the embedded Python, and operating-system paths outside the account's own directory (see above) |
| **`sd-on`** \| **`sd-off`** | may reach files under the directory of an account the person could `logto` (also allowed on a group account) |
| **`voc-on`** \| **`voc-off`** | may save a change to a VOC (see *The edit switches*) |
| **`bp-on`** \| **`bp-off`** | may save a change to a program file (source or object code), and compile and catalog |
| **`dict-on`** \| **`dict-off`** | may save a change to a dictionary |
| **`start-menu`** \| **`start-terminal`** \| **`start-default`** | where a session on a terminal starts: the home screen, the command prompt, or the system default (see *Where a session starts*) |
| **`pins-on`** \| **`pins-off`** | may add its own programs to the home screen (see *What the home screen shows*) |
| **`shared-read-on`** \| **`shared-read-off`**, **`shared-write-on`** \| **`shared-write-off`** | open, and write, the files of the shared account by name (blank read means on, blank write means off; see [The Shared Account](13-the-shared-account.html)) |
| **`net-on`** \| **`net-off`** | may use SDNet: open a file on another SD server (see [The NET switch](01-accounts-and-security-3-edit-switches.html#the-net-switch-net-on-and-net-off)) |
| **`files-on`** \| **`files-off`**, **`files-write-on`** \| **`files-write-off`**, **`files-admin-on`** \| **`files-admin-off`** | may log in over the API for files only, and, with the second pair, change files there, and, with the third, administer them there (see [The files-only route](01-accounts-and-security-4-shared-and-files-only.html#the-files-only-route-files-on-and-files-off)) |
| **`ai-on`** \| **`ai-off`** | may use the AI the administrator has chosen: the `ai` verb and the AI line of the pages and editors (see [The AI](01-accounts-and-security-5-files-write-ai-pointers.html#the-ai-ai-on-and-ai-off)) |
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

### The recovery copy: `recovery-on` and `recovery-off`

```
modify.account account recovery-on | recovery-off
create.account user <name> recovery-on
:modify.account fred recovery-on
Account fred keeps a recovery copy of unsaved editor text: yes
```

With `recovery-on` the `ide` of that account copies the text of every record it has changed and not
saved: after a second without typing, before it hands the screen to a program, and when the session
ends. A hung-up terminal, a lost connection or an abort then does not lose the text. **The copy sits in
the person's own Windows profile**, in `AppData\Local\.local\state\sd\recovery\<account>\` (the profile the
person's sign-in token names, never an environment variable), one file per record, readable only by
the person, SYSTEM and the Administrators, **outside every account**; it is deleted when the person saves, closes or quits normally, and the
next time the record is opened the `ide` asks whether to use the copy, delete it, or leave the record
unopened (which keeps it). The record itself is never changed until the person saves. `sed` keeps
no copies.

* **Off as delivered.** `create.account` and an existing account have it off until you say so. `recovery-off`
  is the word for `modify.account` only (as `pins-off` is); `create.account` takes `recovery-on` alone, and
  the audit line of a `create.account` that used it ends `gates=` with `recovery-on` among the words.
* **User accounts only, as the verbs have it.** `recovery-on` for a group or other account is refused
  ("... is not a user account, and a recovery copy is kept only in a user account, for its own person; nothing
  was changed"). The administrator is not given a copy either, by the same rule.
* **Where, and when there are none.** The copies are made only when the person's profile directory and every
  directory below it down to the account's own are real directories (no junction or link) that nobody else can
  change, and every directory **above** the profile cannot be renamed or replaced by an ordinary user. A profile
  that does not pass therefore gets no copies, and the `ide` says the copy could not be written; the text is still in
  the editor. A session that runs as a service account (LocalSystem, LocalService, NetworkService) has no profile and gets none.
* **You cannot read the copies, by design.** The directories and the files can be read only by the person, SYSTEM
  and the Administrators. `recovery-off` stops new copies; copies already made stay and are still
  offered to the person.
* **When it reaches a session.** `recovery-off` stops new copies at once. A running `ide` learned at its start
  whether to keep copies, so `recovery-on` reaches it the next time the person starts the `ide`.
* **The copies are not part of the account.** `backup.account` archives do not contain them (they are in the
  person's profile, not in the account), so a text that was not saved never ends up in a backup that
  the administrator can read; the person's own backup of their profile does contain them. `restore.account`
  puts the account back with the switch it had.

### File transfer: `xfer-on` and `xfer-off`

```
modify.account account xfer-on | xfer-off
create.account user <name> xfer-on
:modify.account fred xfer-on
Account fred may move files over its ssh login (receive / send): yes
```

With `xfer-on`, and with `XFER=1` in `C:\ProgramData\SD\sd.conf`, the account's person can move plain-text
files into and out of their own account with an sftp client (WinSCP, FileZilla, Windows' own `sftp`) signed
in with the same name and password as for ssh. They open each transfer themselves, from their SD session,
with `receive` or `send` (*User: Moving Files In and Out*); nothing can be moved before that command is typed
or after it ends.

**What turning it on opens, plainly.** That person can then bring text of their choosing into the account
from another machine, and take copies of the account's records out to another machine. That is all it
opens, and it is held to this:

* **Off twice as delivered.** `XFER` is 0 and every account has the switch off; both must be on. Neither is
  changed by an upgrade.
* **One directory.** Files come in to `xfer.in` and go out from `xfer.out`, two directory files in the
  account's own directory, and the client can reach nothing else: no other directory, no path, no link is
  followed, and nothing is made, renamed or removed except a file the same connection has just sent. The
  server is SD itself; there is no shell and no Windows sftp server behind it.
* **Plain text only.** A file with a NUL byte or one of the bytes 248 to 255 is refused, in either
  direction, and so is a name that is not a plain file name. `XFERKIND` narrows it to the extensions you
  list. `XFERFILE` and `XFERSLOT` bound the size of a file and of a whole transfer; `XFERWAIT`, `XFERIDLE`
  and `XFERMAX` bound the time (*Configuration*).
* **Nothing is replaced** unless the person typed `receive overwrite`.
* **User accounts only, and the person's own.** A group or `other` account is refused the switch ("... is
  not a user account, and file transfer is only for a user account, for its own person; nothing was
  changed"), the transfer is opened from the account named after the Windows user and not from one reached
  with `logto`, and the administrator (`sdsys`) has no transfer at all.
* **It needs the ssh route.** The client signs in over ssh, so an account with no `ssh` route cannot
  connect. A file that arrives is only a record in `xfer.in`: bringing a program in does not compile or run
  it, and what the person may then do with it is what the account's other switches allow.
* **Everything is in the audit trail**: each opening and closing, each connection with the address it came
  from, each file with its size and SHA-256, and each refusal with its reason.

A change takes effect at the next connection: the register is read each time a client connects. To end a
transfer that is under way, `logout` the person's session or the connection (it shows in `listu` as `sftp`).

**On Windows, sshd needs no change of SD's for this.** SD's ssh settings already send every ssh session,
an sftp request included, to SD; until a transfer is opened, an sftp client is told in words that none is.

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
* **`create.account` takes `start-menu` or `start-terminal`**,
  for any kind of account; without one the new account follows the default. Two
  different start words in one command are refused (*start-menu and start-terminal set
  the same access to different states*), and a start word that is neither is refused
  as an unexpected token, **before anything is made**, so a refused word makes no
  Windows user, no folder and no account. `start-default` is not a word of
  `create.account` (it only restates what the account has when the words are left out).
  The command says `Account fred starts at: menu` back, and the audit line ends
  `start=menu` or `start=terminal` when a start word was typed.

## Continued in

[Accounts and Security: The Home Screen, ssh Keys and Passwords](01-accounts-and-security-8-home-screen-ssh-keys-passwords.html) — the home screen's tiles, ssh keys, suspension, the grant and passwords.
