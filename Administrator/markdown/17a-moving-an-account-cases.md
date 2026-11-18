Title: Moving an Account: the Windows User and the Cases
Subtitle: What a restore does to the Windows user, and the cases where the two machines differ.

This page continues [Moving an Account](17-moving-an-account.html).

## When the machines differ

* **A different folder for the accounts.** VOC entries that hold the account's old path are
  rewritten to the new one. A pointer to somewhere outside the account is listed, not followed.
* **From SD Core for Linux.** The archive's `product` says which system made it, and a Linux
  account restores onto Windows like any other full-product backup; its paths are rewritten as
  above.
* **From a Windows archive**, a rewritten path that does not exist with exactly that spelling is
  listed, so a path whose case changed on the way is seen before a program trips over it.
* **Indices kept outside the account.** A hashed file whose indices were relocated inside the
  account is pointed at its new index path. Indices outside the account are not in the archive,
  and the restore says so: build them again with `build.index`.
* **The account's Windows user.** An account the new machine already has keeps its own
  operating-system user, password and groups. One that SD creates is made as `create.account`
  makes it, from the manifest's description, routes, members and suspension.
* **`latest` will not find a zip made elsewhere.** `restore.account latest` picks the newest
  backup *made on this computer* that holds every named account, and a zip made on another
  machine names another host in its file name: name the zip by its path.

The steps on the previous page are what the two verbs do for a move between machines and for a
restore from SD Core for Linux.

## See also

[Account Maintenance](01a-account-maintenance.html) for the verbs and `set.backup.directory`;
[Accounts and Security](01-accounts-and-security.html) for the switches;
[Data at Rest](04a-data-at-rest.html) for backups and encryption.
