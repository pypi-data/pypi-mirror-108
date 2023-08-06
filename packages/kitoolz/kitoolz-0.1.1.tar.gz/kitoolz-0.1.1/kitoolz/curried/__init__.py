"""
Alternate namespace for toolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

    Get usually requires two arguments, an index and a collection
    >>> from kitoolz.curried import get
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
    kitoolz.functoolz.curry
"""
import kitoolz
from . import operator
from kitoolz import (
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

accumulate = kitoolz.curry(kitoolz.accumulate)
assoc = kitoolz.curry(kitoolz.assoc)
assoc_in = kitoolz.curry(kitoolz.assoc_in)
cons = kitoolz.curry(kitoolz.cons)
countby = kitoolz.curry(kitoolz.countby)
dissoc = kitoolz.curry(kitoolz.dissoc)
do = kitoolz.curry(kitoolz.do)
drop = kitoolz.curry(kitoolz.drop)
excepts = kitoolz.curry(kitoolz.excepts)
filter = kitoolz.curry(kitoolz.filter)
get = kitoolz.curry(kitoolz.get)
get_in = kitoolz.curry(kitoolz.get_in)
groupby = kitoolz.curry(kitoolz.groupby)
interpose = kitoolz.curry(kitoolz.interpose)
itemfilter = kitoolz.curry(kitoolz.itemfilter)
itemmap = kitoolz.curry(kitoolz.itemmap)
iterate = kitoolz.curry(kitoolz.iterate)
join = kitoolz.curry(kitoolz.join)
keyfilter = kitoolz.curry(kitoolz.keyfilter)
keymap = kitoolz.curry(kitoolz.keymap)
map = kitoolz.curry(kitoolz.map)
mapcat = kitoolz.curry(kitoolz.mapcat)
nth = kitoolz.curry(kitoolz.nth)
partial = kitoolz.curry(kitoolz.partial)
partition = kitoolz.curry(kitoolz.partition)
partition_all = kitoolz.curry(kitoolz.partition_all)
partitionby = kitoolz.curry(kitoolz.partitionby)
peekn = kitoolz.curry(kitoolz.peekn)
pluck = kitoolz.curry(kitoolz.pluck)
random_sample = kitoolz.curry(kitoolz.random_sample)
reduce = kitoolz.curry(kitoolz.reduce)
reduceby = kitoolz.curry(kitoolz.reduceby)
remove = kitoolz.curry(kitoolz.remove)
sliding_window = kitoolz.curry(kitoolz.sliding_window)
sorted = kitoolz.curry(kitoolz.sorted)
tail = kitoolz.curry(kitoolz.tail)
take = kitoolz.curry(kitoolz.take)
take_nth = kitoolz.curry(kitoolz.take_nth)
topk = kitoolz.curry(kitoolz.topk)
unique = kitoolz.curry(kitoolz.unique)
update_in = kitoolz.curry(kitoolz.update_in)
valfilter = kitoolz.curry(kitoolz.valfilter)
valmap = kitoolz.curry(kitoolz.valmap)

del exceptions
del kitoolz
