Title: Installing SD Core: Warnings and Things to Know
Subtitle: What Setup changes in Windows, what to check afterwards, and what to do when a step does not complete.

This page continues [Installing SD Core: What Lands Where and Changing
It](01-installation-2-what-lands-where-and-changing-it.html).

## Warnings and things to know

**The installer's own screens give options and results, and nothing else.**
Every reason, warning and caveat that used to appear on them is here.

### Before you install

- **What Setup changes in Windows.** It creates the group `sdusers` and adds you
  to it, and the group `sdsshonly`, whose members are denied console and Remote
  Desktop sign-in (accounts SD Core creates go in it; yours does not). It
  restricts `C:\ProgramData\SD` to SYSTEM, administrators and `sdusers`,
  installs a Windows service that starts SD Core after every restart, and adds
  SD Core to the system PATH unless you clear that option. The program files
  (`C:\Program Files\SD`) and the database (`C:\ProgramData\SD`) cannot be
  moved.
- **The Task Scheduler folder `SD`.** Setup makes it, open to SYSTEM and
  administrators only: scheduled jobs and remote administration keep tasks there
  that run as SDSYS or SYSTEM, and by Windows' default any signed-in user could
  otherwise create that folder, or a task in it, first. A folder `SD` that is
  already there and owned by an administrator is closed the same way; one owned
  by anyone else is named on the installer's last screen, and SD will not use it
  until an administrator deletes it.
- **Sign out and back in afterwards.** Windows applies a new group membership
  only when you sign in. Until you do, `sd` answers that it is not recognized
  (in a window opened before the install — a new window cures that), that it
  cannot open its files, or `Error 5 getting semaphores` (followed by two lines
  saying that this Windows user is not an SD user, or was made one after
  signing in, and what to do). Only signing out
  cures those two. Switching to another user and back does not, and
  `whoami /groups` does not list `sdusers` until you have signed out.
- **An existing account called `shared` stops the install.** The name `shared`
  belongs to SD's shared account, whose files every account can open by name.
  If an account of that name that SD did not make is already registered, the
  installer stops before it changes anything and names its register record
  (`sdsys\accounts\shared` in the data folder). Move that account aside by hand
  (the record and its directory) and run the installer again.
- **A silent install is refused.** The install ends by asking for a password
  and a silent install has nobody to ask, so it would finish with no password
  set. Run the installer normally, at the keyboard or through Remote Desktop.
- **Another ssh server stops the install.** SD supports only the OpenSSH
  server that ships with Windows, so that it knows how the server is
  configured. If a different ssh server is installed or using port 22, or
  somebody has changed how the Windows ssh server is configured, the installer
  says so and stops before changing anything. Remove the other server, or
  return the configuration to the way Windows shipped it, and run the
  installer again.
- **Installing OpenSSH can take time when it has to be downloaded.** From the
  `ssh-server` folder it is quick. Without that folder it downloads from Windows
  Update and can take up to 30 minutes. Do not stop it, and expect it to want a
  restart: until you restart, nobody can sign in over ssh.
- **Which OpenSSH.** The server from the `ssh-server` folder is Microsoft's
  OpenSSH, installed in `C:\Program Files\OpenSSH`; the one from Windows Update
  is in `C:\Windows\System32\OpenSSH`. SD treats both as Windows' own ssh server,
  and `ssh.server remove` removes whichever it finds: the first at once, the
  second at the next restart.
- **What ssh does once SD is installed.** SD limits ssh to SD Core users, and
  every ssh session goes straight into SD Core rather than a command prompt,
  so an SD Core account cannot get a shell on the computer. Port forwarding is
  off for every ssh session. **`scp` and `sftp` stop working for everyone on
  the computer**, because the command is forced and there is no subsystem left
  to run; remote-control tools that copy files, the console and Remote Desktop
  are unaffected. Any existing `sshd_config` is kept as
  `sshd_config.before-sd`; uninstalling removes SD's block and restarts the ssh
  server, which leaves the file as it was.
- **If you do not ask for the ssh server**, SD touches no ssh configuration,
  opens no port, and leaves `scp` and `sftp` as they are.
- **If OpenSSH is already installed**, SD uses it and configures it the same
  way. Who may reach it is the one box offered, and it starts out matching the
  computer's current firewall rule, so leaving it alone changes nothing. Open
  ssh sessions are dropped when the service restarts, so check that your
  server accepts SD Core accounts.
- **Installing Python runs with nothing else on screen** but the installer's
  *Installing Python...* line. Do not stop it. It must be an all-users install — a
  "for me only" Python cannot be reached by SD Core — which is the only kind
  the installer makes. Its own log is `C:\ProgramData\SD\python-install.log`.
- **The AI is installed off.** Setup
  installs the AI helper service `sd-ai`, which starts with Windows. It has no
  provider and no key, and no account may use it, until SDSYS turns it on. **On
  Windows SDSYS is an elevated Administrator and can read a provider's key; so
  can any Windows administrator of this machine. Turning the AI on sends what a
  person types, and anything they paste, to the provider's servers on the
  internet.** The Administrator set's *The AI Helper* has the rest.
- **Accounts are separate from each other.** The permissions on each account's
  directory allow only SYSTEM, administrators and that account's own `sdu_`
  group. Administrators and SDSYS can read everything.

### After the install

- **The SDSYS password.** SDSYS is the administrator account: sign in to
  Windows as SDSYS and start SD Core from an **elevated** prompt. It is the
  only way to administer SD Core. In the finishing window, pressing Enter keeps
  the current SDSYS password; typing a new one changes it (not shown; at least 8 characters with a
  lower-case letter, an upper-case letter, a digit and a symbol). The rule is
  checked before the repeat is asked for (*Repeat new password*), and there are three tries:
  a failure says *ERROR: *, then the rule or *Passwords do not match.*, then
  *That was attempt N of 3.* On a fresh install, pressing Enter keeps the generated
  password and shows it. If you do not know the SDSYS password, set one from an
  elevated PowerShell prompt:

  ```
  Set-LocalUser -Name SDSYS -Password (Read-Host -AsSecureString)
  ```

- **Your own SD Core password.** It is not your Windows password and does not
  replace it. It is needed only to reach SD Core from another computer, over
  ssh or the SD API. Without one, your account works at the keyboard but not
  from another computer, and SD Core asks for one at the next elevated
  sign-in. Change it at any time with `modify.password` in SD Core.
- **If the installer installed Python, restart Windows** before using the
  `PY_` functions, so that SD Core's service and every session see Python on
  the PATH.
- **SDSYS's remote doors are not asked about: they are installed shut.** SDSYS
  itself never signs in over ssh. Two features open the administrator's remote
  doors after the install, at the SD prompt, signed in to Windows as SDSYS:
  `remote.sdsys on` opens remote administration for the separate account
  SDRADMIN over ssh, and `remote.sdsys api on` *address* opens SDSYS's API login
  for chosen addresses. An upgrade that keeps the configuration leaves each as it
  was (open stays open, shut stays shut). **Once a door is open, that password
  alone stands between those addresses and the administrator**, so choose a
  strong one and shut the door (`remote.sdsys off`, `remote.sdsys api off`)
  when it is not needed. See the Administrator set's *Remote administration
  over ssh* and *Remote administration through the API*.
- **A first install gives nobody ssh.** The group `sdssh` is made empty. Your own
  account gets ssh if you tick the installer's "open every gate" box; otherwise
  SDSYS gives it with `modify.account <name> ssh`. An upgrade keeps the ssh access
  the system had.
- **Giving somebody else access.** At the machine itself, sign in to Windows
  as SDSYS and type `sd`, elevated, then `create.account user <name> ssh`.
  Windows asks you to confirm at the UAC prompt: do it at the machine,
  because over a remote-control tool that cannot display it the screen
  freezes instead. The new account then signs in with `ssh <name>@localhost`.
- **After a reinstall over a kept database**, the Windows groups that decide
  who may reach SD were recreated: the ssh-only confinement is restored from
  the account register, ssh is restored for every member of `sdusers` (including
  an account whose ssh you had withdrawn), and **API access is not restored**.
  Set access per account with `modify.account <name> ssh | api | both | none`;
  the keyword sets access to exactly what it names, so `api` on its own takes
  ssh away. If the API is listening but no firewall rule admits other
  computers, `remote.api on` (or `remote.api local`) fixes it.
- **Upgrading** keeps your database, accounts and settings, replaces SD Core's
  own system files, and does not change `sd.conf` or your ssh, API and PATH
  settings. Every account is given the release's new commands. Change the
  settings with `remote.ssh`, `remote.api`, `ssh.server` and `append.sd.path`
  (see *Changing any of it afterwards*).

### When a step reports that it did not complete

The installer prints what failed and the command to run, from an **elevated**
PowerShell prompt. This is what each failure means until it is put right:

| The installer says | What it means until you fix it |
|---|---|
| The account directories were NOT locked | Any SD Core user can read and rewrite any other account's files outside SD Core |
| The shell permission list was NOT locked | Any SD Core user can add themselves to it and obtain a command shell |
| The batch command list was NOT locked | Any SD Core user can add commands to their own record and run them from the command line |
| The global catalog was NOT locked | Any SD Core user can replace the programs SD Core runs for every session |
| The pcode library was NOT locked | Any SD Core user can replace the interpreter every session runs |
| An SD Core system directory was NOT locked | Any SD Core user can rewrite the account register, the system programs SDSYS runs, or the configuration SD Core reads at start-up |
| The credential store was NOT locked | Any SD Core user can overwrite another account's stored password and then sign in as them |
| Accounts were NOT confined to ssh / the ssh-only confinement was NOT restored | Accounts SD Core created can sign in at the console and over Remote Desktop; if `restore-sshonly.ps1` is missing, add them back to the `sdsshonly` group |
| The ssh and API access groups were NOT set up | ssh is refused to everyone except administrators |
| ssh was NOT limited | Usually OpenSSH has not started yet: restart and run the command. It also stops if `sshd_config` already says who may connect, and that setting is left alone |
| Who may reach ssh could not be set | Port 22 is open to the local network, which is the Windows default |
| Who may reach the SD Core API could not be set | No firewall rule was created, so other computers cannot reach port 4247 |
| SD Core could NOT create its administrator account | There is no way into SD Core until it exists; the reason is in `install-sdsys.log` |
| SD Core could NOT create an SD Core account for you | SD only admits accounts it creates and will not create one for a Windows account that already exists, so this is the one moment such an account can be made: running the installer again will not create it. The reason is in `attach-account.log` |
| The AI helper service was NOT set up | Nobody can use the AI; nothing else is affected. The reason is in `install-aihelper.log`; run `install-aihelper.ps1 -Install` from `C:\Program Files\SD` (see *4. Python*, which also covers the AI helper) |
| The OpenSSH server could NOT be installed | Usually a policy that blocks optional features, a metered connection, or no connection. Accounts cannot sign in over ssh until it is there (API-only accounts can use the API meanwhile) |
| The dictionary, vocabulary or case-conversion step did not run | The upgrade kept what it had: SD Core works, a field added by the release may not be recognized, a command added by the release cannot be typed until `update.accounts` is run in SDSYS (answer Y), and records are still found typed in any case. If two record ids differ only by case, or the file is indexed, or it lies outside its account or under SDSYS, the file is left unchanged and the closing box says some files were not converted (`nocase-upgrade.log` names each): rename or delete one of each pair of ids, then run `configure.file no.case` on it, as its owner. SDSYS's own files are not walked |

### Uninstalling

- **The database and the configuration file are separate questions**, and
  **Keep** is the normal answer to both: a reinstall finds the database again
  and reuses the settings. **Deleting the database is permanent**: every SD
  Core account, every password and all data stored in them, including SDSYS.
  If you delete only the configuration file, a reinstall writes a fresh one.
- **Accounts you keep** remain ordinary Windows accounts, with their
  passwords, and are no longer confined to ssh. Your own account is always
  kept. A profile whose registry hive is still loaded cannot be deleted until
  the next restart (the log names any that were left), and the sweep refuses
  to run rather than remove the last account able to sign in to Windows.
- **`sdusers` is always left behind**, because deleting it would orphan the
  permissions on your database. `sdssh`, `sdapi`, `sdaiusers` and `sdsshonly`
  are removed without asking.
- **The AI helper service `sd-ai` is removed with SD Core.** Its folder
  `C:\ProgramData\SD\ai` (the AI settings and the provider keys) is part of the
  database: when you keep the database, a reinstall finds them again.
- **If something could not be removed**, it may be in use by a running SD Core
  process; treat anything marked for deletion as gone.

## Continued in

[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html) — upgrading
an existing installation, and uninstalling.

[Differences from W1.0-0](01b-differences-from-w1-0-0.html) — what changed
since the previous release, for somebody upgrading into it.
