"""
Alternate namespace for cytoolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

    Get usually requires two arguments, an index and a collection
    >>> from cytoolz.curried import get
    >>> get(0, ('a', 'b'))
    'a'

    When we use it in higher order functions we often want to pass a partially
    evaluated form
    >>> data = [(1, 2), (11, 22), (111, 222)]
    >>> list(map(lambda seq: get(0, seq), data))
    [1, 11, 111]

    The curried version allows simple expression of partial evaluation
    >>> list(map(get(0), data))
    [1, 11, 111]

See Also:
    cytoolz.functoolz.curry
"""
import ckitoolz
from . import operator
from ckitoolz import (
    apply,
    comp,
    complement,
    compose,
    compose_left,
    concat,
    concatv,
    count,
    curry,
    diff,
    first,
    flip,
    frequencies,
    identity,
    interleave,
    isdistinct,
    isiterable,
    juxt,
    last,
    memoize,
    merge_sorted,
    peek,
    pipe,
    second,
    thread_first,
    thread_last,
)
from .exceptions import merge, merge_with

accumulate = ckitoolz.curry(ckitoolz.accumulate)
assoc = ckitoolz.curry(ckitoolz.assoc)
assoc_in = ckitoolz.curry(ckitoolz.assoc_in)
cons = ckitoolz.curry(ckitoolz.cons)
countby = ckitoolz.curry(ckitoolz.countby)
dissoc = ckitoolz.curry(ckitoolz.dissoc)
do = ckitoolz.curry(ckitoolz.do)
drop = ckitoolz.curry(ckitoolz.drop)
excepts = ckitoolz.curry(ckitoolz.excepts)
filter = ckitoolz.curry(ckitoolz.filter)
get = ckitoolz.curry(ckitoolz.get)
get_in = ckitoolz.curry(ckitoolz.get_in)
groupby = ckitoolz.curry(ckitoolz.groupby)
interpose = ckitoolz.curry(ckitoolz.interpose)
itemfilter = ckitoolz.curry(ckitoolz.itemfilter)
itemmap = ckitoolz.curry(ckitoolz.itemmap)
iterate = ckitoolz.curry(ckitoolz.iterate)
join = ckitoolz.curry(ckitoolz.join)
keyfilter = ckitoolz.curry(ckitoolz.keyfilter)
keymap = ckitoolz.curry(ckitoolz.keymap)
map = ckitoolz.curry(ckitoolz.map)
mapcat = ckitoolz.curry(ckitoolz.mapcat)
nth = ckitoolz.curry(ckitoolz.nth)
partial = ckitoolz.curry(ckitoolz.partial)
partition = ckitoolz.curry(ckitoolz.partition)
partition_all = ckitoolz.curry(ckitoolz.partition_all)
partitionby = ckitoolz.curry(ckitoolz.partitionby)
peekn = ckitoolz.curry(ckitoolz.peekn)
pluck = ckitoolz.curry(ckitoolz.pluck)
random_sample = ckitoolz.curry(ckitoolz.random_sample)
reduce = ckitoolz.curry(ckitoolz.reduce)
reduceby = ckitoolz.curry(ckitoolz.reduceby)
remove = ckitoolz.curry(ckitoolz.remove)
sliding_window = ckitoolz.curry(ckitoolz.sliding_window)
sorted = ckitoolz.curry(ckitoolz.sorted)
tail = ckitoolz.curry(ckitoolz.tail)
take = ckitoolz.curry(ckitoolz.take)
take_nth = ckitoolz.curry(ckitoolz.take_nth)
topk = ckitoolz.curry(ckitoolz.topk)
unique = ckitoolz.curry(ckitoolz.unique)
update_in = ckitoolz.curry(ckitoolz.update_in)
valfilter = ckitoolz.curry(ckitoolz.valfilter)
valmap = ckitoolz.curry(ckitoolz.valmap)

del exceptions
del ckitoolz
