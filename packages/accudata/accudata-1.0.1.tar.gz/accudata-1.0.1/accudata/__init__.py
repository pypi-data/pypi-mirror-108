# -*- coding: utf-8 -*-
"""
Created on Tue May  4 19:56:15 2021

@author: Pavel Gostev
"""
from pandas import DataFrame
from numpy import hstack


class ListData:
    lists = []

    def __init__(self, lists=[]):
        self.lists = lists
        for attr in self.lists:
            setattr(self, attr, [])

    def next(self):
        for attr in self.lists:
            getattr(self, attr).append([])

    def get(self, i):
        return {attr: getattr(self, attr)[i] for attr in self.lists}

    def append(self, *args, **kwargs):
        for kw in kwargs:
            if hasattr(self, kw):
                getattr(self, kw)[-1].append(kwargs[kw])

        for i, v in enumerate(args):
            getattr(self, self.lists[i])[-1].append(v)

    def remove(self, i):
        for attr in self.lists:
            del getattr(self, attr)[i]

    def remove_last(self):
        self.remove(-1)

    def todict(self):
        return {k: hstack(getattr(self, k)) for k in self.lists}

    def todf(self):
        return DataFrame(self.todict())

    def __repr__(self):
        lens = [len(getattr(self, attr)) for attr in self.lists]
        types = [(getattr(self, attr)[0][0].__class__.__name__ if len(
            getattr(self, attr)) > 0 else None) for attr in self.lists]
        lists_repr = ' '.join(
            [f'{v!r} {t}[0..{l-1}]' for v, t, l in zip(self.lists, types, lens)])
        return f'{self.__class__.__name__}: {lists_repr}'


class AccumulativeData(ListData):
    dicts = {}

    def __init__(self, lists=[], dicts={}):
        super().__init__(lists=lists)
        self.dicts = dicts
        for attr in self.dicts:
            setattr(self, attr, ListData(lists=self.dicts[attr]))

    def next(self):
        super().next()
        for attr in self.dicts:
            getattr(self, attr).next()

    def get(self, i):
        lres = {'self': super().get(i)}
        for attr in self.dicts:
            lres[attr] = getattr(self, attr).get(i)
        return lres

    def append(self, *args, **kwargs):
        super().append(*args)
        for attr in self.dicts:
            getattr(self, attr).append(*kwargs[attr])

    def remove(self, i):
        super().remove(i)
        for attr in self.dicts:
            getattr(self, attr).remove(i)

    def remove_last(self):
        self.remove(-1)

    def todict(self):
        ldict = super().todict()
        for dkey in self.dicts:
            odict = getattr(self, dkey).todict()
            for okey in odict:
                ldict[f'{dkey}.{okey}'] = odict[okey]
        return ldict

    def __repr__(self):
        lists_repr = super().__repr__() + '\n\t'
        lists_repr += '\n\t'.join(
            [f'{k}: {getattr(self, k).__repr__()}' for k in self.dicts])
        return lists_repr
