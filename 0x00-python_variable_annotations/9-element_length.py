#!/usr/bin/env python3
""" Let's duck type an iterable object """
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Return list of tuples, one for each element of lst,
        each containing a Sequence and its length. """
    return [(i, len(i)) for i in lst]
