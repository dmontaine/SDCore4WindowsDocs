Title: run.in
Subtitle: The administrator's account-scoped run: one command from a fixed list, inside a registered account, and always back in SDSYS - and what it refuses on Windows because an SDSYS session's token is elevated.

A program is compiled and cataloged in its own account: its VOC, its private catalog, the files its
I-types translate through. An account that is locked out of its own programs (`bp-off`) cannot do
that, so the administrator does it for the account. `tool.entries` (see
[The master files](19-the-master-files.html)) and the editor it opens use it for every compile.

```
run.in acme basic bp prog
run.in acme basic bp prog debugging no.query
run.in acme catalog bp prog local no.query
run.in acme decatalog prog
run.in acme delete.catalog prog local
run.in acme compile.dict cust total
```

The verb is in the SDSYS VOC only and refuses anyone else ("Command requires administrator
privileges"). It runs **one** command from the list above, in a **registered** account (never
SDSYS itself, never a path), and **it is back in SDSYS when the command ends**. That includes a
command that aborts, a break and a run-time error: the session is put back before anything else
happens and says so ("run.in: the command did not finish; the session is back in account acme").
`LOGTO SDSYS` is refused for everybody, so without this an administrator who had gone into an
account would have no way back for the rest of the session.

**There is no `debug` on Windows** (Linux has a sixth command, `run.in` *account* `debug` *file*
*program*): the debugger runs the account's program, and here it would run with the session's
elevated token. `run.in acme debug bp prog` is refused (`debug is not a command run.in runs`).
Debug a program in its own account.

## What it checks before it changes anything

The account and every name are one plain word (a-z, 0-9, dot, dash and underscore, a letter or digit
first, at most 64 characters, and not a word SD reads as an option); each option is on that
command's own list and is given once; the first name of `basic`, `catalog` and `compile.dict` is a
file in **that account's** VOC. **The command SD runs is built from those words and is never the
text you typed.** **`basic` is always given `no.catalog`**, so a `$catalog` directive in the
account's source (or in a file it includes, or in its `$BASIC.OPTIONS`) is not acted on: without
it, compiling the source as the administrator would catalog it as the administrator, in the global
catalog if the directive says `global`. To catalog a program of an account, say so:
`run.in acme catalog bp prog`. `run.in` does not start the account's `login` paragraph (it would
run with the administrator's rights), and it does not nest.

## The command does not run as the administrator

The account's files, VOC and programs are written by the account's user, so nothing in them is
trusted. For the command itself the administrator flag is **off**, only the edit gate the command
needs is on (`bp-edit` for `basic`, `catalog`, `decatalog` and `delete.catalog`, `dict-edit` for
`compile.dict`), and `sh` and `os.execute` are off whatever the account's own switches say.
Everything is put back when the command ends, the flag last. So `run.in acme catalog` with a
`global` request is refused, as it would be for the account.

**The words must be SD's own.** The command word and every option word (`no.catalog` included)
must be, in that account's VOC, exactly the entry SD ships: the record of the same name in
`newvoc`, its type letter and everything after the description. An account that has changed or
removed one (its own `basic`, say) is refused before anything happens, and before anything is
kept or changed: *run.in: basic is not SD's own entry in the VOC of account acme (it is missing or
was changed there); nothing was run*. Put SD's own entry back in that account's VOC and try again:
`update.accounts` does it, since it adds a shipped entry that is missing and rewrites one that differs
from the record of the same name in `newvoc` (it asks first where the type letter differs, and keeps an
entry whose description says `[LOCKED]` unless it is a verb). **An account whose VOC has no `no.catalog` keyword** (one made before the keyword
existed and not updated since) is refused for `basic` until its VOC has it.

**On Windows that is not the whole of it.** An SDSYS session's own Windows token is elevated for the
whole session, and turning SD's flag off does not change it. So anything of the account's that ran
during the command, and any file it read, would have the elevated administrator's reach. So, once
it is in the account and before the command runs, `run.in` also refuses:

* **a file the command writes that lies outside the account**: the named file's data and dictionary,
  the `.out` file of `basic` and `catalog`, and the private catalog of `catalog`, `decatalog` and
  `delete.catalog`. A path must be relative, with no `..`, no `@` token and no drive, and what of
  it exists is asked of the kernel (which resolves it as an open would). A VOC entry could
  otherwise point the compile's output at SDSYS's own files, which this session can write. `bp.out
  in account ACME names a path outside the account; run.in did not run the command`.
* **a file the command opens that has a trigger**: the VOC, the named file and its dictionary, the
  `.out` file and the private catalog. A trigger is a program found in the account's own catalog,
  and it would run in this session. `bp in account ACME has a trigger function; run.in did not run
  the command`.
* **a `$execute` line in the source it compiles.** The compiler runs the command a `$execute`
  directive names while it compiles; under `run.in` it refuses it instead, and the compile fails
  with `$execute is refused in a compile started by run.in: it would run a command from the
  administrator's session`.

And while the command runs:

* **an include file or a dictionary outside the account.** A `$include` (or `include`), `$dict` or
  `file` that leads outside the account's own directory, through a pointer in its VOC, fails the
  compile: `... is outside the account: a compile started by run.in reads include records and
  dictionaries in the account and syscom only`. SD's own `syscom` headers are still found.
* **a Q-pointer out of the account.** A Q-pointer, or the *account*`:`*file* form, leads only into
  the account the command runs in.
* **`logto`.** `logto is refused while run.in is running a command in account acme`.

Each refusal writes `run.in refused account=ACME reason=...` to the audit trail (a refused word
also gives `word=`).

**What it does not cover:** a source that includes a record from another of the account's own files
reads that file too, and a read trigger on that file would run. The files a command reads by a name
in the source are not listed in advance.

## The audit trail

Every use writes `run.in begin account=… command=…` and `run.in end account=…` (or
`run.in revert account=… reason=abort`) to the audit trail, and a refusal writes `run.in refused …`
with the reason.
