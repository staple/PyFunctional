from __future__ import absolute_import, division

import collections
import math
from functools import reduce
from itertools import chain, count, islice, takewhile

import six


if six.PY2:
    PROTOCOL = 2
else:
    PROTOCOL = serializer.HIGHEST_PROTOCOL


def is_primitive(val):
    """
    Checks if the passed value is a primitive type.

    >>> is_primitive(1)
    True

    >>> is_primitive("abc")
    True

    >>> is_primitive(True)
    True

    >>> is_primitive({})
    False

    >>> is_primitive([])
    False

    >>> is_primitive(set([]))

    :param val: value to check
    :return: True if value is a primitive, else False
    """
    return isinstance(val,
                      (str, bool, float, complex, bytes, six.text_type)
                      + six.string_types + six.integer_types)


def is_namedtuple(val):
    """
    Use Duck Typing to check if val is a named tuple. Checks that val is of type tuple and contains
    the attribute _fields which is defined for named tuples.
    :param val: value to check type of
    :return: True if val is a namedtuple
    """
    val_type = type(val)
    bases = val_type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(val_type, '_fields', None)
    return all(isinstance(n, str) for n in fields)


def identity(arg):
    """
    Function which returns the argument. Used as a default lambda function.

    >>> obj = object()
    >>> obj is identity(obj)
    True

    :param arg: object to take identity of
    :return: return arg
    """
    return arg


def is_iterable(val):
    """
    Check if val is not a list, but is a collections.Iterable type. This is used to determine
    when list() should be called on val

    >>> l = [1, 2]
    >>> is_iterable(l)
    False
    >>> is_iterable(iter(l))
    True

    :param val: value to check
    :return: True if it is not a list, but is a collections.Iterable
    """
    if isinstance(val, list):
        return False
    return isinstance(val, collections.Iterable)


def is_tabulatable(val):
    if is_primitive(val):
        return False
    if is_iterable(val) or is_namedtuple(val) or isinstance(val, list):
        return True
    return False


def split_every(parts, iterable):
    """
    Split an iterable into parts of length parts

    >>> l = iter([1, 2, 3, 4])
    >>> split_every(2, l)
    [[1, 2], [3, 4]]

    :param iterable: iterable to split
    :param parts: number of chunks
    :return: return the iterable split in parts
    """
    return takewhile(bool, (list(islice(iterable, parts)) for _ in count()))


def compute_partition_size(result, processes):
    """
    Attempts to compute the partition size to evenly distribute work across processes. Defaults to
    1 if the length of result cannot be determined.

    :param result: Result to compute on
    :param processes: Number of processes to use
    :return: Best partition size
    """
    try:
        return max(math.ceil(len(result) / processes), 1)
    except TypeError:
        return 1


def compose(*functions):
    """
    Compose all the function arguments together
    :param functions: Functions to compose
    :return: Single composed function
    """
    # pylint: disable=undefined-variable
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
