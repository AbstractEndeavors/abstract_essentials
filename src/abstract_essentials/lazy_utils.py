"""
abstract_essentials.lazy_utils
================================
Safe deferred-import helpers.

``lazy_import``  — imports immediately but returns nullProxy on failure.
``lazy_module``  — true deferral: nothing imported until first attribute access.
``nullProxy``    — chainable, callable placeholder for a missing module or attr.
"""
import sys
import logging
import importlib
from functools import lru_cache

_logger = logging.getLogger("abstract.lazy_import")


# ---------------------------------------------------------------------------
# nullProxy
# ---------------------------------------------------------------------------

class nullProxy:
    """Safe, chainable, callable placeholder for a missing module or attribute."""

    def __init__(self, name, path=(), fallback=None):
        self._name = name
        self._path = path
        self.fallback = fallback

    def __getattr__(self, attr):
        return nullProxy(self._name, self._path + (attr,))

    def __call__(self, *args, **kwargs):
        if self.fallback is not None:
            try:
                return self.fallback(*args, **kwargs)
            except Exception as e:
                _logger.info("%s", e)
        _logger.warning(
            "[lazy_import] Call to missing module/attr: %s.%s args=%s kwargs=%s",
            self._name, ".".join(self._path), args, kwargs,
        )
        return None

    def __repr__(self):
        full = ".".join((self._name, *self._path))
        return f"<nullProxy {full}>"

    def __bool__(self):
        return False


# ---------------------------------------------------------------------------
# lazy_import
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def lazy_import_single(name, fallback=None):
    """Import *name* safely, returning a nullProxy if unavailable."""
    if name in sys.modules:
        return sys.modules[name]
    try:
        return importlib.import_module(name)
    except Exception as e:
        _logger.warning("[lazy_import] Failed to import '%s': %s", name, e)
        return nullProxy(name, fallback=fallback)


def get_lazy_attr(module_name, *attrs, fallback=None):
    obj = lazy_import(module_name, fallback=fallback)
    for attr in attrs:
        try:
            obj = getattr(obj, attr)
        except Exception:
            return nullProxy(module_name, attrs, fallback=fallback)
    return obj


def lazy_import(name, *attrs, fallback=None):
    """
    Import a module (and optionally walk into *attrs*) safely.

    Returns the module/attribute, or a nullProxy placeholder if the
    import fails — so the result is always safe to reference.
    """
    if attrs:
        return get_lazy_attr(name, *attrs, fallback=fallback)
    return lazy_import_single(name, fallback=fallback)


# ---------------------------------------------------------------------------
# lazy_module  (true deferral — import on first attribute access/call)
# ---------------------------------------------------------------------------

class _LazyModuleProxy:
    """Defer ``import name`` until the first attribute access or call.

    Degrades to nullProxy if the import ultimately fails.
    """
    __slots__ = ("_lm_name", "_lm_fallback", "_lm_mod")

    def __init__(self, name, fallback=None):
        object.__setattr__(self, "_lm_name", name)
        object.__setattr__(self, "_lm_fallback", fallback)
        object.__setattr__(self, "_lm_mod", None)

    def _lm_resolve(self):
        mod = object.__getattribute__(self, "_lm_mod")
        if mod is None:
            name = object.__getattribute__(self, "_lm_name")
            if name in sys.modules:
                mod = sys.modules[name]
            else:
                try:
                    mod = importlib.import_module(name)
                except Exception as e:
                    _logger.warning(
                        "[lazy_module] failed to import '%s': %s", name, e
                    )
                    mod = nullProxy(
                        name,
                        fallback=object.__getattribute__(self, "_lm_fallback"),
                    )
            object.__setattr__(self, "_lm_mod", mod)
        return mod

    def __getattr__(self, attr):
        return getattr(self._lm_resolve(), attr)

    def __call__(self, *args, **kwargs):
        return self._lm_resolve()(*args, **kwargs)

    def __repr__(self):
        return f"<lazy_module {object.__getattribute__(self, '_lm_name')!r}>"


def lazy_module(name, fallback=None):
    """Return a proxy that imports *name* on FIRST use (true deferral).

    Unlike :func:`lazy_import` (imports immediately, nullProxy only on failure),
    this stays unloaded until the first attribute access or call::

        pd = lazy_module("pandas")     # pandas NOT imported here
        df = pd.DataFrame(rows)        # imported now, on first use
    """
    return _LazyModuleProxy(name, fallback=fallback)


__all__ = ["nullProxy", "lazy_import", "lazy_import_single", "get_lazy_attr", "lazy_module"]
