#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""BAPY Package."""
from .main import *
from .main import __version__
print(DOC)
print(globals()['DOC'])
print(main.__dict__)

__all__ = main.__all__

if __name__ == '__main__':
    try:
        typer.Exit(app())
    except KeyError:
        pass
