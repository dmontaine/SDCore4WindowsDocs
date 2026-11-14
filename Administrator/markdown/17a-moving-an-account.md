Title: Moving an Account
Subtitle: Taking an account to another SD machine with backup.account and restore.account: what you need, the steps, what comes across, and the cases where the machines differ.

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
  SD lists any it finds and stops. While a backup or restore runs nobody can sign in, at the
  console, over ssh or through the API.
* **Disk for a second copy on the new machine.** A restore unpacks the zip into
  `.sdrestore.`*n*, in the folder that holds `user_accounts` and `group_accounts`, before it
  changes anything, and removes it when it ends. If a restore that did not finish left one, the
  next refuses until it is removed.

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

   A bare file name is looked for in the folder `set.backup.directory` saved. **`latest` will not
   find this zip**: `latest` picks the newest backup *made on this computer* that holds every
   named account, and a zip made elsewhere names another host.
7. SD checks the whole zip against its manifest **before it changes anything**: the format, the
   product, the number of accounts, and every account's files, bytes and directories. Any
   difference stops it with nothing changed. Then it says which accounts will be **created** and
   which **replaced** (with what they hold now), and asks once (Enter is no).
   **Replaced means the account's folder is swapped for the zip's and the old one is removed.**
   Whatever was made in it since is gone, and nothing is kept to undo it. If that matters, run
   `backup.account` on the new machine first.
8. Check it: sign in as the person and open a file. `settings.report` gives the same switch names
   as the manifest, to compare with step 1.

## What comes across

Everything under the account's folder: files, programs and their object code, the VOC and
dictionaries. The zip also holds a manifest that any zip tool will show you, in plain ASCII: a
header (`format`, `product`, `sd.version`, `created`, `host`, `source.root`, `accounts`), then one
section per account, `[account` *name*`]`, with its `type`, its operating-system user and group,
its routes (`route.ssh`, `route.api`, `route.files`, `route.files.write`, `route.files.admin`), its
switches (`os.sh`, `os.execute`, `edit.voc`, `edit.bp`, `edit.dict`, `shared.read`,
`shared.write`, `net`, `recovery`), `description`, `suspended`, `source.path`, the counts
(`files`, `bytes`, `dirs`) and a `gcat:` line for each globally catalogued program that belongs
to it. A group account's section has `members:` in place of the switches.

| In the manifest | On an account **SD has to create** | On an account that **already exists** |
|---|---|---|
| the files | fill the new folder | replace the folder |
| `description`, `suspended` | set from the zip | **set from the zip**, so a suspended account comes back suspended |
| the routes, `type`, `members` | the kind of account made, its routes, and a group account's members | unchanged |
| the switches | set as the zip says | **unchanged** (change one with `modify.account`) |
| `gcat:` lines | the program is put in the global catalog again | same |

**Global programs.** The backup notes each global program whose object file is in the account, and
the restore catalogs it again from the restored file. A program recompiled after it was cataloged
no longer matches, so it is not carried; `settings.report` lists the global catalog. A name that
the new machine's global catalog already uses for a different program is left alone and listed.

## When the machines differ

* **A different folder for the accounts.** VOC entries that hold the account's old path are
  rewritten to the new one. A pointer to somewhere outside the account is listed, not followed.
* **From SD Core for Linux.** The archive's `product` says which system made it, and a Linux
  account restores onto Windows like any other full-product backup; its paths are rewritten as
  above.
* **From a Windows archive**, a rewritten path that does not exist with exactly that spelling is
  listed, so a path whose case changed on the way is seen before a program trips over it.
* **Indices kept outside the account.** A hashed file whose indices were relocated inside the
  account is pointed at its new index path. Indices outside the account are not in the archive,
  and the restore says so: build them again with `build.index`.
* **The account's Windows user.** An account the new machine already has keeps its own
  operating-system user, password and groups. One that SD creates is made as `create.account`
  makes it, from the manifest's description, routes, members and suspension.

A move between machines, and a restore from SD Core for Linux, have not been run on this release;
the steps above are what the two verbs are written to do.
