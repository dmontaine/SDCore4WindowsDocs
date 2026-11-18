Title: Reaching SDSYS from Your Own Login
Subtitle: How the administrator can let chosen Windows users become SDSYS from this computer, by ssh or through the API, without signing in to Windows as SDSYS; how to list them and take them off; the risk; and what it refuses.

**The administrator can let chosen Windows users reach SDSYS from this computer without signing out
of Windows and in again as SDSYS.** There are two lists, one for an ssh login and one for a program
that signs in through the API. **Both are empty as delivered**, and with both empty SDSYS is reached
exactly as it was before: signed in to Windows as SDSYS and running `sd` elevated, or through the
doors `remote.sdsys` opens. The installer does not ask about it. An upgrade keeps the lists as they
were; a full uninstall removes them.

* A user on the **ssh list** types `ssh -t fred@localhost sd-sdsys` on this computer, is asked for
  the SD password of `sdsys` once, and is then the administrator in an SDSYS session.
* A user on the **api list** may have a program of theirs on this computer sign in as `sdsys` over
  the API at this computer's loopback address, `127.0.0.1`, with the SD password of `sdsys`.

Either way the SD password of `sdsys` is still needed every time. It is SD's own password for
`sdsys`, the one `modify.password` sets and an API sign-in checks, not SDSYS's Windows password.

> **Listing a name is a decision about that Windows user, not about one login.** A listed user,
> from any session of theirs on this computer, **a session they reached over the network
> included**, can become the administrator if they also know the SD password of `sdsys`. Every
> program that user runs can try that password, and so can anything that user lets through to this
> computer. The administrator can change every account on the system and runs as a Windows
> administrator. A password typed once into the wrong place, or kept in a file that user can read,
> is then the whole of the protection. List only your own Windows login, the one you use as the
> administrator, and not ordinary users. Keep the lists short, use a long SD password for `sdsys`
> that is used nowhere else, and take a name off (`local.sdsys` *list* `remove`) when it is no
> longer needed.
>
> **Two places where SD Core for Windows has less to go on than SD Core for Linux.** Over the API,
> Windows does not tell a server which program is at the other end of a connection; SD reads it from
> Windows' table of connections, which a program that is quick enough could in principle stand in for
> during the moment between the connection and the reading (SD refuses a program younger than the
> connection, which closes the case it knows of). Over ssh, the record SD reads to know the login
> came from this computer is in a Windows log that ordinary users may also write to; SD accepts only
> an entry written by the ssh server's own process for that very connection. In both cases only a
> listed user could try it, and the SD password of `sdsys` is still asked.

## The two lists and who may be listed

| List | What a listed user may do |
|---|---|
| `ssh` | become SDSYS from an ssh login on this computer, with `sd-sdsys` |
| `api` | have a program on this computer sign in as `sdsys` over the API at `127.0.0.1` |

Each list holds at most 32 names. A list is a plain text file, one Windows user name and that user's
Windows security identifier (SID) to a line, in
`C:\ProgramData\SD\sd-tls`, the folder that holds the API's key, which the installer makes readable
and writable by SYSTEM and Administrators only: `sdsys-local-ssh` and `sdsys-local-api`. The
administrator changes a list only through `local.sdsys` (or the two fields on the remote
administration view of `tool.remote`, with keys to add a name, remove a name and clear a list), never
by editing the file. A list that does not exist is an empty list. A listed user cannot read the list.

**A name can be listed only if** it is the name of an existing local Windows user of this computer
(found whatever its case, and kept in the account's own spelling), 1 to 20 characters with no space,
no control character and none of the characters Windows forbids in a user name, that is enabled, is
not one of Windows' own built-in accounts, and is a member of `sdusers` (it has an SD account).
SDSYS, SDRADMIN and SD's service accounts (`sdrunin`, `sdrelay`) are never listed. Anything else is
refused by name and nothing is changed. SD compares the Windows account itself, not the name a
program gives: a listed user is recognised by the account Windows says the session or program runs
as. **The SID is what is listed**: a user renamed in Windows stays listed, and the report shows the
name the account has now; a user deleted and made again under the same name is a new account and
is not listed. Only accounts of this computer can be listed, not domain accounts.

**An ssh-listed user still needs SD's ssh route** (`modify.account` *name* `ssh` or `both`) for the
ssh server to let them in at all; listing a name does not give it.

**A list that is not safe is treated as empty.** SD uses a list only when the file is a plain file
(not a link, with no other name), owned by SYSTEM or Administrators, that nobody else may change,
under 8 KB, in the folder above in the state the installer left it, with only valid names and no
more than 32 of them. Anything else, and the list refuses everybody; `local.sdsys` says so (see "The
verb"), and `clear` removes the file so the list can be made again.

## The verb: `local.sdsys`

```
local.sdsys
local.sdsys {ssh | api}
local.sdsys {ssh | api} add user {no.query}
local.sdsys {ssh | api} remove user
local.sdsys {ssh | api} clear
```

Only the administrator can use it; anyone else is told "Command requires administrator
privileges". The words, and the user name, are read as lower case whatever was typed.

| | |
|---|---|
| *(no keyword)* | reports both lists and changes nothing |
| `ssh`, `api` | reports that list and changes nothing |
| `add` *user* | puts the name on the list, after a plain warning and a question (below) |
| `remove` *user* | takes the name off; this works for a name whose Windows user has gone |
| `clear` | empties the list (the file is removed); the one way to leave an unsafe list |

`add` says once what listing the name means and asks, unless `no.query` is given. Anything but `y` is
no, and so is an input that ends:

```
:local.sdsys ssh add fred
Listing fred lets that user, from any session of theirs on this computer - one
they reached over the network included - become the administrator with the
SD password of sdsys (ssh -t fred@localhost sd-sdsys).
List fred for sdsys over ssh? (y/<n>) y
sd-sdsyslocal: sdsys local ssh: added fred; listed now: fred
```

For the `api` list the warning says that the programs of that user sign in as `sdsys` over the API at
`127.0.0.1` instead. An answer other than `y` prints "fred was not listed; nothing was changed." and
writes nothing.

The report is one line a list:

```
:local.sdsys
sdsys local ssh: listed fred
sdsys local api: none listed
```

A list that is not safe is reported as `sdsys local ssh: unsafe, treated as none listed`, with the
file's name. Listing a name that is listed already, or taking off one that is not, says so and
changes nothing; a 33rd name is refused ("the ssh list holds 32 names already, the most it takes").
A refusal is shown as it was said, and `local.sdsys` adds that the command did not succeed.

The lists can also be read, or emptied, from an elevated PowerShell without SD:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\sd-sdsyslocal.ps1" -List ssh -Action status
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\sd-sdsyslocal.ps1" -List ssh -Action clear
```

Adding a name is SDSYS's alone.

## Reaching SDSYS over ssh

A listed user, on this computer, types:

```
> ssh -t fred@localhost sd-sdsys
SD password of sdsys:
```

The user's ordinary ssh sign-in to this computer comes first, with their own Windows password, as for
any ssh login. Every ssh login to SD starts `sd`; only the requested command `sd-sdsys`, exactly
that word and with `-t`, turns the login towards SDSYS. **Any other login of a listed user, with no
command or with any other one, is their own session exactly as before.**

**The `-t` is needed.** It gives the login a terminal, which the password is typed at. Without it
(`ssh fred@localhost sd-sdsys`, or input from a pipe) nothing is started and the login ends with
"sd-sdsys needs a terminal: ssh -t <user>@localhost sd-sdsys".

The SD service then asks Windows, and SD asks again, whether this is a listed user's ssh login from
this computer. **What counts as "an ssh login from this computer" is this: the login came through
Windows' own ssh server (the `sshd` service), and the ssh server recorded its source as a loopback
address** (`127.x.x.x` or `::1`; `localhost` arrives as `::1`). A login that came in from another
computer does not count, nor one that came in at this computer's own network address; neither does
the console, Remote Desktop, `runas`, a scheduled task, or `sd-sdsys` typed inside an SD session.

* **The password** is asked for once, with nothing shown as it is typed. The answer is the SD
  password of `sdsys`.
* **A right password** makes the session the administrator, and the session says so:

  ```
  SD administration granted: this session is the SDSYS Windows account, elevated,
  reached from the ssh login of fred on this computer with the SD password of sdsys
  ```

  The session is `sd` running as the Windows account SDSYS, elevated, started for you by the SD
  service (`sdsvc.exe`), with its screen and keyboard passed through your ssh login. It is not on
  anybody's desktop, so nothing that needs a desktop (a Windows consent prompt, a window) can be done
  from it.
* **A wrong password** ends the session with "The SD password of sdsys was not right, so this session
  is not the administrator and ends here." There is **one try**. After a wrong password SD waits for
  the number of seconds `PWDELAY` gives (3 as delivered, 0 for none) before the session ends.
* **No password to check** (`sdsys` has none set): the session ends with a message that says to
  set one with `modify.password` from a `sdsys` login. Nothing is granted.

A second try is a new ssh login, and the wait applies again.

**The ssh server's own log must be on.** SD reads the ssh server's record of where the login came
from, which it writes to the Windows event log (`OpenSSH/Operational`) as delivered. If that logging
has been turned off in `sshd_config`, every `sd-sdsys` is refused.

## Reaching SDSYS over the API

A program of a listed user on this computer connects to the API at `127.0.0.1` and signs in as
`sdsys`, with the SD password of `sdsys`, as any API program signs in as any account. **It has to do
nothing different: the sign-in is the ordinary one, as `sdsys`.** A session so admitted has every right
the administrator has.

* **Only from this computer, at `127.0.0.1`.** SD asks Windows which program is at the other end of
  the connection and which Windows account that program runs as, before anything else happens on the
  connection. A program it cannot identify, one that has gone, or one whose account it cannot read,
  is refused.
* **The program must run as the listed user, in a sign-in of that user's own.**
* **The addresses of `remote.sdsys api` never cover this computer.** Neither a listed address nor
  `any` admits a connection from `127.0.0.1`; only this list does, and `remote.sdsys api on` refuses
  a loopback address.
* **The password is checked as for every API sign-in**: a wrong one is refused in the same words
  and after the same wait.

SDSYS's own programs keep the local connection they always had (signed in to Windows as SDSYS,
elevated, no network port); this list is not needed for that.

## What is refused

Everything that is not a listed user's ssh login from this computer, or a listed user's API program,
meets the refusal it met before the list existed.

**Over ssh**, `sd-sdsys` is refused by the SD service before SDSYS is started. Nothing is started and
the refusal is one line, with a reason word, also written to the SD service's log
(`C:\ProgramData\SD\sdsvc.log`):

```
sd-sdsys refused: not-listed
```

| Reason word | when |
|---|---|
| `list-empty` | nobody is on the ssh list (as delivered) |
| `list-unsafe` | the ssh list is not a plain file of the administrators' (see above) |
| `not-listed` | this user is not on the list |
| `not-sd-user` | this user could not be listed now: not in `sdusers`, disabled, or a built-in account |
| `no-user` | the login's Windows user no longer exists |
| `not-ssh` | the login did not come through the ssh server: the console, Remote Desktop, `runas`, a scheduled task |
| `not-local` | the ssh login came from another computer, or from this computer's own network address |
| `no-login`, `other-user`, `other-session`, `no-session`, `session-unsafe` | Windows' record of the login is missing or is not this user's own ssh login: the ssh server's log has no record of it, the connection has gone, or something other than the ssh server stands between it and `sd-sdsys` (`sd-sdsys` run from inside another program) |

**If the SD service let the session in but SD's own check disagrees**, or an SDSYS session that was
not elevated at a desktop is started in some other way, the old refusal stands: "SDSYS Account access
is restricted to privileged users", and the session ends. While the ssh list has names on it, the
audit line for that refusal carries the reason word as well.

**Over the API**, a sign-in as `sdsys` from `127.0.0.1` that this list does not admit is refused with
"SDSYS may use the API from this computer only from a program of a user listed with local.sdsys
api.", and the audit line names the Windows user the program ran as and, while the api list has
names on it, a `why=` word (`not-listed`, `list-unsafe`, `not-sd-user`, `other-user` when the program
runs in somebody else's sign-in, `other-session` when the program is younger than its connection, or
`peer-unknown` when the program could not be identified).

**A list file that is not safe** refuses everybody on that list, in the same words as an empty list
and with `list-unsafe` as the reason.

## What is written down

Every line is in the audit trail ([The Audit Trail](21-the-audit-trail.html)):

* Each change of a list, by the administrator:
  `local.sdsys ssh add user=fred status=ok`, `local.sdsys api remove user=fred status=ok`,
  `local.sdsys ssh clear status=ok`. A change that was refused ends `status=refused`. An `add` that
  was answered no writes nothing.
* A grant over ssh: `elevation granted reason=sdsys local ssh user=fred`.
* A refusal over ssh after the password was asked:
  `elevation refused reason=sdsys local ssh wrong password user=fred`, or
  `elevation refused reason=sdsys local ssh no credential user=fred`.
* A grant through the API:
  `elevation granted reason=sdsys api from=this machine user=fred`.
* A refusal through the API: `api refused user=sdsys reason=...`, naming the Windows user the program
  ran as.

The SD service's own lines, for a refused `sd-sdsys` and for each SDSYS session it starts, are in
`C:\ProgramData\SD\sdsvc.log`.

## Taking a name off, and closing it again

```
local.sdsys ssh remove fred
local.sdsys api clear
```

`remove` takes a name off one list. `clear` empties a list, and taking off the last name does the
same: the file is removed, which is what "off" is. **With both lists empty nobody has this way
in**, and nothing else was changed to give it: no account, group, firewall rule or ssh server setting.
The next try by that user is refused.

## What it does not do

* **It is not for another computer.** Over the network SDSYS is reached only through the doors
  `remote.sdsys` opens ([Remote Administration over ssh](22-remote-administration-over-ssh.html) and
  [Remote Administration through the API](22a-remote-administration-through-the-api.html)), each shut
  as delivered; neither is changed by this page's lists, and a login from another computer is not
  admitted by them.
* **It does not replace the SD password.** The password of `sdsys` is asked every time, once, and a
  listed user who does not know it is refused.
* **It does not let a user in who is not listed**, and does not list anybody for you: both lists are
  empty as delivered.
* **It does not protect against a listed user.** That user, and anyone who has that user's login on
  this computer, can ask for the administrator; only the password stands in the way.
* **It cannot tell the keyboard from the network.** A listed user who signs in to this computer from
  elsewhere and then uses ssh to `localhost`, or whose program relays a connection to `127.0.0.1`,
  arrives from this computer.
* **It is not in SD Core Solo**, which has no SDSYS.
* **A background process cannot be started from such a session.** A phantom begins a session of its
  own, which has no terminal to be asked the password at, and is refused (the audit line ends
  `why=no-terminal`). Start background work signed in to Windows as SDSYS.

## See also

[Remote Administration over ssh](22-remote-administration-over-ssh.html) and [Remote
Administration through the API](22a-remote-administration-through-the-api.html) for the doors that
reach SDSYS from other computers. [Accounts and Security](01-accounts-and-security.html) for what
being SDSYS means. [The Audit Trail](21-the-audit-trail.html) for the lines this writes.
