Title: Lower case
Subtitle: Commands, file names, record ids and account names are lower case now — and nothing you type has to change.

**Everything that can be lower case is lower case, completely — no name
exists in two casings.** BASIC source is free-form and usually written lower
case; file names, field names and account names are lower case as well.

**What you type does not change.** `LIST`, `list` and `List` all run the same
verb, and so does every keyword — `with`, `by`, `no.page` and the rest.

## The lookup rule

SD tries a name **as you typed it, then in lower case, then in upper case**.

```
as typed  →  lower  →  upper
```

A name that matches exactly still wins, so nothing that works today changes. A
name that exists in **no** case is still reported as not found.

This order is used everywhere: the parser, the query processor, `run`,
the `login` paragraph lookup, and `set.file`'s default `qfile` pointer.

## What is spelled in lower case, and that is the whole of it

| | |
|---|---|
| Commands in the VOC | **`list`**, `count`, **`select`**, **`create.file`**, **`setptr`** … and that is how they appear in `list voc` and `ct voc` |
| BASIC source and include records | the `gpl.bp` programs and the `syscom` includes — all of them |
| System files on disk | `accounts`, `bp`, `bp.out`, `gpl.bp`, `gpl.bp.out`, `messages`, `newvoc`, `pcode.out`, `syscom`, `voc`, `voc.dic`, `voc_template` and the rest under `sdsys` |
| Account names on disk | `sdsys\accounts\sam`, matching the account's own directory in `user_accounts` |
| Files in a new account | created with lower-case names on disk |

**Renaming these is cosmetic for resolution** — NTFS matches without being
asked — but the stored path text is user-visible through `list voc with type = "F"` and the
current-directory reporting, which is the point.

## Record ids in directory files are no longer case sensitive

Two changes that go together:

- **Record ids in directory files** are matched case insensitively.
- **Queries against a directory file** match ids the same way.

Every file `create.file` makes treats record ids as case insensitive (there is
no `no.case` or `case` word to give it): SD writes records preserving the
casing given by whatever performs the write, and reads locate records
regardless of casing.

**An upgrade converts the files you already had**, account by account, and leaves
what it cannot convert safely: a file with two ids that differ only by case, an indexed
file, a file outside its account's directory or under SDSYS, and SDSYS's own files.
`nocase-upgrade.log` names each one, and the installer's closing box says that some were
left. The mechanics are in [Upgrading and uninstalling](01a-upgrading-and-uninstalling.html).

## One lookup order everywhere

**`list` and `ct` find a name the same way.** `list voc $hold` finds the record
`ct voc $hold` shows. `list`, `sort`, `select` and the rest of the query
language use the same as-typed → lower → upper order as everything else.

## Account names

**Account names have never been case sensitive and still are not.**
**`create.account`**, **`logto`** and the rest accept whatever case you type.

What changed is how the register file is named on disk: accounts are
recorded in lower case, so `sdsys\accounts\sam` matches the account's own
directory on disk.

## Two related refusals that no longer depend on case

**`delete.file`**'s refusal to delete `voc` and `$acc` no longer depends on the
case you type. It could not be got round before, because those names were upper
case — **it could have been, once they are not.**
