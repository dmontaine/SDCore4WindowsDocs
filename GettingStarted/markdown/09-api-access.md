Title: API access
Subtitle: The client API, the port it answers on, the login that replaced the old one, and what a remote session may reach.

**The API is a normal way for any account to use SD.** A person running a
custom GUI program that talks to SD needs API access and may need nothing
else — no ssh, no terminal. An account with `api` access is an ordinary
thing to create, and probably the commonest shape a deployed system will
have:

```
create.account user jane api
modify.account jane api
```

**An account has it only if SDSYS gave it — a new account has none, and `api`
(or `both`) gives it.**

Your application code does not change. `SDConnect()` and `SDConnectLocal()`
take the same arguments and return the same things. **What changed is
underneath: the login protocol, the encryption of the connection, the port, the
identity a session runs as, and what it is allowed to open.**

> **SDSYS is the one exception: from another computer it has no API access
> until the administrator opens that door**, and then only from the addresses
> named — see [Reaching the port is not getting in](#reaching-the-port-is-not-getting-in)
> below. **Every other account has no API access until SDSYS gives it** —
> `modify.account` *name* `api` (or `both`), or `api` at `create.account` — and
> an account that has not been given it is refused at the door.

**There is a second, narrower route for a client that only needs files.** An
account SDSYS gave `files-on` (and not `api`) can log in over the API but is
held to files: opening, closing, reading, writing, deleting, selecting, locking,
indices and file information. A request to call a subroutine, execute a
command, enter another account (`logto`), read a variable or use a sequential
file is refused with *"This login is for files only: request n is not
allowed"*, and the connection stays open. An account with `api` has the whole
API whether or not it also has `files-on`. This is the route SDNet's logins are
meant to use.

## The login is SCRAM-SHA-256, and the old one is gone

**A client that sends a password in clear is refused.** It gets *"Cleartext
login is no longer supported; this server requires SCRAM authentication"* and
the connection drops.

The API used to send the user name and password as plain text — anything able
to watch the connection could read the password. It now runs a challenge and
response: the server sets a puzzle only someone who knows the password can
answer, and **the password itself is never sent in any form.**

**The server also proves itself to you.** It finishes by returning a value
only the real server can compute, and the client refuses the connection if it
does not match. Another program that grabbed the port before SD started cannot
pretend to be SD in order to collect passwords.

### What you have to do

| | |
|---|---|
| **Use a client library from this release or later.** | An older one is refused outright |
| **Run `modify.password` again for every account that uses the API.** | The stored credentials changed shape and the old ones cannot be converted |

**An account whose password has not been re-set is refused, and the refusal
reads as a wrong password.** From the server's point of view there is no
credential to check. If a working client suddenly cannot log in after an
upgrade, this is the first thing to try.

The old credentials cannot be converted because **the password was never kept
anywhere, by design** — there is nothing to convert them from.

**Programs using the `!sdclient` class are covered.** The class module BASIC
programs use to reach another SD server speaks the new login too. Your code
does not change — `connect()` takes the same arguments — but the program has to
be running under this release **at both ends**.

**`SDConnectLocal()` connections are unaffected.** They send no password and
never did.

## The connection is encrypted

**Every API connection — the network port and the local one alike — is wrapped
in TLS 1.3 before SD sends anything**, and the login is bound to that encrypted
connection. A machine sitting between a client and the server cannot read the
traffic or log in on the client's behalf, even by pretending to be the server.
Until W1.1-0 only the login was protected: the password never crossed the
network, but every command, record and result after it did, as plain text.

**The client libraries do this automatically.** `sdclilib`, `sdclient` and the
BASIC `!sdclient` class all negotiate TLS themselves. A program linked against
an *older* copy of the library cannot connect at all: the server waits for the
encryption handshake and closes the connection after ten seconds of silence.
Relink it.

**The client library remembers each server's certificate.** The first time a
client library connects to a server it keeps that server's certificate; after
that it connects only to a server that presents the same one. This is *first
use* trust: the first connection is taken on trust, and every later one is
checked, so a machine in the middle cannot pose as the server and collect a
login to guess the password from offline.

| | |
|---|---|
| **What is kept** | the SHA-256 of the server's whole certificate, as 64 lower-case hex digits |
| **Where** | `%USERPROFILE%\.sdcore\known_servers`, or the file named by the environment variable `SD_KNOWN_SERVERS`; one line per server, `host:port` and the digits. A different port is a different server |
| **When it is checked** | right after the secure connection is made and before anything is sent — no login byte, no password |

**A changed certificate is refused**, with *"THE SERVER'S CERTIFICATE HAS CHANGED
since this client first connected to host:port (pinned ..., now ...). The
connection was refused before any password was sent. If the server was
reinstalled, remove the line for host:port from ... and connect again"*. Nothing
updates the file by itself and nothing asks you; **removing the line is the
remedy**, and only if you know why the certificate changed. **A file that cannot
be opened or written refuses the connection** ("cannot pin the server: cannot
open ...") rather than connecting unchecked, so a program that runs with no user
profile, such as a service, needs `SD_KNOWN_SERVERS` set to a file it may write.

**A server whose certificate was replaced is a different server to a client that
knew the old one** — for instance SD installed on a fresh data folder. The
client refuses it until its line is removed.

**What this does not cover.** The very first connection is trusted, as with
`ssh`: a machine in the middle at that moment would be remembered in the
server's place. **Programs that reach another SD with the `!sdclient` class or
SDNet do not go through the client library and are not pinned.** Use long API
passwords that are not reused elsewhere.

**A low-privilege Windows account, `sdrelay`, appears in Computer Management.**
The small helper program that ends the encryption for each connection
(`sdtlsrelay.exe`, beside `sd.exe`) runs as `sdrelay`, an account with every
privilege stripped, at low integrity, unable to sign in interactively and in no
group. SD's service creates it and removes it. **Leave it alone**: if it is
deleted by hand, every API connection is refused until the service is
reinstalled.

## The port

**The API port is 4247, and nothing can change it.** It used to be 4243, which
OpenQM and ScarletDME also use. `sd.conf`'s `APIPORT` now only switches the API
on: any number above zero means on, and SD listens on 4247 whatever the number
is. A file that says `APIPORT=4243` keeps working and means 4247. A program that
names port 4243 must name 4247 instead; one that names no port needs no change.
The server accepts API connections on any network interface, unless
`remote.api local` has limited it to `127.0.0.1` (`APILOCAL=1` in `sd.conf`),
in which case only this computer can connect.

**If you tunnel, stop.** `ssh -L 4247:127.0.0.1:4247 user@host` still works
but is no longer what the design expects. Point the
client straight at port 4247 on the server.

**Reaching the port from another computer is off unless you tick the box during
installation.** To change it afterwards, from an elevated prompt:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\api-firewall.ps1" -Open
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\api-firewall.ps1" -Restrict
```

**To turn the API off altogether**, comment out the `APIPORT` line in
`C:\ProgramData\SD\sd.conf` and restart SD. With no `APIPORT` set, SD creates
no socket at all — "no API" is a real state, not just a firewall rule.

> **Declining the API at install time leaves no listener at all.** The
> installer writes an `sd.conf` with no `APIPORT` line, so nothing listens and
> there is no firewall rule to open. The API box is unticked by default.
> `remote.api on` puts a listener back.

## Reaching the port is not getting in

A caller must clear two gates, in this order:

1. **Complete the SCRAM exchange** against a password held for that account —
   so **an account with no password cannot connect at all**.
2. **Be a member of the `sdapi` group**, which an account joins only when you
   give it API access. `create.account user fred api` or `... both` does that;
   `ssh` or `none` does not.

**SDSYS is admitted from another computer only through a door the
administrator opens.** It is never joined to `sdapi`, because only
`create.account` does that and SDSYS is not created that way, so the ordinary
route is closed to it. Signed in to Windows as SDSYS, the administrator can open
a separate door for chosen addresses with `remote.sdsys api on` *address*, and
shut it again with `remote.sdsys api off`; as delivered it is shut. A session
that comes through it must still complete the SCRAM exchange with SDSYS's own
SD password, the one SD asked SDSYS to set the first time it signed in. The
Administrator Guide's chapter *Remote Administration through the API* says what
opening the door means for security. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**Failed API logins are written to the audit trail**, with the reason and
the address they came from. The line is written **before** the wait (`PWDELAY`,
three seconds unless you set it) that SD adds to slow down guessing, so a
program that hangs up during the wait is recorded as well. See
[Other hardening](13-hardening.html).

## A session is confined to its own account

| | |
|---|---|
| **Allowed** | everything inside its own account, and the shipped SDSYS files every account needs — messages, `syscom`, the dictionaries. Ordinary programs are unaffected |
| **Not allowed** | opening, renaming, deleting or listing anything else |

**A refused `OPEN` takes the `ELSE` branch and `STATUS()` is 3035**, which
means *not permitted* rather than *not found*. That distinction matters when
you are debugging: 3035 is a containment refusal, not a missing file.

**A suspended account is refused here too, and deliberately says nothing
about why.** `modify.account fred suspended` denies the API as well as ssh,
and the message is the one this page already gives for an account that does
not exist and for one you are not granted:

```
User not allowed in requested account
```

**All three answer identically on purpose**, so the API cannot be used to
enumerate which accounts exist or what state they are in. If you are debugging
a client that has suddenly stopped connecting, `list accounts` from SDSYS
is where the answer is — a suspended account shows it in that listing.

### If your data lives outside an account

Name the directory in the **`NETDIRS`** setting in `C:\ProgramData\SD\sd.conf`,
separating several with a semicolon. Nothing else needs changing.
`config('NETDIRS')` prints what is in force.

**THE PASSWORD FILE, THE PROGRAM CATALOG AND THE ACCOUNT REGISTER ARE NEVER
REACHABLE from an API session, and cannot be added to `NETDIRS`.**

## An API session runs as you

**Records an API session creates are owned by the account that logged in**,
and the session reaches files with your access rather than the service's. If
your account may not read something, the API session may not read it either.

**If your identity cannot be taken on, the login is refused** rather than
continued with the service's identity. A session that believes it is you while
holding the service's rights is worse than one that never started.

**There is an alarm for the condition returning.** If a session ever believes
it is you while Windows says it is not, SD's error log gets:

```
API IDENTITY LOST at record write - session believes it is ...
```

Nothing is written when the two agree, so **a healthy session is silent** and
you should never see this. It refuses and slows nothing; it exists so the
condition cannot go unnoticed.

## `sh` and `OS.EXECUTE` over the API

**They follow the account's switches, the same as anywhere else.** The
per-account switches `sh-on` and `os-on` are read when a session enters its
account, and by the API server when it enters the account for an API session,
so an account that holds `sh-on` has the `sh` verb over the API, one that holds
`os-on` has `OS.EXECUTE`, and a new account has neither. **That puts a shell
behind the account's API credential, reachable from wherever the API port
is**: weigh it before you turn either on for an account that also has the
`api` route. SDSYS is the exception: an API session is not treated as an
administrator for any purpose, so there is no shell over the API for it; use
the local sign-in. An API session runs with the signed-in user's own rights,
never as the service's LocalSystem account. `SDCLIENT` in `sd.conf` is the
further control, if a site wants one: see the *Administrator* set's
*Configuration* chapter. One limit is Windows': a process started the way an
API login starts one cannot launch anything that needs a desktop, which
includes PowerShell (see [Differences from W1.0-0](01b-differences-from-w1-0-0.html)).

## Client libraries

| | |
|---|---|
| 64-bit | `sdclilib.dll` |
| 32-bit | built separately; 32-bit remains a supported target, not a test convenience |

**Both must come from this release or later.** A client library that predates
SCRAM is refused by the server, and the 32-bit client in particular once
shipped sending passwords in clear — check which one your application is
actually loading.
