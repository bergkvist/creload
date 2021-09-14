from importlib import import_module
from functools import reduce
from typing import List
import sys

from .subprocess_call import subprocess_call


class lazyimport:
    modulename: str = None
    attrs: List[str] = None
    
    def __init__(self, modulename: str, attrs: List[str] = None):
        self.modulename = modulename
        self.attrs = attrs if attrs is not None else []
                
    def __dir__(self):
        return self.apply(dir)
    
    def __repr__(self):
        return self.apply(lambda m: m.__repr__())
    
    def __getattr__(self, key: str):
        return lazyimport(self.modulename, [ *self.attrs, key ])
    
    def __getitem__(self, key: str):
        return lazyimport(self.modulename, [ *self.attrs, key ])
    
    def __call__(self, *args, **kwargs):
        return subprocess_call(lambda: self.load()(*args, **kwargs))
    
    def apply(self, fn):
        return subprocess_call(lambda: fn(self.load()))
    
    def load(self):
        assert self.modulename not in sys.modules.keys(), \
            f'{self.modulename} is already imported, which prevents this from working as expected'
        return reduce(getattr, [ import_module(self.modulename), *self.attrs ])

