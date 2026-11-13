Title: The Audit Trail
Subtitle: What SD writes to its audit trail, who writes it, where it is kept, how it is rotated, and how to read it.

SD writes **one line to the audit trail for every act that changes who may do what, or that crosses a
boundary**: a sign-on, a refused request, an account created or changed, a gate turned on, a backup, a
command run from a toolkit page. The trail is a text file of the SDSYS system directory. This page
says what a line looks like, who is able to write one, how the file is kept, and how to read it.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set. Where a user-set page is worth naming, it is named in words.

## A line

```
2026-11-13 14:03:11 user=OFFICE\fred uid=1001 pid=48213 modify.account net-on account=fred
2026-11-13 14:03:40 user=OFFICE\SDSYS uid=1002 pid=48990 tool start app=tool.sessions
```

A line is the time, then `user=` (the Windows user that made the entry, as `DOMAIN\name`), `uid=` (the
session's SD user number) and `pid=` (its Windows process id), then the **event words**, then any number of
`key=value` pairs. The event words come first and are all lower case (`login`, `modify.account`,
`api refused`, `tool start`); a pair's key is lower case too; a value is whatever a person typed or the
system knows (an account name, a reason) and keeps its case. A value may hold spaces: a word that holds no
`=` after a pair belongs to that pair's value.

**Every line written by a run of a scheduled administrator job ends `job=`*name***, starting with
`elevation granted reason=scheduled job`; see Scheduled Jobs, in this set.

## Who writes it

**The user and the process on a line are not the session's word.** Every session hands its record to the
SD service (`sdsvc.exe`, which runs as LocalSystem), through the named pipe `\\.\pipe\sd-audit`. The
service writes `user=` from the Windows token of the session at the other end of the pipe and `pid=` from
Windows, so a line cannot name someone else. `uid=`, the SD user number, is the session's own.

A session checks that the pipe belongs to LocalSystem before it sends anything, and the service refuses a
pipe name someone else made first and refuses connections from other computers.

**If the SD service is not running**, a session appends its line itself, as SD did before the service
wrote the trail; such a line's `user=` is the name the session gives, without a domain. A run of such
lines therefore marks a time when the service was down.

The service takes at most **600 records from one Windows user in any 60 seconds** and drops the rest;
when that user's minute is over it writes one line saying how many were dropped. The limit is compiled
in and is not a setting.

## Where it is kept

| | |
|---|---|
| File | `audit` in the system directory (`C:\ProgramData\SD\sdsys\audit`) |
| Who may do what | the installer gives the SD users group the right to **add** to the end of the file and nothing else: an ordinary user cannot read it, empty it, overwrite a line, rename it or delete it. SYSTEM and the Administrators group keep full control |
| Rotation | at one megabyte the service (and `sd -start`) renames it to `audit.yyyymmdd-hhmmss` and starts a new file with the same permissions; it refuses to rotate when it cannot read those permissions. A rotated file is not pruned by SD: that is the site's decision |

**SDSYS reads it**, being an administrator; no ordinary account can.

## Reading it

This release has no full-screen page for the trail on Windows. Read the file as an administrator: open
`C:\ProgramData\SD\sdsys\audit` (or a rotated `audit.yyyymmdd-hhmmss` beside it) in an editor started
as administrator.

## What the trail does not do

It does not show an account holder's own lines: the trail names every account, user and address on the
machine. Nothing in SD edits, deletes or prunes a line.
