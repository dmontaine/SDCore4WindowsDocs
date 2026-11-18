Title: Remote Administration through the API
Subtitle: How SDSYS, the administrator, can sign in through the API from another computer, for chosen addresses; how to open and shut it; what it gives; the risk; and what it refuses.

**SDSYS can sign in through the API from another computer, but only after you have opened that
door, and only from the addresses you name.** As delivered the door is shut. The installer does
not ask about it. An upgrade leaves it as it was; an uninstall that deletes the database removes
it. It is meant for an administration program on another computer, such as an API administration
client, that signs in as SDSYS.

**Open it with care: with the door open, nothing but SDSYS's SD password stands between those
addresses and the administrator, and on Windows the administrator is a Windows administrator.**
An API session signed in as SDSYS runs as the Windows account SDSYS with its full, elevated rights,
exactly as SDSYS does at this computer's keyboard: whatever SDSYS can do there, a client with the
password can do from a listed address. The password is SDSYS's **SD** password, the one
SD asked SDSYS to set the first time SDSYS signed in ("Account SDSYS needs a password"), not its
Windows password. Use a long password that is used nowhere else (and is not SDSYS's Windows
password), name the narrowest addresses that work, and shut the door again when it is not needed.

**What a session gets.** An API session signed in as SDSYS has every right the administrator has,
the same as SDSYS at the computer's own keyboard. An API session into any other account has exactly
that account's rights and nothing more: the API never gives an ordinary account more than it has
elsewhere.

> This document is separate so that it can be withheld. It links to nothing outside the
> administrator set. Where a page in another set is worth naming, it is named in words.

## Opening and shutting the door

Signed in to Windows as SDSYS at this computer, in SD:

```
remote.sdsys api on address ...
remote.sdsys api on any
remote.sdsys api off
remote.sdsys api
```

| | |
|---|---|
| `api on` *address ...* | opens the door for those addresses, and only those. Up to 32. The list replaces the one before |
| `api on any` | opens it for every address. Only on its own, never in a list |
| `api off` | shuts it again, as delivered |
| `api` | says whether it is open and for which addresses, and changes nothing |
| *(no keyword)* | says how both doors stand, ssh (SDRADMIN, [Remote Administration over ssh](22-remote-administration-over-ssh.html)) and the API, and changes nothing |

An address is written in one of these forms:

| | |
|---|---|
| `192.168.1.20` | one IPv4 address |
| `2001:db8::20` | one IPv6 address |
| `192.168.1.0/24` | a range: every address whose first 24 bits are those of `192.168.1.0` |
| `fd00:1:2:3::/64` | an IPv6 range |

A range of length 0 (`0.0.0.0/0`, `::/0`) is refused: it would be every address, and the word
`any` is the only way to ask for that. Anything that is not an address or a range is refused before
anything is changed, and so is `any` together with other addresses. SD's API listens on IPv4, so an
IPv6 address or range is accepted and kept but no client reaches SD from one.

SDRADMIN's remote session over ssh can open and shut this door too, with the same words
([Remote Administration over ssh](22-remote-administration-over-ssh.html)). So can an API session signed in as
SDSYS, as it can do everything else the administrator does.

The same can be done without SD, in an elevated PowerShell:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\sd-sdsysapi.ps1" -Action on -Entries 192.168.1.20
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\sd-sdsysapi.ps1" -Action off
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\sd-sdsysapi.ps1" -Action status
```

Several addresses are given with commas: `-Entries 192.168.1.20,10.0.0.0/8`.

**The API must also be open to other computers** for a client to reach it at all: the installer's
question about API access, or `remote.api on` later. That opens TCP port 4247 for every account;
this door decides whether SDSYS may use it. With `remote.api local`, SD listens on `127.0.0.1`
only, and this door then admits nobody: a client on this computer is decided by the list described
in [Reaching SDSYS from Your Own Login](22b-reaching-sdsys-from-your-own-login.html).

## SDSYS's SD password

SD asks SDSYS to set its SD password the first time SDSYS signs in at this computer. To change it,
sign in to Windows as SDSYS and type `modify.password` in SD. It is stored the way every SD password
is (SCRAM, never the password itself), it never changes SDSYS's Windows password, and a client
proves it without sending it. A wrong password is refused in the same words as for any account,
after the same delay.

## Choosing the addresses

* **An address that never changes** is the tightest choice: the administration computer's own
  address. If it gets its address from DHCP, ask the network's router for a reservation, so that it
  always gets the same one.
* **A range** suits a computer whose address changes inside one network: `192.168.1.0/24` admits
  any address of that network. Every computer in the range can then reach the sign-in, though each
  still needs the password.
* **Travelling** is safest through a VPN into your own network, so that the client arrives from a
  listed range. `any` is there for when a VPN is not possible: with it, anyone who can reach this
  computer's API port, from anywhere on the internet, can try the password.
* **This computer** (`127.0.0.1`) is never covered by this door: neither a listed address nor `any`
  admits a connection from it, and `remote.sdsys api on` refuses a loopback address. A program here
  that connects over the network port as SDSYS is admitted only if the Windows user it runs as is on
  the list of [Reaching SDSYS from Your Own Login](22b-reaching-sdsys-from-your-own-login.html),
  which is empty as delivered.

A client that comes in through a gateway that translates addresses (a home router, a cloud load
balancer) arrives from the gateway's address, not its own; name that one. A refusal says which
address SD saw.

## From this computer

SDSYS may always use the API from this computer, whatever the door says, by the local connection
(no network port): a program signed in to Windows as SDSYS and running elevated starts SD itself,
and no SD password is asked, as at the keyboard. Such a session has every right of the
administrator. A program that is not running as SDSYS, or that Windows has not elevated, is
refused, exactly as it is at the keyboard. The administrator can also list Windows users whose
programs on this computer may sign in as SDSYS over the network port at `127.0.0.1`, with SDSYS's SD
password; the list is empty as delivered (see
[Reaching SDSYS from Your Own Login](22b-reaching-sdsys-from-your-own-login.html)).

## What refuses

| SD says | when |
|---|---|
| SDSYS may be reached through the API from another computer only when the administrator has opened it | the door is shut; or the session SD started for SDSYS was not elevated by Windows (the audit trail says which) |
| SDSYS may use the API from another computer only from an address the administrator listed with remote.sdsys api on, and *address* is not one of them | the door is open, but not for that address |

## What is written down

* Each change of the door: an audit line `remote.sdsys api on from=192.168.1.0/24 status=0` and the
  like, with the addresses you gave and the helper's exit status.
* Each SDSYS sign-in through the API: `elevation granted reason=sdsys api from=192.168.1.20`, or
  `from=this machine` for the local connection, or `from=this machine user=fred` for a listed user's
  program at `127.0.0.1`.
* Each refusal: the reason and the address, in the audit trail.

## What SD changes on the computer

* **`C:\ProgramData\SD\sd-tls\sdsys-api`**, in the folder that holds the API's key, which the
  installer makes readable and writable by SYSTEM and Administrators only, and which SD refuses to
  use in any other state. The first line is `on`, and each line after it is one address or range,
  written in its standard form (`192.168.1.99/24` becomes `192.168.1.0/24`, an address alone gets
  `/32` or `/128`). `off` removes the file.
* Nothing else: no firewall rule, no listener and no account is changed by this door.

## What it does not do

* It does not open the API port; `remote.api` does.
* It does not give any account but SDSYS more than its own rights.
* It does not accept a key, a certificate or a second factor: the SD password is the whole of it.
* It does not protect against someone who has the password and an address you listed.
