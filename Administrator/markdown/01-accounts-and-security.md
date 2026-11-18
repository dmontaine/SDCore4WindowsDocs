Title: Accounts and Security
Subtitle: Making and changing accounts, passwords, and who may enter an account.

These are the verbs that decide **who may use this installation and what
they may do with it.** They are SDSYS's set — not in any other account's
VOC at all — and almost all of them need more than the verb before they
will do anything.

> **This document is separate so that it can be withheld.** Everything in
> the administrator set describes verbs an ordinary account does not have
> and cannot run. It is a complete set on its own and **links to nothing
> outside itself**, so that handing somebody the user documentation without
> this never leaves them at a page that is not there. Where a user-set page
> is worth naming, it is named in words rather than linked.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **Anything you put in the `shared` account can be read by every account,**
> by file name, with no `logto` and no pointer, **unless you type
> `shared-read-off` for an account.** The installer makes the `shared` account;
> every account, new or old, starts with the right to read its files, and
> without the right to write them. This is the one right here that is on until
> you take it away. See *The shared account*, below, and
> [The shared account](13-the-shared-account.html).

## Read this before anything else: being SDSYS is the whole of it

**Having the verb is not having the right to use it — and there is exactly
one gate, one route in, and nothing that widens it.** Every verb on this
page is refused outright to any session that is not actually SDSYS, whether
or not that session is elevated:

```
:modify.account fred suspended
Command requires administrator privileges
:delete.account sdsys
Command requires administrator privileges
:modify.password sdsys
Command requires administrator privileges
```

**Every one of those refusals came before the command was looked at.**
`delete.account sdsys` would have been refused anyway — you cannot delete
`SDSYS` — and it never got that far.

**A gate is a wall for an SD *session*, not for a person who has a shell on the
machine.** Every SD user is in the Windows group `sdusers`, and a member who has a
shell can write SD's shared memory (the lock, file and user tables): such a person
can release other people's locks or log sessions out, which is damage and denial of
service, not a way to become SDSYS or to turn a gate on. How far that matters, and
how an installation that cannot accept it closes it, is in [SD
installation](08-sd-installation.html), *What this does not close*.

**Being SDSYS means having signed in to Windows as the account named
`sdsys`**, made once by the installer, and nothing else. Being a Windows
administrator grants nothing by itself — an elevated session in an ordinary
account is still an ordinary account. **Start SD by signing in to Windows
as SDSYS and running it elevated.** The three verbs on this page that do
*not* require this are `clean.account`, `config` and `update.accounts`, and
each of them acts only on the account you are already standing in or on
your own session.

**The administrator can also list Windows users who may reach SDSYS from
their own login on this computer** (`local.sdsys`), by
`ssh -t` *user*`@localhost sd-sdsys` or from a program over the API at
`127.0.0.1`, each asked for SDSYS's SD password. It is off as delivered:
both lists are empty. See [Reaching SDSYS from Your Own
Login](22b-reaching-sdsys-from-your-own-login.html).

**SDSYS may be signed on in more than one place, and when it is you can see it.**
Nothing stops a second console window or a second sign-in of the `sdsys` user from
starting SD, and one reason to want that is recovery: a session that is stuck at a
page can be ended by `logout` from another. A limit of one would lock the
administrator out until `sd -cleanup`. So the second session is made visible,
three ways:

| where | what it shows |
|---|---|
| the audit trail | one line, `sdsys second session others=<n>`, written by a session of SDSYS that signs on while *n* other sessions of SDSYS are on a terminal (after the `login account=sdsys` line it writes as always) |
| `tool.sessions` | each of those rows says `sdsys x<n>` in its State column, the counts line says `SDSYS in <n> places`, and the box under the list says so for the row under the cursor |
| the home screen | the Sessions and locks tile says `<m> signed, <n> sdsys` in place of `<m> signed on` |

What counts is a session of the account `sdsys` that is **on a terminal**: a
phantom, an API or SDNet process, a session being logged out, and a session with
no terminal (a piped `sd 'command'`, `sd -internal`, a program started from a
script) are not counted and write no line, because they are not a second person
at the machine. Seeing the second session is not the same as stopping it; the
audit line and the page are how you notice one you did not expect.

## Continued in

[Accounts and Security: Making an
Account](01-accounts-and-security-2-making-an-account.html) — create.account,
the sh-on, os-on and sd-on switches.
