import ckitoolz

__all__ = ['merge', 'merge_with']


@ckitoolz.curry
def merge(d, *dicts, **kwargs):
    return ckitoolz.merge(d, *dicts, **kwargs)


@ckitoolz.curry
def merge_with(func, d, *dicts, **kwargs):
    return ckitoolz.merge_with(func, d, *dicts, **kwargs)


merge.__doc__ = ckitoolz.merge.__doc__
merge_with.__doc__ = ckitoolz.merge_with.__doc__
