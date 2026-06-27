# abstract_essentials

The lean, **dependency-free** core carved out of `abstract_utilities`.

Every symbol here depends only on the Python standard library — no third-party
imports, no `from .imports import *` chains, no submodule fan-out. It imports fast
and installs anywhere (desktop, server, **Termux/Android phone**), which makes it a
safe foundation for the rest of the `abstract_*` tree to build on without dragging
in the monolith.

## Why this exists

`abstract_utilities` is imported by nearly every `abstract_*` package, so its size
and entanglement (star-exports across a dozen submodules) ripple everywhere.
`abstract_essentials` is the ~50-function subset that is actually used in practice,
extracted as a clean, explicit API.

## Install

```sh
pip install abstract_essentials
```

## Use

```python
from abstract_essentials import make_list, get_any_value, safe_read_from_json, get_logFile
```

The public API is whatever is listed in `abstract_essentials.__all__` (53 symbols:
json/path/file/string/list/type/log helpers).

## Migrating off abstract_utilities

`abstract_utilities` can become a thin compatibility shim that re-exports from here
(see `abstract_utilities_compat_shim.py` shipped alongside this scaffold), so existing
`from abstract_utilities import X` keeps working while new code imports from
`abstract_essentials`.

## License

MIT — putkoff / Abstract Endeavors.
