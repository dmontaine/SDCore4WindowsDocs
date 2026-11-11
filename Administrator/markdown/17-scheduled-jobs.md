Title: Scheduled Jobs
Subtitle: The administrator's own jobs on Task Scheduler, the commands an account may run unattended, and how SD tells a scheduled run from anything else.

SD runs work unattended in **two ways, and nothing of either kind is allowed or scheduled as
delivered.** Each is a deliberate act of SDSYS, written to the audit trail, and undone the same way.

| | An account's job | An administrator's job |
|---|---|---|
| Runs as | the account's own Windows user, with the account's rights | the Windows account SDSYS, with the administrator's rights |
| Scheduled by | a Task Scheduler task of that user's | a Task Scheduler task that only the job helper writes |
| May run | a paragraph or sentence of the account, if it is on the account's list | one of two fixed commands |
| Set up with | `set.batch`, or the account view of `tool.jobs` | `set.job`, or the Jobs view of `tool.jobs` |

An account's job can reach only what its account can. **Work that has to reach every account** (a
backup of all of them, an update of every VOC) is an administrator's job.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set. The walk-through of an account's job, from the paragraph to the task, is
> *Scheduled jobs* in the **Getting Started** set.

## The administrator's jobs

### What a job can run

A job runs **one command from a list the job helper owns**, chosen by an id. No command text comes from
the page, from `set.job` or from the person typing:

| Job | Runs |
|---|---|
| `backup-all` | `backup.account all`: one archive of every account, in the saved backup directory |
| `update-accounts` | `update.accounts all`: every account's VOC refreshed from the shipped records |

Each runs exactly as it does when typed at the prompt; [Account maintenance](01a-account-maintenance.html)
has both. **A backup starts only when every other session has logged out**, so schedule `backup-all`
for a time when nobody is signed on: a run that finds someone still logged in does not back up.

A command that takes an account name or a path is not on the list. The list changes only with a
release of SD.

### Schedules

A schedule is one of five shapes. The job helper turns it into the task's trigger, so no calendar text
is taken from anyone:

| Schedule | Runs |
|---|---|
| `every 5 minutes` (or `10`, `15`, `20`, `30`) | at minutes divisible by that number, every hour |
| `hourly` | at the start of every hour |
| `daily 02:30` | every day at that time |
| `weekly sun 03:00` | that day (`mon` to `sun`) at that time |
| `monthly 1 04:00` | that day of the month, `1` to `28` (every month has it), at that time |

Times are 00:00 to 23:59 in **the machine's own time**. **A run missed while the machine was off is not
made up**: the next one is at the next time the schedule names. A run still going when the next is due
is not started a second time, and a run is stopped after 72 hours.

### `set.job`

`set.job` is in SDSYS's VOC only and is refused to anyone else ("Command requires administrator
privileges").

```
set.job
set.job add name job schedule
set.job change name job schedule
set.job delete name
set.job run name
```

| Form | Does |
|---|---|
| `set.job` | lists the jobs, each with its schedule, its command, when it runs next and how its last run ended |
| `add` | makes a job; refused when one of that name exists (`set.job change` changes it) |
| `change` | gives an existing job a new job id or schedule; refused when there is no job of that name |
| `delete` | removes the task, then the job |
| `run` | starts the job now, exactly as its trigger would, and does not wait for it |

**The name** is 1 to 32 characters: a lower-case letter first, then lower-case letters, digits and dashes,
not ending in a dash. **There can be at most 32 jobs.** A time may also be written *hh.mm*.

```
:set.job add nightly backup-all daily 02:30
sd-jobs: job nightly created
sd-jobs: job nightly is scheduled: daily 02:30
:set.job
job nightly: daily 02:30: backup.account all (backup-all)
   next run: 2026-11-11 02:30:00; last run: never
```

What you see is what the job helper did; the lines it prints about what it is about to do are left
out. A last run shows its end time and Task Scheduler's own result number (`result 0` is success);
`running now` while it runs.

**`set.job` writes no file.** Every change is the job helper, `sd-jobs.ps1` in SD's program folder, run
with `job-set`, `job-delete` or `job-run` (and `job-list` for the list) through the SDSYS session's
elevated helper. It checks the name, the job and the schedule again, and it refuses any caller but the
Windows account SDSYS, elevated. The change is judged on the helper's own success line, not on its exit
status alone. When the helper refuses, what it said is shown, then `The job helper did not do it
(status n)`. Each change is written to the audit trail with its result:

```
set.job add name=nightly job=backup-all result=done schedule=daily 02:30
```

**That a job exists, or does not, is checked against the list just before the change.** The helper
itself makes or replaces the definition, so two administrator sessions acting on the same name at the
same moment are not kept apart: the last one to reach the helper wins.

### The Jobs view of `tool.jobs`

`tool.jobs` is the Scheduled jobs page, in SDSYS's VOC only, in a window of at least 140 columns by 43
lines. **J** shows the Jobs view and **A** goes back to the account commands. The view lists every job
with its schedule, its command, when it runs next and how its last run ended.

| Key | Does |
|---|---|
| **N** | makes a job: a form asks for the name, the job and the schedule |
| **C** or Enter | changes the selected job's job or schedule (its name stays) |
| **D** | deletes the selected job: you type its name in the box |
| **R** | starts the selected job now; the page does not wait for it |
| **/** | goes to the next row of the box you are in whose name holds a text you type (any case; it goes round to the top) |
| **F5** | reads the list again (a run shows there when it has finished) |
| **Ctrl-O** | shows what each command answered, newest first |

The form refuses a name, a job or a schedule the helper would refuse, before anything is sent. Every
change is then shown as its `set.job` command, with the job's command and the schedule in words, and
runs only when you answer Run; **Cancel is what Enter chooses**. The page writes nothing itself.

### A damaged job

The list shows a definition as **damaged** when it is not what the helper would have written. The line
says why, in one of five ways:

| The line ends | What causes it |
|---|---|
| `not a job name` | a file whose name is not a job name (it was not written by the helper) |
| `not a plain file` | a link, a folder or anything but a plain file under a job's name |
| `not the administrators' file` | a file owned by, or open to, anybody but SYSTEM and Administrators |
| `damaged` | a line missing, doubled or unknown, or a file over 4096 bytes |
| `the definition does not agree with the helper` | a job id or a schedule the helper no longer has |

```
damaged nightly: the definition does not agree with the helper
```

**A damaged job is not started by hand**: `set.job run` and **R** refuse it (`Job nightly is damaged;
nothing was started`), and so does the job helper. `set.job change` writes a damaged plain file again
unless it is not the administrators' file, and `set.job delete` removes any damaged plain file. **Its
task goes on firing until then**, and each run is admitted only if the definition is still the
administrators' file and still names the exact command the task starts (below); otherwise the session
is refused as any other SDSYS session that is not elevated at a desktop
(`login refused account=SDSYS reason=SDSYS requires an elevated session`) and runs nothing.

A file whose name is not a job name, and a link or anything but a plain file under a job's name, cannot
be changed or removed by the page or `set.job` (the helper refuses both); an administrator removes it
from `C:\ProgramData\SD\sd-jobs`.

## How a run is recognized

A job's run has nobody at a desktop: Task Scheduler starts it, and no UAC prompt can be answered. SD
therefore does not ask for the elevated desktop sign-in it requires of every other SDSYS session; it
asks three things that only an administrator of the machine controls.

1. **The session was started as `sd -job` *name***. That is only a key: anybody may type it, and for
   anybody else it changes nothing.
2. **The process is SDSYS's own elevated batch logon.** Its token is the local Windows account SDSYS
   (a domain account of the same name is not it), logged on as a batch job, not from the network and
   not at a desktop, with the Administrators group enabled. Task Scheduler makes that logon for the
   job's task; an ordinary SD user cannot make it.
3. **The definition names this very command.** `C:\ProgramData\SD\sd-jobs\`*name* and its folder are
   not links, are owned by SYSTEM or Administrators and allow nobody else anything, and the file's
   `command=` line is **exactly the command the session was started with**. The folder is found from
   Windows' own record of where ProgramData is, never from an environment variable.

Only then is the session made the administrator. The audit trail says so, and **every line the run
writes ends `job=`*name***:

```
2026-11-11 02:30:01 user=sdsys uid=1 pid=5120 elevation granted account=SDSYS reason=scheduled job job=nightly
```

**What this does not prove** is that Task Scheduler, rather than another Windows administrator who made
the same logon by hand, started the process. A Windows administrator is already above SD.

The task holds **no password**: it runs "whether the user is logged on or not" with "do not store
password". Windows gives such a run no network credentials, so **a job cannot reach a network share as
SDSYS**; keep the backup directory on the machine.

## Where a job is kept

| | |
|---|---|
| Definition | `C:\ProgramData\SD\sd-jobs\`*name*; the file and the folder allow SYSTEM and Administrators only |
| Task | `\SD\sdcore-job-`*name* in Task Scheduler (Task Scheduler Library ▸ SD) |

```
# an SD scheduled job, written by sd-jobs.ps1 job-set; changed only by sd-jobs.ps1 job-set and job-delete
name=nightly
job=backup-all
command=backup.account all
schedule=daily 02:30
```

The task runs `sd.exe -job nightly backup.account all` from SD's program folder, once, as SDSYS with the
highest privileges, starting in `C:\ProgramData\SD\sdsys`. **Change a job only through `set.job`**: a
definition edited by hand is shown as damaged, and a task edited by hand is written again by the next
`set.job change`. Task Scheduler shows the task, its trigger and its last result; what a run printed is
not kept, and what it did is in the audit trail.

**Uninstalling SD** removes every `sdcore-job-` task, then the definitions and their folder, **whether
or not the database is kept**: a task left behind would name a program that is gone.

## An account's commands

An account's job is `sd` started with a command by a Task Scheduler task of the account's own Windows
user, not elevated. **The login lets it run only a command on the account's list** in the SD system
file `batch.jobs` (in `C:\ProgramData\SD\sdsys`, read-only to SD users, one record per account), and
only if it is a single name with nothing after it and a paragraph (`PA`) or sentence (`S`) of that
account's VOC. SDSYS's own sessions are not held to a list, and SDSYS has none.

### `set.batch`

```
set.batch
set.batch add account command
set.batch remove account command
```

`set.batch` alone lists every account's commands. `add` checks that the command is a paragraph or a
sentence in that account's VOC (the test the login makes) before it adds it; `remove` takes it off, and
an account whose list is then empty has no record left. Each change is written to the audit trail
(`set.batch add account=fred command=my.report`) and takes effect at the next such session:

```
:set.batch add fred my.report
my.report may now be run from the command line in account fred
:set.batch
Account fred may run from the command line: my.report
```

It refuses `sdsys` (the administrator's account has no list), an account that is not registered, and a
name that is not a paragraph or a sentence there.

**Whoever can change the paragraph changes what the job does.** An allowed command runs with the
account's own rights; keep its VOC record where the account's people may change it only if they may also
decide what runs unattended.

### The account view of `tool.jobs`

The page opens on it. **Accounts** lists every registered account but SDSYS with how many commands it
may run that way; Enter or F6 goes to **Commands**, the paragraphs and sentences of that account's VOC,
each allowed or not. Enter or the space bar on one shows the `set.batch` command and what it does, and
runs it only when you answer Run. A name still on the list whose VOC record is gone, or is no longer a
paragraph or a sentence, is shown as such, and Enter takes it off. A name holding a character other
than a lower-case letter, a digit, a dot, a dash or an underscore cannot be sent from the page: it shows
the `set.batch` command to type at the prompt.

**The page does not write the account's schedule**; that is a task of the account's Windows user, made
in Task Scheduler.

### When the login refuses

A refused run writes `login refused account=`*account*` reason=`*why* to the audit trail:

| Reason | Means |
|---|---|
| `command line carried arguments` | something followed the name |
| `batch.jobs could not be opened` | the list is missing or unreadable |
| `command is not on the account list` | not allowed for that account |
| `no VOC record for the command` | the account has no such VOC entry |
| `VOC type is not PA or S` | it is there, but not a paragraph or a sentence |
