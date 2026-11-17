Title: Accounts and Security: Gates, Recovery, Transfer and Start
Subtitle: tool.gates, the recovery copy, file transfer and where a session starts.

This page continues [Accounts and Security: Changing One
Account](01-accounts-and-security-4-modify-account.html).

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
sh-wr files f-wr f-adm ai home sock`. **`home`** is where a session of the account
starts: ON is the home screen, off the command prompt (the words `start-menu` and
`start-terminal`). A cell says **ON**, **off**, a **dash** (the gate
does not apply to this kind of account: ssh, api, files and ai are routes for a
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
  (ssh, api, sh, os, sd, net, files, files-write, files-admin, ai) **asks for the
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
  (sh, os, sd, net, shared), the next login (ssh, api, files) or the next
  request (ai).
* **Home-screen settings are not gates and are not on this page:** `pins-on` /
  `pins-off` and the three start words are managed on the menu management page
  (`tool.menus`, below).

The page needs a window of at least 140 columns by 43 lines.

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

[Accounts and Security: Home Screen, Shared Account and
NET](01-accounts-and-security-6-home-screen-shared-account-and-net.html) —
set.tile, pins-on, the shared account and the NET switch.
