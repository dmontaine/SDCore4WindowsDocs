Title: The AI Helper
Subtitle: One provider and one model for every account, a key that SD never sees, and a gate for each account.

SD can ask an AI model a question for an account holder (the `ai` verb, see *SD TCL - Asking the AI* in the User documentation). This page is for the administrator: it says what is set up, what leaves the machine, how to choose the provider and give it a model and a key, and how to allow or stop an account.

> **Nothing is on as delivered.** There is no provider, no key, and no account has the gate (each named provider comes with a default model, so the model is the one thing you need not supply). Until you have done the other three, the `ai` verb says so in words and nothing is sent anywhere. Turning one of them on is your act, and each is one command (or one key on the AI choice page) that can be undone. The one exception is the installer's box *Open every access gate for your SD Core account*: ticked, it gives the installing user's own account the `ai` gate along with the others. It still sends nothing until you have chosen a provider and set its key.

## Security warning

Read this before you turn the AI on.

- **On Windows SDSYS is an elevated Administrator and can read a provider's key; so can any Windows administrator of this machine.** The key is encrypted for the helper's own service account, and the folder that holds it is open only to that account and SYSTEM, but an administrator can take ownership of the folder, run a program as the service, replace the helper's program or change the file that says where a key is sent. On SD Core for Linux the administrator account cannot do any of that. There is no tighter form on Windows while SDSYS is an administrator: treat everyone who is an administrator of this machine as someone who can obtain the key.
- **Turning the AI on sends what a person types, and anything they paste, to the provider's servers on the internet.** SD shows the person what will be sent and sends nothing without their `y`, but it cannot tell what is confidential. Give the gate only to accounts whose people may send their text to that provider, under that provider's terms.
- **Every request is paid for by whoever holds the provider's key.** The limits below cap what one Windows user can use; they are not a budget.

## What leaves the machine

When a person types `ai some text`, SD shows them the provider, the model and the size of all that will be sent, then their text, and asks whether to send it. Only if they answer `y` or `yes` does anything go out. What goes out is your standing text (below), that text, one fixed sentence that asks for a short plain answer, and a limit on the length of the answer. It is sent over **https**, with the certificate checked, to the address of the provider you chose, and to nowhere else. The key goes only to that address. No proxy is used: a machine that reaches the internet only through an HTTP proxy cannot use the AI.

SD adds nothing of the account, the session or the data. A person can of course type or paste whatever they like into the question, which is why the preview is not optional and why the gate is yours to give.

**The standing text.** Every request, from the `ai` verb and from every AI line, begins with a few lines of yours: what SD is, how its commands are written, which gates there are, and where SD's help is. SD ships a default; you can replace it (see [The standing text](20a-the-ai-helper-set-ai-and-the-key.html#the-standing-text) below). It is invisible to the person asking: it is not in their preview and it does not change their question. The preview's size counts it.

**Passages of the documentation.** The AI line (the home screen, the pages of the toolkit, the IDE, SED, the collection editor and the debugger; not the `ai` verb) also adds up to four sections of SD's own documentation that match the request, at most 2,400 bytes each and 6,000 in all. They are sent and counted in the preview's size, but the preview does not list them. The installer puts the markdown of the User and Administrator documents in `docs\user` and `docs\admin` under the system directory (`C:\ProgramData\SD\sdsys`), from the documentation repository (`SDCore4WindowsDocs`) beside the source on the machine that builds the installer. `docs` and `docs\user` are read-only for the group `sdusers`. **`docs\admin` is yours alone: only SYSTEM and the Administrators group can open it, there is no entry for `sdusers`, and the routine asks SD for the administrator before it looks there.** An account holder's request is never answered from those pages. An upgrade replaces the directory whole and locks it again, and it is not a place to put your own text. The installer is not built without the documentation repository, so an installed system always has the pages. This is documentation, not source: the rule below that the AI is never given SD's own code is unchanged.

## What the AI is never given, and what is not taken to it

**The AI in SD helps a person use SD and write their own programs, dictionaries and files. It is never given SD's own code or any other system information, whichever provider you chose, and not even the administrator can take a question about changing SD to it from inside SD.** The source is open, so someone who wants help changing SD can ask an AI outside SD; inside SD that help is not offered. Two things enforce this, and they are not equally strong.

1. **Where the text comes from (enforced).** Every program that puts the text of a record or file into a request (the IDE and SED, the collection editor and the debugger) tells the AI routine where the text comes from. Before anything is shown or sent, the routine refuses text that is part of SD itself, and text whose origin it cannot tell. SD's own files are everything in the system directory (`C:\ProgramData\SD\sdsys`: the programs, headers, messages, help text, dictionaries and files of the system account, the account register, the audit trail and the error log) and any directory called `gplsrc`, `gplbld` or `gplobj`. It is decided by where a file is, never by what the text says. The headers in `syscom` live in the system directory, so they are not sent either; a person's own programs are, `$include` lines and all. If you want the AI to see one of those headers for a person's program, copy it into that person's account: a copy there is the account's own file, and nothing is opened up.
2. **What is typed (a screen).** A request that names the system's code or build is refused in words before it is shown, and nothing is sent: `gpl.bp`, `gplsrc`, `gplbld`, `$internal`, a kernel file such as `op_sort.c`, a kernel key such as `k$audit`, the compiler's own programs, the makefile, SD's source or kernel code. **This is a screen, not a wall.** A question that names none of those is not caught, and a question that does reach an AI may be answered from whatever that AI learned of the open source. SD's gate is here, in SD.

Nothing the AI returns is run, and the output of a command is never given back to it. A refusal writes one line to the audit trail (`ai refused why=request ...` or `ai refused why=origin ...`) and never the text. What a person types or pastes themselves is theirs, and is in the preview.

## The pieces

| Piece | What it is |
|---|---|
| The service `sd-ai` | The helper, a native program (`C:\Program Files\SD\lib\sd-ai\sd-ai.exe`), runs as the Windows service **`sd-ai`** (display name *SD Core AI helper*). It runs as the virtual account **`NT SERVICE\sd-ai`**: no password to keep, no interactive sign-in, a security identifier of its own. It starts automatically, with a restricted service SID (it can write only where its own account is granted) and one privilege (`SeChangeNotifyPrivilege`), and Windows restarts it twice if it fails. For each request it starts one short-lived process of the same program, as the same account; a job object ends them all when the service stops. It is the only part of SD that connects outward and the only part that can read a key. |
| `\\.\pipe\sd-ai` | The named pipe the service listens on: at most 16 connections at once, none from another computer (remote clients are rejected). Its access list is SYSTEM and the service in full, and `sdusers` and Administrators may connect and read and write; nobody else may open it, and nobody but the service may add another instance of it. The service is its owner. Whoever connects is identified by Windows, not by anything they write. |
| `C:\Program Files\SD\lib\sd-ai\` | The program `sd-ai.exe` (it is also the administrator's client) and the two data files below. Only administrators can change them; no SD account can. |
| `ai-providers` | In that folder: the connection details that come with SD for Anthropic, OpenAI, Google and DeepSeek, and each one's default model. |
| `ai-context` | In that folder: the standing text that comes with SD. An install replaces it. Your own text, when you have saved one, is `C:\ProgramData\SD\ai\context` and is kept by an upgrade. |
| `C:\ProgramData\SD\ai\` | The helper's own folder: the settings (`ai.conf`), your standing text (`context`), the counters of the limits (`state\`) and the helper's log (`sd-ai.log`: the caller's security identifier, the provider, the result and the sizes of each request, never the text or the key). SYSTEM has full control, the service may change it, Administrators may read it. An upgrade keeps it, and so does an uninstall that keeps the database. |
| `C:\ProgramData\SD\ai\keys\` | One key file per provider. Open only to the service and SYSTEM; each file is encrypted with Windows DPAPI for the service account, so a copy of the file, a backup or a copied disk does not carry a usable key. A key file whose access list names anyone else is refused, not repaired. |
| `sdaiusers` | The Windows group that is the **gate**. Membership of it is what lets an account use the AI. The installer makes it empty. |
| `install-aihelper.ps1` | In `C:\Program Files\SD\`: makes, starts and removes the service. The installer runs it; run it yourself if the service was not set up (see [Setting the service up again](#setting-the-service-up-again)). |

The helper asks Windows who is calling (the account of the process at the other end of the pipe, read at identification level: it can read who called and can never act as them), so the gate does not depend on SD's own programs being honest: a program that talks to the pipe directly gets the same answer. **Before sending anything, SD checks that the pipe's owner is `NT SERVICE\sd-ai`.** The pipe namespace is shared by the whole machine, so while the service is stopped any user could create a pipe of that name and read every request sent to it. A session that finds a pipe owned by anyone else sends nothing, writes `ai refused reason=pipe.owner` to the audit trail and says the helper could not be reached. The service itself refuses to start if a pipe of its name already exists, and says so in the Application log.

## Setting the service up again

The helper needs nothing beyond SD itself: no Python. Every install and upgrade sets up the service. To set it up again, run this in an **elevated** PowerShell window:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\install-aihelper.ps1" -Install
```

It prints what it made, read back from the machine (the service's state, account, start type and command, whether the pipe is there, and the access lists of the two folders), and exits **0** when the helper is running, **2** when it was not run elevated (or its program files are missing), and **1** for anything else. Its log is `C:\ProgramData\SD\install-aihelper.log`.

## Who may ask

| Caller | May ask | May change the settings |
|---|---|---|
| An account whose Windows user is in `sdaiusers` | yes | no |
| SDSYS (always an elevated sign-in) | yes, without the gate | yes |
| Another Windows administrator, in an elevated process | only if in `sdaiusers` | yes, with the helper's client |
| Anyone else | no | no |
| A process running as LocalSystem, LocalService or NetworkService | no, whatever the gate says | no |

**Sessions that get no AI.** The helper refuses a process running as one of Windows' own service accounts (LocalSystem, LocalService, NetworkService), because such a process is never a person and never SDSYS. A session at the console or over ssh runs as the person's own Windows user; an API session is started as the Windows user who logged in; a phantom runs as the session that started it; an account's scheduled job runs as that account's Windows user. A session that nobody can answer (a phantom, a scheduled job, a script fed from a file) reaches the preview and sends nothing, because only a typed `y` or `yes` sends.

**Another Windows administrator.** As on Linux, where root may change the settings, an elevated administrator of this machine may change the AI settings by running the helper's client directly (`C:\Program Files\SD\lib\sd-ai\sd-ai.exe`, the words of `set.ai` below). Inside SD only SDSYS can: `set.ai` and `tool.ai` are SDSYS's.

## The things that turn it on

1. **A provider.** One for the whole machine: Anthropic, OpenAI, Google, DeepSeek or Custom.
2. **A model** for that provider. Each of the four named providers comes with a default model, shown on the page and used until you name another (`set.ai model PROVIDER NAME`; a dash goes back to the default). The defaults are the balanced model of each provider as its own documentation named it (DeepSeek's is `deepseek-v4-flash` since DeepSeek retired `deepseek-chat`): **model names change, so check the one you will pay for.** On the page the model is chosen from the provider's own list in the setup dialog (S), and `set.ai models PROVIDER` prints that list at the prompt. Model names are case-sensitive: `deepseek-v4-pro` works, `Deepseek-V4-Pro` does not. Custom has no default; its model is yours.
3. **A key** for that provider, from the provider's own account. It is typed or pasted in the setup dialog (shown as `*`) or at the helper's own prompt, and kept for the helper only.
4. **The gate for each account that may use it**: `modify.account NAME ai-on`.

The same provider and the same model serve every account; there is no choice per account and no key per account. Of the four, only the provider, the key and the gates have to be supplied: the AI stays off until all three are. The service must be running as well (see [Setting the service up again](#setting-the-service-up-again)).

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
| F6, Shift-F6, Left, Right | change box (F6 goes on to the AI line when the AI is on for this account) | change box |
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

## Continued in

[The AI Helper: set.ai, the Key and
Troubleshooting](20a-the-ai-helper-set-ai-and-the-key.html) — set.ai, the
standing text, the key and troubleshooting.
