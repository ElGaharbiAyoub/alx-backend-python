#!/usr/bin/env python3
""" Duck typing - first element of a sequence """
from typing import Any, Sequence, Union


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ Return first element of lst if there is any, otherwise None. """
    if lst:
        return lst[0]
    else:
        return None
