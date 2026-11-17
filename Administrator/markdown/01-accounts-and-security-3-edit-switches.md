Title: Accounts and Security: The Edit Switches
Subtitle: voc-on, bp-on and dict-on, where a file pointer may lead, and what os-on costs.

This page continues [Accounts and Security: Making an
Account](01-accounts-and-security-2-making-an-account.html).

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
| **a program file** | `bp`, `bp.out` (the object code), or any name ending in `.bp` or `.bp.out`; the private catalog directory (`cat`, or whatever `$private.catalog` names) counts as one |

Capitals do not matter.

**What stops.** A program's `WRITE`, `WRITEV`, `DELETE` and `CLEARFILE` of
such a file is refused with a message that names the missing switch (messages
12410 to 12412), or sets the `ON ERROR` status. The verbs and statements that
change a file the person names ask the same question first, before they lock or
change anything, and give the reason: `sed`, `ide` and `ced` show it in their
message line, and every other verb prints it and stops. They are `ed`, `edit` and
`copy` into the file or moving records out of it, `delete`,
`clear.file`, `cname` of a record, `delete.file` of a program file or of a
dictionary on its own, `fixdir`, `format`, `map file`, `sp.view` (the X key that
deletes an item), `set.trigger` when it installs or removes a trigger,
`copy.list` into the file or with `deleting` from it, `delete.list ... in`,
`get.list ... deleting in`, `save.list ... in`, `sort.list ... from`,
`reformat ... to`, `list ... pageseq`, a delimited report written `to` a
pathname, `compile.dict data`, `generate`, `como on ... in`, and the `.s` and `.d`
stack commands on an existing VOC record. Making a new file is not asked. `cname` will not take a
program file out of its name, or put a file under one, for a person without the
switch, so a rename is not a way round. `OPENSEQ` in such a place opens the file
for reading only and cannot create one; `DELETESEQ`, a print file made there,
the socket trace file (`set.socket.mode` with `skt$info.trace`, status 3035) and `!OSCOPY` or `!IOSCOPY` into it are refused. For these operating-system routes the name of the record or file
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
(`OPENSEQ`, `DELETESEQ`, print files, `!OSCOPY`, `!IOSCOPY`) are not looked at for an account that
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
records, so writing one needs `voc-on`. (See the User set's page on the private
vocabulary and parser.)

**Internal programs run only from the global catalog.** The gates on files
and on operating-system paths do not apply to a program compiled in *internal
mode*, which SD's own commands are. That mark is a bit in the program's own
object file, and SD used to believe it wherever the object came from, so a
user who could put an object file where SD would run it could set the bit and
skip every gate. SD now honors the bit only for an object from the global
catalog, which only SDSYS can write, or for the administrator; for any other
object the bit is cleared when the object is loaded. SD's own commands are all
in the global catalog and are unaffected; a program that SDSYS compiled in
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

The `account:file` form of a file name is always available, with no `sd.conf`
setting: a name in no VOC record with one colon is read as a Q-pointer to that
account and file, and the **Q-pointer rule above applies to it unchanged**, so it
opens only what a Q-pointer the account wrote could open. A drive-letter pathname
such as `C:\data\x` has one colon too; it is read as account `C`, which is not
registered, so it is not found. Any other file outside the account is reached only
through a VOC pointer, which is held to the `os-on` rule and the Q-pointer rule
above.

### What `os-on` actually costs

Granting `os-on` to any account is a larger decision than it looks.

**That account reaches the operating system over the API as well as
locally** — and over the API the session's process token is LocalSystem.
On an ordinary account with both `os-on` and API access, a remote API
connection makes the operating system report the session as
`nt authority\system`.

This is accepted behavior rather than a defect, and it follows from the
way SD's listener creates a session — it is unrelated to the account's own
identity, which is why it is stated here rather than assumed. It is stated
here because it is not something a reader should have to discover: `os-on`
on an account with API access gives that account the operating system, as
LocalSystem, from any machine that can reach the API port.

The full account of what creating a user account does to Windows — the
groups, the disabled-then-enabled login, the console denial — is in the SD
Core for Windows release documentation, under *Accounts*, and is not
repeated here.

## Continued in

[Accounts and Security: Changing One
Account](01-accounts-and-security-4-modify-account.html) — modify.account, its
keywords and tool.accounts.
