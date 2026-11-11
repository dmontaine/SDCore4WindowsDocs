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

## What it refuses on Windows, and why

**On Windows `run.in` is new authority.** `LOGTO` out of SDSYS gives up the administrator's rights
and ends the elevated helper; `run.in` keeps both for the one command, so the command has the
administrator's rights inside the account. And an SDSYS session's own Windows token is elevated, so
anything of the account's that ran during the command would run as the elevated administrator. So,
once it is in the account and before the command runs, `run.in` refuses:

* **a command or option word that is not the VOC entry SD supplies.** The account's VOC entry for
  the command (`basic`, `catalog` ...) and for each option word (`no.catalog` included) must be
  SD's own: the same as SDSYS's entry, its type letter and what it runs. An account could otherwise
  make `basic` a program of its own. `basic in the VOC of account ACME is not the entry SD supplies;
  run.in did not run the command`. **An account whose VOC has no `no.catalog` keyword** (one made
  before the keyword existed and not updated since) is refused for `basic` until its VOC has it.
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
  with `$EXECUTE is not run in a compile that run.in runs`.

Each refusal writes `run.in refused account=ACME reason=...` to the audit trail.

**What it does not cover:** a source that includes a record (`$include`) from another of the
account's files reads that file too; a read trigger on that file would run. The files a command
reads by a name in the source are not listed in advance.

## The audit trail

Every use writes `run.in begin account=… command=…` and `run.in end account=…` (or
`run.in revert account=… reason=abort`) to the audit trail, and a refusal writes `run.in refused …`
with the reason.
