Title: SD Terminal Information (Terminfo)
Subtitle: The terminfo database, the definitions that ship, and the compiler that ships with them.

SD uses a terminfo database to know what byte sequences a terminal sends for
each key, and what sequences to emit for screen control — cursor movement,
clear, color, bold, underline.

Most installations never touch it. The shipped definitions cover the
terminals in ordinary use, and `windows` works with any Windows console, cmd,
PowerShell or Windows Terminal session.

## The default terminal

```
term
```

```
Page width: 120
Page depth: 36
Device    : windows
```

The default terminal type is `windows`. This is an exact copy of the
`linux` definition, which had the right byte sequences for Windows
consoles, cmd, PowerShell and Windows Terminal.

> Existing accounts keep their old setting until their VOC is updated.
> Until then, `term windows` sets it for the session.

## What ships

**26 terminfo definitions ship with SD**, compiling to **37 terminal
names** — the extra names are variants. For example, `vt100-w` is an alias
that maps to the same definition as its base name.

Common names that work out of the box: `windows`, `linux`, `vt100`,
`vt220`, `wyse60`, `ansi`, `xterm`.

The `-at` terminal types (`vt100-at`, `vt220-at`, `wy60-at` and the rest)
were AccuTerm's, and `sdterm` was SDTerm's. They are gone: SD no longer
supports either terminal program. A session that was set to one of them
should use `xterm`, `vt100` or `vt220`.

A name that is not installed is refused and your current type is kept:

```
:term vt320
Unrecognized terminal name
```

There is no `vt320` definition; `vt220` or `xterm` does the same job.

## Setting the terminal

```
term                    * report current type and page size
term windows            * set for this session
term 140,43             * set page size
term default            * restore 140 x 43 (prints nothing; check with bare term)
```

The page size is worked out at login in this order:

1. the `LINES` and `COLUMNS` environment variables if they are numeric
2. the terminfo entry's `lines` and `cols`
3. otherwise 43 and 140

A console or ssh session normally gets its real window size. 140 × 43
is the fallback when nothing answers — a phantom or a piped script.
The terminfo entries that name a width and a depth say 140 and 43; the
132-column entries keep their own depth.

## The page is 140 × 43

SD's default is **140 columns by 43 lines**, not 80 × 24. A console window
narrower than that makes wide reports look wrapped or truncated — which
reads as a formatting bug and is not one. `term 120,36` sets a smaller
size for a session that wants it.

The default is only a default. `term w,h` takes any width from 20 to 32767 and
any depth from 10 to 32767, larger or smaller than 140 × 43, and nothing else
clamps it. A real terminal still decides its own size, and `term default` puts
the page back to 140 × 43 whatever the window.

## The terminfo source

`terminfo.src` ships with SD. It is a text file containing all the
definitions in source form. You can read it to see what a terminal
definition looks like, and you can use it as a template for a custom
definition.

## Ending one attribute: `eblink`, `edim`, `erev`, `ebold` and `eprot`

SD turned blink, half intensity, reverse video and bold off with `sgr0`, which ends **every**
attribute and the colors as well. A terminal entry can now give each its own capability:

| capability | ends | sent by |
|---|---|---|
| `eblink` | flashing text | `@(-6)` |
| `edim` | half intensity | `@(-12)` |
| `erev` | reverse video | `@(-14)` |
| `ebold` | bold | `@(-59)` |
| `eprot` | protected mode | nothing yet: no `@()` function uses it |

When the entry defines the capability, the function sends it; **when it does not, the function
sends `sgr0` as before.** No entry that ships with SD defines any of the five, so nothing changes
until you add them. SD's own programs that use `@(-14)` to put the colors back (the query
processor's styles, SED, the pick lists) therefore behave as they did on every stock terminal.
Think before you give an entry an `erev` of its own: it ends reverse video and nothing else, where
`sgr0` ended the colors too.

`terminfo.src` is replaced by an upgrade, so keep the additions in a separate file of
your own, and compile them with `sdtic` as described below. The start functions `@(-5)` and `@(-13)` are not changed.

## Compiling a definition

**The terminfo compiler ships with SD.** `sdtic.exe` is in
`C:\Program Files\SD\usr\bin`, beside `sd.exe`. Nothing needs building and
nothing needs downloading.

```
sdtic {options} src...
```

| | |
|---|---|
| `-d` | decompile a named terminal entry instead of compiling |
| `-i` | display an index of terminal names |
| `-p`*path* | use the terminfo library at *path* |
| `-t`*name* | compile only *name*; may be repeated |
| `-v` | verbose |
| `-x` | do not overwrite entries that already exist |

Without `-d` it compiles the source files you name. With `-d`, the argument is a
terminal name to decompile rather than a file.

Two things follow from `-d` that are worth knowing. It is how you read a shipped
definition without hunting through `terminfo.src`, and it is how you produce a
starting point for a variant of one:

```
sdtic -d vt220 > myterm.src
```

Edit that, then compile it back in. `-x` is the safe form while you are
experimenting, because it refuses to overwrite a definition that already
exists.

The compiled definitions live under `C:\ProgramData\SD\sdsys\terminfo`, in
single-letter directories by first letter. Writing there needs administrator
rights, so run `sdtic` from an elevated prompt when you are adding a definition
for the machine.
