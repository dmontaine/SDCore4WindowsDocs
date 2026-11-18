Title: Accounts and Security: File Writing, the AI and VOC Pointers
Subtitle: files-write-on, files-admin-on, ai-on, where a file pointer may lead, and what os-on costs.

This page continues [Accounts and Security: The Shared Account and the Files-only Route](01-accounts-and-security-4-shared-and-files-only.html).

### Changing files: `files-write-on` and `files-write-off`

A files-only login may write, delete, lock and clear **only if the person is also in
the Windows group `sdfileswrite`**, which the administrator of that server gives with
`modify.account` *name* `files-write-on` (or `files-write-on` after `files-on` in
`create.account user`) and takes away with `files-write-off`. It is off for a new
account. The line SD prints after a change is read back from the group, as for
`files-on`:

```
:modify.account fred files-write-on
Account fred has files-write yes
```

`files-write-on` for a person who is not in `sdfiles` is refused ("Account fred does
not have files access, so it cannot be given files-write: use files-on first"), because
the group on its own gives nothing; `files-off` takes the person out of both groups.
**`files-off` takes the groups above `sdfiles` away first (administration, then write), then `sdfiles`, and reads each back**,
and it does the work for a person who is in only one of them. A person who is in `sdfileswrite`
and not in `sdfiles` (a removal that stopped half way, or a change made by hand) is taken out
of `sdfileswrite` too, so the next `files-on` cannot turn that membership into write access
nobody gave. If a removal fails SD says so and stops, leaving the person with the lower access
and never a higher one without it. `files-on` takes a leftover `sdfileswrite` or `sdfilesadmin`
membership away before it adds `sdfiles`, and stops with the same message if it cannot. A
refused change is answered "This login cannot change or lock files here: ask the
administrator for files-write-on (request *n*)", is not carried out, and goes to the audit
trail as `api refused request=16 route=sdfiles write=off admin=off user=fred`; the login line says
`write=on` or `write=off` (and `admin=on` or `admin=off`). `sdapi` members are not affected. Like `sdfiles`, the group is
read at login, so a change reaches the person at their next login. The account's manifest
(`backup.account`) records it as `route.files.write`, and `restore.account` gives it back
only to an account that is in `sdfiles`.

### Administering files: `files-admin-on` and `files-admin-off`

A files-only login may configure a file, build and delete its indices, create and delete a file,
and set or take the file's counter (`WRITE ... CREATING.SEQKEY`, `FCONTROL`) **only if the person
is in both `sdfileswrite` and the Windows group `sdfilesadmin`**: `modify.account` *name*
`files-admin-on` (needs `files-on` and `files-write-on` first, else "Account fred does not have
files-write, so it cannot be given files-admin: use files-write-on first", message 12531),
`files-admin-off`, and `files-admin-on` after `files-on` and `files-write-on` in `create.account
user` (without them it is refused the same way, before anything is made). **It is off for every new
account, and nothing in the installer turns it on.** The line
printed is `Account fred has files-admin yes`, read back from the group. A group account or an
`other` account is refused as it is for `files-on`.

The three groups are a chain, `sdfiles` < `sdfileswrite` < `sdfilesadmin`: `files-write-off` and
`files-off` take the higher groups away first (administration, write, files), each removal read
back, and a failure half way reports the removals that did happen (`Account fred has files-admin
no`, and the audit line `modify.account files-admin-off account=fred`) before it reports the
failure. `files-on` and `files-write-on` take a stray higher membership away before they add. Two
words that ask for opposite things in one command are refused with message 12796 and nothing is
changed (`files-admin-on` with `files-off` or with `files-write-off`, and `files-write-on` with
`files-off`). What the permission allows, what the server checks and how it is audited is in
[SDNet](12-sdnet.html), *The administration group*. A refused request is answered "This login
cannot administer files here: ask the administrator for files-admin-on (request *n*)" (message
12529) and nothing is carried out. The account's backup manifest records the membership as
`route.files.admin`, and `restore.account` gives it back only to an account that is in `sdfiles`
and `sdfileswrite`.

**What is not changed.** Everything else about the session applies as it does to any
other: the account must be entered, the account's own switches (the OS-access
gate, the three edit switches, the NET switch) are loaded and enforced, `SDCLIENT` in
`sd.conf` still decides whether a client may open the files it names, and the
API listener must be on (`remote.api`). **`sdfiles` alone is a read-only route.**
`modify.account fred none` takes away `ssh` and the API and not the files-only
login; withdraw it with `files-off`. `sdapi` is never touched by `files-on` or
`files-off`.

### The AI: `ai-on` and `ai-off`

An account may send text to the AI provider you have chosen (the `ai` verb and the AI line of
the pages and editors) **only if the person is in the Windows group `sdaiusers`**:
`modify.account` *name* `ai-on`, `ai-off`, and `ai-on` in `create.account user`. **It is off for
every new account.** The installer turns it on only for the installing user's own account, and
only when its box *Open every access gate for your SD Core account* is ticked, because each request
is paid for by whoever holds the provider's key and sends the person's text off the machine. The
line printed is `Account fred has ai yes`, read back from the group. It stands alone (no other gate
is needed), is for accounts that belong to a person (a group account is refused), needs the person
to be in `sdusers`, and takes effect at the person's next request: the AI helper, the Windows
service `sd-ai`, reads the group each time, from the Windows user it sees at the other end of its
pipe. SDSYS has no gate and may always use the AI. The account's manifest records it as
`route.ai`, and `restore.account` gives it back. Which provider, model and key, what leaves the
machine, the security warning, and the page that does all of this, `tool.ai`, are in
[The AI Helper](20-the-ai-helper.html).

### VOC pointers: where a file pointer may lead, and which Q-pointers are followed

**A VOC pointer is a way to name a file, so it is held to the same rule.** An
account can write a pointer into its own VOC with `ed`, or make one with
`create.file ... pathname`, and a Q-pointer is what `set.file` makes into
another account. For everybody but SDSYS:

| | |
|---|---|
| **a file pointer (F-type)** | must lead **inside the account's own directory**, or be **the pointer SD itself put in the VOC** (the stock entries of `newvoc`). An account that holds `os-on` may go anywhere its Windows user can. Anything else is refused with status 3035 |
| **a Q-pointer** into a **registered account** | is followed only if the user **could `logto` that account**: a member of its Windows group, and the account not suspended — `logto`'s own test — **whether or not the account holds `os-on`** |
| **a Q-pointer** that **names a path** | is an operating-system path, and the `os-on` question |

So `set.file` into somebody else's account works only for a user who may enter
that account, and a hand-made pointer at a system directory or another
account's directory is refused unless the account holds `os-on`. A refused
open takes the `ELSE` branch with status 3035, like any other refusal here.
**SDSYS is never refused.** The accounts that existed at an upgrade hold what
`os.users` gave them (above), so an account that had `os-on` keeps its own
pointers; the Q-pointer rule applies to every account. The API's request 29,
"open an SDNet file", asks the same question of the account named in the
request ([SDNet](12-sdnet.html)).

The `account:file` form of a file name is always available, with no `sd.conf`
setting: a name in no VOC record with one colon is read as a Q-pointer to that
account and file, and the **Q-pointer rule above applies to it unchanged**, so it
opens only what a Q-pointer the account wrote could open. A drive-letter pathname
such as `C:\data\x` has one colon too; it is read as account `C`, which is not
registered, so it is not found. Any other file outside the account is reached only
through a VOC pointer, which is held to the `os-on` rule and the Q-pointer rule
above.

### What `os-on` actually costs

Granting `os-on` to any account is a larger decision than it looks.

**That account reaches the operating system over the API as well as
locally** — and over the API the session's process token is LocalSystem.
On an ordinary account with both `os-on` and API access, a remote API
connection makes the operating system report the session as
`nt authority\system`.

This is accepted behavior rather than a defect, and it follows from the
way SD's listener creates a session — it is unrelated to the account's own
identity, which is why it is stated here rather than assumed. It is stated
here because it is not something a reader should have to discover: `os-on`
on an account with API access gives that account the operating system, as
LocalSystem, from any machine that can reach the API port.

## Continued in

[Accounts and Security: Changing One Account](01-accounts-and-security-6-modify-account.html) — modify.account and the two account screens.
