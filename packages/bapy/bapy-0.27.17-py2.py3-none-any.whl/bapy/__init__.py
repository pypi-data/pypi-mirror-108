#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""BAPY Package."""
__all__ = ()
import ast
import asyncio
import collections.abc
import contextlib
import dataclasses
import enum
import functools
import importlib
import inspect
import io
import os
import pathlib
import platform
import re
import subprocess
import sys
import textwrap
import threading
import types
import typing


__version__ = '0.27.17'


# Calls
ALL_PORTS = range(0, 65535)
CURLYBRACKETS = '{}'
USERLOCAL = pathlib.Path('/usr/local')
LOCALBIN = USERLOCAL / 'bin'
MACOS = platform.system() == 'Darwin'
WITHSUDO = '' if MACOS else 'sudo '

# As
Alias = typing._alias
ByteString = collections.abc.ByteString
Callable = collections.abc.Callable
cancel_all_tasks = asyncio.runners._cancel_all_tasks
Container = collections.abc.Container
CRLock = threading._CRLock
current_frames = sys._current_frames
datafield = dataclasses.field
Generator = collections.abc.Generator
getframe = sys._getframe
inspect_empty = inspect._empty
Iterable = collections.abc.Iterable
Iterator = collections.abc.Iterator
KeysView = collections.abc.KeysView
Mapping = collections.abc.Mapping
ModuleSpec = importlib._bootstrap.ModuleSpec
MutableMapping = collections.abc.MutableMapping
MutableSequence = collections.abc.MutableSequence
MutableSet = collections.abc.MutableSet
RunningLoop = asyncio.events._RunningLoop
Sequence = collections.abc.Sequence
Simple = types.SimpleNamespace
Sized = collections.abc.Sized
ThreadLock = threading.Lock
ValuesView = collections.abc.ValuesView

# Aliases
LockClass = type(ThreadLock())

# Typing
AsyncsUnion = typing.Union[ast.AsyncFor, ast.AsyncWith, ast.Await]
# noinspection PyAnnotations
BaseTypesUnion = typing.Union[int, float, list, dict, set, tuple, object, bytes]
DefsUnion = typing.Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda]
DictStrAny = dict[str, typing.Any]
ExceptionUnion = typing.Union[tuple[typing.Type[Exception]], typing.Type[Exception]]
Frames = typing.Union[inspect.FrameInfo, types.FrameType, types.TracebackType]
FunctionTypesUnion = typing.Union[types.FunctionType, types.MethodType, types.LambdaType, types.BuiltinFunctionType,
                                  types.BuiltinMethodType]
IteratorTypes = (type(iter('')),)
LST = typing.Union[list, set, tuple]
OpenIO = typing.Union[io.BufferedRandom, io.BufferedReader, io.BufferedWriter, io.FileIO, io.TextIOWrapper]
PrimitiveTypesUnion = typing.Union[str, bool, type(None), int, float]
SeqNoStr = typing.Union[Iterator, KeysView, MutableSequence, MutableSet, Sequence, tuple, ValuesView]
SeqTuple = typing.Union[MutableSequence, MutableSet, tuple]
SeqUnion = typing.Union[bytes, ByteString, SeqNoStr, str]
TupleStr = tuple[str, ...]
TupleType = tuple[typing.Type, ...]


# EnumBase
@functools.total_ordering
class EnumBase(enum.Enum):
    """Enum Base Class."""

    def __call__(self):
        """Returns Value."""
        return self.value

    def __eq__(self, other):
        """
        Equal Using Enum Key and Enum Instance.

        Examples:
            >>> assert Access['field'] == Access.PUBLIC
            >>> assert Access['field'] is Access.PUBLIC
            >>> assert Access['field'] != '_field'
            >>> assert Access['_field'] == '_field'
            >>> assert Access['_field'] is not '_field'

        Returns:
            True if Enum Key or Enum Instance are equal to self.
        """
        try:
            rv = type(self)[other]
            return self._name_ == rv._name_ and self._value_ == rv._value_
        except KeyError:
            return False

    def __gt__(self, other):
        """
        Greater Than Using Enum Key and Enum Instance.

        Examples:
            >>> assert Access['field'] == Access.PUBLIC
            >>> assert Access['field'] > '_field'
            >>> assert Access['field'] > Access.ALL
            >>> assert Access['field'] >= 'field'
            >>> assert Access['field'] >= Access.PUBLIC
            >>> assert (Access['field'] < Access.ALL) is False
            >>> assert Access.PROTECTED >= Access.ALL
            >>> assert Access['field'] >= Access.ALL
            >>> assert Access['field'] >= '_field'

        Raises:
            TypeError: '>' not supported between instances of '{type(self)}' and '{type(rv)}'.

        Returns:
            True self (index/int) is greater than other Enum Key or Enum Instance.
        """
        try:
            rv = type(self)[other]
            if isinstance(rv, typing.SupportsInt):
                return self.__int__() > rv.__int__()
            raise TypeError(f"'>' not supported between instances of '{type(self)}' and '{type(rv)}'")
        except KeyError:
            raise TypeError(f"'>' not supported between instances of '{type(self)}' and '{type(other)}'")

    def __hash__(self): return hash(self._name_)

    def __int__(self):
        """
        int based on index to compare.

        Examples:
            >>> assert int(Access.PROTECTED) == 2

        Returns:
            Index.
        """
        return list(Access.__members__.values()).index(self)

    def _generate_next_value_(self, start, count, last_values): return self.lower() if isinstance(self, str) else self

    @classmethod
    def asdict(cls): return {key: value._value_ for key, value in cls.__members__.items()}

    @classmethod
    def attrs(cls): return list(cls.__members__)

    @classmethod
    def default(cls): return cls._member_map_[cls._member_names_[0]]

    @classmethod
    def default_attr(cls): return cls.attrs()[0]

    @classmethod
    def default_dict(cls): return {cls.default_attr(): cls.default_value()}

    @classmethod
    def default_value(cls): return cls[cls.default_attr()]

    @property
    def describe(self):
        """
        Returns:
            tuple:
        """
        # self is the member here
        return self.name, self()

    lower = property(lambda self: self.name.lower())

    @classmethod
    def values(cls): return list(cls.asdict().values())


EnumBaseAlias = Alias(EnumBase, 0, name=EnumBase.__name__)


class EnumBaseMeta(enum.EnumMeta):
    def __getitem__(cls, item):
        """
        Access Instance Value:
            - If str and is enum key: returns value.
            - If str and not enum key: returns value base on re.compile.
            - If Access Instance: returns item.

        Examples:
            >>> assert (Access[str()], Access[Access.PROTECTED], Access['__name__'], Access['_name__'], \
            Access['name__'], ) == (None, Access.PROTECTED, Access.PRIVATE, Access.PROTECTED, Access.PUBLIC)
            >>> assert Access['PROTECTED'] == Access.PROTECTED
            >>> Access[dict()] # doctest: +IGNORE_EXCEPTION_DETAIL, +ELLIPSIS
            Traceback (most recent call last):
            KeyError: "{} not in ...

        Raises:
            KeyError: item not in cls.__members__.

        Args:
            item: Access key, string to run re.compile or Access Instance.

        Returns:
            Access Instance.
        """
        if isinstance(item, str):
            if item == '':
                return
            if item in cls._member_map_:
                return cls._member_map_[item]
            for key in list(cls._member_map_.keys())[1:]:
                value = cls._member_map_[key]
                v = value()
                if callable(v) and bool(v(item)):
                    return value
            raise KeyError(f'{item} not in {cls._member_map_}')
        elif isinstance(item, enum.Enum):
            return item
        else:
            for value in cls._member_map_.values():
                if value() == item:
                    return item
        raise KeyError(f'{item} not in {cls._member_map_}')

    __class_getitem__ = __getitem__


# Classes
class Access(EnumBase, metaclass=EnumBaseMeta):
    """Access Attributes Enum Class."""
    ALL = re.compile('.')
    PRIVATE = re.compile('^__.*')
    PROTECTED = re.compile('^_(?!_).*$')
    PUBLIC = re.compile('^(?!_)..*$')

    def include(self, name: str) -> bool:
        """
        Include Key.

        Examples:
            >>> assert (Access.ALL.include(str()), Access.PRIVATE.include(str()), Access.PROTECTED.include(str()), \
            Access.PUBLIC.include(str())) == (None, None, None, None)
            >>> assert (Access.ALL.include('__name__'), Access.PRIVATE.include('__name__'), \
            Access.PROTECTED.include('__name__'), Access.PUBLIC.include('__name__')) == (True, True, False, False)
            >>> assert (Access.ALL.include('_name__'), Access.PRIVATE.include('_name__'), \
            Access.PROTECTED.include('_name__'), Access.PUBLIC.include('_name__')) == (True, True, True, False)
            >>> assert (Access.ALL.include('name__'), Access.PRIVATE.include('name__'), \
            Access.PROTECTED.include('name__'), Access.PUBLIC.include('name__')) == (True, True, True, True)

        Args:
            name: name.

        Returns:
            True if key to be included.
        """
        return type(self)[name] >= self


class getter(typing.Callable[[typing.Any], typing.Union[typing.Any, typing.Tuple[typing.Any, ...]]]):
    """
    Return a callable object that fetches the given attribute(s)/item(s) from its operand.

    >>> from types import SimpleNamespace
    >>> from pickle import dumps, loads
    >>> from copy import deepcopy
    >>>
    >>> test = SimpleNamespace(a='a', b='b')
    >>> assert getter('a b')(test) == (test.a, test.b)
    >>> assert getter('a c')(test) == (test.a, None)
    >>> dicts = getter('a c d', default={})(test)
    >>> assert dicts == (test.a, {}, {})
    >>> assert id(dicts[1]) != id(dicts[2])
    >>> assert getter('a')(test) == test.a
    >>> assert getter('a b', 'c')(test) == (test.a, test.b, None)
    >>> assert getter(['a', 'b'], 'c')(test) == (test.a, test.b, None)
    >>> assert getter(['a', 'b'])(test) == (test.a, test.b)
    >>>
    >>> test = dict(a='a', b='b')
    >>> assert getter('a b')(test) == (test['a'], test['b'])
    >>> assert getter('a c')(test) == (test['a'], None)
    >>> dicts = getter('a c d', default={})(test)
    >>> assert dicts == (test['a'], {}, {})
    >>> assert id(dicts[1]) != id(dicts[2])
    >>> assert getter('a')(test) == test['a']
    >>> assert getter('a b', 'c')(test) == (test['a'], test['b'], None)
    >>> assert getter(['a', 'b'], 'c')(test) == (test['a'], test['b'], None)
    >>> assert getter(['a', 'b'])(test) == (test['a'], test['b'])
    >>>
    >>> test = SimpleNamespace(a='a', b='b')
    >>> test1 = SimpleNamespace(d='d', test=test)
    >>> assert getter('d test.a test.a.c test.c test.m.j.k')(test1) == (test1.d, test1.test.a, None, None, None)
    >>> assert getter('a c')(test1) == (None, None)
    >>> dicts = getter('a c d test.a', 'test.b', default={})(test1)
    >>> assert dicts == ({}, {}, test1.d, test1.test.a, test1.test.b)
    >>> assert id(dicts[1]) != id(dicts[2])
    >>> assert getter('a')(test1) is None
    >>> assert getter('test.b')(test1) == test1.test.b
    >>> assert getter(['a', 'test.b'], 'c')(test1) == (None, test1.test.b, None)
    >>> assert getter(['a', 'a.b.c'])(test1) == (None, None)
    >>>
    >>> test = dict(a='a', b='b')
    >>> test1_dict = dict(d='d', test=test)
    >>> assert getter('d test.a test.a.c test.c test.m.j.k')(test1_dict) == \
    getter('d test.a test.a.c test.c test.m.j.k')(test1)
    >>> assert getter('d test.a test.a.c test.c test.m.j.k')(test1_dict) == (test1_dict['d'], test1_dict['test']['a'], \
    None, None, None)
    >>> assert getter('a c')(test1_dict) == (None, None)
    >>> dicts = getter('a c d test.a', 'test.b', default={})(test1_dict)
    >>> assert dicts == ({}, {}, test1_dict['d'], test1_dict['test']['a'], test1_dict['test']['b'])
    >>> assert id(dicts[1]) != id(dicts[2])
    >>> assert getter('a')(test1_dict) is None
    >>> assert getter('test.b')(test1_dict) == test1_dict['test']['b']
    >>> assert getter(['a', 'test.b'], 'c')(test1_dict) == (None, test1_dict['test']['b'], None)
    >>> assert getter(['a', 'a.b.c'])(test1_dict) == (None, None)
    >>>
    >>> encode = dumps(test1_dict)
    >>> test1_dict_decode = loads(encode)
    >>> assert id(test1_dict) != id(test1_dict_decode)
    >>> test1_dict_copy = deepcopy(test1_dict)
    >>> assert id(test1_dict) != id(test1_dict_copy)
    >>>
    >>> assert getter('d test.a test.a.c test.c test.m.j.k')(test1_dict_decode) == \
    (test1_dict_decode['d'], test1_dict_decode['test']['a'], None, None, None)
    >>> assert getter('a c')(test1_dict_decode) == (None, None)
    >>> dicts = getter('a c d test.a', 'test.b', default={})(test1_dict_decode)
    >>> assert dicts == ({}, {}, test1_dict_decode['d'], test1_dict['test']['a'], test1_dict_decode['test']['b'])
    >>> assert id(dicts[1]) != id(dicts[2])
    >>> assert getter('a')(test1_dict_decode) is None
    >>> assert getter('test.b')(test1_dict_decode) == test1_dict_decode['test']['b']
    >>> assert getter(['a', 'test.b'], 'c')(test1_dict_decode) == (None, test1_dict_decode['test']['b'], None)
    >>> assert getter(['a', 'a.b.c'])(test1_dict_decode) == (None, None)

    The call returns:
        - getter('name')(r): r.name/r['name'].
        - getter('name', 'date')(r): (r.name, r.date)/(r['name'], r['date']).
        - getter('name.first', 'name.last')(r):(r.name.first, r.name.last)/(r['name.first'], r['name.last']).
    """
    __slots__ = ('_attrs', '_call', '_copy', '_default', '_mm')

    def __init__(self, attr: typing.Union[str, typing.Iterable[str]], *attrs: str, default: typing.Any = None) -> None:
        self._copy = True if 'copy' in dir(type(default)) else False
        self._default = default
        _attrs = toiter(attr)
        attr = _attrs[0]
        attrs = (tuple(_attrs[1:]) if len(_attrs) > 1 else ()) + attrs
        if not attrs:
            if not isinstance(attr, str):
                raise TypeError('attribute name must be a string')
            self._attrs = (attr,)
            names = attr.split('.')

            def func(obj):
                mm = isinstance(obj, MutableMapping)
                count = 0
                total = len(names)
                for name in names:
                    count += 1
                    _default = self._default.copy() if self._copy else self._default
                    if mm:
                        try:
                            obj = obj[name]
                            if not isinstance(obj, MutableMapping) and count < total:
                                obj = None
                                break
                        except KeyError:
                            obj = _default
                            break
                    else:
                        obj = getattr(obj, name, _default)
                return obj

            self._call = func
        else:
            self._attrs = (attr,) + attrs
            callers = tuple(self.__class__(item, default=self._default) for item in self._attrs)

            def func(obj):
                return tuple(call(obj) for call in callers)

            self._call = func

    def __call__(self, obj: typing.Any) -> typing.Union[typing.Any, tuple[typing.Any, ...]]: return self._call(obj)
    def __reduce__(self): return self.__class__, self._attrs
    def __repr__(self) -> str: return f'{self.__class__}({self._attrs})'


class Missing:
    name = 'MISSING'
    __slots__ = ()

    def __hash__(self): return hash((self.__class__, self.name,))

    def __reduce__(self): return self.__class__, (self.name,)

    def __repr__(self): return f'<{self.name}>'


MISSING = Missing()


class nstr(str):
    """Value Str Class."""
    __slots__ = ('name',)

    def __new__(cls, value='', *args, **kwargs):
        v = value
        value = super().__new__(cls, value)
        value = cls(f'__{cls.lower(value)}__') if cls.isupper(value) else value
        value.name = v
        return value

    def __call__(self, data=None): return self in data if isinstance(data, Container) else hasattr(data, self)

    # noinspection PyUnusedLocal
    def __init__(self, value=''): super().__init__()

    def get(self, obj, default=None):
        """
        Get key/attr value.

        Args:
            obj: object.
            default: default value (default: None).

        Returns:
            Value.
        """
        return hasget(obj, name=self, default=default)

    def getset(self, obj, default=None, setvalue=True):
        """
        Get key/attr value and sets if does not exists.

        Args:
            obj: object.
            default: default value (default: None).
            setvalue: setattr in object if AttributeError (default: True).

        Returns:
            Value.
        """
        return getset(obj, name=self, default=default, setvalue=setvalue)

    def has(self, obj):
        # noinspection PyUnresolvedReferences
        """
        Checks if object/dict has attr/key.

        >>> from bapy import *
        >>> class Test:
        ...     __repr_newline__ = True
        >>>
        >>> assert REPR_NEWLINE.has(Test()) is True
        >>> assert REPR_EXCLUDE.has(Test()) is False
        >>> assert MODULE.has(tuple) is True
        >>> assert NAME.has(tuple) is True
        >>> assert FILE.has(tuple) is False
        >>> assert FILE.has(asyncio) is True
        >>> assert name.has({'name': ''}) is True
        >>> assert name.has({1: 1}) is False

        Args:
            obj: object.

        Returns:
            True if object/dict has attr/key.
        """
        return has(obj, self)

    def hasget(self, obj, default=None): return hasget(obj, self, default=default)

    def hasgetany(self, obj, default=None): return hasgetany(obj, self, default=default)

    @property
    def getter(self) -> getter:
        # noinspection PyUnresolvedReferences
        """
        Value Getter.

        >>> from bapy import *
        >>> assert MODULE.getter(tuple) == 'builtins'
        >>> assert NAME.getter(tuple) == 'tuple'
        >>> assert 'asyncio/__init__.py' in FILE.getter(asyncio)

        Returns:
            getter(str)
        """
        return getter(self)


# Functions
def has(data: typing.Any, name: typing.Union[str, nstr]) -> bool:
    """
    Name in Data.

    Args:
        data: object.
        name: attribute name.

    Returns:
        True if Name in Data.
    """
    return name in data if isinstance(data, Container) else hasattr(data, name)


def hasget(data: typing.Any, name: typing.Union[str, nstr], default: typing.Any = ...) -> typing.Any:
    """
    Return Attribute Value if Has Attribute.

    Args:
        data: object.
        name: attribute name.
        default: fallback (default: None)

    Returns:
        Attribute Value.
    """
    if isinstance(data, (MutableMapping, types.MappingProxyType)):
        if name in data:
            return data[name]
        return default
    if hasattr(data, name):
        return getattr(data, name)
    return default


def hasgetany(data: typing.Any, name: typing.Union[str, nstr], default: typing.Any = ...) -> typing.Any:
    """
    Return Attribute Value if Has Attribute in instance or class.

    Args:
        data: object.
        name: attribute name.
        default: fallback (default: None)

    Returns:
        Attribute Value.
    """
    if hasattr(data, name):
        return getattr(data, name)
    if not isinstance(data, type):
        if hasattr(data.__class__, name):
            return getattr(data.__class__, name)
    return default


def getm(data: typing.Union[typing.MutableMapping, typing.Any],
         name: typing.Any = 'name') -> typing.Union[Missing, typing.Any]:
    if isinstance(data, MutableMapping):
        return data.get(name, MISSING)
    return data.__getattribute__(name) if hasattr(data, name) else MISSING


def getset(data: typing.Any, name: str, default: typing.Any = None, setvalue: bool = True) -> typing.Any:
    """
    Sets attribute with default if it does not exists and returns value.

    Examples:
        >>> class Dict: pass
        >>> class Slots: __slots__ = ('a', )
        >>>
        >>> d = Dict()
        >>> s = Slots()
        >>> getset(d, 'a')
        >>> # noinspection PyUnresolvedReferences
        >>> d.a
        >>> getset(s, 'a')
        >>> s.a
        >>>
        >>> d = Dict()
        >>> s = Slots()
        >>> getset(d, 'a', 2)
        2
        >>> # noinspection PyUnresolvedReferences
        >>> d.a
        2
        >>> getset(s, 'a', 2)
        2
        >>> s.a
        2
        >>>
        >>> class Dict: a = 1
        >>> class Slots:
        ...     __slots__ = ('a', )
        ...     def __init__(self):
        ...         self.a = 1
        >>> d = Dict()
        >>> s = Slots()
        >>> getset(d, 'a')
        1
        >>> getset(s, 'a')
        1
        >>> getset(d, 'a', 2)
        1
        >>> getset(s, 'a', 2)
        1

    Args:
        data: object.
        name: attr name.
        default: default value (default: None)
        setvalue: setattr in object if AttributeError (default: True).

    Returns:
        Attribute value or sets default value and returns.
    """
    try:
        return object.__getattribute__(data, name)
    except AttributeError:
        if setvalue:
            object.__setattr__(data, name, default)
            return object.__getattribute__(data, name)
        return default

import typer
app = typer.Typer()

@app.command()
def localbin(path: typing.Union[pathlib.Path, str] = __file__) -> None:
    """
    Copy files in directory/path to /usr/local/bin (except __init__.py).

    >>> from tempfile import TemporaryDirectory
    >>> from pathlib import Path
    >>> from stat import ST_MODE, S_IXUSR
    >>> from bapy import localbin
    >>>
    >>> with TemporaryDirectory() as tmp:
    ...     d = Path(tmp)
    ...     bin = Path(LOCALBIN)
    ...     # noinspection PyUnresolvedReferences
    ...     files = ('__init__.py', 'test', '.test', 'test.py', 'package.py',)
    ...     paths = {i: d / i for i in ('__init__.py', 'test', '.test', 'test.py', 'package.py')}
    ...     for i in files:
    ...         Path(d / i).touch()
    ...     localbin(d / '__init__.py')
    ...     assert (LOCALBIN / '__init__.py').exists() is False
    ...     assert (LOCALBIN / '.test').exists() is False
    ...     assert (LOCALBIN / 'test').exists() is True
    ...     assert (LOCALBIN / 'test.py').exists() is True
    ...     assert bool((LOCALBIN / 'test').stat()[ST_MODE] & S_IXUSR) is True
    ...     for i in files:
    ...         (LOCALBIN / i).unlink(missing_ok=True)
    ...     assert (LOCALBIN / 'test').exists() is False

    Args:
        path: source directory or file.

    Returns:
        None
    """
    path = pathlib.Path(path)
    path = path.parent if path.is_file() else path
    subprocess.run(f'find {pathlib.Path(path)} -mindepth 1 -maxdepth 1 -type f ! -name ".*" ! -name "__init__.py" '
                   f'-exec {WITHSUDO} chmod +x "{CURLYBRACKETS}" \; -print | '
                   f'xargs -I {CURLYBRACKETS} {WITHSUDO} cp "{CURLYBRACKETS}" {LOCALBIN}', shell=True, check=True)


def missing(data: typing.Any) -> bool: return data == MISSING


def notmissing(data: typing.Any) -> bool: return not (data == MISSING)


def prefixed(name: typing.Any) -> typing.Optional[str]:
    try:
        return f'{name.upper()}_'
    except AttributeError:
        pass


def splitsep(sep: str = '_') -> dict[str, str]: return dict(sep=sep) if sep else dict()


def toiter(data: typing.Any, always: bool = False, split: str = ' '
           ) -> typing.Union[typing.Sized, typing.MutableMapping, typing.Sequence, typing.MutableSequence]:
    """
    To iter.

    Examples:
        >>> assert toiter('test1') == ['test1']
        >>> assert toiter('test1 test2') == ['test1', 'test2']
        >>> assert toiter({'a': 1}) == {'a': 1}
        >>> assert toiter({'a': 1}, always=True) == [{'a': 1}]
        >>> assert toiter('test1.test2') == ['test1.test2']
        >>> assert toiter('test1.test2', split='.') == ['test1', 'test2']

    Args:
        data: data.
        always: return any iterable into a list.
        split: split for str.

    Returns:
        Iterable.
    """
    if isinstance(data, str):
        data = data.split(split)
    elif not isinstance(data, Iterable) or always:
        data = [data]
    return data


def varname(index: int = 2, lower: bool = True, sep: str = '_') -> typing.Optional[nstr]:
    """
    Caller var name.

    Examples:
        >>> from dataclasses import dataclass
        >>> def function() -> str:
        ...     return varname()
        >>>
        >>> class ClassTest:
        ...     def __init__(self):
        ...         self.name = varname()
        ...
        ...     @property
        ...     def prop(self):
        ...         return varname()
        ...
        ...     # noinspection PyMethodMayBeStatic
        ...     def method(self):
        ...         return varname()
        >>>
        >>> @dataclass
        ... class DataClassTest:
        ...     def __post_init__(self):
        ...         self.name = varname()
        >>>
        >>> name = varname(1)
        >>> Function = function()
        >>> classtest = ClassTest()
        >>> method = classtest.method()
        >>> prop = classtest.prop
        >>> dataclasstest = DataClassTest()
        >>>
        >>> def test_var():
        ...     assert name == 'name'
        >>>
        >>> def test_function():
        ...     assert Function == function.__name__.lower()
        >>>
        >>> def test_class():
        ...     assert classtest.name == ClassTest.__name__.lower()
        >>>
        >>> def test_method():
        ...     assert classtest.method() == ClassTest.__name__.lower()
        ...     assert method == 'method'
        >>> def test_property():
        ...     assert classtest.prop == ClassTest.__name__.lower()
        ...     assert prop == 'prop'
        >>> def test_dataclass():
        ...     assert dataclasstest.name == DataClassTest.__name__.lower()

        .. code-block:: python

            class A:

                def __init__(self):

                    self.instance = varname()

            a = A()

            var = varname(1)


    Args:
        index: index.
        lower: lower.
        sep: split.

    Returns:
        Optional[str]: Var name.
    """
    with contextlib.suppress(IndexError, KeyError):
        _stack = inspect.stack()
        func = _stack[index - 1].function
        index = index + 1 if func == dataclasses._POST_INIT_NAME else index
        if line := textwrap.dedent(_stack[index].code_context[0]):
            if var := re.sub(f'(.| ){func}.*', str(), line.split(' = ')[0].replace('assert ', str()).split(' ')[0]):
                var = nstr(var)
                return (var.lower() if lower else var).split(**splitsep(sep))[0]


# Environ
globals() | os.environ | {__i: nstr(__i) for __i in (
    'ABOUT', 'ABSTRACTMETHODS', 'AUTHOR', 'ADAPT', 'ALL', 'ALLOC', 'ANNOTATIONS',
    'ARGS', 'ASDICT', 'ATTRIBUTES', 'BASE', 'BASICSIZE', 'BUILD_CLASS', 'BUILTINS',
    'CACHE_CLEAR', 'CACHE_INFO', 'CACHED', 'CLASS', 'CODE', 'CONFORM', 'CONTAINS',
    'CREDITS', 'COPY', 'COPYRIGHT', 'CVSID', 'DATACLASS_FIELDS', 'DATACLASS_PARAMS',
    'DATE', 'DECIMAL_CONTEXT', 'DEEPCOPY', 'DELATTR', 'DICT', 'DICTOFFSET',
    'DIR', 'DOC', 'DOCFORMAT', 'EMAIL', 'EQ', 'EXCEPTION', 'FILE', 'FLAGS', 'FUNC', 'GET',
    'GETATTRIBUTE', 'GETFORMAT', 'GETINITARGS', 'GETITEM', 'GETNEWARGS', 'GETSTATE',
    'HASH', 'HASH_EXCLUDE', 'IGNORE_ATTR', 'IGNORE_COPY', 'IGNORE_HASH', 'IGNORE_INIT',
    'IGNORE_KWARG', 'IGNORE_REPR', 'IGNORE_STATE', 'IGNORE_STR', 'IMPORT', 'INIT', 'INIT_SUBCLASS',
    'INITIALIZING', 'ISABSTRACTMETHOD', 'ITEMSIZE', 'LEN', 'LIBMPDEC_VERSION', 'LOADER',
    'LTRACE', 'MAIN', 'MEMBERS', 'METHODS', 'MODULE', 'MP_MAIN', 'MRO', 'NAME', 'NEW', 'NEW_MEMBER',
    'NEW_OBJ', 'NEW_OBJ_EX', 'OBJ_CLASS', 'OBJCLASS', 'PACKAGE', 'POST_INIT', 'PREPARE',
    'QUALNAME', 'REDUCE', 'REDUCE_EX', 'REPR', 'REPR_EXCLUDE', 'REPR_NEWLINE',
    'REPR_PPROPERTY', 'RETURN', 'SELF_CLASS', 'SETATTR', 'SETFORMAT', 'SETSTATE',
    'SIGNATURE', 'SIZEOF', 'SLOTNAMES', 'SLOTS', 'SPEC', 'STATE', 'STATUS', 'STR',
    'SUBCLASSHOOK', 'TEST', 'TEXT_SIGNATURE', 'THIS_CLASS', 'TRUNC', 'VERSION', 'WARNING_REGISTRY',
    'WEAKREF', 'WEAKREFOFFSET', 'WRAPPED',
)}

# noinspection PyRedeclaration
__all__ = tuple(k for k, v in globals().items()
                if k.isupper() or k.istitle() or isinstance(v, (type, types.FunctionType)))
