Title: Encrypting the data SD keeps on disk
Subtitle: Putting SD's data on a BitLocker volume, what that protects, what it does not, and what must be on the encrypted drive.

This page is about the bottom layer in the table on the encryption page: the
disk. SD itself is unchanged by it. The encryption is done by Windows, to the
drive SD's folders live on. [SD Encryption](04-sd-encryption.html) explains the
other two layers, which are the application's.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

## The short version

**Turn BitLocker on for the drive that holds `C:\ProgramData\SD`**, which on an
ordinary install is the system drive, C:. A stolen or discarded disk then holds
ciphertext. **It protects nothing once the drive is unlocked.** While Windows is
running, anyone who can sign in as an administrator, as SDSYS or as an SD user
reads SD's data as plain text, exactly as before.

**Encrypt the system drive, not only a data drive.** Several things SD writes
are on the system drive whatever you choose for the accounts: each person's
temporary folder (where a large sort writes its work files), the page file and
the hibernation file (which can hold SD's memory) and, on an ordinary install,
SD's shared-memory file. BitLocker on C: covers all of them at once.

## Where SD keeps its data

| Path | What is there |
|---|---|
| `C:\ProgramData\SD\sdsys` | the register (`accounts`), `$cred`, the audit trail, the error log and dumps |
| `C:\ProgramData\SD\user_accounts`, `group_accounts` | the account files (`USRDIR`, `GRPDIR` in `sd.conf`) |
| `C:\ProgramData\SD\sd-net` | the SDNet sign-ins, per user and per server |
| `C:\ProgramData\SD\sd-tls` | the API server's TLS identity, including its private key |
| `C:\ProgramData\SD\shm` | the shared-memory file, `sd_shm_`*n*, made again each time SD starts |
| `C:\ProgramData\SD\sd.conf` | the configuration: paths and sizes, no data |
| `C:\Program Files\SD` | the programs; no data |

**The sort work area is not under `C:\ProgramData\SD`.** `SORTWORK` follows
`TEMPDIR`, and `TEMPDIR` with no line in `sd.conf` is the `TMP` folder of the
process that sorts: for a person at the keyboard their own
`%LOCALAPPDATA%\Temp`, for the SD service its own. The work files of a large
sort hold the keys being sorted, in plain text. On an encrypted system drive
they are covered. If SD's data is on another drive and only that drive is
encrypted, point both at a folder on it:

```
TEMPDIR=D:\SDData\temp
SORTWORK=D:\SDData\sortwork
```

## Doing it

1. Turn BitLocker on for the system drive (Settings, *Privacy & security*,
   *Device encryption*, or Control Panel, *BitLocker Drive Encryption*). With a
   TPM, the drive unlocks at start-up without a prompt; a start-up PIN as well
   (group policy *Require additional authentication at startup*) stops a stolen
   machine from unlocking itself.
2. **Keep the recovery key away from the machine.** Without it, a drive that
   will not unlock is lost, and SD's data with it.
3. If the accounts are on another drive (`USRDIR` and `GRPDIR` moved there),
   turn BitLocker on for that drive as well and let it unlock automatically
   with the system drive.

SD needs nothing changed: it starts after Windows has unlocked the drives.

## What this does not cover

- **A running machine.** Everything is plain text to anyone signed in with the
  right to read it.
- **Backups.** A backup folder protects nothing unless it is on an encrypted
  drive or the backups are encrypted another way. `backup.account` writes an
  ordinary zip.
- **The API and SDNet.** Nothing here changes how data travels over a
  connection; that is TLS's job.
- **Copies you make.** A record exported to a file, a report printed to a file,
  or a file copied off the machine is outside BitLocker once it leaves the drive.

None of this has been tried on an SD install for this release: it is Windows'
encryption of the drive under SD, and SD is not aware of it.
