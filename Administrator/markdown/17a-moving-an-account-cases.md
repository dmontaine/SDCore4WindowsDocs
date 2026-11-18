Title: Moving an Account: the Windows User and the Cases
Subtitle: What does not come across, what a restore does to the Windows user and groups, and the cases where the two machines differ.

This page continues [Moving an Account](17-moving-an-account.html).

## What does not come across

* **Passwords**, the SD one and the Windows one.
* **The `sd-on` switch.** It is not in the manifest, so a restored account has it off, an
  existing one keeps what it had. (`settings.report` does not show it either.)
* **The Windows user's profile**, its ssh keys and its other group memberships.
* **The system**: SDSYS and its VOC, `sd.conf`, the TLS certificate, the ssh and API setup, the
  audit trail, and every global program that is not tied to an account's object file.
* **Anything the account only points at.** A VOC pointer to a file outside the account is named
  (*outer in jack points outside the account (C:\Data) and was left unchanged.*) and not
  followed. Indices kept outside the account are not in the zip; the restore says *Rebuild them
  with build.index*.

`backup.account all` takes every registered account but SDSYS, so **the shared account is in it**.
When you move only some accounts, name them.

## The Windows user and groups

**An account that already exists** keeps its Windows user, its password and its groups. Only its
files, its description and its suspension change.

**A user account SD has to create** is made the way `create.account` makes one:

* The Windows user is named after the **account**. `os.user` and `os.group` in the manifest are
  not read. The user is made with the group `sdu_jack`, joins `sdusers`, and joins `sdssh`,
  `sdapi` and `sdfiles` where the manifest says 1.
* **SD asks for the password at the terminal** and prints the rule (*A password needs at least 8
  characters, with a lower-case letter, an upper-case letter, a digit and a symbol.*). If Windows
  or SD refuses it, SD says why and asks *Warning, user created but password not set, Retry
  (y/<n>)?*. If you decline, SD removes the
  Windows user again, says *An account must have a password. Nothing was created.* and the
  account is *not restored*. **`no.query` removes the "Restore these accounts" question and not
  this one.** Commands typed after a `no.query` restore are taken as passwords.
* A route the machine cannot yet serve is said and not refused: *… is set up to sign in over ssh,
  but this machine has no ssh server yet.* The account is still made.

A **group account** is made with its Windows group `sdg_`*name*. Its `members:` are Windows user
names. One that cannot be added is named and the rest go on: *nosuchuser could not be added to
sdg_work (status 2); the account was made*.

## When the machines differ

* **A different folder for the accounts.** VOC entries that hold the account's old path are
  rewritten to the new one. A pointer to somewhere outside the account is listed, not followed.
  Only the VOC is rewritten: a path written in a record or a program is left as it is.
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
* **The Windows user name is already taken.** SD takes the user over only if SD itself made it,
  and asks for a **new** password (Windows keeps the Windows password and SD's own credential
  together, so the old one is not kept): *SD made the Windows account jack for an earlier
  account; it is used again, with a new password.* If no new password is set, SD says *jack was
  not given a new password, so the account was not made* and the user is left as it was. **The
  user is taken out of every route group the restored account does not ask for** (`sdssh`,
  `sdapi`, `sdfiles`, `sdfileswrite`, `sdfilesadmin` and `sdaiusers`), so a leftover user does
  not keep the remote routes of the account it belonged to before; a membership SD cannot read
  or remove stops the restore with *Unable to change remote access*. **It is also restored with
  key sign-in over ssh off** (a backup holds no such setting; `modify.account` *name*
  `ssh-key-on` afterwards if it should have it). Any other user is refused, nothing is created,
  and the account is not restored:

  ```
  Windows account jack already exists.  SD accounts create their own OS account
  jack was not restored.
  ```

  Rename or remove that Windows user with the operating system's tools, then run the restore
  again. **There is no way to restore under another account name.** A word such as `as` is read
  as an account name: *as is not in this backup.*
* **`latest` will not find a zip made elsewhere.** `restore.account latest` picks the newest
  backup *made on this computer* that holds every named account, and a zip made on another
  machine names another host in its file name: it gives *No backup of jack made on this computer
  was found in …*. Name the zip by its path. A renamed file is also never picked by `latest`.

The steps on the previous page are what the two verbs do for a move between machines and for a
restore from SD Core for Linux.

## When it refuses

| It says | Why |
|---|---|
| The archive does not match its manifest: jack (manifest 99/45332/6, unpacked 10/45332/6). Nothing was restored. | the zip was changed or damaged |
| … has manifest format 2, and this version reads format 1. Nothing was restored. | a newer zip format |
| This backup is from windows-solo and this system is windows-full. … | the wrong product |
| nosuch is not in this backup. | the name is not in the manifest |
| 1 other session(s) are logged in. Every other session must log out first: | log them out and run it again |
| … already exists, left by an earlier restore that did not finish. | remove that `.sdrestore.`*n* folder |

None of these changed an account, and the restore leaves no `.sdrestore.`*n* folder behind (except
in the last row, where it is the folder that is the cause). A zip with an entry outside
`manifest.txt` and `accounts/`, a `..` or absolute path, a backslash or a colon in a name, or a
name that is not plain printable ASCII is refused before anything is unpacked.

## See also

[Account Maintenance](01a-account-maintenance.html) for the verbs and `set.backup.directory`;
[Accounts and Security](01-accounts-and-security.html) for the switches;
[Data at Rest](04a-data-at-rest.html) for backups and encryption.
