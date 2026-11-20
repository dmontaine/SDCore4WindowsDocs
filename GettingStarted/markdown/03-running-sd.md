Title: Running SD
Subtitle: The service, starting and stopping, and what to do when the last shutdown was not a clean one.

**SD is a Windows service and it is already running.** Nobody types
`sd -start` after every restart.

| | |
|---|---|
| Display name | **String Database (SD)** |
| Service name | `SD` |
| Start type | automatic — Windows starts it at every boot |
| Created by | the installer, which also starts it |
| Removed by | the uninstaller |

## Starting and stopping

**Stopping SD ends every session on the machine**, which is exactly what
`sd -stop` has always done. Either is fine:

```
Stop-Service SD
Start-Service SD
```

```
sd -stop
sd -start
```

**If SD stops on its own, the service starts it again.** When SD's background
program ends without being asked to (it crashed, or something ended it), the
service starts SD again after 5 seconds, and once more after 15 seconds if it
stops again; after that it leaves it stopped until the next day or the next
restart, so a fault that keeps SD from running is not hidden by a loop. A stop
you asked for, with `sd -stop` or `Stop-Service SD`, is never undone. The
service's log, `C:\ProgramData\SD\sdsvc.log`, says which of the two it was.

**A session still running ten seconds after the stop is ended.** `sd -stop`
and `sd -restart` send every session the termination signal, wait up to ten
seconds for them to leave, and end any SD process still running by force (the
runtime's `SIGKILL`, which gives the process no chance to clean up); they say how
many they ended, for example `1 process(es) still running after ten seconds
were ended with SIGKILL`. Only a process whose program is in SD's own folder is
touched, and a session ended this way does not run its own logout.

## `sd -start` and `sd -stop` check the real process, not just the segment

SD's shared state lives in a shared memory segment, which — unlike a file — can
outlive the daemon process that created it if SD is killed rather than stopped
cleanly. `sd -start` and `sd -stop` validate the daemon's actual process id
rather than trusting the segment's mere existence:

**"SD is already started" is only said when the daemon really is
running**, and it names the process id — the Windows one, the number Task
Manager and `Stop-Process` use.

**If the segment is there but the daemon is not** — what a killed or
crashed SD leaves behind — `sd -start` says so and tells you to run `sd -stop`
first, rather than silently reporting success against a segment nothing is
actually serving. It does **not** clear the wreckage for you: that would end
any sessions still attached to the segment. The count of those is printed so you
can decide.

**`sd -stop` checks that the daemon actually stopped.** A daemon started
from an elevated session cannot be stopped from an ordinary one — Windows
refuses the signal — so you get a warning naming the process id and the command
to stop it with.

> **Known limit.** If the segment has already gone, `sd -stop` has nowhere
> left to read the daemon's process id from and cannot report on it at all.
> Check by hand:
>
> ```
> Get-Process sdwind
> ```

**A script may capture what `sd -start` prints.** `$x = sd -start` or
`sd -start | Tee-Object start.log` returns as soon as SD has started. The
background process it leaves running does not keep the script's pipe: it writes
to `/dev/null` instead, so anything it prints after the start is not seen there.
Sent to a file or a console window, its output goes there as before, and so does
the SD service's own log.

**One arrangement still waits.** `sd -start` run through `cmd /c ... > file` from a
PowerShell script whose own output is captured (`*> file`) returned, but the
script went on waiting until SD was stopped: the background process kept a
Windows handle to the script's output, which it cannot see to give back. Run
`sd -start` directly as above, or use `sd -restart` or `Start-Service SD`, which
return at once.

## After an unclean shutdown

If SD is stopped abruptly — the power goes, or the process is killed — it
leaves a shared memory segment behind. **On Windows that survives a reboot.**
Nothing from before a restart can still be using that segment, so SD discards
it at the next start and starts normally, printing:

```
Discarding the shared segment left by the previous boot -
SD did not shut down cleanly.
```

**This changes nothing while the machine is running.** A segment belonging to
a live SD is still never touched, and `sd -start` still refuses to disturb a
system that is already up.

## SD will not start a second time inside itself

**Starting `sd` from inside `sh`** is refused. The shell that `sh` and
`os.execute` start is marked as SD's own (the environment variable `SD_SESSION`
is set in it), and `sd` typed there answers "SD is already running in this
session - type exit to return to it." in every form of the command. It keeps a
second session from being nested inside the first; it is not a wall, because
the mark is an environment variable of that shell.

Worth knowing alongside it: **`sh` itself needs the account's `sh-on` switch
(or SDSYS)**, which is off for a new account, so an ordinary account cannot
leave SD this way until an administrator turns it on for it. See
[Administrator commands](06-administrator-commands.html#the-shell-sh).

## The command line

```
sd                  enter the SD account named after your Windows login
sd -a               prompt for an account
sd -a<name>         enter account <name>  -- refused unless it is your own
sd <command>        run one command       -- needs elevation, or batch.jobs
sd -quiet           suppress the displays on entry
sd -u               list current users   -- elevated only
sd -k <n> | -k all  log out user n, or everybody
sd -start           start the system
sd -stop            stop the system
sd -suspend         suspend updates   -- elevated only
sd -resume          resume updates    -- elevated only
sd -d               diagnostic dump   -- elevated only
sd -m               dump shared memory -- elevated only
sd --version        report the version
sd --help           this summary
```

**Three of these behave differently from what you may expect.**

**`sd -a<name>` is refused unless `<name>` is your own account.** An
administrator no longer opens somebody else's account without ever being in
their own — they arrive in their own (`sdsys`) and reach the rest with **`logto`**, which is
where SD checks whether they are allowed in.

**`sd <command>` needs an elevated session**, or an entry for that account in
`batch.jobs`. **Any account can be given one** — every account has the same
VOC now, so there is nothing about the account to consider here; SDSYS's own
`batch.jobs` list is what decides what may run. That is what makes scheduled
jobs possible without giving them SDSYS's own rights — see
[Scheduled jobs](04-scheduled-jobs.html).

**`sd -suspend`, `sd -resume`, `sd -d` and `sd -m` need an elevated session**, as
`-start`, `-stop`, `-restart` and `-k` do, and otherwise answer "This command
needs an elevated session". `-suspend` stops every update on the system and the
two dumps show every session and the configuration, so they are not for
ordinary users.

**`sd -cleanup` and `sd -u` need an elevated session**, and answer anybody else
the same way: `-u` lists every session on the machine with its user and process,
and `-cleanup` removes other people's entries from the user table. Inside SD,
`listu` shows an ordinary user their own sessions. `sd -status` is for anyone.

**`sd <command>` runs and exits, and is never asked to set a password.** Nor
is any session with no terminal — a scheduled task, or a piped script. **Only
an interactive `sd` with no command after it still asks**, and then only of
an account that has no password yet.

## Where things are

| | |
|---|---|
| Binaries | `C:\Program Files\SD\usr\bin\` |
| The changelog | `C:\Program Files\SD\changelog` |
| Configuration | `C:\ProgramData\SD\sd.conf` |
| The database | `C:\ProgramData\SD\sdsys\` |
| Accounts | `C:\ProgramData\SD\user_accounts\`, `...\group_accounts\` |
| Audit trail | `C:\ProgramData\SD\sdsys\audit` |
| Error log | `C:\ProgramData\SD\sdsys\errlog` |
| Elevation helper log | `C:\ProgramData\SD\sd-elevate.log` |

**Do not move the binaries.** `usr\bin` is load-bearing: shipping
`msys-2.0.dll` beside the executable relocates the POSIX root to the DLL's
directory minus two components, and only that depth puts `/` on
`C:\Program Files\SD\`.

The DLLs ship beside `sd.exe` deliberately — Windows searches the executable's
own directory before `PATH`, which avoids Git for Windows's rival
`msys-2.0.dll` being picked up. **That failure makes SD report "SD has not been
started" while it is running**, which is worth recognizing because it looks
like nothing else.

## The Start Menu

| | |
|---|---|
| **SD** | starts `sd.exe` in the data directory, in a classic console window (it runs `conhost.exe`) |

**SD always runs in a window of its own**, as a Windows application does. The
Start Menu entry opens it; typing `sd` at a PowerShell or cmd prompt opens it
too, and the prompt comes back at once, as it does after `notepad`. The window
is a classic console window that SD controls: it starts at 140 columns by 43
lines (make it bigger whenever you like) and is titled **SD Core**. SD is
designed for Windows 11 on a screen of at least 1920 by 1080.

When SD ends normally (`OFF`) its window closes. **When it ends with an error,
for example a refused sign-in, the window stays open** with "SD stopped - the
reason is shown above. Press Enter to close this window. (exit status *n*)", so
the reason can be read.

These still run where you type them, because they open no session: `sd` with a
command (`sd COUNT VOC`), the switches such as `sd -start` and `sd -stop`,
anything whose input or output is redirected, and an ssh session.
| **Check the SD installation** | the post-install check, re-runnable at any time. Closes on a keypress |
