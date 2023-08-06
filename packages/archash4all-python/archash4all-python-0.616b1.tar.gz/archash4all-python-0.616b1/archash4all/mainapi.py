from typing import Optional


def do_hash_dict(d: Optional[dict] = None) -> str:
    if d is None:
        d = {}
    return _real_do_hash(str(d))


def do_str_dict(s: str = "") -> str:
    return _real_do_hash(s)


def _real_do_hash(s: str) -> str:
    print("in _real_do_hash:" + s)
    # todo: call archash in archash.c -> archash.pyd/archash.so
    return ""
