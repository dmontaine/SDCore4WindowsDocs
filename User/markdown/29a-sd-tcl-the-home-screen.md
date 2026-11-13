Title: SD TCL - The Home Screen
Subtitle: A start screen of tiles that every account can open: its tools, a terminal, switch account and sign out.

```
home
menu
exit
```

**`home`** opens a full-screen start screen for the account you are signed in to:
a page of **tiles**, each of which starts something. **`menu`** does the same (it is
the plain word for "bring up the full-screen menu", at the prompt or in the terminal
the screen gave you), and **`exit`** is the way back to it from that terminal.
Your administrator decides, account by account,
whether a session **starts** here or at the command prompt (see *Where a session
starts*, below); you can always type `home` or `menu` at the prompt to open it.

The keys, menus, boxes and pick lists that every full-screen page shares are described once in
[Using the Full-Screen Pages](29d-sd-tcl-using-the-full-screen-pages.html); this page adds what is
particular to the home screen.

It needs a window of at least **140 columns by 43 lines** (the same as the other
full-screen tools) and a real terminal. In a smaller window it says so, with the
size it found, and leaves you at the prompt; in a session with no terminal (a
pipe, a phantom, a script) it says `home needs a terminal` and reads nothing, so
a script is never taken for someone typing.

> **Not run on Windows yet.** The home screen is SD Core for Linux's program,
> carried here unchanged and compiled (25 October 2026); nothing on this page has
> been seen on a Windows console.

## What is on it

```
 File  Go  View  AI  Help                                                       home  alice@sales

   alice @ sales                                                  <> Switch account   -> Sign out
   Thursday 22 Oct 2026  -  18:52

   My tools
     [=]                  </>                    [ ]
     Editor               IDE                    Record editor
     edit a record        programs and files     fields of a record

   Everyone
     >_                                          ^K
     Terminal                                    Keys
     type exit to come back                      test your keyboard
```

(The listing is Linux's, from a session on 22 October 2026.)

| tile | what it does |
|---|---|
| **Editor** | runs `sed` (it asks which file and record) |
| **IDE** | runs `ide` |
| **Record editor** | runs `ced` |
| **Terminal** | leaves the screen for the ordinary command prompt (below) |
| **Keys** | runs `tool.keys`, the terminal and keyboard diagnostic |
| **Switch account** | a list of the accounts you may enter; then the home screen of the one you pick |
| **Sign out** | asks `Sign out of SD?` and ends the session |

**A tile starts a command exactly as you would have typed it.** It adds no
access: if the command needs a switch your account does not have, you get the same
refusal you would at the prompt. A command that takes the screen (the editors,
`tool.keys`) gives it back when you leave it, and the home screen is drawn again;
a command that only prints waits for Enter before the screen returns.

The **administrator's page** has the same tools in a group called *Tools*, and
shows `administrator` at the top and at the right end of the menu bar; an account
holder's page says `My tools` and `name @ account`. The two are built from one
table and differ only in what is in it. The tools that other parts of SD add (the
account manager, the gate matrix and the rest) each add their own tile when they
are built. The *AI* menu of the menu bar holds *Ask the AI*, which, like F6,
moves to the AI line when the AI is on for your account; when it is not, the
entry is dimmed and its reason is that the AI is not on for this account. The AI line is described in
[SD TCL - Asking the AI](29b-sd-tcl-asking-the-ai.html).

**The page scrolls.** It is laid out at its full height and only the rows that fit
are drawn, with a scroll bar in the last column when there is more than fits, so
the number of tiles can pass the height of the screen. The header (your name, the
date and time, Switch account and Sign out) stays where it is.

## Keys and the mouse

| key | does |
|---|---|
| the arrow keys | move to the nearest tile in that direction (a tile in the same row or column comes first) |
| Tab, Back-tab | the next and previous tile, in reading order |
| Home, End | the first and the last tile |
| Page Down, Page Up | the first tile of the next and of the previous group |
| a letter | the next tile whose label begins with it |
| Enter, the space bar | start the tile |
| F5 | build the page again |
| F10 | open the menu bar (File, Go, View, AI, Help) |
| Ctrl-Q | sign out (asks first; **Cancel** is the button Enter chooses, so a stray Enter signs nobody out) |

A **click** starts a tile; the **wheel** scrolls the page three rows; a click on the
menu bar opens the menu under it. The foot of the screen is the same as the
other full-screen tools: a hint line, the status line, a border and the row of
function keys.

On a terminal with colour the tiles are filled in the colour of their group; on one
without, each tile is a box and the one with the focus is in reverse video, so
nothing depends on colour.

## The terminal, and `exit`

The **Terminal** tile gives the screen back and shows

```
Terminal - type exit to return to the home screen
:
```

That is the ordinary command prompt, with all of its features (the command stack,
paragraphs, select lists, everything you can type at a prompt that did not come
from the home screen). **`exit`** brings the home screen back. At a prompt that
*did not* come from the home screen, `exit` does what `quit` does and ends the
session. The home screen remembers that you left by the Terminal tile for the rest
of the session, so `exit` goes on coming back to it.

## Switch account and sign out

**Switch account** lists the accounts you may enter, by the rule `logto` uses
(an administrator may enter any account; anyone else the accounts whose Windows
group they belong to), never a suspended account and never SDSYS. Pick one and you
are in that account: its LOGIN paragraph has run, and **the home screen of that
account is shown**. Picking the account you are already in says so and changes
nothing. This moves you between the accounts your Windows user belongs to; it
cannot make you someone else. To be another person, sign out and connect again.

**Sign out** (the tile, the File menu, or Ctrl-Q) asks first and then ends the
session as `quit` does.

## Where a session starts

```
set.start.default
set.start.default menu | terminal
```

The administrator sets this for each account (`modify.account name start-menu`,
`start-terminal` or `start-default`, in the Administrator's guide), and sets what
accounts with no setting of their own do with `set.start.default menu` or
`terminal`. **It is menu as delivered.** The setting is read when you sign on, and
when you type `logto` at the prompt to enter an account. Starting in the menu does
not confine anyone: the Terminal tile is always there.

The screen is never given to a session that cannot use it: a window under 140 by 43,
a pipe, a phantom, an API server, or a `logto` that a program ran with `execute`
(the home screen runs its own `logto` itself and shows the new account's page).

## Tiles the administrator turns off

Every tile is on as delivered, and the administrator can turn a tile off **for your
account** (`set.tile`, or the *Menu management* page): it is then not on your page,
and its menu entry cannot be chosen. If the **Terminal** tile is off and your account
starts in the home screen, you are never given the command prompt: when the screen
ends (a window too small, an error, the cursor lock) you are signed out. An account
that starts at the prompt keeps it. Sign out cannot be turned off.

## Your own programs: `my.menu`

```
my.menu
```

**Only if the administrator has allowed it for your account** (`pins-on`; it is off as
delivered). Your home screen then has a group **My programs**, with a tile **Add a
program** that opens `my.menu`, and a tile for each program you have added. A program
is a **label** (up to 21 characters), a **command** (what you would type at your
prompt), an optional three-character **glyph**, and whether the screen should **wait
for Enter** when the command has finished printing.

| key | does |
|---|---|
| F2 | add a program (it asks for the label, the command, the glyph and the wait) |
| Enter | change the selected one |
| F3 | remove it (asks first; Cancel is the default) |
| F4, F6 | move it up or down the list |
| Ctrl-Q | leave; the home screen is built again and shows the list |

**It manages only your own list.** The standard tiles are the administrator's and
are not touched. A program of yours runs the command exactly as you would type it,
so it adds no access: the gates apply as at the prompt. The list is the record
`home` of the file `&menus&` in your own account. If the administrator takes the
permission away (`pins-off`) the group disappears from your screen and `my.menu`
says it is not allowed; the list stays in your file.

## The Recent group

**View > Recent group** turns on, for you, a group at the top of your home screen with
the tiles you started last, **newest first, six at most**; the same entry turns it
off. **It is off as delivered.** The list is the record `recent` of the file
`&menus&` in your own account (the file is made as `my.menu` makes it). It holds
tile ids and never a command: each recent tile is built from the page as it is now,
so a tile the administrator has turned off is not offered, and a record edited by
hand cannot start anything the page does not offer. Your own programs (`my.menu`)
are not kept in it. Turning the group off forgets the list, and while it is off
nothing is written.

The administrator can forbid it for your account: `set.tile account recent off`.
The group is then not on your page, nothing is read or written for it, and the
View entry cannot be chosen.

## Sub-menus

A tile whose action is `menu:name` opens a page of its own: the groups of the page
table that belong to that menu. The new page has a **Back** tile at the left of the
header (your name moves right to make room), and the status line shows the way in,
for example `Home > Develop`. **Esc, Backspace, the Back tile and Go > Back** each go
back one page, with the tile that was selected. Eight pages are the most; a page that
is already open above cannot be opened again; a menu none of whose tiles is on the
page has no tile to open it; and **Switch account** starts the other account at its
top page. The Back tile cannot be turned off with `set.tile`. **The delivered page
has no sub-menu yet**: this is the mechanism, in the page table of the `tool_home`
program, for a page that wants one.

## The AI line

When the AI is on for your account (the administrator has chosen a provider, given it a
key, **and allowed your account**; see [Asking the AI](29b-sd-tcl-asking-the-ai.html))
the home screen has one more row, just above the status line, that starts **`AI>`**. Without
the AI there is no such row and nothing on this page changes.

**Press F6, choose AI > Ask the AI, or click the row**, type
what you want in your own words, and press Enter:

```
AI> open the ide
AI> show me who I am
```

Enter does not send anything. It shows the provider, the model, the size of all that will be
sent, and **your request**. SD's own text that goes with it (one fixed instruction, the list of
what this page can do, what the page says about itself) is sent and counted, but not shown. **Cancel is the default button**,
so Enter alone sends nothing; choose **Send** (press `s`) to send. While the AI answers the row
says so and **Esc gives the request up**.

The answer comes in a popup. It says what the AI said, and it may *propose* one thing:

| The AI proposes | What you see | What happens |
|---|---|---|
| a **tile** that opens a tool (Editor, IDE, Keys, and the administrator's tiles) | `The AI proposes: IDE - programs and files`, with **Accept** and Reject | **Accept** starts the tile exactly as a click on it would. Enter alone accepts, because the tile only opens a tool you could open anyway. |
| the **Terminal** tile, or one of **your own programs** on the page | the same, with **Accept** and Reject | **Accept** starts it as a click would. **Enter alone rejects**: the Terminal tile leaves the screen for the command prompt and a program of yours runs a command you wrote, so neither starts unless you choose Accept. |
| a **command** | the command on a line of its own, with **Run** and Cancel | **Run** runs it as the Terminal tile's prompt would, and waits for Enter. **Enter alone cancels**: a command never runs unless you choose Run. |
| nothing | only what it said, with Close | nothing |

What it cannot do: it is never offered **Sign out** or **Switch account**; a tile that is not on
your page is ignored, with a note; a command with a control character in it or of more than 200
characters is not shown; anything that is not one JSON object is shown as words, with a note, and
nothing is proposed. The accepted tile or command runs with **your** rights: the gates of your
account apply as they would if you had typed it.

The audit trail records that you asked (`ai request account=... program=tk_ai bytes.out=...`),
never what you asked or what came back.

## Not yet

Programs the administrator assigns to an account and a live line on a tile are
planned and not built; today the page is the table above plus your own programs, and
the Recent group if you turn it on.
