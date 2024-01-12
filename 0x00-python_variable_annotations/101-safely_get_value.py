#!/usr/bin/env python3
""" More involved type annotations """
from typing import Any, Mapping, TypeVar, Union


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[TypeVar('T'), None] = None
                     ) -> Union[Any, TypeVar('T')]:
    """ Return value linked to key in dct, or default if key doesn't exist. """
    if key in dct:
        return dct[key]
    else:
        return default
