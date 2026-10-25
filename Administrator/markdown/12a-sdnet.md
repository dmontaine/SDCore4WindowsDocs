Title: SDNet
Subtitle: The NET switch and the server definitions: what is in place for files on another SD server, and what is not there yet.

SDNet is the name for opening a file that lives on **another SD server** and using
it with `READ`, `WRITE`, `SELECT` and `LIST` as if it were local. **This release
has the permission (the NET switch), the list of servers, a person's own login on a
server (`set.netlogin`, kept as values derived from the password and never as the
password), and a VOC pointer of type `N` that opens a file on a defined server: for
reading, selecting and querying, and, only for a server defined `write` whose
administrator has also put the remote user in the Windows group `sdfileswrite`, for
writing and locking.** On the server side there is a second, narrower API route,
`sdfiles`, which lets a login work with files and do nothing else. **Nothing of
SDNet has been run from end to end on Windows yet** (see "What has and has not been
run" at the end of this page). The pieces that are not there are listed under "What
does not exist yet".

An earlier SDNet was removed (a `server;file` VOC entry over port 4245, with each
server's password in `sd.conf`, which any local user could read). **This is not
that.** Nothing from it is back: there is no `;` in a path, no port 4245 and no
password in any file.

## What SDNet is

- **Files on another SD server, read only unless two people say otherwise.** A server is
  `read` unless SDSYS defines it `write` on the client, and the administrator of the
  *target* must also allow writing for that remote user (`sdfileswrite`).
- **The same channel as the API.** The connection is the target server's own API port,
  TLS 1.3 with the SCRAM login bound to the TLS session, and no new listener. A full
  SD Core listens for the API on 4247.
- **Delivered off, and loosened by SDSYS.** The switch is off for every account,
  the list of accounts allowed to use a server is empty, and a server is
  `read` unless SDSYS says otherwise. SDSYS turns each on, one account and
  one server at a time.

## What is in this release

| | |
|---|---|
| the **NET switch** | `modify.account` *name* `net-on` / `net-off`, and `net-on` in `create.account user`. See [Accounts and Security](01-accounts-and-security.html#the-net-switch-net-on-and-net-off) |
| the **server definitions** | one file, `netservers`, in the `gcat` folder of the SDSYS directory |
| **`set.server`** | adds a definition, or replaces one |
| **`delete.server`** | removes one |
| **`list.servers`** | shows them |
| **`set.netlogin`** | a person makes their own login on a defined server: SD runs the SCRAM exchange once and keeps the derived values (see "Your login on a server") |
| **`delete.netlogin`** | removes it |
| the **files-only route** | the Windows group `sdfiles`, on the server being reached: `modify.account` *name* `files-on` / `files-off`, and `files-on` in `create.account user`. See "The files-only route on a server" below |

**The first three verbs are SDSYS's.** They are in SDSYS's VOC and in no other account's,
and each one also stops with "Command requires administrator privileges" for
anyone who is not the administrator. **`set.netlogin` and `delete.netlogin` are in
every account's VOC**, because they are for the person whose login it is; the
gates they ask are described below. Commands are shown here in lower case.

### What does not exist yet

- **A connection that is not one of three.** The only things in SD that open a socket
  to a server are `set.server` with the word `connect`, once, for the handshake
  alone, `set.netlogin`, once, for the login exchange, and opening a remote file
  through an `N` pointer (all below). No other verb, statement or program dials a
  server *defined* here. A definition is a record on disk and nothing reads it but
  these.
- **A check that a typed pin is right.** When you type the 64 digits, nothing
  connects and nothing checks them; use `connect` to have the server's own hash
  shown to you. `set.netlogin` and every remote open compare the key the server
  presents with the definition's pin before they send anything.
- **Using the login, apart from a remote file.** The only thing that reads a stored
  login to log in is opening a remote file through an `N` pointer (below).
  `set.netlogin` proves the login works once, at the moment it is made, and keeps
  the result.
- **A way to make the client use only the files-only route.** The server has the route
  (below), the client that opens remote files asks only for requests the route allows,
  and the person who runs the other server can give the remote user `files-on` instead
  of `api`. But `set.netlogin` does not require it. A remote user who is in `sdapi`
  still has the whole API, and so does a stored login made for that user: whoever
  holds the file can do on that server what that remote user can do over the API.
  Give the remote user `files-on` and not `api`, or choose the remote user with that
  in mind. **A files-only login is read only on the server unless the remote user is
  also in the Windows group `sdfileswrite`** (`modify.account` *name* `files-write-on`,
  below): without it the server refuses every write, delete, record lock, file lock
  and clear, and the locking forms of a read, whatever the client's definition says.
  The definition's `mode` on the *client* is still enforced there, but it is no longer
  the only thing between a stored login and a write: **a target's administrator
  decides whether a login may change anything on that target.**
- **Remote files.** A VOC pointer of type `N` opens a file on another server for
  reading, selecting and querying (see "Remote files, read only" below), and, only
  for a server defined with `write`, for writing and locking (see "Writing and
  locking"). Not there: anything that changes the structure of a remote file or its
  indices, `WRITE ... CREATING.SEQKEY`, `FCONTROL`, `CONFIGURE.FILE`, `ANALYSE.FILE`,
  making or deleting a remote file, and the index statements (`SELECTINDEX`, `SETLEFT`,
  `SETRIGHT`, `SELECTLEFT`, `SELECTRIGHT`, and the `AK` statements). They stop with
  message 12516 and nothing is sent. `INDICES()` of a remote file is the null string.
- **`NETFILES`** in `sd.conf` is not what this uses. Opening a remote file through an
  `N` pointer does not read it. The one thing that does is the API server's old request
  29, "open an SDNet file": it needs bit 2 of `NETFILES` and the same account rules as
  `logto` and the account's NET switch, and a files-only login can never make it (see
  [SD Admin Configuration](07-sd-admin-configuration.html)). What you can set in
  `sd.conf` for SDNet is the two waits, `NETWAIT` and `NETREPLY` (below).

## The security model

**Nothing a user can type chooses a host.** The only machines SD will ever be
asked to call are the ones SDSYS has written down, and only SDSYS can write them:
the file is replaced only by these verbs, and the verbs are SDSYS's. A program
cannot define, change or point at a server. (`set.server ... connect` is the one
connection that takes a host as typed: it dials the host SDSYS typed, for a
handshake, and sends nothing. Every other connection goes to a defined server.)
Two things must then both be true before an account can use one: it has the NET
switch (off by default), and it is named in that server's *accounts* list (empty
by default). Neither is a
judgement that nobody should have the capability; each is a decision about who
decides, and it is yours.

**The file holds no secret, and must never hold one.** A definition is a name, an
address, a port, the name of an account, and the hash of a *public* key. The file
can be read by every SD user on purpose, and only an administrator can write it.
A person's login on a server is kept somewhere else, in a folder only that person
(and the administrators) can open (see "Your login on a server").

## The file: `netservers`

It is a plain text file in the `gcat` folder of the SDSYS directory
(`C:\ProgramData\SD\sdsys\gcat\netservers` on a standard install), one definition
to a line, at most **ten**. It is kept in `gcat` and not in the SDSYS directory
itself because the SDSYS directory gives the group `sdusers` Modify, while `gcat`
gives it read and execute only: a file in the SDSYS directory could be rewritten by
any SD user who has an operating system prompt.

```
name|host|port|account|pin|mode|accounts|created
```

It is always written **whole**: the new text goes to `netservers.new` beside it
and is renamed over the old file, so it is never half written. A session that
changes it holds a lock for the length of the change (a second administrator
session that tries meanwhile is told to try again). The SDSYS session that
defines a server is the elevated one, which is what can write there.

| field | rule |
|---|---|
| **name** | a lower case letter, then up to 15 lower case letters or digits. Capitals typed are converted |
| **host** | 1 to 253 letters, digits, dots, hyphens or colons: a DNS name, an IPv4 address or an IPv6 literal. It does not start with a hyphen or a dot. Capitals are converted |
| **port** | a whole number from 1 to 65535: the port **of the server you are defining**, chosen when you define it (4247 for a full SD Core). SD does not insist on a number. `04247` is stored as 4247 |
| **account** | the account to enter on the remote server: 1 to 32 letters, digits, dots, underscores or hyphens. Kept as typed, because the other server's names are its own |
| **pin** | the SHA-256 hash of the server's public key: exactly 64 hexadecimal digits, stored in lower case. A new certificate with the same key keeps the same pin |
| **mode** | `read` or `write`. `read` unless `write` is given. What a program may do with the server's files, once it can open them |
| **accounts** | the **local** accounts that may use the server: registered account names separated by commas, no spaces, no empty name, at most 2000 characters, each listed once. **Empty means nobody**, and empty is what you get unless you list some |
| **created** | the date the definition was made, `yyyy-mm-dd`. Set by SD |

No field may hold a vertical bar, a control character or a character above the
ASCII range, so a line cannot be made into something else.

## Defining a server: `set.server`

```
set.server name host port account {pin | connect} {read | write} {accounts a,b,c} {no.query}
```

The fifth word is **either the pin, 64 hexadecimal digits, typed (no connection is
made), or the word `connect`** (SD fetches the hash and asks you to confirm it:
see "Getting the pin by connecting" below). Everything after it is optional and may
come in either order. `no.query` skips the question about replacing a definition,
**and never the question about trusting a key**. Capitals in the name, host, pin,
mode and account list are converted. Words are split at spaces, so nothing can be
quoted.

```
:set.server hq2 192.168.1.40 4247 sduser 5f29e23fd38c423996bef4450ba56aa16e11f06e926ddb0828b5d9649064b9b9
Server hq2 (192.168.1.40:4247) is defined
No account is listed, so no account may use server hq2 yet.  Set it again with accounts, and give each account the NET gate (modify.account name net-on)
```

(The pin above is an example value, not a real server's.) The last line is there
on purpose: a definition with an empty *accounts* list is complete and harmless,
and nobody may use it. To name accounts, give them with the definition:

```
:set.server hq2 192.168.1.40 4247 sduser 5f29e23fd38c423996bef4450ba56aa16e11f06e926ddb0828b5d9649064b9b9 read accounts fred,jane
Server hq2 is already defined (192.168.1.40:4247).  Replace it (y/<n>)?y
Server hq2 (192.168.1.40:4247) was replaced
```

Fewer than six words (the verb, then name, host, port, account and pin or
`connect`) print the usage and a reminder of where the pin comes from, and stop:

```
:set.server hq2 192.168.1.40 4247 sduser
Usage: set.server name host port account {pin | connect} {read | write} {accounts a,b,c} {no.query}
The pin is the server's public key hash: 64 hexadecimal digits from its administrator (nothing is dialled), or the word connect to see the hash the server presents and confirm it.  no.query never skips that question.
```

**Every field is checked before anything is written, and each field that is wrong
gets a message of its own**, so one run shows all of them:

```
:set.server hq2 -bad 99999 sduser abc
Host -bad is not valid: 1 to 253 letters, digits, dots, hyphens or colons, not starting with a hyphen or a dot
Port 99999 is not valid: a whole number from 1 to 65535
The pin is not valid: it must be exactly 64 hexadecimal digits
```

The other refusals have messages of their own: a name that is not valid, a remote
account that is not valid, a mode that is not `read` or `write`, an accounts list
that is not valid, and "Account *x* in the accounts list is not a registered
account" for a name that is not in the register (SDSYS is never in it, so it cannot
be listed). A refusal writes nothing.

**Replacing.** A name that is already defined is replaced, after the question
above, which defaults to no (and so does an input that ends). `no.query` goes
ahead without asking **that** question, and no other (see the next section).
**A replacement is the whole definition, not a merge:**
the accounts list is whatever the new command gives, so give it again. With ten
servers already defined, a new name is refused until you delete one.

### Getting the pin by connecting: `set.server ... connect`

Typing 64 digits from a message is how a pin gets mistyped, or swapped for the
wrong one. Give the word `connect` in place of the pin and SD fetches the hash
itself, shows it to you, and writes the definition only if you say the hash is
the right one:

```
set.server name host port account connect {read | write} {accounts a,b,c} {no.query}
```

`connect` may be in any case. This is what happens, in this order:

1. **Every other field is checked first**, exactly as above (the pin check is
   the only one left out, because there is no pin yet). **Nothing is dialled for
   a definition that would be refused.**
2. The definitions are read and the limit of ten is checked. If the name is
   already defined and `no.query` was not given, the replacement question is
   asked **before any connection**, so answering no (or ending the input)
   dials nothing.
3. SD opens a **TLS connection to *host*:*port*, waiting at most `NETWAIT` seconds (5
   unless `sd.conf` says otherwise; see "The two waits")**, and
   reads the SHA-256 hash of the public key the server presented. It closes the
   connection at once. **It is a handshake only: nothing is sent to the server.**
4. SD shows the hash and asks you to trust it. The answer defaults to no, and so
   does an input that ends.
5. On **y** the definition is written with that hash as its pin. On **n** nothing
   is written.

```
:set.server hq hq.example.com 4247 reports connect read accounts fred
Connected to hq.example.com:4247 (a TLS handshake only: nothing was sent).  The server presented a public key with this hash:
90b7bd01319812c22b8a37b3170d3026955a4e640bb9b216acf9db468475bc06
Compare it with the hash the administrator of that server gives you, by a way that does not use this network.  If it differs, answer n: something may be standing between this server and that one.
Trust this key (y/<n>)?y
Server hq (hq.example.com:4247) is defined
```

(The hash above is an example value, not a real server's. The hash is printed
alone on its line, in lower case, so it can be copied.) Answering n:

```
Trust this key (y/<n>)?n
The key was not trusted.  Nothing was written: server hq is as it was
```

**THE KEY QUESTION IS ALWAYS ASKED. `no.query` does not skip it.** `no.query` only
skips the question about replacing a definition that exists. An administrator
who scripts `set.server` with `no.query` and `connect` still has to answer
whether the hash is the right one, because that answer is the whole point of
`connect`: with no one to compare, the pin would be whatever answered the call,
and that is no check at all. A replacement with `connect` therefore asks two
questions when `no.query` is absent (replace, then trust) and one when it is
present (trust). When the input ends before an answer, the answer is no.

**Why you compare, and what to compare with.** SD does not check the server's
certificate against anything here: it has nothing to check it against, which is
what the pin is for. So the connection can tell you what key *something* at that
address holds, but not that the something is the server you meant. If another
machine were standing between the two (or the address were wrong), the hash
would be that machine's. **Compare the hash with one you get another way: ask the
administrator of that server, by telephone or in person or by a channel you
already trust, and not over the network this connection used.**

**What the hash is.** It is the SHA-256 of the server's **public key**, shown as 64
lower case hex digits (the certificate's SubjectPublicKeyInfo, DER encoded). It is
not the hash of the certificate. A certificate that is renewed over
the **same key** therefore has the same hash, and a pin does not go stale at a
renewal; a new key is a new hash and the pin has to be set again.

**How the other administrator gets the hash.** The administrator of the server
being defined asks that server for it. On a Windows SD Core server, `settings.report`
(see [Backup and Restore](01b-backup-and-restore.html)) writes a line
`public key sha256: ` followed by the 64 digits in the `[api]` section of its report.
It decodes the certificate in `C:\ProgramData\SD\sd-tls\api.pem` and never prints the
private key that is in the same file. If that section says
`certificate: not yet generated`, the server has no key to show yet. The line was
added to the report for this purpose and its figure has not yet been compared with
the one `set.server ... connect` shows for the same server (see "What has and has not
been run").

**When it does not work, nothing is written.** There is a message for each case:

| you see | meaning |
|---|---|
| `Cannot connect to host:port (status n, os error m).  Nothing was written` | the connection was not made: nothing is listening there, the address is wrong, or `NETWAIT` seconds passed |
| `The TLS handshake with host:port did not complete.  Is that the API port of an SD server?  Nothing was written` | something answered, but it did not complete a TLS handshake: most likely the port is not an SD server's API port |
| `host:port completed the handshake but gave no public key hash.  Nothing was written` | a TLS session was made but no hash could be read from it |

The first two are told apart by the operating system's error number, which is
zero for a handshake that failed after the connection was made. That is read off
the source and has not been tried against a closed port, a port that is not TLS
and an address that does not answer.

**One thing to know about the lock.** The definitions are locked from the time
they are read until the answer is acted on, which includes the connection (up to
`NETWAIT` seconds, 5 unless changed) and the time you take to answer. A second administrator session that
changes the definitions meanwhile is told to try again. The lock is so that the
definition cannot change between the confirmation and the write.

## Removing a server: `delete.server`

```
delete.server name
```

```
:delete.server hq2
Server hq2 was deleted
```

It does not ask: a definition is one line and `set.server` makes it again. A name
that is not defined gets "No server is defined with the name hq2".

## Showing them: `list.servers`

```
list.servers {name}
```

One line for each server: the name, *host*:*port*, the remote account and the mode
as *account*/*mode*, the pin cut to its first sixteen digits, and the local accounts
allowed (the word `none` when there are none).

```
:list.servers
hq2  192.168.1.40:4247  sduser/read  5f29e23fd38c4239...  fred,jane
hq  hq.example.com:4247  reports/read  90b7bd01319812c2...  none
```

With a name it shows only that server, with the **whole** pin, and the date it was
defined:

```
:list.servers hq
hq  hq.example.com:4247  reports/read  90b7bd01319812c22b8a37b3170d3026955a4e640bb9b216acf9db468475bc06  none
Defined on 2026-10-17
```

With none defined, on its own it says "No servers are defined". It changes nothing and takes no
lock. If the file holds a line these verbs did not write, all three stop and say
which line, "The server definitions file has a line that is not a definition",
without changing anything; correct the file at the operating system.

## Your login on a server: `set.netlogin` and `delete.netlogin`

A defined server is a name, an address and a key. To use it, a person also needs a
**login** on it: a user name and password that the other server knows. `set.netlogin`
is how a person gives SD that login, once, and `delete.netlogin` is how they take
it away. **They are the person's own verbs, in every account's VOC, and SDSYS does
not set a login for anyone else.**

```
set.netlogin name
delete.netlogin name
```

### What is kept: not the password

**SD never stores the password.** It is typed hidden, used once to work out some
values, and cleared from memory. What is kept is what the SCRAM-SHA-256 login
(RFC 5802 and 7677, the same login the API uses) derives from the password:

- the **salt** and **iteration count** the other server chose for that user,
- the **ClientKey** and the **ServerKey**, which are keyed hashes of a
  PBKDF2-HMAC-SHA-256 stretch of the password and the salt.

A later login needs those and not the password. That is the whole reason for
keeping them: the file can be used without anyone typing anything, and it is not
the password.

**What a person who reads the file can and cannot do.** Be exact about this,
because "not the password" can sound safer than it is.

- **They can log in as that remote user to that one server.** The ClientKey is
  the secret that proves the user, so having it is as good as having the password
  *for that server*. They cannot log in to a different server, because the salt
  and so the keys are different there, even if the password was the same.
- **They cannot read the password from it.** The keys are one-way. **They can
  guess it offline.** Anyone holding the salt, the count and a key can try
  passwords at their own speed and check each against the key, with no server
  involved. The iteration count (the server chose it; this release accepts nothing
  outside the API's own limits) slows that, but a weak password still falls to it,
  and a password that was reused elsewhere is then known elsewhere. This is why
  the file is kept private (below), and why the remote password should be a
  strong one that is not used for anything else.
- **The ServerKey does not let them pretend to be the server to you.** It would
  let a program produce a signature that looks right, but SD compares the key the
  server presents with the pin in the definition before it sends anything, and an
  impostor does not have the real server's private key.

### Where it is kept, and why there

```
C:\ProgramData\SD\sd-net\<Windows user name>\<server name>
```

- `sd-net` is made by the installer (`secure-sdnet.ps1`). SYSTEM and Administrators
  have full control of it and of everything below it. The group `sdusers` may list
  the folder and add a sub-folder to it, **this folder only**, and has nothing in
  what is made below. CREATOR OWNER has full control of what is made below, which
  is the person who makes it.
- `sd-net\<Windows user name>` is made by `set.netlogin` itself, as the person
  (there is no helper and no `sudo` on Windows). The person owns it, and what it
  inherits is SYSTEM, Administrators and that owner and nobody else, so no other SD
  user can read, write or rename anything in it, and an SD user cannot delete or
  rename another person's folder.
- The file is one line, written whole through a temporary file `<server name>.new`
  and renamed, so a failure leaves any older login as it was:

```
v1|remote user|salt (base64)|iterations|ClientKey (base64)|ServerKey (base64)|pin|created
```

`pin` is the pin of the definition *when the login was made* (64 hex digits) and
`created` is `yyyy-mm-dd`.

**Removing a person.** When the uninstaller removes a person's Windows account
(`remove-sdaccounts.ps1`) it removes that person's `sd-net` folder with it, and says
`server logins removed`. A stored login is as good as that server's password, and one
left behind would outlive the account that made it. Deleting a server definition does
not remove anyone's login (see `delete.netlogin` below).

**It is outside the account directory on purpose.** An account's programs reach
the operating system's files only through the account's own directory unless the
account holds the `sh` or `os.execute` switch. Anything kept inside an account
directory, or under the home directory, could be read by an account program with
`OPENSEQ`; a file in `sd-net\<user>` cannot be reached that way by an
account without those switches. That makes the file safe from the ordinary
account program. It does not make it safe from a person.

**The honest limit.** An account that holds the **`sh`** or the **`os.execute`**
switch can read anything its Windows user can read, and this file is something that
Windows user can read, **exactly as such an account can read the user's `.ssh`
folder**. The file's privacy is the operating system's privacy of that one user, no
more. If an account runs untrusted code with one of those switches on, a login kept
by the same Windows user is exposed to it. Two accounts of the same Windows user
share the one file for a server, because the file belongs to the Windows user and
not to the SD account. **The administrators of the machine, and SYSTEM, can read
every person's folder**: that is how the uninstaller removes it, and an administrator
can always take ownership of a file anyway.

**How a program reads it.** Only through an internal subroutine, `$netcred`, that
no ordinary program can call (its name starts with a dollar sign). Before every
use of the file or its directory, `$netcred` asks the C check `SD_FILE_PRIVATE`
(one of the SDEXT functions, key 111, again callable only from an internal
program). On Windows that check reads the access list: the path is a **plain file
and not a link** (no reparse point, so no junction or symbolic link), **owned by the
user who is running**, and its access list allows **nobody but that user, SYSTEM and
Administrators**; an access list that is missing altogether (which means everyone)
fails; and the folder it is in passes the same test as a folder. That is the test
`ssh` makes of a private key, read from the access list in place of mode bits. A file
or folder that fails it is **never opened**: the stored login is reported as not
trusted and nothing in it is used. `$netcred` also refuses a login made for a different
pin than the definition has now, so a login does not carry over to a server whose key
has changed (or to a server redefined under the same name).

### `set.netlogin`

```
:set.netlogin hq
Setting up your login on server hq (hq.example.com:4247).  Your password is used once here and is not stored
Remote user: reports
Remote password:
Your login on server hq as reports is stored.  The password is not stored
```

(`Remote password:` is typed hidden.) *Remote user* is the user name that the other
server has for you; it is not the *account* field of the definition (which is the
account entered on the other server later, once something uses the login).

**The checks, in order.** Every local check comes first and asks you for
nothing; the prompts come after them; the network comes after the prompts.

1. The command has exactly one word after it, and that word is a valid server name.
2. **The account has the NET switch**, or the session is the administrator.
3. **The server is defined**, and its pin is a well formed one.
4. **The account is in the server's *accounts* list**, unless the session is the
   administrator's.
5. The session is a Windows user that can keep a login: not SDSYS (message 12467),
   and a user name that can be a folder name (message 12468 otherwise).
6. **The folder is ready:** `sd-net` must exist (the installer made it), and SD makes
   `sd-net\<your name>` if it is not there. Then it asks `SD_FILE_PRIVATE` whether that
   folder is private and the person's own. A folder that is not there or is not
   private ends the command with message 12468 and nothing done.
7. The two prompts. A user name that is empty or not valid (letters, digits,
   dots, underscores and hyphens, up to 32) ends the command before the password is
   asked. An empty password, or input that ends, ends it too.
8. **One TLS connection** to the host and port of the definition, waiting at most
   `NETWAIT` seconds (5 unless changed).
9. **The key the server presents is compared with the pin, before anything is
   sent.** A different key ends the command with nothing sent and the password
   still unspent.
10. The server's one-byte acknowledgement, then the SCRAM exchange exactly as the
    API client makes it: two packets from SD, two replies from the server, bound to
    the TLS session. SD checks that the server's nonce extends its own, that the
    iteration count is a whole number within the API's limits, that the salt is
    well formed, and **that the server's signature is right**, so the server has
    to know the password too. Each read or write waits at most 15 seconds.
11. Only then is the login written, through `$netcred`.

**Nothing else is sent.** No account is entered on the other server and no quit
is sent; the connection is closed when the exchange ends. On any failure nothing
is stored, and **an existing login is left exactly as it was**. When the exchange
succeeds, an existing login for the same server is **replaced without a question**,
because the person has just proved the new one.

**When it does not work:**

| you see | meaning |
|---|---|
| `Usage: set.netlogin server` | the wrong number of words |
| `Server name x is not valid` | not a lower case letter followed by up to 15 lower case letters or digits |
| `This account does not have the NET gate, so it cannot log in to a server.  Ask the administrator (modify.account x net-on)` | no NET switch |
| `No server is defined with the name x` | there is no such definition |
| `Account x is not listed for server y.  Ask the administrator to list it (set.server ... accounts)` | the account is not in the definition's list |
| `The administrator has no Windows login of its own to keep a server login in.  Use an ordinary user's account` | the session is SDSYS |
| `The directory for your server logins is not ready or is not private (...).  Nothing was done` | `sd-net` is missing (an installation from before this release has not been given it), your folder could not be made, or it failed the private check; the text in the brackets is the folder |
| `The remote user name is not valid (...)` / `A password is required.  Nothing was changed` | the prompts |
| `Cannot connect to host:port (status n, os error m).  Nothing was sent or stored` | nothing is listening, the address is wrong, or `NETWAIT` seconds passed |
| `The TLS handshake with host:port did not complete.  Nothing was sent or stored` | something answered but not with TLS |
| `The server at host:port gave no public key hash.  Nothing was sent or stored` | a session was made but no hash could be read |
| `The key presented by host:port is not the key in the definition of server x.  Nothing was sent to it and nothing was stored.  It is not the server that was defined, or its key was renewed` | the pin check. If the other server really did get a new key, define the server again (with `connect`) and then run `set.netlogin` again |
| `The connection to host:port failed or timed out at ...` | a read or write of the exchange failed or waited 15 seconds |
| `The server's first message was not valid (...)` | the server's reply was not what the exchange allows |
| `The server refused the login (...)` | wrong user name or password, or the server will not allow it; the server's text, if any, is cleaned to printable characters and cut |
| `The server's signature did not verify, so it does not know the password or is not the real server` | the final check |
| `The keys could not be derived (...)` | SD could not work out the values; the final message was not sent |
| `The login for server x could not be stored or removed (...)` | the last step failed; any older login is as it was |

### `delete.netlogin`

```
:delete.netlogin hq
Your login on server hq was deleted
```

It removes **your** login on that server and nothing else. It asks for no switch,
since removing a login adds nothing to what an account may do, and it connects to
nothing; the definition is not touched. If there is no login:
`There is no login stored for server hq.  set.netlogin hq makes one`. **A file
that is not the plain private file `set.netlogin` makes is refused and left where
it is** (the message says the stored login is not trusted); a person with such a
file in the way removes it at the operating system.

`delete.server` leaves people's login files behind. They are inert: a login made
for a pin the definition no longer has is refused, so it cannot be used. But a
server defined again under the same name *with the same pin* finds them valid, so
people who do not want that run `delete.netlogin` first.

### Where it works

`set.netlogin` and `delete.netlogin` are meant for a **local session of an ordinary
Windows user**: the file is that user's and the ownership check is made against the
user the session runs as. Whether they work in an API session has not been tried,
and a check that cannot tell whose the file is fails closed (the stored login is
"not trusted"). SDSYS has no login of its own to keep.

## The files-only route on a server

This section is about the server being **reached**, the one whose administrator is
giving somebody a login. (The same machine is that server for others and the client
for its own people, so both halves can be yours.)

The only way to log in to a server's API used to be membership of the Windows
group `sdapi`, which gives everything the API offers: execute commands, call
subroutines, enter other accounts with `logto`, work with sequential files and files.
A stored SDNet login on that route, taken from a machine, would give whoever took it
all of that. **So there is a second route, the Windows group `sdfiles`: a login that is
in `sdusers` and `sdfiles` and not in `sdapi` is let in "files only".** The rest of
the rules, the table of what is allowed and refused and why, the words and the
messages are in [Accounts and Security](01-accounts-and-security.html#the-files-only-route-files-on-and-files-off); in short:

- **`sdapi` wins.** A remote user who is in both groups has the whole API.
- **A user in neither group is refused**, as before. Both groups are empty for a new
  account until the administrator of that server adds the person
  (`modify.account` *name* `files-on`, or `files-on` when the account is made).
- A files-only session may open and close files; read records; select, read the next
  id and read and save lists; ask about locks and release them; use indices; ask for
  file information; and set its account **once**, which is the entry after login.
  **With the write group as well** (next section) it may also write and delete
  records, take record and file locks (and read with a lock), and clear a file.
  **It may not** call a
  subroutine, execute a command or answer its prompts, enter another account,
  use sequential files, read variables, run `system()`, `trans()` or an evaluation or
  conversion, run a transaction, or open an SDNet file on a third server. Any other
  request, and any request number this release does not know, is refused: the table
  is an allow list.
- A refused request is not carried out. It is answered with "This login is for files
  only: request *n* is not allowed" and written to the audit trail; the connection
  stays up.
- Everything else about the session is as for any other API login: the account has to
  be entered, its switches (OS access, the edit switches, NET) apply, `SDCLIENT` still
  applies, and SDSYS is never made files-only.
- **It is a read-only route unless the remote user is also in `sdfileswrite`** (next
  section). The table above is what `sdfiles` alone allows: the writes, deletes, locks
  and clear are in it only for a login that also has the write group.

**How the Windows API serves it.** The API listener runs as LocalSystem and hands a
signed-in connection to a new session that already has the person's identity. That
session works out for itself, from the Windows groups and live, whether it is files
only and whether it has the write group: `sdapi` first (it wins), then `sdfiles`, then
`sdfileswrite`. A person in neither `sdapi` nor `sdfiles`, or whose groups cannot be
read, is refused and never reaches the request loop. A group that cannot be read at
all counts as **not** a member, so a doubt never grants write.

### The write group: `sdfileswrite`

**A login on the target server may change something only if the target's administrator
allows it.** That is why a *write* server definition on a client is not enough by
itself: the definition says what the client is willing to do, the write group says
what the target is willing to let that login do.

- The Windows group **`sdfileswrite`** is made, empty, by the installer beside `sdfiles`.
  SDSYS gives it to one person at a time on the server being reached:
  `modify.account` *name* `files-write-on`, taken away with `files-write-off`, and
  `files-write-on` after `files-on` in `create.account user`. **It is off for a new
  account.**
- **`files-write-on` needs `files-on` first.** The group alone gives nothing (the login
  route is `sdfiles`), so for a person who is not in `sdfiles` it is refused: "Account
  *name* does not have FILES access, so it cannot be given FILES-WRITE: use files-on
  first" (message 12528). `create.account user` *name* `files-write-on` without `files-on`
  is refused the same way before anything is made. A group or other account is refused
  as for `files-on`.
- **`files-off` takes the person out of `sdfileswrite` too, and first**, so a later
  `files-on` does not hand the write back without you saying so. It removes the write
  group, reads it back, then removes `sdfiles` and reads that back, and it does the work
  for a person who is in only one of the two: a person who is in `sdfileswrite` and
  not in `sdfiles` (a removal that stopped half way, or a change made by hand) is
  taken out of it. If a removal fails the command says so ("Unable to change remote
  access for *name*, status: *n*") and stops: a failure of the write group's removal
  leaves the person exactly as they were, and a failure of the second removal leaves
  them in `sdfiles` alone, with read access and never write access without read. **In
  that second case the command says what did happen before it says it failed**: it
  prints `Account fred has files-write no` and writes the audit line
  `modify.account files-write-off account=fred` for the removal that worked, so the
  screen and the trail agree with the group. When the write group went and the command
  went on to succeed, the same line `Account fred has files-write no` comes before
  `Account fred has files no`.
  `files-on` removes a leftover `sdfileswrite` membership **before** it adds `sdfiles`,
  and stops with the same failure message if it cannot; if the leftover went and the add
  of `sdfiles` then fails, the person is left in neither group, and the command says so in
  the same way (`files-write no` line, `files-write-off` audit line, then the failure).
- **What it changes.** Without it a files-only login is refused: write (16), writeu (17),
  delete (18), deleteu (19), lock record (30), clearfile (31), file lock (32) and file
  unlock (33), a test of a lock (34, which is what `RECORDLOCKED()` sends), the four
  locking reads (7 to 10), and a `READV` with a lock flag. They are
  answered "This login cannot change or lock files here: ask the administrator for
  files-write-on (request *n*)" (message 12526) and **nothing is carried out**. Reads,
  selects, `READV` without a lock, file information, the indices and `RELEASE` still work. (A
  test of a lock names the holder by his user number on this server, which a login that
  cannot lock has no business with.)
- **`sdapi` is not touched.** A remote user in `sdapi` has the whole API as before, with
  or without the write group, and SDSYS is never made files-only.
- **The refusal is in the audit trail of the target**, in lower case:
  `api refused request=16 route=sdfiles write=off user=name`, and a login by this route is
  written `api login route=sdfiles write=on user=name` (`write=off` for a login without the
  group). **The person at the client is told why**: a program that does not trap the error
  with `ON ERROR` stops with message 12505, "Server *name* answered *write* with an error:
  This login cannot change or lock files here: ask the administrator for files-write-on
  (request 16)". A program that traps the error with `ON ERROR` sees `STATUS()` 7000. The
  audit trail on the target also has the request number.
- **The group is read at login**, from the Windows groups, so a change takes effect at the
  person's **next** login on that server, and a refusal to read the groups refuses the
  login.
- **The consequence for existing definitions.** A server defined `write` on a client
  stops writing the day the target runs this release, until the remote user is given
  the group there (one `modify.account` word on the target). Reads are unaffected.
- An installation made before this release has neither group until the installer is run
  again; until then `files-on` and `files-write-on` say that the group does not exist
  and change nothing.

**The remote user must be a real account on that server.** It is still a Windows user,
a member of `sdusers`, with an SD account of its own, and every gate that account has
there applies to it. What `files-on` replaces is the need for `sdapi`, not for the
account. An administrator who wants an SDNet login for a person on another SD server
creates it there with `create.account user` *name* `files-on` (no `api`; add
`files-write-on` only if the person is to change files there), then gives
the name and the password to the person, who runs `set.netlogin` here.

**The client.** The SDNet client logs in with the stored login (made by
`set.netlogin`) and uses only the requests this route allows, so that it needs no more
than `sdfiles`, plus `sdfileswrite` for a server defined `write`. Opening a remote file
through an `N` pointer is the client. `set.netlogin` itself makes the login exchange as it
always did, which does not depend on the route: the server decides the route at the end of
the exchange.

**On the machine being reached:** the groups `sdfiles` and `sdfileswrite` are made, empty,
by the installer beside `sdssh` and `sdapi`, and removed by an interactive uninstall (a
silent uninstall leaves all of the groups). The API listener has to be on
(`remote.api`, see [Remote Access and the Machine](05-remote-access-and-the-machine.html)),
as for any API login.

## Remote files, read only

A VOC entry whose first field is `N` names a file on another SD server. It has two more
fields: the server's **name** as defined with `set.server` (field 2) and the file's name
on that server (field 3). Names are lower case; the server name is a letter and up to 15
letters or digits, the file name up to 63 letters, digits and `. _ - $`. Anything else is
refused.

```
N
nfa
customers
```

Opening it with `OPEN 'customers' TO f` (using the VOC name) gives a file variable that
`READ`, `MATREAD`, `READV`, `SELECT`, `SELECTV`, `SSELECT`, `FILEINFO` and `CLOSE` work on, and
`GETLOCKS()` (the local view, see "Writing and locking" below).
`RECORDLOCKED()` is **not** on this list: it needs a `write` definition and the write group like
a lock (see "Writing and locking" below).
`OPEN 'DICT', 'customers' TO d` opens the **dictionary** of the remote file, from the same
server, and the same statements work on it. (The client asks for it as `dict customers`,
in lower case. The server opens `dict` and a name, in any case, as a dictionary. A client on
this release against a server that has not been updated cannot open a dictionary.)
**Nothing else does.** Every other statement
given the file variable (writes, deletes, `CLEARFILE`, locks including `FILELOCK` and
`FILEUNLOCK`, `AKREAD`...) stops with
message 12506 (or, with `ON ERROR`, sets `STATUS()` and goes on), and nothing is sent to the
other server. `OPENPATH`, `OPENTEMP`, `OPENSEQ` and `CALL "file program"` never see such a
pointer.

**Queries.** `LIST`, `COUNT`, `SORT`, `SELECT`, `SSELECT`, `LIST.ITEM` and `LIST DICT` work on
the VOC name, with the dictionary read from the server. A `SELECT` takes **every record id** of
the remote file in one reply and turns it into an ordinary select list; each record a query
needs is then one request to the server, so a query that reads every record of a big file costs
one round trip per record, and a `WITH` clause reads each record. An id list given on the
command line (`LIST customers 'c2'`) selects nothing and reads only those records.
**A remote file has no index here:** `INDICES(f)` is the null string and a query reads the
records, so an index the other server holds is never used. A remote file
answers `FILEINFO(f, FL$TYPE)` with 7 (`FL$TYPE.NET`).

Who may open one, checked in this order before anything is dialled: the account holds the
**NET switch** (or is SDSYS), the server is defined, the account is in the definition's
*accounts* list, the user has a stored login (`set.netlogin`) and the server's key still
matches the pin, and the limits (10 servers, 100 open remote files per process) hold.
An `$internal` program is not exempt. Each failure has its own message and an audit line,
`netfile refused server=... reason=...`; a success writes `netfile open server=... file=...`.

**Who may write the pointer.** The VOC is protected by the `voc.edit` switch, which is off
for an ordinary account, so only SDSYS or an account SDSYS has given `voc.edit` can make
one. The switch that matters for *using* it is the NET switch of whoever opens the file.

The login to the other server is the stored one of the person running the program, made
with `set.netlogin`; the connection is the other server's API port, TLS 1.3, with the
pinned key checked before a byte is sent. A connection that dies is noticed on the next
use and reported; it is never quietly remade in the middle of an operation. All of a
process's connections end when the process does, and **at `LOGTO`**: going into another account,
and coming back, closes every connection and invalidates every remote file variable opened before
(a `READ` on one is an error), so a remote file never follows a person into an account that was
not asked whether it may use it. A new `OPEN` dials again.

**The record cache.** To save requests, a process keeps the last 64 records it `READ` from remote
files for **2 seconds**, and the fact that the server did not have a record. A second `READ` of the
same record from the same file variable in that time is answered from memory. This means a `READ`
can show a record up to 2 seconds old: a program that waits for another user's change to a remote
record sees it up to 2 seconds late. A record over 32,768 bytes is not kept, `READV` is not cached,
and the entries of a file go when it is closed, when it is `SELECT`ed again, and at `LOGTO`. Ids
are kept as given, so `READ`s of `JACK` and `jack` are two entries.

**What is not here yet:** saved lists on the remote side.

### Which remote files work

A remote file is whatever the remote **account's VOC** names, opened by the server with its
ordinary `OPEN`, so the rules are the server's. What the client adds is on this page: the
name is 63 characters or fewer, an id is 1 to 63 characters (anything longer is refused on
the client before it is sent), and what a program receives is the record the server sends,
with the marks as the server holds them.

## Writing and locking: the definition's `write` mode

A server is `read` unless SDSYS defined it with the word `write` (`set.server ... write`).
**With `read` nothing changes from the section above: every statement that changes or locks a
remote file is refused with message 12506 and nothing is sent.** With `write`, a file opened
through an `N` pointer to that server can be changed and locked by the statements below, for
every account that holds the `net` switch and is on the definition's *accounts* list.

**The mode is the client's.** It is a field of the definition on the machine that is
reading; the server it points at is never told. The server's own limits still apply to the
stored login: the files-only route lets a login write and delete, the server's `voc.edit`,
`dict.edit` and `bp.edit` switches (off by default) refuse a write to a VOC, dictionary or
program file of the remote account, and the remote user's own file permissions decide the
rest. The mode is looked up when the file is opened **and again on every change**, so
`set.server ... read` stops writes through a handle that is already open; a handle opened
while the mode was `read` does not write after the mode is changed to `write` until it is
opened again.

| Statement | What happens |
|---|---|
| `WRITE`, `WRITEU`, `MATWRITE` | one request; the record is written on the server. `WRITE` releases the session's lock on the record, `WRITEU` keeps it |
| `WRITEV`, `WRITEVU` | read the record (never from the cache), change the field, write it, as for a local file |
| `DELETE`, `DELETEU` | one request; a record that is not there is not an error |
| `CLEARFILE` | one request; a big file can take minutes, and the connection is only called lost after five |
| `READU`, `READL`, `MATREADU/L`, `READVU/L` | the lock, then the read; a busy record takes the `LOCKED` branch (`STATUS()` is the holder) or, without a `LOCKED` clause, the statement tries again every quarter of a second until the lock is free |
| `RECORDLOCKU`, `RECORDLOCKL` | the lock, with the same busy behaviour |
| `FILELOCK` | one request for the **whole file's** lock; a busy file (another user's file lock, or another user's lock on any record of the file) takes the `LOCKED` clause and `STATUS()` is the holder's user number on that server; with no `LOCKED` clause the statement asks again every quarter of a second. **Only for a server defined `write` and a login in the other server's `sdfileswrite` group** |
| `FILEUNLOCK` | one request; `STATUS()` afterwards is 0 (it was this session's and is free now), 3011 (another user's, still held) or 3012 (nobody held it), as for a local file. Same conditions as `FILELOCK`. It is never stopped by the definition being set back to `read`: giving a lock back changes no data |
| `RELEASE` | the record form, the file form (which also gives the file lock back) and plain `RELEASE` (every lock this process holds on a write-mode server) |
| `RECORDLOCKED()` | the other server's answer (-3 -2 -1 another user holds a file, update or read lock; 0 none; 1 2 3 this session holds a read, update or file lock), and `STATUS()` is the lock owner's user number on that server. **Only for a server defined `write` and a login in the other server's `sdfileswrite` group**, like a lock. A `read` definition stops the program with message 12506 (`recordlocked`) and nothing is sent; a login without the write group is refused by the other server (message 12505 with its text, "request 34"). It is allowed inside `BEGIN TRANSACTION` for a `write` definition: it changes nothing, so a rollback has nothing to undo |
| `GETLOCKS()` | **the local view, for either mode, and nothing is sent**: the one field of three counters (`NUMLOCKS`, the lock count, the peak) of *this* machine's lock table and no lock line. The locks of a remote file are held on the other server and never appear here, in `GETLOCKS()` or in `LIST.READU`; look on the other server for them. `GETLOCKS()` is an internal-programs-only function |

**A verb that takes the file lock works.** `CLEAR.FILE` locks the file, clears it and gives the
lock back, so on a write-mode remote file it clears one, to the same two conditions as a
`CLEARFILE` statement in a program (and the edit gates by the remote file's name still apply). The query
processor's `LOCKING` keyword (`LIST customers LOCKING`) takes the same file lock and works the same
way; a `read` definition still stops both, because `FILELOCK` is refused there.

Locks are held by the connection: closing the file variable releases the locks taken through
it (a file lock too), ending the process or a `LOGTO` closes the connection and releases them all, and a file
variable that merely goes out of scope has its close sent at the next prompt. Waiting is done
by asking again, so it costs about four requests a second and two machines cannot detect a
deadlock between them. **The wait is never done by the other server:** the client always sends
the "do not wait" form of a lock request (the wait flag of API request 32 is 0), so a wait cannot
look like a lost connection and the break key ends it.

**A file lock keeps everyone else out of a whole file** (they cannot take a read or update lock on
any record of it, or a file lock). That is what `FILELOCK` is for, and it is also why it is held
to the same two conditions as a write: your definition says `write` **and** the other server's
administrator put this login in `sdfileswrite`. A login that is only in `sdfiles` is refused by
the other server with message 12526 and the line `api refused request=32 route=sdfiles write=off
user=...` in its audit trail. The administrator of the server that is reached sees a file lock in
`list.readu` (type `FX`, on the server's own user number) and can clear one with
`unlock file n filelock` (see [Sessions and Locks](02-sessions-and-locks.html)); the lock also ends when the session that
holds it does. The first `FILELOCK` through each file variable is audited on the client
(`netfile filelock server=... file=...`); a file lock waited for is one line, not one for each
request.

**`RECORDLOCKED()` is held to the same two conditions.** It asks the other server who holds a
record, and the answer names the holder by his user number on that server, so it is not offered
to a login that cannot lock. A `read` definition stops the program with message 12506
(`recordlocked`, "The file on server ... is read only: recordlocked is refused. Nothing was
sent") and **nothing reaches the other server**. That is the clear text; the wall is on the other
server, where request 34 is in the change set of the files-only route: a login that is only in
`sdfiles` is refused with message 12526 and the line
`api refused request=34 route=sdfiles write=off user=...` in that server's audit trail, whatever
this machine's definition says, and a program is told by message 12505 with that text ("request
34"). `RECORDLOCKED()` has no `ON ERROR` clause, so a refusal always stops the program. Inside
`BEGIN TRANSACTION` it works for a `write` definition: it is a read of the lock table and changes
nothing, so unlike a lock it has nothing for a rollback to undo. **One consequence:** under
`MUSTLOCK` the check that this session holds the lock is the same request, so for a login
without the write group the check itself is refused by the other server, and a write or delete
ends with `STATUS()` 7000 and message 12505 naming request 34 instead of `STATUS()` 3023; nothing
is written in either case.

**Never repeated.** A change that gets no answer (the connection dropped, the server stopped)
is *not* sent again: its outcome is not known. Without `ON ERROR` the program stops with
message 12514 ("it is not known whether the change was made"); with `ON ERROR` `STATUS()` is
7000. The handle and every other handle of that server are dropped; open the file again and
read the record to find out.

**What is refused even with `write`.** A change or lock inside `BEGIN TRANSACTION` (message
12515: a remote write can't be rolled back, so it never joins a local transaction; this holds for
`FILELOCK` and `FILEUNLOCK` too, where openQM's QMNet lets them through without a rollback, which
is a silent loss of the guarantee the program asked for); the statements that only read an index,
`OPENSEQ` and the other sequential-file statements; and everything under "What does not exist
yet" (message 12516). `MUSTLOCK` and `$MODE AUTOLOCK` are honoured as for a local file: a write
without the lock held is refused with `STATUS()` 3023 (for a login without the write group see
`RECORDLOCKED()` above).

**The local edit gates apply by the remote file's name.** A write, delete or clear of a remote
file that is a VOC, a program file or a dictionary (`OPEN 'DICT', ...`) needs the account to
hold `voc.edit`, `bp.edit` or `dict.edit` as it would for a local file (messages 12410 to
12412).

**The cache is off for a write-mode handle**, so a record is never read from memory a second
before it is changed; a `LIST` or `SORT` over such a file makes about twice the read requests.

## The two waits: `NETWAIT` and `NETREPLY`

Two settings in `sd.conf` (and readable with `config('NETWAIT')` and `config('NETREPLY')`,
listed by `config`) say how long SD waits on another server. Both are in **seconds, 1 to
3600**, and both are per computer, not per server definition:

| setting | what it bounds | default |
|---|---|---|
| `NETWAIT` | the connection: `set.server ... connect`, `set.netlogin`, and the first use of a defined server by an `OPEN` of a remote file. **Each of the two steps of making it has this long: the TCP connect, then the TLS handshake** | 5 |
| `NETREPLY` | each wait for a reply from the server once connected, in the login and in every request, **whatever the server has sent meanwhile** (the TLS session tickets, or half of a record, do not use the wait up) | 30 |

A server that is slower than `NETREPLY` is treated as lost; **a changing request that gets no
answer is never sent again** whatever the setting is. A `CLEARFILE` waits for the longer of five
minutes and `NETREPLY`, because a big file takes longer than a reply bound. The login exchange of
`set.netlogin` keeps its own 15 seconds for each packet. **A zero is refused**, and SD does not
start with `NETWAIT=0` or `NETREPLY=0` in `sd.conf` (openQM reads zero as "wait for ever"; here
that is never what an administrator of a pinned peer wants). **A value that is too large is
refused whatever it looks like in 16 bits**: the two are 32 bit values and SD does not start
with `NETWAIT=65541` (`PWDELAY` and `DHCACHE` are read the other way and still wrap). The names
are eight characters or fewer because `config()` reads no longer one. openQM's `NETDELAY`, which
keeps a connection open after the last file is closed, is not this and does not exist in SD.
See also [SD Admin Configuration](07-sd-admin-configuration.html).

**A reply that cannot be true.** The client reads the length a reply announces before it reads
the reply. A server that announces less than the ten bytes of its own header, or more than the
largest string SD can hold (a little over a gigabyte), is treated as a lost connection at once:
nothing of it is read, a changing request answers 12514 as for any lost reply, and the
connection is dropped. Nothing is refused that a real record could
need: the ceiling is the size of the largest record. **The ceiling applies once the login is
over.** The login exchange itself has no ceiling on the length a reply announces (only the test
for less than ten bytes), so a server whose key you have pinned, and which has turned hostile,
can still announce a large length in a login reply and send slowly, for `NETREPLY` seconds a
read; the pin is what you trust it with.

**The silent server.** A server that completes the TLS handshake and then sends nothing at all,
or sends half of a TLS record and stops, is given up on at `NETREPLY` seconds (and a server that
accepts the connection and never answers the TLS hello at `NETWAIT` seconds). After the handshake
a TLS 1.3 server sends its session tickets; the read is made without waiting and the wait is on
the connection, for the time that is *left* of the caller's limit, so the tickets and a half
record cost what they have used and no more. What the caller sees is what it always saw for a lost connection:
`set.netlogin` and the login of an `OPEN` say "No acknowledgement from host:port at the start of
the session", "No reply from host:port during the login" or "The TLS handshake with host:port
did not complete"; a request that was sent and got no answer is message 12502 (message 12514 for
a change, and **a change that got no answer is never sent again**). A reply that stops in the
*middle of its body* is the same lost connection as a reply that never started, with message
12502 and the connection dropped. A server that sends a little at a time and never stops is
still waited for one read at a time; the limit is for each read, not for a whole reply.

`OPEN.SOCKET` takes the number of seconds to wait for the connection as its fourth argument
(`NETWAIT` for every SDNet caller); see the User set's page on sockets.

## What is audited

Defining and deleting are written to the audit trail, in lower case:

```
set.server name=hq2 host=192.168.1.40 port=4247 mode=read replaced=no pin=typed
set.server name=hq host=hq.example.com port=4247 mode=read replaced=no pin=confirmed
delete.server name=hq2 host=192.168.1.40 port=4247
set.netlogin server=hq remote=reports
delete.netlogin server=hq
```

The last word of a `set.server` line says how the pin was obtained: `pin=typed`
for 64 digits typed in the command, `pin=confirmed` for a hash that SD fetched with
`connect` and SDSYS answered y to. The pin itself is not in the line (it is not
secret, only long). A refusal, a declined replacement, a key that was not trusted,
a connection that failed and `list.servers` write nothing. `set.netlogin` and
`delete.netlogin` write a line **on success only**; the `set.netlogin` line carries
the remote user name you typed, and **no password, key, salt or hash is ever
audited**. A refusal, a failed exchange and a login that was not stored write
nothing. Giving or taking the NET switch is
audited like every other `modify.account` word (`modify.account net-on
account=fred`).

On the client, a write-mode handle adds lines in lower case (no record data, no id):

```
netfile open server=hq file=customers mode=write
netfile write server=hq file=customers
netfile delete server=hq file=customers
netfile clear server=hq file=customers
netfile filelock server=hq file=customers
netfile refused server=hq reason=mode
netfile lost server=hq op=write
```

`write` and `delete` are written the first time through a handle, `clear` every time, `filelock`
the first time a `FILELOCK` is tried through a handle (before the request, so an attempt the other
server refuses is on the trail too; waiting for a busy file is many requests and one line),
`refused ... reason=mode` once per handle when the definition says `read` by then, and `lost` when a
change got no answer. A lost connection during a `FILELOCK`, `FILEUNLOCK` or `RECORDLOCKED()` is
not a `lost` line: they change no data, so it is message 12502 and nothing else. The refusals the kernel makes itself (a read-mode handle, a transaction,
an edit gate) write nothing.

On the server that is reached, the files-only route writes, in lower case:

```
api login route=sdfiles write=off user=reports
api refused request=20 route=sdfiles write=off user=reports
modify.account files-on account=reports
modify.account files-write-on account=reports
api login route=sdfiles write=on user=reports
api refused user=reports reason=not a member of sdapi or sdfiles
```

The first is a successful files-only login (`write=on` when the person is also in
`sdfileswrite`, as in the fifth line), the second a request the route does not allow or, for a login
without the write group, a change or a lock (the number is the request; `write` is the state of the
login), the third and fourth the administrator giving the route and the write group, and the last a
login of a person who is in neither `sdapi` nor `sdfiles`. All of them are written on the server being reached.

## What has and has not been run

On Windows the code for all of this is carried from SD Core for Linux and compiled, and the free
checks (the guards that read the source) pass. The one new piece of Windows code, the test of the
access list that stands in for the file modes (`SD_FILE_PRIVATE`), was run against real access
lists: a file and folder of the person's own pass, and an Everyone entry, a `sdusers` entry, a
junction, the wrong kind of object, a path that is not there and a foreign owner each fail.
**Nothing of SDNet has been run from end to end on Windows yet**: no `set.netlogin` against a
server, no remote file opened, no write group changed on a real machine, no connection between
two machines. The figure `settings.report` prints as `public key sha256:` has not been compared
with the one `set.server ... connect` shows for the same server. The installer step that makes
`sd-net` and the two groups has been compiled, not run. Until these are run, treat every
statement on this page about what the code does as read from the source and not seen.

## See also

[Accounts and Security](01-accounts-and-security.html) for the NET switch beside the
other per-account switches. [Remote Access and the Machine](05-remote-access-and-the-machine.html)
for the API listener a server's port refers to. [SD Admin Configuration](07-sd-admin-configuration.html)
for `NETWAIT`, `NETREPLY` and `NETFILES`.
