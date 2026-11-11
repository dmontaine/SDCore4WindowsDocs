Title: The Master Files: Programs and Global Changes
Subtitle: The programs view of tool.entries - editing and compiling a program in its own account - and G, the change of every row shown, with U to put it back.

This page continues [The master files](19-the-master-files.html), which describes the page
`tool.entries`, its lists and the pointer rule.

## Programs: `E`, `N` and `C`

**In the programs view, `E` and `N` open the program in the editor and `C` compiles it, in the
account it belongs to.** `E` and `N` go the same way as for a VOC entry: the program file must lie
inside the account (a program file reached through a pointer to another account, marked `>`, is
refused), and so must the program's own file. The temporary pointer reaches the program file's data
only. The editor is told which account the program belongs to, so its **Compile** (F8) and
**Compile and catalog** (F9) do not run BASIC in SDSYS through the pointer: they run
[run.in](19b-run-in.html) in that account, so the object goes into the account's own `bp.out`, a
`$catalog` line in the source is not acted on, and the catalog is the account's. **Run** is refused
in the editor (run it in its account), and so is **Debug** of such a program: `run.in` does not
debug in another account on Windows, and says so (`debug is not a command run.in runs`).

**`C`** on the page compiles the program under the cursor the same way and shows what the compiler
said in a box; the Built column follows. The page writes `master edit account=ZE1 kind=bp file=bp
id=prog new=0` for an edit and `master compile account=ZE1 file=bp id=prog result=ok` (or `failed`)
for `C`; `run.in` writes its own `run.in begin` and `run.in end` lines for each compile. A compile
that `run.in` refuses (a command word that is not SD's own entry in that account, a file outside the
account, a file with a trigger, a `$execute` line in the source) shows the refusal in the same box.

**`B` is not built on Windows.** On Linux it debugs the program under the cursor in its account; here
it says `B is not built on Windows: run.in does not debug in another account.  Debug the program in
its own account`, and does nothing else.

## A global change of every row shown: `G`, and `U` to put it back

**`G` makes one change to every row the page shows, in every account the rows come from.** The rows
are exactly those on the screen: the hits of a find (`F`, every account) or the entries a filter
(`/`) keeps in the account under the cursor. A filter or a find must be on, and a list cut short at
the page's limit is refused (narrow it until every row is shown). `G` asks what to change:

- **VOC entries and dictionary items**: the field, by its number (1 to 500) or, for a dictionary
  item, the word `heading` (field 4 of a D, I, E or L item; an item of another type is refused for
  having no heading), then `S` to set the field to a value or `R` to replace a text in it with
  another (an empty replacement takes the text out).
- **Field 1 is the type of the record** (a VOC entry's V, F, Q, PA ...; a dictionary item's D, I,
  PH ...), and changing it turns a verb or a pointer into something else. `G` therefore changes it
  on **one record only**: when more than one record is shown it is refused before the box
  (`field 1 is the type of the record: G changes it on one record only, and 3 are shown ...`), and
  on a single record the box carries a **WARNING** line with the old and the new type (`"X" ->
  "PA"`). Cancel is still the default, and `U` puts field 1 back like any other field (the owner,
  3 Nov 2026: exclude field 1 from batch actions, allow it on a single item with a confirm warning).
- **Programs**: a text to replace in the source and what replaces it. Each program changed is then
  compiled again **in its own account** through `run.in` (as `C` does), and is counted as failed
  when the compiler does not say it compiled.

The texts are printable characters only, up to 120 of them. **One box** (titled *Update these
records?*) then shows the change, and each account with how many records would change, the first
ids, how many are as they are already and how many would be refused, with the first reasons. **Run
or Cancel is all it asks** (Cancel is the default): no name or count is typed. This is looser than
`D`, which asks for the id; it is the owner's choice (3 Nov 2026), made after he was told so, and
it is how the page is delivered.

Run writes **account by account**. Each account is judged again (it must still be in the register),
and each file by **the pointer rule** before it is opened for writing: the path, what the kernel
opened, and the two parts of a hashed file must lie inside the account (a program's own file too). A
row whose file lies outside the account it is listed under - the dictionary of `@SDSYS/voc.dic`,
another account's file reached through a pointer, a path written with `..` - is **refused**, in the
box and again at the write; its target is never written. Each record is read with its update lock
(a record another session holds is refused) and must still be what the box read (one changed since
is refused). **A refusal or a failure is counted and the run goes on**, in that account and in the
next. A box then shows, for each account, how many records were changed, refused and failed, with
the first reasons; the audit trail gets one line per account:
`master global account=ZE1 kind=dict changed=2 refused=3 failed=0` (`kind=voc`, `dict` or `bp`).

**`U` puts the last global change back.** Before each record is written, the record as it was is
kept in `&entries.undo&`, a file of SDSYS's own account; the first time, a box shows the command
that makes it (`create.file &entries.undo&`) and nothing is changed unless it is made. It holds the
last run only: a new run replaces it. `U` (offered while there is a run that has not been put back)
shows a box titled *Put these records back?* (Run or Cancel) and then puts back each record **only
if it is still exactly what the run wrote**; a record edited since is left as it is and counted,
never overwritten, and so is one that has gone or that another session holds. The pointer rule is
asked again, and a program put back is compiled again in its account. The audit trail gets
`entries undo account=ZE1 records=2` for each account. When nothing was held, refused or failed the
run is marked put back and `U` is no longer offered.

The AI line of the page is not offered `G` or `U`.
