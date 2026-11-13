Title: Remote Administration over ssh
Subtitle: The SDRADMIN account: what remote.sdsys opens, what it can and cannot do, and what opening it means for security.

Remote administration lets one dedicated account, **SDRADMIN**, sign in to SD over ssh from another computer and manage
SD accounts. **It is shut as delivered. Opening it is the administrator's decision**, made at this computer with
`remote.sdsys on`, or with the installer's "Remote administration" page, which is not ticked by default.

```
remote.sdsys on
remote.sdsys off
remote.sdsys
```

`remote.sdsys off` shuts it again at once and logs SDRADMIN out. `remote.sdsys` with no keyword shows each wall: the
account, the `sdssh` group, the sshd arm, the broker and the state. An elevated administrator can do the same from
PowerShell:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\remote-admin.ps1" -Status
```

with `-On` or `-Off` in place of `-Status`. `tool.remote` shows remote administration as its sixth view.

## The account

The first `remote.sdsys on` makes SDRADMIN and asks for its Windows password. **Choose a long password used nowhere
else.** To change it later, run `net user SDRADMIN *` in an elevated prompt. That Windows password is the only one:
SD does not ask SDRADMIN for a second.

SDRADMIN is never a Windows administrator. It may sign in over ssh only: not at the console, not by Remote Desktop,
not as a scheduled task. It lands in its own SD account, with every gate shut, and cannot `logto` another account.
An upgrade keeps remote administration as it was; the uninstaller removes the broker and SD's sshd lines, and the
account goes with the question about the Windows accounts SD made.

## What SDRADMIN can do

Once signed in, SDRADMIN can use `create.account`, `delete.account`, `modify.account`, `modify.password`, and
`remote.sdsys off`, `remote.sdsys audit` {*n*}, `remote.sdsys accounts` and `remote.sdsys` with no keyword. A helper
checks every word and runs the command as the administrator would at the console. Every request is in the audit
trail, and in `C:\ProgramData\SD\remote-admin\broker.log`, which only administrators can read.

## Security warning: what opening it means

While remote administration is open, anyone who knows or guesses SDRADMIN's password, and can reach this computer's
ssh port, **can**:

- create SD accounts and set any SD account's password, then sign in as that account and read its data;
- change any account's access, including giving it a shell or `os.execute`;
- suspend accounts;
- **delete any SD account together with all of its data**; only your backups can bring it back;
- read the audit trail and the list of accounts;
- shut remote administration.

They **cannot**:

- become a Windows administrator or run commands as one;
- touch the SDSYS account, SD's system files or any account SD did not make;
- sign in at the console or by Remote Desktop;
- run a shell, `scp`, `sftp` or port forwarding;
- use an ssh key;
- `logto` another account;
- open remote administration again from a distance.

The password also works for any other Windows network service that accepts every user, exactly as every SD user's
password already does. **Windows' account-lockout policy is the only limit on guessing.** Open it only if you need it,
on a network you trust, and shut it when you are done.
