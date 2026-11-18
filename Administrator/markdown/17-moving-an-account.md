Title: Moving an Account
Subtitle: Taking an account to another SD machine with backup.account and restore.account: what you need, the steps and what comes across. The cases where the machines differ.

Moving an account is a backup on one machine, a copy of one file, and a restore on the other.
There is no verb that does it in one go. The two verbs are described on
[Backing Up and Restoring Accounts](01b-backup-and-restore.html); this page is the procedure for
using them between two machines.

> **Three things to know before you start.**
> **No password comes with the account.** An account the new machine does not have asks for a
> new one while it is restored, and `no.query` does not remove that question.
> **The backup is an ordinary, unencrypted zip** of every file in the account. Keep it where
> only administrators can read it, and delete it when the move is done.
> **A new account gets its switches from the zip's manifest, a plain text file.** Whoever can
> edit the zip decides what access a restored account is created with.

## What you need

* **Both machines run the full product**, SD Core for Windows or SD Core for Linux. A backup
  from SD Core Solo is refused, and a full backup does not restore onto Solo: a full product's
  backup restores only to a full product, and a Solo backup only to Solo. The manifest records
  the SD release but the restore does not compare it, so put the same release, or a newer one,
  on the new machine.
* **You are SDSYS on both**, and **no other session is logged in on either** while the verb runs.
  SD lists any it finds: *1 other session(s) are logged in. Every other session must log out
  first:*, then a line for each. While a backup or restore runs nobody can sign in, at the
  console, over ssh or through the API.
* **Disk for a second copy on the new machine.** A restore unpacks the zip into
  `.sdrestore.`*n*, in the folder that holds `user_accounts` and `group_accounts`, before it
  changes anything, and removes it when it ends. If a restore that did not finish left one, the
  next refuses: *… already exists, left by an earlier restore that did not finish. Remove it,
  then run restore.account again.*

## The steps

**On the old machine, as SDSYS.**

1. *(Optional.)* Record the system's settings to compare after the move: `settings.report`
   *folder*.
2. Say where backups go, once: `set.backup.directory` *folder* (for example
   `set.backup.directory C:\SDBackups`). Or give a folder each time with `to`.
3. Back the account up. Several names, or `all`, make one zip, named
   `SD-`*host*`-`*accounts*`-`*yyyymmdd-hhmmss*`.zip`. SD counts the files, bytes and directories
   of each account before it packs, compares them with what it wrote, and **deletes the zip if
   they differ**. The restore checks the same numbers. A junction or other link inside an account
   is not followed and not packed; the backup goes on and names it:
   *Not in the backup: C:\ProgramData\SD\user_accounts\jack\link*.
4. **Copy the zip to the new machine** with whatever you use for files (a network share, a USB
   drive, `scp`). SD has no verb for this.

**On the new machine, as SDSYS.**

5. Put the zip in a folder that only administrators can read.
6. Restore it, naming the zip by its **full path**:

   ```
   restore.account C:\SDBackups\SD-oldbox-jack-20261018-114948.zip jack
   ```

   A bare file name is looked for in the folder `set.backup.directory` saved (and asked for if
   none is). A relative path starts from SD's current folder, not yours, and gives *… does not
   exist.* **`latest` will not find this zip** (see the next page).
7. SD checks the whole zip against its manifest **before it changes anything**, says what will
   happen and asks once (Enter is no):

   ```
     jack will be CREATED.
   Restore these accounts (y/<n>)? y
   ```

   An account the machine already has says *jack will be REPLACED. It now holds 11 files, 45332
   bytes.* **Replaced means its folder is swapped for the zip's and the old one is removed.**
   Whatever was made in it since is gone, and nothing is kept to undo it. If that matters, run
   `backup.account jack` on the new machine first.
8. Check it. For a user account that SD created, the lines it printed say what the account was
   given (*SD routes for jack: …*, *Account jack has SH no, OS.EXECUTE no*, and the lines for the
   edit, NET, FILES and shared switches). `settings.report` gives the same keys to compare with
   step 1. Sign in as the person and open a file.

An account that fails (a name clash, a refused password) is reported as *jack was not restored.*
and the others in the same zip go on. The restore ends with the count of those it restored, and a
non-zero return code if any failed.

## What comes across

Everything under the account's folder **except links** (a junction or other link inside an
account is left out and named): files, programs and their object code, the VOC and
dictionaries. A hashed file is copied as the files it is on disk. The zip also holds a manifest, `manifest.txt`, that any zip tool will show you. It is
plain ASCII text: a header, then one section per account.

```
format: 1
product: windows-full
sd.version: W2.0-0
created: 2026-10-18T11:49:48
host: oldbox
source.root: C:\ProgramData\SD
accounts: 1

[account jack]
type: USER
os.user: jack
os.group: sdu_jack
route.ssh: 0
route.api: 0
route.files: 0
route.files.write: 0
route.files.admin: 0
route.ai: 0
ssh.key: 0
os.sh: 1
os.execute: 0
edit.voc: 1
edit.bp: 1
edit.dict: 1
net: 1
shared.read: 1
shared.write: 1
recovery: 0
xfer: 0
description: Jack's test account
suspended: 0
source.path: C:\ProgramData\SD\user_accounts\jack
files: 10
bytes: 45332
dirs: 6
gcat: hello = bp.out hello
```

A group account's section has `members:` in place of the `route`, `os`, `edit`, `net` and `shared`
lines.

| In the manifest | On an account **SD has to create** | On an account that **already exists** |
|---|---|---|
| the files | fill the new folder | replace the folder |
| `description`, `suspended` | set from the zip | **set from the zip**, so a suspended account comes back suspended |
| `route.ssh`, `route.api`, `route.files` | the Windows user joins `sdssh`, `sdapi`, `sdfiles` as the zip says | unchanged |
| `ssh.key` (ssh key sign-in) | the Windows user is put in `sdsshnokey`, so key sign-in is **off**, unless the zip says it had it (`ssh.key: 1`); a zip made without `ssh.key` leaves it off, and `modify.account` *name* `ssh-key-on` afterwards turns it on | unchanged |
| `os.sh`, `os.execute`, `edit.*`, `net`, `shared.read`, `shared.write` | set as the zip says | **unchanged** |
| `type`, `members` | the kind of account made, and a group account's members | unchanged |
| `gcat:` lines | the program is put in the global catalog again | same |

A key the zip does not have (an older backup) gives the delivered default: every gate off,
`shared.read` on, `shared.write` off. **An existing account keeps its own switches whatever the zip
says**: a zip with `os.sh: 1` restored over an account with `sh` off leaves it off; to change one,
use `modify.account`.

**Global programs.** The backup notes each global program whose object file is in the account, and
the restore catalogs it again from the restored file. A program recompiled after it was cataloged
no longer matches, so it is not carried; `settings.report` lists the global catalog. A name that
the new machine's global catalog already uses for a different program is left alone and listed
(message 13017).

## Continued in

[Moving an Account: the Windows User and the Cases](17a-moving-an-account-cases.html).
