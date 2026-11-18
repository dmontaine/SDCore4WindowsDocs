Title: Embedded Python
Subtitle: The CPython interpreter SD runs for a BASIC program, the dictionary, list and string objects it exposes, and the twenty-one cataloged functions that reach it from BASIC.

SD Core for Windows runs CPython so a BASIC program can run Python code and
exchange data with it. Twenty-one cataloged routines carry this - counted
alongside the rest of SD's global catalog in the User set's *SD Standard
Subroutines* page, which does not repeat them; this page is where they are
documented.

## The short version

A BASIC program declares each function it uses, then calls it like any other.
`$INCLUDE SDPYFUNC.H` declares all twenty-one at once; none of them is a TCL
verb, so there is no way to call Python from a command prompt, only from a
compiled BASIC program:

```
$INCLUDE SDPYFUNC.H
status = PY_CREATEDICT('mydict')
```

All twenty-one are `$internal`-compiled and ship already cataloged, so no
account needs to compile or catalog anything to use them - only the include
and a call. Failure is always `status()`, not the returned value: several of
these functions return an empty string on both "genuinely empty" and
"failed," so `status()` is what tells them apart. **Every one of the
twenty-one refuses an empty object, dictionary, list or string name before
making the underlying call**, setting `status()` to 1 and returning an empty
string, `0`, or `1`, whichever the function normally returns on success - never
one of the `-120xx` codes below, which all describe something Python or the
helper process said.

**Starting the interpreter and running code in it need the account's `os-on`
switch** - the same one as `OS.EXECUTE`, because Python runs arbitrary code
for your session. SDSYS always has it; a new account does not. See the
Administrator set's *Operating System Access* chapter for how the grant is made
and read.

## The model: a separate process, not a library

**Python does not run inside `sd.exe`.** It runs in its own program,
`sdpy.exe`, installed beside `sd.exe`, and a session that calls a `PY_`
function talks to it down a pipe. Nothing starts or stops it by hand: the
first `PY_` call in a session starts the helper, and it goes away when the
session ends. Python and the MSYS2 runtime `sd.exe` is built on cannot safely
share one process (`long` is a different width on each side), and a Python
crash cannot take the database down with it.

**Requires an all-users install of Python 3.13 or later.** Windows does
not ship Python. The SD Core release zip carries python.org's installer,
and SD Core's installer offers to install it for all users (an unticked
box, shown only when no suitable Python is there already); restart Windows
afterwards. You can also install Python yourself - for all users. A "for
me only" install cannot be found or used. Without a usable Python on the machine, every `PY_` function
returns `-12040` and nothing else about SD is affected -
`PY_IS_INITIALIZED()` still works and answers `0`.

## Access control

**`PY_` access is gated exactly like `SH` and `OS.EXECUTE`** - the same
`os-on` permission of the account, checked once, the first time a session calls
any `PY_` function, and the decision stands for the rest of the session:

| Result | Meaning |
|---|---|
| allowed | the helper starts (or a prior failure to start is retried) |
| `-12041` | this session may not use the operating system, so it may not have Python either |
| `-12042` | SD could not determine the permission at all - one line is written to the error log saying which. (The permission is a field of the account's record, read at account entry.) |
| `-12040` | the session **is** permitted, but the helper itself could not be started or has died - typically no usable Python on the machine |

## Interpreter lifecycle

| Function | Returns |
|---|---|
| `PY_INITIALIZE()` | 0 if the interpreter is already running or starts cleanly; otherwise an error code below. A second call is a no-op that also returns `0` |
| `PY_IS_INITIALIZED()` | 1 if the interpreter is running, 0 if not. Never fails and never needs the permission check, so it is the one `PY_` call safe to make from any session as a probe |
| `PY_FINALIZE()` | Shuts the interpreter down. Rarely needed - a session ending does this for you |
| `PY_RUNSTRING(script)` | Runs `script` as Python source in the interpreter's global namespace. An empty `script` is refused before it reaches Python (`status()` 1) |
| `PY_RUNFILE(path)` | Runs the Python file at `path`, read on the machine `sdpy.exe` runs on. `path` is checked for shape before it is sent - an obviously unsafe or malformed path is refused (`status()` 1) without reaching Python |

```
st = PY_INITIALIZE()
if st # 0 then
   * st is one of the error codes below
end
```

Python's own `print()` does not reach your terminal. `sdpy.exe`'s standard
output is the pipe protocol itself, not a console, so anything a script
prints is not visible - get a value back with `PY_GETATTR` instead.

## Dictionaries

A "dictionary" here is a Python `dict`, held by name in the interpreter's own
namespace - `dictname` is a handle, not a value. It has string keys and string
values.

| Function | Returns |
|---|---|
| `PY_CREATEDICT(dictname)` | Creates an empty dictionary |
| `PY_CLEARDICT(dictname)` | Empties it. The name stays in the namespace |
| `PY_DICTVALSETS(dictname,key,value)` | Sets (or creates) `key` to the string `value` |
| `PY_DICTVALGETS(dictname,key)` | Returns the string value of `key`, or an empty string if it is not there |
| `PY_DICTIDEL(dictname,key)` | Deletes `key` |
| `PY_DICTGETKEYS(dictname)` | Returns every key, tab-separated |
| `PY_DICTGETVALUES(dictname)` | Returns every value, field-mark (`@FM`) separated - not tabs, unlike the keys |

## Lists

A Python `list`, likewise held by name.

| Function | Returns |
|---|---|
| `PY_LISTCREATE(listname)` | Creates an empty list. `PY_LISTCRTE` is the same function under an older name; both work |
| `PY_LISTCLR(listname)` | Empties it |
| `PY_LISTAPPD(listname,objname)` | Appends the named Python object - a string, a dictionary, or another list made with these functions - to the list |
| `PY_LISTGETS(listname)` | Returns every item, tab-separated |

A list has to be made with `PY_LISTCREATE` before anything is appended to it.
It is shaped like `PY_CREATEDICT`, and a name that is already taken is refused
with the same "already exists" code (`-12012`).

## Strings

A Python `str`, held by name - distinct from an ordinary BASIC string
variable.

| Function | Returns |
|---|---|
| `PY_STRSET(strname,value)` | Sets (or creates) the named Python string to `value` |
| `PY_STRGET(strname)` | Returns its value |

## Reading an object generically

These take the name of any Python object already created above - a
dictionary, a list, a string, or anything a run script left in the
namespace - rather than a type-specific handle.

| Function | Returns |
|---|---|
| `PY_OBJLEN(objname)` | Its length, as Python's own `len()` would report |
| `PY_OBJTYPE(objname)` | Its Python type name as a string - `str`, `list`, `dict`, `int`, and so on |
| `PY_GETATTR(objname)` | Its value as a string. `objname` is looked up in the interpreter's global namespace - this is how a value a script computed comes back into BASIC |

## A worked sequence

This starts the interpreter, runs a line of Python, reads a value back and
makes a list:

```
$INCLUDE SDPYFUNC.H

st = PY_INITIALIZE()
if st then stop 'PY_INITIALIZE failed: ' : st

rs = PY_RUNSTRING("zz_probe = 'SDPY-' : str(6*7)")
if rs then stop 'PY_RUNSTRING failed: ' : rs

vv = PY_GETATTR('zz_probe')      * vv = 'SDPY-42' - Python did the arithmetic
ot = PY_OBJTYPE('zz_probe')      * ot = 'str'

lc = PY_LISTCREATE('zz_list')
if lc then stop 'PY_LISTCREATE failed: ' : lc
lty = PY_OBJTYPE('zz_list')      * lty = 'list'
```

## Error codes

Every function that returns a status uses one of these, defined in
`SYSCOM ERR.H`. They travel back from `sdpy.exe` over the pipe.

| Code | Meaning |
|---|---|
| -12001 | interpreter not initialized |
| -12002 | `PyDict_New()` failed |
| -12003 | failed to set `__builtins__` |
| -12004 | an exception was raised running the script |
| -12005 | error reported by `PY_FINALIZE` |
| -12006 | could not open the script file |
| -12007 | key not found in the dictionary |
| -12008 | failed to convert a Python object to a string |
| -12009 | error encoding a Python string from Unicode to Latin-1 |
| -12010 | cannot import `__main__` |
| -12011 | could not get the `__main__` dictionary |
| -12012 | dictionary already exists |
| -12013 | failed to add to the namespace |
| -12014 | the named object does not exist |
| -12015 | failed to set a dictionary key/value |
| -12016 | failed to delete a dictionary key/value |
| -12017 | object is not a dictionary |
| -12018 | error encoding a string from Latin-1 to Unicode |
| -12019 | object is not a string |
| -12020 | failed to remove the object from the namespace |
| -12030 | object contains no items |
| -12031 | failed to create a Python string object |
| -12032 | failed to concatenate Python string objects |
| -12033 | failed to access a list item |
| -12034 | object is not a list |

The gap between -12020 and -12030 is not a reservation for anything
documented here - it is simply where the two error blocks were written, ten
codes apart.

The list functions reuse codes from this range instead of minting their own:
a wrong type reports -12034, a missing append target -12014, and the append or
clear call itself failing -12033 or -12004. There is no code from -12035 to
-12038.

**-12040 and up describe the helper process and the operating-system
permission**, so they are seen only here:

| Code | Meaning |
|---|---|
| -12040 | permitted, but the helper process could not be started, or has died |
| -12041 | this session may not use the operating system, so may not use Python |
| -12042 | SD could not determine the operating-system permission at all |

## Example programs

Four example programs are installed in the SDSYS account's `bp` file:

| Program | What it shows |
|---|---|
| `PY_TEST` | starting Python, running a short script, and reading its results back |
| `PY_TEST2` | the same with data read from a file; set the path at the top (`xxxx` is an account name) before you run it |
| `PY_JSON` | Python's `json` module on a file you name |
| `PY_TERM` | a minimal prompt that runs the Python you type |

Copy one into your own account's `bp` to compile and run it. Like any use
of Python, it needs the account's OS switch.
