Title: SD Client API: Language Bindings
Subtitle: The headers for six languages, and what the API cannot do.

This page continues [SD Client API](37-sd-client-api.html).

## Language bindings

The API headers define bindings for six languages. The function
signatures are identical in meaning; the syntax differs.

### Gambas3

```
Library "./sdclilib"
Extern SDConnect(Host As String, Port As Integer, UserName As String,
  Password As String, Account As String) As Boolean
Extern SDRead(FileNo As Integer, Id As String,
  ByRef Errno As Integer) As String
```

### PureBasic

```
PrototypeC.l P_SDConnect(host.p-utf8, port.l, user.p-utf8,
  pass.p-utf8, account.p-utf8)
PrototypeC.i P_SDRead(fno.l, id.p-utf8, *err)
```

Per-arity prototypes are provided for `SDCall` and `SDCallx`:
`P_SDCall0` through `P_SDCall20`, `P_SDCallx0` through `P_SDCallx20`.

### Free Pascal / Lazarus

```pascal
type
  TSDConnectFn = function(Host: PAnsiChar; Port: LongInt;
    User, Pass, Account: PAnsiChar): LongInt; cdecl;
  TSDReadFn = function(FileNo: LongInt; Id: PAnsiChar;
    Err: PLongInt): PAnsiChar; cdecl;
```

A `LoadSdCliLib` function loads the library and resolves all
function pointers; `UnloadSdCliLib` releases it.

### Python (ctypes)

```python
import ctypes
_lib = ctypes.CDLL('./sdclilib.dll')

SDConnect = _lib.SDConnect
SDConnect.argtypes = [ctypes.c_char_p, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
SDConnect.restype = ctypes.c_int

SDRead = _lib.SDRead
SDRead.argtypes = [ctypes.c_int, ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int)]
SDRead.restype = ctypes.c_char_p
```

Per-arity `CFUNCTYPE` definitions are provided for `SDCall` and
`SDCallx` wrappers.

### C# and .NET (P/Invoke)

`syscom\sdclient.cs`:

```csharp
using static SDClient;

if (SDConnect(Z("server"), 4247, Z("user"), Z("password"), Z("account")) != 0)
{
    int fno = SDOpen(Z("CUSTOMERS"));
    string rec = Str(SDRead(fno, Z("1001"), out int err));
    SDDisconnect();
}
```

**Strings are bytes.** SD strings carry the marks `0xFB` to `0xFF`, and a UTF-8 conversion by .NET would damage them, so every string parameter is a `byte[]` and every string result an `IntPtr`; `Z(s)` makes the NUL-terminated bytes of a string (one byte for each character; characters above 255 are not allowed) and `Str(p)` / `StrN(p, n)` read a result the same way and give the library's memory back with `SDFree`. `FM`, `VM` and `SVM` are the marks as characters. An `int *` parameter is an `out int`. Variadic C functions cannot be declared in C#, so `SDCall` and `SDCallx` are `SDCall0` to `SDCall20` and `SDCallx0` to `SDCallx20`, all the same entry point; **`SDCall` writes the subroutine's results back into the buffers you give it with no check of their size, so use `SDCallx` and read the arguments with `SDGetArg`.**

The library is loaded by the name `sdclilib`, so .NET looks for `sdclilib.dll` where it looks for any native library: the program's directory or `PATH`, or where a resolver you set with `NativeLibrary.SetDllImportResolver` points. It is the C client library, `sdclilib.dll`, not the Visual Basic DLL `sdclient.dll` (whose calls are `stdcall`); the calling convention is `cdecl`. A 64-bit program needs the 64-bit library and a 32-bit program the 32-bit one.

### PHP (FFI)

`syscom\sdclient.php`, for PHP 7.4 and later with the FFI extension enabled:

```php
require 'sdclient.php';
$sd = SDClient::load('C:\\Program Files\\SD\\usr\\bin\\sdclilib.dll');
if ($sd->SDConnect('server', 4247, 'user', 'password', 'account')) {
    $fno = $sd->SDOpen('CUSTOMERS');
    $err = SDClient::intRef();
    $rec = SDClient::str($sd->SDRead($fno, '1001', FFI::addr($err)));
    $sd->SDDisconnect();
}
```

A PHP string is already a string of bytes, so the marks pass through unchanged. `SDClient::str($p)` copies a result into a PHP string and frees the library's copy; `strn($p, $n)` does the same for `$n` bytes that may hold zeros (`SDReadBlk`). Use `SDCallx` and `SDGetArg` rather than `SDCall`, which writes into the buffers it is given and must not be given a PHP string.

**Neither of these two files has been run.** No .NET or PHP runtime was available when they were written (on Linux); they are held to the library's header by a check (`gplbld\test-clientheaders-units.py`: every function, every parameter and result type, the calling convention, the status constants, and the PHP declarations read by a C compiler beside the header itself), which is not the same as a program having called the library. If one does not load for you, the report is welcome.

## What the API cannot do

| | |
|---|---|
| `sh` and `OS.EXECUTE` | **only if the account holds `sh-on` / `os-on`**: the API server reads the account's switches when it enters the account, as sign-in does, and a new account has neither (SDSYS has none, so it has no shell over the API). `SDCLIENT` in `sd.conf` is the further control, if a site wants one; see the *Administrator* set's *Configuration* chapter |
| Open files outside the account | refused (status 3035 — *not permitted*) |
| Reach the credential file | never, and cannot be added |
| Enumerate accounts | refused; all three failure cases give the same message |
