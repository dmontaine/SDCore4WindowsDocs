Title: The Scripts SD Runs For Itself
Subtitle: The scripts the installer, the administrator verbs, the uninstaller and SD itself call, which nobody types.

This page continues [The Installed Scripts](09-the-installed-scripts.html).

## The ones the installer runs

**You should not need any of these**, and running one out of order can undo
work rather than repeat it - most of them must run *after* the step that
secures the data tree, or inheritance puts back exactly what they took away.
They are listed so that a name in a log or an error message can be looked up.

| | |
|---|---|
| `install-sdsys.ps1` | makes the one Windows account that may administer SD, `SDSYS`: a member of Administrators and `sdusers`, and of no remote-access group. It generates a password and writes it to `install-sdsys.log`; `finish-install.ps1` then asks for one of your own. Exit 0 made or repaired, 2 already right, 1 failed. Without it nobody can administer SD |
| `attach-account.ps1` | gives the Windows user who ran the installer their ordinary SD account, through the one door `CREATE.ACCOUNT` keeps for the installer. Without it the person who installed SD has no SD account of their own. Exit 0 made, 2 already there, 3 SD would not start, 1 refused |
| `internal-marker.ps1` | a helper the installer's other scripts load, never run on its own. It writes the one-shot marker an `sd -internal` session needs, and removes it; it prints nothing |
| `deny-logon.ps1` | denies a local group the console and Remote Desktop, which is what confines an account to ssh |
| `finish-install.ps1` | the two steps that happen after the installer closes - SD opens so you can set your own password, then the post-install check runs |
| `install-service.ps1` | creates, starts and removes the Windows service **String Database (SD)** |
| `install-editors.ps1` | makes sure the editors the `edit` and `micro` verbs run are on the machine |
| `ssh-preflight.ps1` | asks whether SD may install here at all, and refuses a machine carrying an ssh server SD does not own. Runs before the wizard is drawn |
| `sync-route-groups.ps1` | creates the two groups that decide which remote route an account may use, and seeds `sdssh` so an existing install does not lose ssh |
| `upgrade-dicts.ps1` | brings an upgraded install's dictionaries up to the release. Runs on an upgrade only |
| `upgrade-voc.ps1` | brings every existing account's VOC up to the release, by running `update.accounts all`. Runs on an upgrade only |
| `upgrade-nocase.ps1` | converts an upgraded install's files to case-insensitive record ids. Runs on an upgrade only. It reads each file first and converts only one that holds no two ids differing only by case; a file that does is left as it is and named in `C:\ProgramData\SD\nocase-upgrade.log`, and so is an indexed file, which needs `CONFIGURE.FILE` by hand. Exit 0 clean, 2 finished with files left (read the log), 1 failed, 3 SD would not start |
| `secure-accounts.ps1` | the containers account directories are created in |
| `secure-account-dirs.ps1` | the ACL on each account's own directory |
| `secure-audit.ps1` | creates the audit trail and makes it append-only |
| `secure-cred.ps1` | locks the credential store to SYSTEM and Administrators |
| `secure-dumps.ps1` | makes the process-dump directory write-only to SD users, so a dump can be added and nobody else's can be read |
| `secure-gcat.ps1` | locks the global catalogue, and separately the compiled objects it is loaded from |
| `secure-log.ps1` | creates a log only administrators can see or write |
| `secure-osusers.ps1` | locks a permission list so only an administrator can change who is on it. The installer calls it four times - twice for `os.users` and twice for `batch.jobs` |
| `secure-pcode.ps1` | locks the pcode library, which is the interpreter every session runs |
| `secure-psdir.ps1` | the directory privileged scripts are written into |
| `secure-reclaim.ps1` | creates the profile-reclaim store and locks it to SYSTEM |
| `secure-sysdirs.ps1` | takes Modify off the system directories that nothing writes |
| `secure-tls.ps1` | creates the directory the API's TLS relay keeps its server key and certificate in, and locks it to SYSTEM and Administrators. An existing key is never deleted, so reinstalling keeps the identity clients already trust |

**THE `secure-` FAMILY IS WHAT KEEPS SD's USERS OUT OF SD's OWN FILES.** The
data tree grants the `sdusers` group Modify, because every SD user needs it to
use the database at all, and that grant is inherited everywhere. Each of these
scripts takes it back off one thing that must not carry it.

## The ones an administrator verb calls

Four SD verbs change the machine rather than the database, and each of them
works by running one of these. **Prefer the verb.** It asks the questions that
need asking, reports what happened in the product's own words, and refuses
when it cannot act; the script does the work and assumes the caller knew what
they were doing.

| | Called by |
|---|---|
| `install-ssh.ps1` | `ssh.server install` - from the OpenSSH installer kept in `ssh-server` under the SD folder when there is one, else the Windows capability. `-Show` reports which and changes nothing |
| `remove-ssh.ps1` | `ssh.server remove` - takes the OpenSSH server off the machine. The Windows capability's removal completes at the next restart; a server from the OpenSSH installer is removed at once (exit 3) |
| `ssh-firewall.ps1` | `remote.ssh on` \| `off` - scopes the shared Windows rule `OpenSSH-Server-In-TCP` rather than disabling it |
| `api-listener.ps1` | `remote.api on` \| `off` - writes or comments out the `APIPORT` line in `sd.conf` |
| `api-firewall.ps1` | `remote.api on` \| `local` - opens or restricts the API port |
| `sd-path.ps1` | `append.sd.path on` \| `off` - puts SD's program directory on the system PATH, or takes it off |
| `restart-sd.ps1` | offered by `remote.api on` and `off`, because the listener is only read at start-up |
| `dism-capability.ps1` | loaded by `install-ssh.ps1` and `remove-ssh.ps1`, never run on its own. It reads, adds and removes a Windows capability through `dism.exe` |

The verbs are covered in the SD Core for Windows administrator documentation,
under *Remote access and the machine*.

Three more verbs run a script for the Windows half of their work. **They are
not for typing either**: each prints one closing line the verb reads, and
nothing else.

| | Called by |
|---|---|
| `sd-account-archive.ps1` | `BACKUP.ACCOUNT` and `RESTORE.ACCOUNT` - writes the backup zip, unpacks one into a staging folder, counts what is there and puts a restored account in place. The zip is the shape SD Core for Linux writes, so a backup made on one can be read on the other, and a junction or symbolic link inside an account is refused rather than followed. Exit 0 done, 1 refused or failed, 2 could not run |
| `sd-backupdir.ps1` | `SET.BACKUP.DIRECTORY` - saves the folder those two verbs use when none is typed, as the one line `BACKUPDIR=<path>` in `sd.conf`. It makes the folder if needed and proves it can write there first. The path must be a full Windows path in plain ASCII. Exit 0 done, 1 refused or failed |
| `sd-settings-os.ps1` | `SETTINGS.REPORT` - the Windows sections of the report. It never prints a password or a private key; of the API's key-and-certificate file it decodes the certificate only. Exit 0 done, 1 failed |

See [Backing Up and Restoring Accounts](01b-backup-and-restore.html) for the verbs.

## The ones the uninstaller runs

| | |
|---|---|
| `remove-sdaccounts.ps1` | takes away the Windows accounts SD created. Only runs if you ask for the data to be removed |
| `reclaim-profiles.ps1` | removes the Windows profiles SD had to leave behind at the time |
| `restore-sshonly.ps1` | puts every non-administrator SD account back into `sdsshonly`, reading the account register rather than anything local |

`restore-sshonly.ps1` is the repair for a half-finished removal: an account
that lost its deny rights but still exists would otherwise become an ordinary
ssh login on the machine.

## The ones SD runs for itself

These are launched by SD while it is running rather than by the installer.
**Do not run them by hand**; they are listed because they appear in logs and in
Task Manager.

| | |
|---|---|
| `sd-elevate.ps1` | the unelevated half of an administrator session, called by SD's `ELEVATE` program with `-Start`, `-Run` or `-Stop`. Exit 0 done, 1 failed, **5 not elevated or elevation refused** |
| `sd-elevate-helper.ps1` | the elevated half. `sd-elevate.ps1` launches it, which is where the UAC prompt appears, and it serves one SD session until that session ends |
| `micro-home.ps1` | gives the calling user a `micro` configuration home they can write to, and prints where it is. Run by the `EDIT` program before it launches `micro` |
| `reconcile-accounts.ps1` | removes register records whose Windows account has gone, and the account directory with them. Runs at every service start |

**A Windows process's token is fixed when it is created**, so nothing can
elevate a running process. That is why administrator work is done by a separate
helper process rather than by an elevated `sd.exe`: SD stays unelevated for its
whole life.

## See also

[Installation and the service](08-sd-installation.html) covers what the
installer puts on the machine and what an upgrade replaces.
[Remote access and the machine](05-remote-access-and-the-machine.html) covers
the four verbs that call seven of these scripts, and is the supported way to
change any of those settings.
