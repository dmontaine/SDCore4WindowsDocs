Title: Not in SD Core
Subtitle: What has been removed, why, and what to use instead.

This page exists so you do not spend time hunting for something that is not
there. **It names what is gone and what to use in its place; it does not
document the removed features themselves.**

Everything here was in OpenQM, in ScarletDME, or in upstream `sdb64`, and is not
in SD Core for Windows. **Most of these removals were made independently on SD
Core for Linux too, for the same reasons.**

> **If you had a use for any of these, say so.** Several were removed on the
> reasoning that nothing needed them. That reasoning is worth testing against
> real use.

## Editors

| Gone | Use instead |
|---|---|
| `update.record` — the full-screen record editor | **`sed`**, **`edit`** or **`ed`** |
| `modify` — the full-screen record editor from OpenQM | **`sed`**, **`edit`** or **`ed`** |
| `nano` — the second external editor (removed in 2.0-0) | **`micro`**, **`sed`** or **`ed`** |

**`sed` has a menu bar that shows the key of every action.** It runs inside SD, so it needs no
operating-system permission, and it needs a window of 140 columns by 43 lines.
With it came `ced`, a full-screen editor for a record that is a data collection,
and `ide`, a workbench for programs and files.

**SD Core's full-screen editing is `sed`, `edit` and `micro`**; the last two open
the record in Microsoft Edit and in micro — see
[Development and file commands](07-programmer-commands.html#editors), which also says
what each is good for and what they cannot do. The three removed programs above are
gone as *programs*; the capability is not.

`modify` is not in SD Core at all, for any account.

> **`edit` and `micro`** are two full-screen editors that start an external
> program: gated by the account's `os-on` switch — every account has the verb,
> not every account has the permission — and refused over the API regardless (a
> session with no terminal has nowhere to draw a full screen).

**`modify.account` and `modify.password` are not affected.** They are
different verbs with different programs behind them. `modify.account` is
SDSYS's alone; `modify.password` is every account's, for its own password —
only naming a different account needs SDSYS.

> **`ed`** reads whole lines and goes through the command-line editor.

## The PROC language

`PROC` is gone. **A VOC item of type `PQ` now reports that PROC is not
supported instead of running.** Your `PQ` records are left alone — it is the
interpreter that has gone, not the records.

**Do not confuse PROC with the query processor.** `list`, `count`, `select`
and `sort` are unaffected. They are a different thing despite the similar name.

## SDNet — remote file access

SD could open a file held on another SD server by putting `server;file` in a
VOC entry, with each server's password in `sd.conf`. **That form is gone, and
it stays gone. A VOC entry containing a semicolon is simply a file name that
does not resolve.**

**A different SDNet has replaced it.** A VOC entry of type `N` names a server
that SDSYS has defined with `set.server` and a file on it; the verbs
`set.server`, `delete.server` and `list.servers` are SDSYS's, and `set.netlogin`
and `delete.netlogin` let a person store their own login (never the password) for
a server. Nothing is open by default: an account needs the `net-on` switch, has to
be named in the server's list, and a server is read only unless SDSYS defines it
as `write` **and** the administrator of the other server has also let that remote
login change files there (`files-write-on` on that server); configuring, indexing,
creating and deleting a remote file, and the file's counter, need a third permission
there (`files-admin-on`). It uses the other
server's API port over TLS and does not put a password in any file. The
*Administrator* set's *SDNet* page describes it.

**The API is not affected.** `!sdclient` and the remote API are a separate
mechanism and are unchanged. See [API access](09-api-access.html).

**`NETFILES` is still accepted in `sd.conf`**, so an existing configuration file
will not stop SD starting, and the new SDNet does not use it. The only
thing that reads it is the API server's old request to open an SDNet file,
which is refused unless bit 2 of `NETFILES` is set (and
unless the caller could `logto` that account and the account has `net-on`, and
a file pointer that leads out of the account is followed only if the
account has `os-on`); the
value is 0 unless `sd.conf` sets it. The two settings the new SDNet does read
are `NETWAIT` and `NETREPLY`, the seconds to wait for a connection and for each
reply.
The *Administrator* set's *Configuration* page has the detail.

## Virtual file systems

**SD has never been able to open a virtual file system.** Nothing in the
file-opening code ever recognized a `VFS:` pathname. What the language carried
was the *outline* of one, and none of it could be reached: a VOC F-pointer
written as `VFS:something` was reported as a virtual file system, passed the
name resolver, and then failed to open with an unrelated error.

All of it has been removed, so the language no longer offers a feature it
cannot perform.

**These names are no longer defined, and a program mentioning one will no
longer compile:**

```
FL$TYPE.VFS      SYSCOM KEYS.H
ER$VFS.NAME      SYSCOM ERR.H
ER$VFS.CLASS     SYSCOM ERR.H
ER$VFS.NGLBL     SYSCOM ERR.H
```

`ftype` no longer returns `VFS` for a `VFS:` pathname. **Error numbers 3038,
3039 and 3040 are retired and will not be given a new meaning.**

**If one of your programs refers to any of these, it was testing for a state SD
could not reach, and the test can be deleted.**

## Tape and restore

The `TAPE`/`RESTORE` subsystem is gone, along with the assumption of a
tape-backed sequential medium it was built around. Back up and restore SD
data with `backup.account` and `restore.account` — see the Administrator
set's *Backing Up and Restoring Accounts* — at the file level, with the
service stopped, or through your own export/import BASIC.

## Language and locale

**SD Core is English only.** `set.language` and `load.language` do not exist.
`nls` is still there: it shows and sets the currency symbol and the thousands
and decimal separators, which is all it ever did.

## Embedded Python

**Python inside `sd.exe` is not there — calling Python from SD BASIC is**, as a
separate, native helper process SD talks to over a pipe rather than a library
loaded into the server. Python and the runtime `sd.exe` is built on cannot share
one process safely (`long` is a different width on each side); the helper avoids
that by never being the same process at all.

**21 `gpl.bp/py_*` programs** are BASIC-callable (`call !py_createdict`,
and so on) — there is no TCL verb, so this is a programming capability, not
a command you type at the prompt. Access is gated per session, at the
moment Python starts, by the same `os-on` switch that gates
`OS.EXECUTE` — a session without it cannot start the helper at all. All
twenty-one functions, their arguments and their error codes are in the User
set's *Embedded Python* chapter.

## Field-level encryption

**`encrypt.field` is gone, and with it the TCL verb that encrypted a field in
place.** What replaces it is the application's own: `sdencrypt()` and
`sddecrypt()` with a key that `sdkey()` makes from a passphrase, and the `XE`
conversion, which shows an encrypted field decrypted to a session that holds the
key. SD does not keep the key. See *Encryption and the SDEXT interface* in the
Administrator set and *SD Basic - Encrypting Data* in the User set.

## Account and configuration items

| Gone | Notes |
|---|---|
| `RDPACCOUNT`, `NO.RDPACCOUNT` | typing it now stops **`create.account`** with *Unexpected token (RDPACCOUNT)* and makes no account |
| `CREATUSR` | **`config`** no longer lists it; `config('CREATUSR')` returns nothing. The parameter itself no longer exists, and a `CREATUSR` line in `sd.conf` now stops SD from starting (the installer takes it out of a kept file) |
| `umask` | removed entirely. It controls POSIX file-mode bits, which Windows does not use for security — see [Security](12-security.html#what-ships-secured-before-you-change-anything) for what does the equivalent job here |
| `grant`/`revoke`/`list.grants` | folded into `modify.account add`/`delete` — see [Accounts](05-account-types.html). There is no verb that lists who is in; the members of the account's Windows group are the answer (`net localgroup sdu_`*name*) |
| the `os.users` permit list | the file is gone; `sh-on`/`sh-off`/`os-on`/`os-off` are kept, and they set two fields of the account's own register record instead — see [Security and the operating system](12a-security-and-the-operating-system.html) |
| Field 4 of an `ACCOUNTS` record | the list of accounts allowed in. The membership of the account's Windows group answers that question now |

**Accounts already created with `RDPACCOUNT` keep their Windows sign-in.**
Nothing goes round and takes it back, because SD did not record which accounts
they were. If you have any, either delete and recreate them, or add them to the
restricted group by hand:

```
net localgroup sdsshonly <name> /add
```

## Eighteen SDSYS test and legacy programs

`bigstr_test`, `msgtest`, `pcl`, `pcl.grid`, `pcode_list`, `sdtest_v8`,
`sd_encrypt`/`_b64`/`_ext`, `sd_ext`, `test.then.else`, `testsz`, `u0032`,
`u50bb`, `vfs.cls`, `pref_t`, `sdTests` and `tilde_test` are no longer
installed into the SDSYS `bp` file — developer-era test and demonstration
programs with no product function, not something an application ever
called. **`py_json`, `py_term`, `py_test` and `py_test2` were kept
deliberately**, as the documented examples for embedded Python, above.

**`pcl` is unaffected as a printer feature** — the `pcl` keyword and the
cataloged `pcl` routine in `gpl.bp` are both still there. What has gone is
a second, older copy of the source sitting in `bp`.

**SD ships only those four examples into the SDSYS `bp` file now.**
Everything else in it is yours — and because of that, **`bp` and its compiled objects
are preserved when you upgrade**,
alongside your accounts and the rest of your own data. An upgrade replaces
those four programs by name and touches nothing else in `bp`.

## Things that were never features, and are not coming

These are not removals. They are stated here because a reader coming from
another MultiValue system will otherwise assume they exist.

**Multi-user access over remote Desktop is not supported.** It follows from
the access model and is settled. One Windows setting covers Remote Desktop and
the physical keyboard together, so allowing one allows the other. If you want it, you want Windows Server, RDP client access licenses and
probably a commercial product built for it. See
[ssh access](08-ssh-access.html).

**SD cannot be installed silently.** `/SILENT` and `/VERYSILENT` are refused,
with a message saying why, and there is no switch to override it. Installing
ends by asking for a password, and a silent install has nobody to ask: it would
finish with **no password on any account**. Unattended deployment is not supported.

**`scp` and `sftp` do not work inbound once SD has configured the ssh server**,
for anybody, administrators included. This is the accepted cost of putting
every ssh session straight into SD. **Pull files rather than pushing them**, or use
`receive` and `send`, which move plain-text files over the same login once the
administrator has turned file transfer on (it is off as delivered). See [ssh access](08-ssh-access.html#the-cost-scp-and-sftp-stop-working-inbound).
A machine with no ssh server is unaffected, because SD has configured nothing.

**The cleartext API login is gone**, and a client that still sends a password
in clear is refused outright. See [API access](09-api-access.html).

## Linux-only mechanisms

The Linux privilege model does not survive the move and has been replaced
rather than emulated. Most of this is invisible unless you are reading source,
but two consequences show:

- **`chmod` does nothing.** The MSYS2 mount is `noacl`, so file-mode bits are
  not a security control here. Windows ACLs are, and SD sets them.
- **There is no `sdsys` uid to drop to.** Privilege is elevation, and the
  operating system's groups are the whole of the authorisation model. See
  [Security](12-security.html).
