Title: The AI Helper
Subtitle: One provider and one model for every account, a key that SD never keeps, and a gate for each account.

SD can ask an AI model a question for an account holder (the `ai` verb, described in the User set under *SD TCL - Asking the AI*). This page is for the administrator: it says what is set up, what leaves the machine, how to choose the provider and give it a model and a key, and how to allow or stop an account.

> **This document is separate so that it can be withheld.** It links to nothing outside the
> administrator set. Where a user-set page is worth naming, it is named in words.

> **Nothing is on as delivered.** There is no provider, no key, and no account has the gate (each named provider comes with a default model, so the model is the one thing you need not supply). Until you have done the other three, the `ai` verb says so in words and nothing is sent anywhere. Turning one of them on is your act, and each is one command (or one key on the AI choice page) that can be undone. The one exception is the installer's box *Open every access gate for your SD Core account*: ticked, it gives the installing user's own account the `ai` gate along with the others. It still sends nothing until you have chosen a provider and set its key.

## Security warning

Read this before you turn the AI on.

- **On Windows SDSYS is an elevated Administrator and can read a provider's key; so can any Windows administrator of this machine.** The key is encrypted for the helper's own service account, and the folder that holds it is open only to that account and SYSTEM, but an administrator can take ownership of the folder, run a program as the service, replace the helper's program or change the file that says where a key is sent. On SD Core for Linux the administrator account cannot do any of that. There is no tighter form on Windows while SDSYS is an administrator: treat everyone who is an administrator of this machine as someone who can obtain the key.
- **Turning the AI on sends what a person types, and anything they paste, to the provider's servers on the internet.** SD shows the person what will be sent and sends nothing without their `y`, but it cannot tell what is confidential. Give the gate only to accounts whose people may send their text to that provider, under that provider's terms.
- **Every request is paid for by whoever holds the provider's key.** The limits below cap what one Windows user can use; they are not a budget.

## What leaves the machine

When a person types `ai some text`, SD shows them the provider, the model and the size of all that will be sent, then their text, and asks whether to send it. Only if they answer `y` or `yes` does anything go out. What goes out is your standing text (below), that text, one fixed sentence that asks for a short plain answer, and a limit on the length of the answer. It is sent over **https**, with the certificate checked, to the address of the provider you chose, and to nowhere else. The key goes only to that address. No proxy is used: a machine that reaches the internet only through an HTTP proxy cannot use the AI.

SD adds nothing of the account, the session or the data. A person can of course type or paste whatever they like into the question, which is why the preview is not optional and why the gate is yours to give.

**The standing text.** Every request, from the `ai` verb and from every AI line, begins with a few lines of yours: what SD is, how its commands are written, which gates there are, and where SD's help is. SD ships a default; you can replace it (see [The standing text](#the-standing-text) below). It is invisible to the person asking: it is not in their preview and it does not change their question. The preview's size counts it.

**Passages of the documentation.** On SD Core for Linux the AI line also adds sections of SD's own documentation, from a copy the installer puts in the system directory. **SD Core for Windows does not install that copy** (there is no `docs\user` or `docs\admin` under `C:\ProgramData\SD\sdsys`), so the AI line here sends no passages, and the preview shows none.

## What the AI is never given, and what is not taken to it

**The AI in SD helps a person use SD and write their own programs, dictionaries and files. It is never given SD's own code or any other system information, whichever provider you chose, and not even the administrator can take a question about changing SD to it from inside SD.** The source is open, so someone who wants help changing SD can ask an AI outside SD; inside SD that help is not offered. Two things enforce this, and they are not equally strong.

1. **Where the text comes from (enforced).** Every program that puts the text of a record or file into a request (the IDE and SED, the collection editor and the debugger) tells the AI routine where the text comes from. Before anything is shown or sent, the routine refuses text that is part of SD itself, and text whose origin it cannot tell. SD's own files are everything in the system directory (`C:\ProgramData\SD\sdsys`: the programs, headers, messages, help text, dictionaries and files of the system account, the account register, the audit trail and the error log) and any directory called `gplsrc`, `gplbld` or `gplobj`. It is decided by where a file is, never by what the text says. The headers in `syscom` live in the system directory, so they are not sent either; a person's own programs are, `$include` lines and all. If you want the AI to see one of those headers for a person's program, copy it into that person's account: a copy there is the account's own file, and nothing is opened up.
2. **What is typed (a screen).** A request that names the system's code or build is refused in words before it is shown, and nothing is sent: `gpl.bp`, `gplsrc`, `gplbld`, `$internal`, a kernel file such as `op_sort.c`, a kernel key such as `k$audit`, the compiler's own programs, the makefile, SD's source or kernel code. **This is a screen, not a wall.** A question that names none of those is not caught, and a question that does reach an AI may be answered from whatever that AI learned of the open source. SD's gate is here, in SD.

Nothing the AI returns is run, and the output of a command is never given back to it. A refusal writes one line to the audit trail (`ai refused why=request ...` or `ai refused why=origin ...`) and never the text. What a person types or pastes themselves is theirs, and is in the preview.

## The pieces

| Piece | What it is |
|---|---|
| The service `sd-ai` | The helper, a Python program (`C:\Program Files\SD\lib\sd-ai\sd-ai`) run by the all-users Python 3.13 or later as the Windows service **`sd-ai`** (display name *SD Core AI helper*). It runs as the virtual account **`NT SERVICE\sd-ai`**: no password to keep, no interactive sign-in, a security identifier of its own. It starts automatically, with a restricted service SID (it can write only where its own account is granted) and one privilege (`SeChangeNotifyPrivilege`), and Windows restarts it twice if it fails. For each request it starts one short-lived process of the same program, as the same account; a job object ends them all when the service stops. It is the only part of SD that connects outward and the only part that can read a key. |
| `\\.\pipe\sd-ai` | The named pipe the service listens on: at most 16 connections at once, none from another computer (remote clients are rejected). Its access list is SYSTEM and the service in full, and `sdusers` and Administrators may connect and read and write; nobody else may open it, and nobody but the service may add another instance of it. The service is its owner. Whoever connects is identified by Windows, not by anything they write. |
| `C:\Program Files\SD\lib\sd-ai\` | The program, the administrator's client (`sd-ai-ctl`, run through `sd-ai-ctl.ps1`), `sd-ai-python.ps1` (which finds the Python), and the two data files below. Only administrators can change them; no SD account can. |
| `ai-providers` | In that folder: the connection details that come with SD for Anthropic, OpenAI, Google and DeepSeek, and each one's default model. |
| `ai-context` | In that folder: the standing text that comes with SD. An install replaces it. Your own text, when you have saved one, is `C:\ProgramData\SD\ai\context` and is kept by an upgrade. |
| `C:\ProgramData\SD\ai\` | The helper's own folder: the settings (`ai.conf`), your standing text (`context`), the counters of the limits (`state\`) and the helper's log (`sd-ai.log`: the caller's security identifier, the provider, the result and the sizes of each request, never the text or the key). SYSTEM has full control, the service may change it, Administrators may read it. An upgrade keeps it, and so does an uninstall that keeps the database. |
| `C:\ProgramData\SD\ai\keys\` | One key file per provider. Open only to the service and SYSTEM; each file is encrypted with Windows DPAPI for the service account, so a copy of the file, a backup or a copied disk does not carry a usable key. A key file whose access list names anyone else is refused, not repaired. |
| `sdaiusers` | The Windows group that is the **gate**. Membership of it is what lets an account use the AI. The installer makes it empty. |
| `install-aihelper.ps1` | In `C:\Program Files\SD\`: makes, starts and removes the service. The installer runs it; you run it after installing Python (see [Python](#python)). |

The helper asks Windows who is calling (the account of the process at the other end of the pipe, read at identification level: it can read who called and can never act as them), so the gate does not depend on SD's own programs being honest: a program that talks to the pipe directly gets the same answer. **Before sending anything, SD checks that the pipe's owner is `NT SERVICE\sd-ai`.** The pipe namespace is shared by the whole machine, so while the service is stopped any user could create a pipe of that name and read every request sent to it. A session that finds a pipe owned by anyone else sends nothing, writes `ai refused reason=pipe.owner` to the audit trail and says the helper could not be reached. The service itself refuses to start if a pipe of its name already exists, and says so in the Application log.

## Python

The helper is a Python program, and Windows has no Python of its own. **The AI needs Python 3.13 or later installed for all users** (64-bit, registered for the whole machine; a "for me only" Python cannot be reached by the service). The installer's box *Install Python for all users* installs one from the release's `python\` folder. With such a Python on the machine, the installer sets up the service; without one, it sets up nothing for the AI and says nothing about it, the `ai` verb says the helper could not be reached, and `set.ai` says *The AI needs Python 3.13 or later installed for all users, and none was found*.

To add the AI afterwards, install Python for all users, then run this in an **elevated** PowerShell window:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\install-aihelper.ps1" -Install
```

It prints what it made, read back from the machine (the service's state, account, start type and command, whether the pipe is there, and the access lists of the two folders), and exits **0** when the helper is running, **3** when there is still no all-users Python 3.13 or later (it then removes any service it finds, and keeps your settings and keys), **2** when it was not run elevated, and **1** for anything else. Its log is `C:\ProgramData\SD\install-aihelper.log`. Every install and upgrade runs it again, so a Python that has moved is picked up.

## Who may ask

| Caller | May ask | May change the settings |
|---|---|---|
| An account whose Windows user is in `sdaiusers` | yes | no |
| SDSYS (always an elevated sign-in) | yes, without the gate | yes |
| Another Windows administrator, in an elevated process | only if in `sdaiusers` | yes, with the helper's client |
| Anyone else | no | no |
| A process running as LocalSystem, LocalService or NetworkService | no, whatever the gate says | no |

**Sessions that get no AI.** The helper refuses a process running as one of Windows' own service accounts (LocalSystem, LocalService, NetworkService), because such a process is never a person and never SDSYS. A session at the console or over ssh runs as the person's own Windows user; an API session is started as the Windows user who logged in; a phantom runs as the session that started it; an account's scheduled job runs as that account's Windows user. A session that nobody can answer (a phantom, a scheduled job, a script fed from a file) reaches the preview and sends nothing, because only a typed `y` or `yes` sends.

**Another Windows administrator.** As on Linux, where root may change the settings, an elevated administrator of this machine may change the AI settings by running the helper's client directly (`C:\Program Files\SD\lib\sd-ai\sd-ai-ctl.ps1`, the words of `set.ai` below). Inside SD only SDSYS can: `set.ai` and `tool.ai` are SDSYS's.

## The things that turn it on

1. **A provider.** One for the whole machine: Anthropic, OpenAI, Google, DeepSeek or Custom.
2. **A model** for that provider. Each of the four named providers comes with a default model, shown on the page and used until you name another (`set.ai model PROVIDER NAME`; a dash goes back to the default). The defaults are the balanced model of each provider as its own documentation named it when this release was made: **model names change, so check the one you will pay for.** On the page the model is chosen from the provider's own list in the setup dialog (S), and `set.ai models PROVIDER` prints that list at the prompt. Model names are case-sensitive: `deepseek-v4-pro` works, `Deepseek-V4-Pro` does not. Custom has no default; its model is yours.
3. **A key** for that provider, from the provider's own account. It is typed or pasted in the setup dialog (shown as `*`) or at the helper's own prompt, and kept for the helper only.
4. **The gate for each account that may use it**: `modify.account NAME ai-on`.

The same provider and the same model serve every account; there is no choice per account and no key per account. Of the four, only the provider, the key and the gates have to be supplied: the AI stays off until all three are. The service must be running as well (see [Python](#python)).

## The AI choice page: `tool.ai`

```
tool.ai
```

An administrator-only full-screen page (140 columns by 43 lines at least; it is in SDSYS's VOC only). It has two boxes.

**Provider** lists Anthropic, OpenAI, Google and DeepSeek, then Custom, one to a row. A check box marks the provider in use; none marked means the AI is off. The four named providers come with their address and a default model filled in (the Model column says `(default)` beside one you have not changed); you supply the key, and S (setup) sets the key and the model together. **Custom** is the fifth choice, where you fill in everything yourself, the model included: a name, an `https://` address, the request layout (`anthropic` or `openai`), the authentication (`bearer` or `x-api-key`), a version header (or none) and the name of the field that limits the length of an answer. Below the list, the row under the cursor is shown in full, with the file of certificate authorities and the limits. When the helper does not answer, the box says so and names the service `sd-ai` and its pipe.

**Accounts** lists the accounts that belong to a person, with each one's Windows user and the state of its `ai` gate.

| Key | In the Provider box | In the Accounts box |
|---|---|---|
| Enter or space | check the provider under the cursor (you type its name to confirm), or uncheck the one in use | turn the account's gate on (you type the account's name) or off |
| S | the setup dialog for the provider under the cursor: the key and the model, the model chosen from the provider's own list (below) | |
| X | remove the key | |
| C | fill in Custom | |
| D | remove the Custom connection (the helper refuses while it is in use) | |
| A | the file of certificate authorities (you type `ca` to confirm) | |
| L | change a limit | |
| T | the standing text, in a box with an editor | the same |
| F6, Shift-F6, Left, Right | change box (F6 goes on to the AI line when the AI is on) | change box |
| F1, `?` or a click on `[?]` | explain the box | explain the box |
| F5 | read the machine again | read the machine again |
| Ctrl-Q | leave | leave |

**The page keeps nothing itself and never shows a key.** Every change is a `set.ai` or `modify.account` sentence, shown with its effect in a box that you answer Run or Cancel (Enter chooses Cancel). The page then runs exactly that sentence. The exception is the setup dialog, whose Save is the confirmation.

**The setup dialog (S).** It looks the same every time, whatever is already set:

- **Key**, a password field. What you type or paste is shown as `*`. When a key is already set the field shows a row of twelve stars, which keeps it; replace them to give a new key.
- **Model**, a list of the provider's own model names, with the one in use chosen. With no key yet the list says the key comes first: enter the key and press Tab, and the list is filled from the provider with that key. A model in use that the list does not hold is pointed out, and when it differs from a listed one only in capitals (`Deepseek-V4-Pro` for `deepseek-v4-pro`) the listed one is chosen for you.
- **Other name**, only for a model the list does not hold, such as on a Custom server that gives no list. A name typed here is still checked against the list when there is one.
- **Save** sets what you chose; **Cancel** or Esc changes nothing more (a key already handed over by Tab stays set, and the page says so).

**What the dialog does with the key.** When you leave the Key field with a new key (Tab, or Enter, which then shows the list rather than saving), the page writes it to the file `key` in the folder `$aikey` of the system directory (`C:\ProgramData\SD\sdsys\$aikey`, whose access list it sets to SDSYS and SYSTEM only), runs `set.ai key PROVIDER handover`, which gives the path of that file to the helper's client, and the file is removed whether or not that worked: the client removes it as soon as it has read it, and `set.ai` removes it again. The key is never on a command line and never in the audit trail. It does pass through SD's memory while the dialog is open, and through that file for a moment (Windows does not overwrite a deleted file's space). If you would rather it never touched SD, use `set.ai key PROVIDER` at the prompt, which hands the console to the helper's own prompt.

Opening the page changes nothing and writes one audit line, `tool start app=tool.ai`.

## The verb: `set.ai`

```
set.ai
set.ai provider anthropic | openai | google | deepseek | custom | none
set.ai model PROVIDER NAME | -
set.ai models PROVIDER
set.ai key PROVIDER
set.ai key PROVIDER handover
set.ai key PROVIDER clear
set.ai custom NAME URL FORMAT AUTH VERSION MAXPARAM
set.ai custom clear
set.ai ca PATH | -
set.ai limit NAME NUMBER
set.ai context HEX | -
```

For the administrator only (SDSYS's VOC). Alone it says what is set: the provider in use, each provider's address, model and whether its key is set, the certificate file and the limits. It never shows a key. `provider none` turns the AI off for everyone. `models` asks the provider, with its key, for the names of its models and prints them, one to a line. `model` keeps the name you give, and says so when the provider does not list it (`deepseek does not list a model named Deepseek-V4-Pro, so requests may be refused`, then `It lists deepseek-v4-pro (model names are case-sensitive)`). `key` hands the console to the helper's prompt; nothing typed there reaches SD. `key PROVIDER handover` is what the page runs: it hands the page's file to the helper's client and removes it. When a provider refuses a request, its own explanation is shown after the HTTP status (`the provider refused the request (HTTP 400): Model Not Exist`), cut to one line, with any copy of the key taken out; a refused key (401 or 403) shows only that the key was not accepted. A word may hold letters, digits and `. _ : / @ + , -` and nothing else, so **a path is written with forward slashes**: `set.ai ca C:/ProgramData/SD/ai/ca.pem`. The helper checks every result whole before it writes it: one provider selected means its details are complete, a Custom address is `https://` with no query string, a limit is a whole number in range.

`set.ai` runs the helper's client, `C:\Program Files\SD\lib\sd-ai\sd-ai-ctl.ps1`, through PowerShell; the client finds the all-users Python itself. The helper decides from the Windows user it reads off the pipe that the caller is the administrator, so the client needs no password.

The limits, and what they are as delivered:

| Limit | Delivered | Meaning |
|---|---|---|
| `requests-hour` | 20 | requests one Windows user may make in an hour |
| `tokens-day` | 100000 | tokens (in plus out) one Windows user may use in a day |
| `timeout` | 30 | seconds to wait for the provider (at most 300) |
| `bytes-request` | 65536 | the most that may be sent in one request |
| `bytes-reply` | 65536 | the most that may come back |
| `max-tokens` | 1024 | the longest answer asked for |

## The standing text

Press **T** on `tool.ai` (or choose Provider, Standing text). A box shows the text that is sent first with every AI request from every account, and says whether it is SD's default or yours. Edit it there: Enter starts a new line and Tab moves to the buttons. **Save** shows the command and its effect in a Run / Cancel box (Enter chooses Cancel), and Run keeps your text. **Shipped default** removes yours, so SD's default is sent again. **Cancel** or Esc changes nothing.

The default tells the AI that this is SD Core for Windows, that it should answer for SD and not for another multivalue product, that command words are lower case, which dictionary types there are, that access to the operating system, the shell and the API is a gate you turn on for each account, and where SD's help is: F1 and the `[?]` buttons, the documentation PDFs in the shared account, the SD BASIC guide and the knowledge pack under `C:\ProgramData\SD\sdsys\agent-pack` (for an AI agent that can read files on this machine), and the documentation on the web. Put your own site's facts in it, such as which accounts and files matter and how your programs are named.

What is kept:

- plain English: printable ASCII characters and new lines, at most 4,000 characters;
- nothing that names SD's own code or build (`gpl.bp`, `gplsrc` and the other names of the screen above). Such a text is refused when you save it, with the line `set.ai context refused name=...` in the audit trail. A text that names them all the same (written into the helper's file by hand) stops every request, with `ai refused why=context`, until it is put right.

The text is sent to the provider with every request, before SD's own instruction, and counts towards `bytes-request`. It is invisible to the person asking: it is not in their preview (the size shown there counts it) and their question is sent as they typed it. It is kept by the helper in `C:\ProgramData\SD\ai\context`, and only you can change it. An upgrade keeps it.

At the prompt the verb takes the text as one word of hexadecimal (`set.ai context 48656c6c6f`), which is how the page passes a text of several lines; `set.ai context -` goes back to the default.

## The gate for each account

```
modify.account NAME ai-on
modify.account NAME ai-off
create.account user NAME ai-on
```

The gate is membership of the Windows group `sdaiusers`, as `sdapi` and `sdfiles` are for the API and the files route. It is **off for every account** as delivered and for every new account; the installer's box *Open every access gate for your SD Core account* turns it on for the installing user's own account, with every other gate, and for no other. It is for accounts that belong to a person (a group account is refused), and `ai-on` needs the person to be a member of `sdusers`, as the other gates do. The line printed is `Account fred has ai yes`, read back from the group. It takes effect at the person's next request, with no new sign-in: the helper reads the group each time. `modify.account NAME ai-on ai-off` in one command is refused. An install from before this release has no `sdaiusers` group until the next install or upgrade makes it, and `ai-on` says the group is not a valid Windows group.

SDSYS has no gate: the administrator, who chooses the provider and holds the key, may always use the AI, from the prompt (`ai`) and from the AI line of every page, once a provider, a model and a key are set. `modify.account sdsys ai-on` is not needed and is refused, as every `modify.account` of SDSYS is.

The backup of an account records the gate (`route.ai`) and a restore puts it back.

## The key

The key is typed at the helper's own prompt (`set.ai key anthropic`) or in the setup dialog on the page. At the prompt it goes from your console straight to the helper's client and SD never sees it. From the dialog it passes through SD's memory and a hand-over file only SDSYS and SYSTEM can reach, which is removed at once (see above). Either way the helper encrypts it with DPAPI for its own account and writes it to `C:\ProgramData\SD\ai\keys\anthropic`, open only to the service and SYSTEM; SD does not keep it, print it or put it in the audit trail, and the page and the verb read back only whether it is **set**. `set.ai key anthropic clear` removes it. A key is never an argument of a command, so it is in no process list and no history.

**The encryption protects a copy, not this machine.** A backup, a copied disk or a key file carried to another machine cannot be opened. On this machine an administrator can obtain the key (see [Security warning](#security-warning)).

If a key is lost or shown to someone, clear it and ask the provider for a new one: SD cannot tell you who has seen it.

## Custom: say it plainly

Custom lets you point the helper at any `https://` address. The text people send, and the key, then go to that host. That is your deliberate act and it is the widest thing on this page. What stays fixed: https only (a local model server on `http://` is not allowed), TLS 1.2 or later, the certificate and the host name are always checked (there is no switch to turn that off), the helper never follows a redirect to another host, and the key is sent only to the address you gave. With no certificate file set, the helper trusts the Windows certificate store. A private certificate authority is the file you name with `set.ai ca` (a drive path written with forward slashes, of a file the helper can read); **it replaces the Windows store for the helper**, so whoever holds one of its keys can read what accounts send and the key. Use a file you trust, and `set.ai ca -` to go back to the Windows store.

If you want only the four named providers, leave Custom unfilled.

## The audit trail

All in lower case, none with a key or the text:

```
ai request account=fred program=ai bytes.out=154
ai refused reason=pipe.owner
set.ai provider=anthropic
set.ai model provider=anthropic model=claude-...
set.ai key set provider=anthropic
set.ai key set provider=anthropic from=page
set.ai key cleared provider=anthropic
set.ai custom name=MyLLM host=api.example.com
set.ai ca file=C:/ProgramData/SD/ai/ca.pem
set.ai limit name=tokens-day value=50000
set.ai context bytes=1640
set.ai context=default
set.ai context refused name=gpl.bp
ai refused why=context app=home name=gpl.bp
modify.account ai-on account=fred
tool start app=tool.ai
```

The `ai request` line is written by the SD kernel **before** the connection is made, with the account and the program that called, so a crash or a refusal still leaves the record. The Custom line names the host and never the whole address. The helper itself writes nothing to the audit trail; its own one line per request is in `C:\ProgramData\SD\ai\sd-ai.log`.

## Troubleshooting

Start with the service. In an ordinary or an elevated prompt:

```
sc.exe query sd-ai
```

A `STATE` line that ends `RUNNING` is what you want. `The specified service does not exist as an installed service` means it was never set up: usually there was no all-users Python 3.13 or later when SD was installed (see [Python](#python)). A service that is stopped and will not start writes the reason to the **Application** event log with the source **`sd-ai`** (Event Viewer, *Windows Logs*, *Application*), for example when a pipe of its name was already made by someone else. The installer's record of setting it up is `C:\ProgramData\SD\install-aihelper.log`, and the helper's own record of each request is `C:\ProgramData\SD\ai\sd-ai.log`.

| What you see | What it means |
|---|---|
| `The AI helper could not be reached: it is not running, or it is not installed` | the service is not running, is not installed, or the pipe is not the service's (then the audit trail has `ai refused reason=pipe.owner`): `sc.exe query sd-ai`, the Application log, and `install-aihelper.ps1` |
| `The AI needs Python 3.13 or later installed for all users, and none was found` | from `set.ai`: install Python for all users, then run `install-aihelper.ps1 -Install` elevated |
| `The AI is off: the administrator has not chosen a provider (tool.ai or set.ai)` | nothing is checked on the page (`set.ai provider ...`) |
| `The AI is not set up for anthropic: the administrator has not set its key` (or `model`) | the provider is chosen but its key is missing; a model is missing only for Custom, which has no default (the named providers have one) |
| `This account may not use the AI: the administrator can allow it with modify.account NAME ai-on` | the account's Windows user is not in `sdaiusers`, or the session runs as one of Windows' service accounts |
| `The AI did not answer: limit (...)` | one of the limits above is used up; wait, or raise it |
| `The AI did not answer: net (...)` or `timeout` | the provider could not be reached; check the address, the certificate, the clock, and whether the machine needs a proxy to reach the internet (the helper uses none) |

## What has not been shown

**Not run on Windows yet.** The helper, the verb and the page are SD Core for Linux's, carried here with the Windows facts on this page, and compiled; their free checks pass. On Linux they were tested against a stand-in provider on the same machine, in a private copy of SD, and **not against a real provider**: the request layouts follow each provider's published documentation, and the one for OpenAI (`max_completion_tokens`) has not been checked against a real key. On Windows none of the following has yet been run on an installed system: the service under its virtual account, the pipe and its owner check, a squatted pipe being refused, the DPAPI key files, the live gate, which Windows user each kind of session reaches the helper as, and `set.ai key` at the prompt handing the console to the client through PowerShell.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Giving an AI Agent an Account](18-the-agent-account.html) ·
[Operating system access](03-operating-system-access.html) ·
[The Audit Trail](20-the-audit-trail.html).
