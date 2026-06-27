"""
abstract_essentials.url_utils
================================
URL decomposition helpers.
"""
from urllib.parse import urlparse as _urlparse


def parse_url(url):
    """
    Decompose a URL into a dict of components.

    ``path`` is returned without its leading slash so ``path.split('/')[0]``
    yields the first segment (e.g. the owner in an ``owner/repo`` URL).
    """
    p = _urlparse(str(url or ""))
    return {
        "scheme":   p.scheme,
        "netloc":   p.netloc,
        "host":     p.hostname,
        "port":     p.port,
        "path":     (p.path or "").strip("/"),
        "params":   p.params,
        "query":    p.query,
        "fragment": p.fragment,
    }


__all__ = ["parse_url"]
