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
import importlib
import inspect
import io
import json
import os
import pathlib
import platform
import re
import socket
import subprocess
import sys
import sysconfig
import tempfile
import textwrap
import threading
import types
import typing
import urllib.error

import colorama
import rich.console
import rich.pretty
import typer


__version__ = '0.27.36'

# Calls & Constants
ALL_PORTS = range(0, 65535)
APP_CONTEXT = dict(help_option_names=['-h', '--help'], color=True)
app = typer.Typer(context_settings=APP_CONTEXT)
console = rich.console.Console(color_system='256')
cp = console.print

BASE_EXEC_PREFIX = sys.base_exec_prefix
BASE_EXECUTABLE = sys._base_executable
BASE_PREFIX = sys.base_prefix
BUILTIN = (__i if isinstance(__i := globals()['__builtins__'], dict) else vars(__i)).copy()
BUILTIN_CLASS = tuple(filter(lambda x: isinstance(x, type), BUILTIN.values()))
BUILTIN_CLASS_NO_EXCEPTION = tuple(filter(lambda x: not issubclass(x, BaseException), BUILTIN_CLASS))
BUILTIN_CLASS_DICT = (classmethod, staticmethod, type, importlib._bootstrap.BuiltinImporter,)
BUILTIN_CLASS_NO_DICT = tuple(set(BUILTIN_CLASS_NO_EXCEPTION).difference(BUILTIN_CLASS_DICT))
BUILTIN_FUNCTION = tuple(filter(lambda x: isinstance(x, (types.BuiltinFunctionType, types.FunctionType,)),
                                BUILTIN.values()))
BUILTIN_MODULE_NAMES = sys.builtin_module_names
CLASSVAR = dataclasses._FIELD_CLASSVAR
CURLYBRACKETS = '{}'
DATA_MISSING = dataclasses.MISSING
DEFAULT_FACTORY = dataclasses._HAS_DEFAULT_FACTORY
EXEC_PREFIX = sys.exec_prefix
EXECUTABLE = pathlib.Path(sys.executable)
EXECUTABLE_SITE = pathlib.Path(EXECUTABLE).resolve()
FIELD = dataclasses._FIELD
FIELD_BASE = dataclasses._FIELD_BASE
FQDN = socket.getfqdn()
FRAME = sys._getframe(0)
HOSTNAME = platform.node().split('.')[0]
INITVAR = dataclasses._FIELD_INITVAR
HTTP_EXCEPTIONS = (urllib.error.HTTPError, json.JSONDecodeError,)
IMPORTLIB_BOOTSTRAP = importlib._bootstrap.__name__
IMPORTLIB_BOOTSTRAP_EXTERNAL = importlib._bootstrap_external.__name__
IMPORTLIB_PYCACHE = importlib._bootstrap_external._PYCACHE
KALI = 'kali' in platform.release()
LINUX = platform.system() == 'Linux'
USERLOCAL = pathlib.Path('/usr/local')
LOCALBIN = USERLOCAL / 'bin'
LOCALHOST = socket.gethostbyname('localhost')
MACOS = platform.system() == 'Darwin'
META_PATH = sys.meta_path
NEWLINE = '\n'
PATH_HOOKS = sys.path_hooks
PATHLIBDIR = sys.platlibdir
print_exception = console.print_exception
SYSCONFIG_PATHS = {__k: pathlib.Path(__v) for __k, __v in sysconfig.get_paths().items()}
SCRIPTS = SYSCONFIG_PATHS['scripts']
SOCKET_VERSION = {4: dict(af=socket.AF_INET), 6: dict(af=socket.AF_INET6)}
SSH_CONFIG = dict(AddressFamily='inet', BatchMode='yes', CheckHostIP='no', ControlMaster='auto',
                  ControlPath='/tmp/ssh-%h-%r-%p', ControlPersist='20m', IdentitiesOnly='yes',
                  LogLevel='QUIET', StrictHostKeyChecking='no', UserKnownHostsFile='/dev/null')
SSH_CONFIG_TEXT = ' '.join([f'-o {key}={value}' for key, value in SSH_CONFIG.items()])
SUDO = bool(os.getenv('SUDO_USER'))
SYSPATH = sys.path
SYSPREFIX = sys.prefix
TEMPDIR = pathlib.Path('/') / tempfile.gettempprefix()
VENV = BASE_PREFIX != SYSPREFIX
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
_T = typing.TypeVar('_T')
AsyncsUnion = typing.Union[ast.AsyncFor, ast.AsyncWith, ast.Await]
# noinspection PyAnnotations
BaseTypesUnion = typing.Union[int, float, list, dict, set, tuple, object, bytes]
BASE_TYPES = set(typing.get_args(BaseTypesUnion))
DefsUnion = typing.Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda]
DictStrAny = dict[str, typing.Any]
ExceptionUnion = typing.Union[tuple[typing.Type[Exception]], typing.Type[Exception]]
FlagsType = typing.Union[int, re.RegexFlag]
Frames = typing.Union[inspect.FrameInfo, types.FrameType, types.TracebackType]
FunctionTypesUnion = typing.Union[types.FunctionType, types.MethodType, types.LambdaType, types.BuiltinFunctionType,
                                  types.BuiltinMethodType]
FUNCTION_TYPES = set(typing.get_args(FunctionTypesUnion))
IteratorTypes = (type(iter('')),)
LST = typing.Union[list, set, tuple]
LST_TYPES = typing.get_args(LST)
MatchAnyStr = typing.Match[typing.AnyStr]
MatchCallable = typing.Callable[[MatchAnyStr], typing.AnyStr]
MatchCallableUnion = typing.Union[typing.Callable[[MatchAnyStr], typing.AnyStr], typing.AnyStr]
MatchIterator = typing.Iterator[MatchAnyStr]
MatchOptional = typing.Optional[MatchAnyStr]
OpenIO = typing.Union[io.BufferedRandom, io.BufferedReader, io.BufferedWriter, io.FileIO, io.TextIOWrapper]
PatternUnion = typing.Union[typing.AnyStr, typing.Pattern[typing.AnyStr]]
PrimitiveTypesUnion = typing.Union[str, bool, type(None), int, float]
PRIMITIVE_TYPES = set(typing.get_args(PrimitiveTypesUnion))
SeqNoStr = typing.Union[Iterator, KeysView, MutableSequence, MutableSet, Sequence, tuple, ValuesView]
SeqTuple = typing.Union[MutableSequence, MutableSet, tuple]
SeqUnion = typing.Union[bytes, ByteString, SeqNoStr, str]
TupleStr = tuple[str, ...]
TupleType = tuple[typing.Type, ...]

NON_REDUCTIBLE_TYPES = BASE_TYPES | FUNCTION_TYPES | PRIMITIVE_TYPES


# nstr & EnumBase
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


class nstr(str, typing.Generic[_T]):
    """Value Str Class."""
    __slots__ = ('name',)

    def __new__(cls, value='', *args, **kwargs) -> _T:
        v = value
        value = super().__new__(cls, value)
        value = cls(f'__{cls.lower(value)}__') if cls.isupper(value) else value
        value.name = v
        return value

    def __call__(self, data: typing.Any = None) -> bool:
        return self in data if isinstance(data, Container) else hasattr(data, self)

    # noinspection PyUnusedLocal
    def __init__(self, value: str = '') -> None: super().__init__()

    def get(self, obj: typing.Any, default: typing.Any = None) -> typing.Any:
        """
        Get key/attr value.

        Args:
            obj: object.
            default: default value (default: None).

        Returns:
            Value.
        """
        return hasget(obj, name=self, default=default)

    def getset(self, obj: typing.Any, default: typing.Any = None, setvalue: bool = True) -> typing.Any:
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

    def has(self, obj: typing.Any) -> bool:
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
        >>> n = nstr('name')
        >>> assert n.has({'name': ''}) is True
        >>> assert n.has({1: 1}) is False

        Args:
            obj: object.

        Returns:
            True if object/dict has attr/key.
        """
        return has(obj, self)

    def hasget(self, obj: typing.Any, default: typing.Any = None) -> typing.Any:
        return hasget(obj, self, default=default)

    def hasgetany(self, obj: typing.Any, default: typing.Any = None) -> typing.Any:
        return hasgetany(obj, self, default=default)

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


class EnumBase(enum.Enum):
    """Enum Base Class."""

    def __call__(self, *args, **kwargs) -> typing.Union[nstr, typing.Any]:
        """Returns Value."""
        return self.value

    def __hash__(self): return hash(self._name_)

    def _generate_next_value_(self, start, count, last_values) -> typing.Union[nstr, typing.Any]:
        return nstr(self).lower() if isinstance(self, str) else self

    @classmethod
    def asdict(cls) -> dict[str, typing.Union[_T, enum.Enum]]:
        return {key: value._value_ for key, value in cls.__members__.items()}

    @classmethod
    def attrs(cls) -> list[str, ...]: return list(cls.__members__)

    @classmethod
    def default(cls) -> typing.Union[_T, enum.Enum]: return cls._member_map_[cls._member_names_[0]]

    @classmethod
    def default_attr(cls) -> str: return cls.attrs()[0]

    @classmethod
    def default_dict(cls) -> dict[str, typing.Union[_T, enum.Enum]]: return {cls.default_attr(): cls.default_value()}

    @classmethod
    def default_value(cls) -> typing.Any: return cls[cls.default_attr()]

    @property
    def describe(self) -> tuple[str, typing.Union[_T, enum.Enum]]:
        """
        Returns:
            tuple:
        """
        # self is the member here
        return self.name, self()

    lower = property(lambda self: self.name.lower())

    @classmethod
    def values(cls) -> tuple[_T, ...]: return tuple(cls.asdict().values())


EnumBaseAlias = Alias(EnumBase, 0, name=EnumBase.__name__)


class EnumBaseMeta(enum.EnumMeta):
    pass


# Classes
class Missing:
    name = 'MISSING'
    __slots__ = ()

    def __hash__(self): return hash((self.__class__, self.name,))

    def __reduce__(self): return self.__class__, (self.name,)

    def __repr__(self): return f'<{self.name}>'


MISSING = Missing()


class N(EnumBase, metaclass=EnumBaseMeta):
    _asdict = enum.auto()
    _cls = enum.auto()
    _copy = enum.auto()
    _count = enum.auto()
    _data = enum.auto()
    _extend = enum.auto()
    _external = enum.auto()
    _field_defaults = enum.auto()
    _field_type = enum.auto()
    _fields = enum.auto()
    _file = enum.auto()
    _filename = enum.auto()
    _frame = enum.auto()
    _func = enum.auto()
    _function = enum.auto()
    _get = enum.auto()
    _globals = enum.auto()
    _id = enum.auto()
    _index = enum.auto()
    _ip = enum.auto()
    _item = enum.auto()
    _items = enum.auto()
    _key = enum.auto()
    _keys = enum.auto()
    _kind = enum.auto()
    _locals = enum.auto()
    _name = enum.auto()
    _node = enum.auto()
    _origin = enum.auto()
    _obj = enum.auto()
    _object = enum.auto()
    _path = enum.auto()
    _repo = enum.auto()
    _RV = enum.auto()
    _rv = enum.auto()
    _pypi = enum.auto()
    _remove = enum.auto()
    _reverse = enum.auto()
    _sort = enum.auto()
    _source = enum.auto()
    _update = enum.auto()
    _value = enum.auto()
    _values = enum.auto()
    _vars = enum.auto()
    add = enum.auto()
    append = enum.auto()
    args = enum.auto()
    asdict = enum.auto()
    attr = enum.auto()
    attrs = enum.auto()
    authorized_keys = enum.auto()
    backup = enum.auto()
    cls = enum.auto()
    clear = enum.auto()
    cli = enum.auto()
    co_name = enum.auto()
    code_context = enum.auto()
    compare = enum.auto()
    copy = enum.auto()
    copyright = enum.auto()
    count = enum.auto()
    credits = enum.auto()
    data = enum.auto()
    default = enum.auto()
    default_factory = enum.auto()
    defaults = enum.auto()
    docs = enum.auto()
    endswith = enum.auto()
    exit = enum.auto()
    extend = enum.auto()
    external = enum.auto()
    f_back = enum.auto()
    f_code = enum.auto()
    f_globals = enum.auto()
    f_lineno = enum.auto()
    f_locals = enum.auto()
    file = enum.auto()
    filename = enum.auto()
    frame = enum.auto()
    func = enum.auto()
    function = enum.auto()
    get = enum.auto()
    globals = enum.auto()
    hash = enum.auto()
    help = enum.auto()
    id = enum.auto()
    id_rsa = enum.auto()
    ignore = enum.auto()
    index = enum.auto()
    init = enum.auto()
    ip = enum.auto()
    item = enum.auto()
    items = enum.auto()
    kali = enum.auto()
    key = enum.auto()
    keys = enum.auto()
    kind = enum.auto()
    kwarg = enum.auto()
    kwargs = enum.auto()
    kwargs_dict = enum.auto()
    license = enum.auto()
    lineno = enum.auto()
    locals = enum.auto()
    metadata = enum.auto()
    name = enum.auto()
    node = enum.auto()
    obj = enum.auto()
    object = enum.auto()
    origin = enum.auto()
    path = enum.auto()
    pop = enum.auto()
    popitem = enum.auto()
    public = enum.auto()
    pypi = enum.auto()
    PYPI = enum.auto()
    quit = enum.auto()
    remove = enum.auto()
    repo = enum.auto()
    REPO = enum.auto()
    repr = enum.auto()
    rv = enum.auto()
    reverse = enum.auto()
    scripts = enum.auto()
    search = enum.auto()
    sort = enum.auto()
    source = enum.auto()
    SOURCE = enum.auto()
    startswith = enum.auto()
    templates = enum.auto()
    test = enum.auto()
    tests = enum.auto()
    tb_frame = enum.auto()
    tb_lineno = enum.auto()
    tb_next = enum.auto()
    tmp = enum.auto()
    type = enum.auto()
    ubuntu = enum.auto()
    update = enum.auto()
    value = enum.auto()
    values = enum.auto()
    values_dict = enum.auto()
    vars = enum.auto()
    venv = enum.auto()


class Re(EnumBase, metaclass=EnumBaseMeta):
    """
    >>> import re
    >>> assert Re.MODULE.findall('a.b.c') == [('a', 'b')]
    >>> next(Re.MODULE.finditer('a.b.c'))
    <re.Match object; span=(0, 3), match='a.b'>
    >>> assert Re.MODULE.fullmatch('a.b.c') is None
    >>> Re.MODULE.match('a.b.c')
    <re.Match object; span=(0, 3), match='a.b'>
    >>> Re.MODULE.search('a.b.c')
    <re.Match object; span=(0, 3), match='a.b'>
    >>> assert Re.MODULE.sub('a.b.c', string='a.b.c') == 'a.b.c.c'
    >>> assert Re.MODULE.subn('a.b.c', string='a.b.c') == ('a.b.c.c', 1)
    >>> assert Re.MODULE.sub('a.b', string='a.b.c') == 'a.b.c'
    >>> assert Re.MODULE.subn('a.b', string='a.b.c') == ('a.b.c', 1)
    >>> assert (bool(Re.ALL.search(str())), bool(Re.PRIVATE.search(str())), bool(Re.PROTECTED.search(str())), \
    bool(Re.PUBLIC.search(str()))) == (False, False, False, False)
    >>> assert (bool(Re.ALL.search('__name__')), bool(Re.PRIVATE.search('__name__')), \
    bool(Re.PROTECTED.search('__name__')), bool(Re.PUBLIC.search('__name__'))) == (True, True, False, False)
    >>> assert (bool(Re.ALL.search('_name__')), bool(Re.PRIVATE.search('_name__')), \
    bool(Re.PROTECTED.search('_name__')), bool(Re.PUBLIC.search('_name__'))) == (True, False, True, False)
    >>> assert (bool(Re.ALL.search('name__')), bool(Re.PRIVATE.search('name__')), \
    bool(Re.PROTECTED.search('name__')), bool(Re.PUBLIC.search('name__'))) == (True, False, False, True)
    """
    ALL = re.compile('.')
    ASYNCDEF = re.compile(r'^(\s*async\s+def\s)')
    BLOCK = re.compile(r'^(\s*def\s)|(\s*async\s+def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')
    DEF = re.compile(r'^(\s*def\s)')
    DECORATOR = re.compile(r'^(\s*@)')
    LAMBDA = re.compile(r'^(.*(?<!\w)lambda(:|\s))')
    MODULE = re.compile(r'^(?:\s*(\w+)\s*\.)?\s*(\w+)')
    PRIVATE = re.compile('^__.*')
    PROTECTED = re.compile('^_(?!_).*$')
    PUBLIC = re.compile('^(?!_)..*$')

    def findall(self, string: typing.Union[bytes, str]) -> list[typing.Any]:
        """Return a list of all non-overlapping matches in the string.

        If one or more capturing groups are present in the pattern, return
        a list of groups; this will be a list of tuples if the pattern
        has more than one group.

        Empty matches are included in the result."""
        return self.value.findall(string=string)

    def finditer(self, string: typing.Union[bytes, str]) -> MatchIterator:
        """Return an iterator over all non-overlapping matches in the
        string.  For each match, the iterator returns a Match object.

        Empty matches are included in the result."""
        return self.value.finditer(string=string)

    def fullmatch(self, string: typing.AnyStr) -> MatchOptional:
        """Try to apply the pattern to all of the string, returning
        a Match object, or None if no match was found."""
        return self.value.fullmatch(string=string)

    def match(self, string: typing.AnyStr) -> MatchOptional:
        """Try to apply the pattern at the start of the string, returning
        a Match object, or None if no match was found."""
        return self.value.match(string=string)

    def search(self, string: typing.AnyStr) -> MatchOptional:
        """Scan through string looking for a match to the pattern, returning
        a Match object, or None if no match was found."""
        return self.value.search(string=string)

    def sub(self, repl: MatchCallableUnion, string: typing.AnyStr, count: int = 0) -> tuple[typing.AnyStr, int]:
        """Return the string obtained by replacing the leftmost
        non-overlapping occurrences of the pattern in string by the
        replacement repl.  repl can be either a string or a callable;
        if a string, backslash escapes in it are processed.  If it is
        a callable, it's passed the Match object and must return
        a replacement string to be used."""
        return self.value.sub(repl=repl, string=string, count=count)

    def subn(self, repl: MatchCallableUnion, string: typing.AnyStr, count: int = 0) -> tuple[typing.AnyStr, int]:
        """Return a 2-tuple containing (new_string, number).
        new_string is the string obtained by replacing the leftmost
        non-overlapping occurrences of the pattern in the source
        string by the replacement repl.  number is the number of
        substitutions that were made. repl can be either a string or a
        callable; if a string, backslash escapes in it are processed.
        If it is a callable, it's passed the Match object and must
        return a replacement string to be used."""
        return self.value.subn(repl=repl, string=string, count=count)


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


@app.command()
def localbin(path: pathlib.Path = __file__) -> None:
    """
    Copy files in directory/path to /usr/local/bin (except __init__.py).

    >>> from tempfile import TemporaryDirectory
    >>> from pathlib import Path
    >>> from stat import ST_MODE, S_IXUSR
    >>> from bapy import localbin, N
    >>>
    >>> with TemporaryDirectory() as tmp:
    ...     d = Path(tmp)
    ...     # noinspection PyUnresolvedReferences
    ...     files = ('__init__.py', 'test', '.test', 'test.py', 'package.py',)
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
    path = (path.parent / N.scripts) if path.is_file() else path

    subprocess.run(f'find {pathlib.Path(path)} -mindepth 1 -maxdepth 1 -type f ! -name ".*" ! -name "__init__.py" '
                   f'! -name "_init.py" -exec {WITHSUDO} chmod +x "{CURLYBRACKETS}" \; -print | '
                   f'xargs -I {CURLYBRACKETS} {WITHSUDO} cp "{CURLYBRACKETS}" {LOCALBIN}', shell=True, check=True)


def missing(data: typing.Any) -> bool: return data == MISSING


def notmissing(data: typing.Any) -> bool: return not (data == MISSING)


def prefixed(name: typing.Any) -> typing.Optional[str]:
    try:
        return f'{name.upper()}_'
    except AttributeError:
        pass


def pretty_install(cons=console, expand=False): return rich.pretty.install(cons, expand_all=expand)


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


def traceback_install(cons=console, extra=5, locs=True): return rich.traceback.install(
    console=cons, extra_lines=extra, show_locals=locs)


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


@app.command(name='version')
def _version() -> None:
    """Version"""
    print(__version__)


# Environ
globals().update(dict(os.environ) | {__i: nstr(__i) for __i in (
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
)} | {__i.__name__.upper(): __i() for __i in (
    platform.machine, platform.node, platform.platform, platform.processor, platform.python_implementation,
    platform.python_version, platform.python_version_tuple, platform.release
)} | {__k: nstr(__v) for __k, __v in {'BLACK': 90, 'BLUE': 94, 'CYAN': 96, 'GREEN': 92, 'MAGENTA': 95, 'RED': 91,
                                      'RESET': 39, 'WHITE': 97, 'YELLOW': 93, }.items()})

colorama.init()
os.environ['PYTHONWARNINGS'] = 'ignore'
pretty_install(expand=True)

# noinspection PyRedeclaration
__all__ = tuple(k for k, v in globals().items()
                if (k.isupper() or k.istitle() or (isinstance(v, (type, types.FunctionType)) and k[0] != '_')))


if __name__ == '__main__':
    try:
        typer.Exit(app())
    except KeyError:
        pass
