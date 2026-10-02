Title: Backing Up and Restoring Accounts
Subtitle: Writing accounts to a zip file, putting them back, remembering the backup folder, and recording the system's settings.

This page continues [Account Maintenance](01a-account-maintenance.html).

## Who has these verbs

**All four are SDSYS's** — `backup.account`, `restore.account`,
`set.backup.directory` and `settings.report`. They are in SDSYS's VOC and in
no other account's, so an ordinary account does not have a permission it lacks;
it simply has no such verbs.

## The backup folder: `set.backup.directory`

```
set.backup.directory folder
set.backup.directory
```

With a folder, the verb makes it if it does not exist, proves SD can write in
it, and remembers it in `sd.conf` as `BACKUPDIR=`. With no folder it shows the
one that is remembered and changes nothing.

**The folder must be a full path**, such as `C:\Backups`. A path that depends on
the current folder is refused, because the setting would then mean something
different every time it was used.

**You do not have to run it first.** If no folder is remembered,
`backup.account` and `restore.account` ask for one and remember the answer
exactly as this verb would. `restore.account` with `NO.QUERY` has nobody to ask
and refuses instead.

**An SD older than this release will not start on an `sd.conf` that carries a
`BACKUPDIR` line.** SD stops at start-up on any key it does not know. Remove the
line before going back to an older release.

## Backing up: `backup.account`

```
backup.account name {name ...} {TO folder}
backup.account ALL {TO folder}
```

Writes the named accounts, or every account except SDSYS, to **one zip file**
in the folder. The file is named after the computer, the accounts and the time,
for example `SD-ace-sduser-20261001-144419.zip`.

* **Without `TO`** the remembered folder is used. **With `TO`** the folder is used
  for that one backup only; nothing is remembered.
* The zip holds each account's files and what is needed to make the account
  again: its type, routes, description, groups and `os.users` settings, and its
  globally catalogued programs.
* **No password is in it.** SDSYS, the configuration and the credentials are not
  backed up; use `settings.report` for the system's settings.
* **Each account is counted before it is packed** and the counts are written in
  the zip. If what was written differs from what was counted, the zip is deleted
  and the verb says which account was short and by how much. A backup that
  reports success has been checked against the account.

**While a backup runs, nobody else may be signed in to SD**, and new sign-ins are
refused until it finishes.

## Restoring: `restore.account`

```
restore.account zipfile name {name ...} {NO.QUERY}
restore.account zipfile ALL {NO.QUERY}
```

Puts accounts back from a backup.

* **A bare file name** is looked for in the remembered folder. A name that
  includes a folder is used as given.
* **The zip is checked against its own counts before anything is changed.** The
  product (a full SD Core backup restores only into a full SD Core), the number
  of accounts, and every account's files, bytes and directories must match what
  was unpacked. Any difference stops the restore with nothing changed.
* **It says which accounts will be replaced and which will be made, and asks
  once.** The default answer is no. `NO.QUERY` skips the question.
* **An account that exists is replaced**, and keeps its Windows user, password
  and groups.
* **An account that does not exist is made first**, from the type, routes,
  description and groups in the backup, and asks for a new password, because a
  password is never in the zip.
* **Globally catalogued programs are catalogued again** from the restored object
  files. A name that is already catalogued in the global catalogue as a different
  program is left alone and listed.
* A VOC entry that holds the account's old path is rewritten to the new one. A
  pointer to somewhere outside the account is listed, not followed.

**While a restore runs, nobody else may be signed in to SD**, and new sign-ins
are refused until it finishes.

## What the system looks like: `settings.report`

```
settings.report {folder}
```

Writes a text report of the system's settings for you to keep. **Nothing reads it
back**: it is a record for an administrator, not something that can be restored.
It also lists any globally catalogued program that no longer matches an
account's object file, which is why such a program is missing from a backup.

## See also

[Account Maintenance](01a-account-maintenance.html) ·
[SD Admin Configuration](07-sd-admin-configuration.html) for `BACKUPDIR` ·
[Features the Developers Could Not Test](11-features-the-developers-could-not-test.html).
