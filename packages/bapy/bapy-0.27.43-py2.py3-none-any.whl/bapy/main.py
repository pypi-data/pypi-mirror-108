#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""BAPY Package."""
__all__ = ()

import abc
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
import ipaddress
import json
import logging
import os
import pathlib
import platform
import re
import requests
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
import warnings
from typing import Any
from typing import AnyStr
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import colorama
import decorator
import furl
import marshmallow.fields
import marshmallow.validate
import more_itertools
import nested_lookup
import rich.console
import rich.pretty
import rich.traceback
import typer
from nested_lookup.nested_lookup import _nested_lookup


__version__ = '0.27.43'

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
FUNCTION_MODULE = '<module>'
HOSTNAME = platform.node().split('.')[0]
ID_RSA_PUB = 'id_rsa.pub'
INITVAR = dataclasses._FIELD_INITVAR
HTTP_EXCEPTIONS = (urllib.error.HTTPError, json.JSONDecodeError,)
IMPORTLIB_BOOTSTRAP = importlib._bootstrap.__name__
IMPORTLIB_BOOTSTRAP_EXTERNAL = importlib._bootstrap_external.__name__
IMPORTLIB_PYCACHE = importlib._bootstrap_external._PYCACHE
INIT_PY = '__init__.py'
KALI = 'kali' in platform.release()
LINUX = platform.system() == 'Linux'
USERLOCAL = pathlib.Path('/usr/local')
LOCALBIN = USERLOCAL / 'bin'
LOCALHOST = socket.gethostbyname('localhost')
MACOS = platform.system() == 'Darwin'
MACHINE = platform.machine
META_PATH = sys.meta_path
NEWLINE = '\n'
NODE = platform.node
PATH_HOOKS = sys.path_hooks
PATHLIBDIR = sys.platlibdir
PLATFORM = platform.platform
print_exception = console.print_exception
PROCESSOR = platform.processor
PYTHON_IMPLEMENTATION = platform.python_implementation
PYTHON_VERSION = platform.python_version
PYTHON_VERSION_TUPLE = platform.python_version_tuple
RELEASE = platform.release
SYSCONFIG_PATHS = {__k: pathlib.Path(__v) for __k, __v in sysconfig.get_paths().items()}
SCRIPTS = SYSCONFIG_PATHS['scripts']
SOCKET_VERSION = {4: dict(af=socket.AF_INET), 6: dict(af=socket.AF_INET6)}
SPECIAL_CHARACTERS = '"' + "'" + '!#$%^&*(){}-+?_=,<>/\\'
SSH_CONFIG = dict(AddressFamily='inet', BatchMode='yes', CheckHostIP='no', ControlMaster='auto',
                  ControlPath='/tmp/ssh-%h-%r-%p', ControlPersist='20m', IdentitiesOnly='yes',
                  LogLevel='QUIET', StrictHostKeyChecking='no', UserKnownHostsFile='/dev/null')
SSH_CONFIG_TEXT = ' '.join([f'-o {key}={value}' for key, value in SSH_CONFIG.items()])
SUDO_USER = os.getenv('SUDO_USER')
SUDO = bool(SUDO_USER)
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
_KT = TypeVar('_KT')
_T = TypeVar('_T')
_U = TypeVar('_U')
_VT = TypeVar('_VT')
AsyncsUnion = Union[ast.AsyncFor, ast.AsyncWith, ast.Await]
# noinspection PyAnnotations
BaseTypesUnion = Union[int, float, list, dict, set, tuple, object, bytes]
BASE_TYPES = set(typing.get_args(BaseTypesUnion))
DefsUnion = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda]
DictStrAny = dict[str, Any]
ExceptionUnion = Union[tuple[Type[Exception]], Type[Exception]]
FlagsType = Union[int, re.RegexFlag]
Frames = Union[inspect.FrameInfo, types.FrameType, types.TracebackType]
FunctionTypesUnion = Union[types.FunctionType, types.MethodType, types.LambdaType, types.BuiltinFunctionType,
                           types.BuiltinMethodType]
FUNCTION_TYPES = set(typing.get_args(FunctionTypesUnion))
IPv = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IteratorTypes = (type(iter('')),)
LST = Union[list, set, tuple]
LST_TYPES = typing.get_args(LST)
MatchAnyStr = typing.Match[AnyStr]
MatchCallable = typing.Callable[[MatchAnyStr], AnyStr]
MatchCallableUnion = Union[typing.Callable[[MatchAnyStr], AnyStr], AnyStr]
MatchIterator = typing.Iterator[MatchAnyStr]
MatchOptional = Optional[MatchAnyStr]
OpenIO = Union[io.BufferedRandom, io.BufferedReader, io.BufferedWriter, io.FileIO, io.TextIOWrapper]
PatternUnion = Union[AnyStr, typing.Pattern[AnyStr]]
PrimitiveTypesUnion = Union[str, bool, type(None), int, float]
PRIMITIVE_TYPES = set(typing.get_args(PrimitiveTypesUnion))
SeqNoStr = Union[Iterator, KeysView, MutableSequence, MutableSet, Sequence, tuple, ValuesView]
SeqTuple = Union[MutableSequence, MutableSet, tuple]
SeqUnion = Union[bytes, ByteString, SeqNoStr, str]
TupleStr = tuple[str, ...]
TupleType = tuple[Type, ...]

NON_REDUCTIBLE_TYPES = BASE_TYPES | FUNCTION_TYPES | PRIMITIVE_TYPES


# Functions
def allin(origin: typing.Iterable, destination: typing.Iterable) -> bool:

    """
    Checks all items in origin are in destination iterable.

    Examples:
        >>> class Int(int):
        ...     pass
        >>> allin(tuple.__mro__, N.BUILTIN_CLASS())
        True
        >>> allin(Int.__mro__, N.BUILTIN_CLASS())
        False
        >>> allin('tuple int', 'bool dict int')
        False
        >>> allin('bool int', ['bool', 'dict', 'int'])
        True
        >>> allin(['bool', 'int'], ['bool', 'dict', 'int'])
        True

    Args:
        origin: origin iterable.
        destination: destination iterable to check if origin items are in.

    Returns:
        True if all items in origin are in destination.
    """
    origin = toiter(origin)
    destination = toiter(destination)
    return all(map(lambda x: x in destination, origin))


def aioclosed() -> bool: return asyncio.get_event_loop().is_closed()


async def aiocmd(command: Union[str, list], decode: bool = True, utf8: bool = False,
                 lines: bool = False) -> subprocess.CompletedProcess:
    """
    Asyncio run cmd.

    Args:
        command: command.
        decode: decode and strip output.
        utf8: utf8 decode.
        lines: split lines.

    Returns:
        CompletedProcess.
    """
    proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE, loop=asyncio.get_running_loop())
    stdout, stderr = await proc.communicate()
    if decode:
        stdout = stdout.decode().rstrip('.\n')
        stderr = stderr.decode().rstrip('.\n')
    elif utf8:
        stdout = stdout.decode('utf8').strip()
        stderr = stderr.decode('utf8').strip()

    out = stdout.splitlines() if lines else stdout

    return subprocess.CompletedProcess(command, proc.returncode, out, stderr)


def aioloop() -> Optional[RunningLoop]: return noexc(RuntimeError, asyncio.get_running_loop)


def aioloopid() -> Optional[int]:
    try:
        return asyncio.get_running_loop()._selector
    except RuntimeError:
        return None


def aiorunning() -> bool: return asyncio.get_event_loop().is_running()


def anyin(origin: typing.Iterable, destination: typing.Iterable) -> Optional[Any]:

    """
    Checks any item in origin are in destination iterable and return the first found.

    Examples:
        >>> class Int(int):
        ...     pass
        >>> anyin(tuple.__mro__, N.BUILTIN_CLASS())
        <class 'tuple'>
        >>> assert anyin('tuple int', N.BUILTIN_CLASS()) is None
        >>> anyin('tuple int', 'bool dict int')
        'int'
        >>> anyin('tuple int', ['bool', 'dict', 'int'])
        'int'
        >>> anyin(['tuple', 'int'], ['bool', 'dict', 'int'])
        'int'

    Args:
        origin: origin iterable.
        destination: destination iterable to check if any of origin items are in.

    Returns:
        First found if any item in origin are in destination.
    """
    origin = toiter(origin)
    destination = toiter(destination)
    for item in toiter(origin):
        if item in destination:
            return item


def cmd(command: typing.Iterable, exc: bool = ..., lines: bool = ..., shell: bool = ..., py: bool = ...,
        pysite: bool = ...) -> Union[subprocess.CompletedProcess, int, list, str]:
    """
    Runs a cmd.

    Examples:
        >>> cmd('ls a')
        CompletedProcess(args='ls a', returncode=1, stdout=[], stderr=['ls: a: No such file or directory'])
        >>> assert 'Requirement already satisfied' in cmd('pip install pip', py=True).stdout[0]
        >>> cmd('ls a', shell=False, lines=False)  # Extra '\' added to avoid docstring error.
        CompletedProcess(args=['ls', 'a'], returncode=1, stdout='', stderr='ls: a: No such file or directory\\n')
        >>> cmd('echo a', lines=False)  # Extra '\' added to avoid docstring error.
        CompletedProcess(args='echo a', returncode=0, stdout='a\\n', stderr='')

    Args:
        command: command.
        exc: raise exception.
        lines: split lines so ``\\n`` is removed from all lines (extra '\' added to avoid docstring error).
        py: runs with python executable.
        shell: expands shell variables and one line (shell True expands variables in shell).
        pysite: run on site python if running on a VENV.

    Returns:
        Union[CompletedProcess, int, list, str]: Completed process output.

    Raises:
        CmdError:
   """
    if py:
        m = '-m'
        if isinstance(command, str) and command.startswith('/'):
            m = ''
        command = f'{str(EXECUTABLE_SITE) if pysite else str(EXECUTABLE)} {m} {command}'
    elif not shell:
        command = toiter(command)

    if lines:
        text = False
    else:
        text = True

    proc = subprocess.run(command, shell=shell, capture_output=True, text=text)

    def std(out=True):
        if out:
            if lines:
                return proc.stdout.decode("utf-8").splitlines()
            else:
                # return proc.stdout.rstrip('.\n')
                return proc.stdout
        else:
            if lines:
                return proc.stderr.decode("utf-8").splitlines()
            else:
                # return proc.stderr.decode("utf-8").rstrip('.\n')
                return proc.stderr

    rv = subprocess.CompletedProcess(proc.args, proc.returncode, std(), std(False))
    if rv.returncode != 0 and exc:
        raise CmdError(rv)
    return rv


def cmdname(func: typing.Callable, sep: str = '_'): return func.__name__.split(**splitsep(sep))[0]


def current_task_name() -> str: return asyncio.current_task().get_name() if aioloop() else str()


@functools.singledispatch
def delete(data: MutableMapping, key=('self', 'cls',)) -> Optional[dict]:
    """
    Deletes item in dict based on key.

    Args:
        data: MutableMapping.
        key: key.

    Returns:
        data: dict with key deleted or the same if key not found.
    """
    key = toiter(key)
    for item in key:
        with contextlib.suppress(KeyError):
            del data[item]
    return data


@delete.register
def delete_list(data: list, key=('self', 'cls',)) -> Optional[list]:
    """
    Deletes value in list.

    Args:
        data: MutableMapping.
        key: key.

    Returns:
        data: list with value deleted or the same if key not found.
    """
    key = toiter(key)
    for item in key:
        with contextlib.suppress(ValueError):
            data.remove(item)
    return data


def dict_sort(data: dict[_KT, _VT], ordered: bool = ...,
              reverse: bool = ...) -> Union[dict[_KT, _VT], collections.OrderedDict[_KT, _VT]]:
    """
    Order a dict based on keys.

    Args:
        data: dict to be ordered.
        ordered: OrderedDict.
        reverse: reverse.

    Returns:
        Union[dict, collections.OrderedDict]: Dict sorted
    """
    rv = {key: data[key] for key in sorted(data.keys(), reverse=reverse)}
    if ordered:
        return collections.OrderedDict(rv)
    return rv.copy()


def iscoro(data: Any): return any([inspect.isasyncgen(data), inspect.isasyncgenfunction(data),
                                   asyncio.iscoroutine(data), inspect.iscoroutinefunction(data)])


def effect(apply: typing.Callable, args: Any) -> Optional[typing.Iterator]:

    """
    Perform function on iterable.

    Examples:
        >>> simple = Simple()
        >>> effect(lambda x: simple.__setattr__(x, dict()), 'a b', 'c')
        >>> assert simple.a == {}
        >>> assert simple.b == {}
        >>> assert simple.c == {}

    Args:
        apply: Function to apply.
        *args: Iterable to perform function.

    Returns:
        No Return.
    """
    for arg in toiter(args):
        for item in arg:
            apply(item)


def enumvalue(data: Any) -> Any:
    # noinspection PyCallingNonCallable
    """
    Returns Enum Value if Enum Instance or Data.

    Examples:
        >>> from bapy import N
        >>> enumvalue(N.ANNOTATIONS())
        '__annotations__'
        >>> enumvalue(None)

    Args:
        data: object.

    Returns:
        Enum Value or Data.
    """
    return data() if isinstance(data, enum.Enum) else data


def filterm(d: dict[_KT, _VT], k: typing.Callable[..., bool] = lambda x: True,
            v: typing.Callable[..., bool] = lambda x: True) -> MutableMapping[_KT, _VT]:
    # noinspection PyUnresolvedReferences
    """
    Filter Mutable Mapping.

    >>> assert filterm({'d':1}) == {'d': 1}
    >>> assert filterm({'d':1}, lambda x: x.startswith('_')) == {}
    >>> assert filterm({'d': 1, '_a': 2}, lambda x: x.startswith('_'), lambda x: isinstance(x, int)) == {'_a': 2}

    Returns:
        Filtered dict with
    """
    return d.__class__({x: y for x, y in d.items() if k(x) and v(y)})


def firstfound(data: typing.Iterable, apply: typing.Callable) -> Any:

    """
    Returns first value in data if apply is True.

    >>> assert firstfound([1, 2, 3], lambda x: x == 2) == 2
    >>> assert firstfound([1, 2, 3], lambda x: x == 4) is None

    Args:
        data: iterable.
        apply: function to apply.

    Returns:
        Value if found.
    """
    for i in data:
        if apply(i):
            return i


def flatten(data: LST, recurse: bool = False, unique: bool = False, sort: bool = True) -> LST:
    """
    Flattens an Iterable

    >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]]) == [1, 2, 3, 1, 5, 7, [2, 4, 1], 7, 6]
    >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]], recurse=True) == [1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 7]
    >>> assert flatten((1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]), unique=True) == (1, 2, 3, 4, 5, 6, 7)

    Args:
        data: iterable
        recurse: recurse
        unique: when recurse
        sort: sort

    Returns:
        Union[list, Iterable]:
    """
    if unique:
        recurse = True

    cls = data.__class__

    flat = []
    _ = [flat.extend(flatten(item, recurse, unique) if recurse else item)
         if isinstance(item, list) else flat.append(item) for item in data if item]
    value = set(flat) if unique else flat
    if sort:
        try:
            value = cls(sorted(value))
        except TypeError:
            value = cls(value)
    return value


def fromiter(data: typing.Iterable[typing.Callable], *args: Union[str, Iterable[str]]) -> DictStrAny:
    """
    Gets attributes from Iterable of objects and returns dict with

    >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], 'a', 'b', 'c') == {'a': [1, 2], 'b': [1]}
    >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], ('a', 'b', ), 'c') == {'a': [1, 2], 'b': [1]}
    >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], 'a b c') == {'a': [1, 2], 'b': [1]}

    Args:
        data: object.
        *args: attributes.

    Returns:
        Tuple
    """
    value = {k: [getattr(C, k) for C in data if N[k].has(C)] for i in args for k in toiter(i)}
    return {k: v for k, v in value.items() if v}


def has(data: Any, name: str) -> bool:
    """
    Name in Data.

    Args:
        data: object.
        name: attribute name.

    Returns:
        True if Name in Data.
    """
    return name in data if isinstance(data, Container) else hasattr(data, name)


def hasget(data: Any, name: str, default: Any = ...) -> Any:
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


def hasgetany(data: Any, name: str, default: Any = ...) -> Any:
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


def get(data: Any, *args: Any, default: bool = None, one: bool = True, recursive: bool = False,
        with_keys: bool = False) -> Any:
    """
    Get value of name in Mutabble Mapping/GetType or object

    Examples:
        >>> get(dict(a=1), 'a')
        1
        >>> get(dict(a=1), 'b')
        >>> get(dict(a=1), 'b', default=2)
        2
        >>> get(dict, '__module__')
        'builtins'
        >>> get(dict, '__file__')

    Args:
        data: MutabbleMapping/GetType to get value.
        *args: keys (default: ('name')).
        default: default value (default: None).
        with_keys: return dict names and values or values (default: False).
        one: return [0] if len == 1 and one instead of list (default: True).
        recursive: recursivily for MutableMapping (default: False).

    Returns:
        Value for key.
    """

    def rv(items):
        if recursive and with_keys:
            items = {key: value[0] if len(value) == 1 and one else value for key, value in items}
        if with_keys:
            return items
        return list(r)[0] if len(r := items.values()) == 1 and one else list(r)

    args = args or ('name',)
    mm = isinstance(data, MutableMapping)
    if recursive and not mm:
        # TODO: to_vars() empty
        # data = to_vars()
        pass
    if mm and recursive:
        return rv(collections.defaultdict(
            list, {k: v for arg in args for k, v in _nested_lookup(arg, data, with_keys=with_keys)}))
    elif mm:
        return rv({arg: data.get(arg, default) for arg in args})

    return rv({attr: getattr(data, attr, default) for attr in args})


def getm(data: Union[MutableMapping, Any], name: Any = 'name') -> Any:
    if isinstance(data, MutableMapping):
        return data.get(name, MISSING)
    return data.__getattribute__(name) if hasattr(data, name) else MISSING


def getnostr(data: Union[str, Any], attr: str = 'value') -> str:
    """
    Get attr if data is not str.

    Examples:
        >>> simple = Simple(value=1)
        >>> assert getnostr(simple) == 1
        >>> assert getnostr(simple, None) == simple
        >>> assert getnostr('test') == 'test'

    Args:
        data: object.
        attr: attribute name (default: 'value').

    Returns:
        Attr value if not str.
    """
    return (data if isinstance(data, str) else getattr(data, attr)) if attr else data


def getprops(data: Any) -> DictStrAny:
    is_type = isinstance(data, type)
    cls = data if is_type else data.__class__
    return {i: obj if is_type else getattr(data, i, Missing)
            for i in dir(cls) if (obj := isinstance(getattr(cls, i), property)) and not iscoro(obj)}


def getset(data: Any, name: str, default: Any = None, setvalue: bool = True) -> Any:
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


def indict(data: typing.MutableMapping, items: typing.MutableMapping = None, **kwargs: Any) -> bool:
    """
    All item/kwargs pairs in flat dict.

    >>> assert indict(N.BUILTIN(), {'iter': iter}, credits=credits) is True
    >>> assert indict(N.BUILTIN(), {'iter': 'fake'}) is False
    >>> assert indict(N.BUILTIN(), {'iter': iter}, credits='fake') is False
    >>> assert indict(N.BUILTIN(), credits='fake') is False

    Args:
        data: dict to search.
        items: key/value pairs.
        **kwargs: key/value pairs.

    Returns:
        True if all pairs in dict.
    """
    return all(map(lambda x: x[0] in data and x[1] == data[x[0]], ((items if items else {}) | kwargs).items()))


def indictr(data: typing.MutableMapping, items: typing.MutableMapping = None, **kwargs: Any) -> bool:
    """
    Is Item in Dict?.

    Examples:
        >>> from bapy import indictr, N
        >>> indictr(globals(), {'True': True, 'False': False})
        True
        >>> indictr(globals()['__builtins__'], {'True': True, 'False': False}, __name__='builtins')
        True
        >>> indictr(globals(), {'True': True, 'False': False}, __name__='builtins')
        True

    Args:
        data: Dict
        items: Dict with key and values for not str keys (default: None)
        **kwargs: keys and values.

    Raises:
        TypeError: item must be a MutabbleMapping.

    Returns:
        True if items in Dict.
    """
    if isinstance(data, MutableMapping):
        if items and not isinstance(items, MutableMapping):
            raise TypeError(f'{items=} must be a MutabbleMapping')
        if d := (items if items else dict()) | kwargs:
            for key, value in d.items():
                values = nested_lookup.nested_lookup(key, data)
                if not values or value not in values:
                    return False
            return True
    return False


def iseven(number: int) -> bool: return not number % 2


def join_newline(data: typing.Iterable) -> str: return NEWLINE.join(data)


@app.command()
def localbin(path: pathlib.Path = __file__) -> None:
    """
    Copy files in directory/path to /usr/local/bin (except __init__.py).

    Args:
        path: source directory or file.

    Returns:
        None
    """
    path = pathlib.Path(path)
    path = (path.parent / N.scripts.value) if path.is_file() else path

    subprocess.run(f'find {pathlib.Path(path)} -mindepth 1 -maxdepth 1 -type f ! -name ".*" ! -name "{INIT_PY}" '
                   f'! -name "_init.py" -exec {WITHSUDO} chmod +x "{CURLYBRACKETS}" \; -print | '
                   f'xargs -I {CURLYBRACKETS} {WITHSUDO} cp "{CURLYBRACKETS}" {LOCALBIN}', shell=True, check=True)


def map_reduce_even(iterable: typing.Iterable[_T]) -> list[_U, list[_T]]:
    return more_itertools.map_reduce(iterable, keyfunc=iseven)


def map_with_args(data: Any, func: typing.Callable, /, *args, pred: typing.Callable = lambda x: True if x else False,
                  split: str = ' ', **kwargs: Any) -> list:
    """
    Apply pred/filter to data and map with args and kwargs.

    Examples:
        >>> # noinspection PyUnresolvedReferences
        >>> def f(i, *ar, **kw):
        ...     return f'{i}: {[a(i) for a in ar]}, {", ".join([f"{k}: {v(i)}" for k, v in kw.items()])}'
        >>> map_with_args('0.1.2', f, int, list, pred=lambda x: x != '0', split='.', int=int, str=str)
        ["1: [1, ['1']], int: 1, str: 1", "2: [2, ['2']], int: 2, str: 2"]

    Args:
        data: data.
        func: final function to map.
        *args: args to final map function.
        pred: pred to filter data before map.
        split: split for data str.
        **kwargs: kwargs to final map function.

    Returns:
        List with results.
    """
    return [func(item, *args, **kwargs) for item in yield_if(data, pred=pred, split=split)]


def missing(data: Any) -> bool: return data == MISSING


def newprop(name: str = None, default: Union[Any, typing.Callable, functools.partial] = None) -> property:
    """
    Get a new property with getter, setter and deleter.

    Examples:
        >>> class Test:
        ...     prop = newprop()
        ...     callable = newprop(default=str)
        >>>
        >>> test = Test()
        >>> '_prop' not in vars(test)
        True
        >>> test.prop
        >>> '_prop' in vars(test)
        True
        >>> test.prop
        >>> test.prop = 2
        >>> test.prop
        2
        >>> del test.prop
        >>> '_prop' in vars(test)
        False
        >>> test.prop
        >>> '_callable' not in vars(test)
        True
        >>> test.callable  # doctest: +ELLIPSIS
        '....Test object at 0x...>'
        >>> '_callable' in vars(test)
        True
        >>> test.callable  # doctest: +ELLIPSIS
        '....Test object at 0x...>'
        >>> test.callable = 2
        >>> test.callable
        2
        >>> del test.callable
        >>> '_callable' in vars(test)
        False
        >>> test.callable  # doctest: +ELLIPSIS
        '....Test object at 0x...>'

    Args:
        name: property name (attribute name: _name). :func:' varname`is used if no name (default: varname())
        default: default for getter if attribute is not defined.
            Could be a callable/partial that will be called with self (default: None)

    Returns:
        Property.
    """
    name = f'_{name if name else varname()}'
    return property(
        lambda self:
        getset(self, name, default=default(self) if isinstance(default, (Callable, functools.partial)) else default),
        lambda self, value: self.__setattr__(name, value),
        lambda self: self.__delattr__(name)
    )


def noexc(func: Callable, *args: Any, default_: Any = None, exc_: ExceptionUnion = Exception, **kwargs: Any) -> Any:
    """
    Execute function suppressing exceptions.

    Examples:
        >>> noexc(dict(a=1).pop, 'b', default_=2, exc_=KeyError)
        2

    Args:
        func: callable.
        *args: args.
        default_: default value if exception is raised.
        exc_: exception or exceptions.
        **kwargs: kwargs.

    Returns:
        Any: Function return.
    """
    try:
        return func(*args, **kwargs)
    except exc_:
        return default_


def notmissing(data: Any) -> bool: return not (data == MISSING)


def prefixed(name: Any) -> Optional[str]:
    try:
        return f'{name.upper()}_'
    except AttributeError:
        pass


def pretty_install(cons=console, expand=False): return rich.pretty.install(cons, expand_all=expand)


def pypifree(name: str, stdout: bool = False) -> bool:
    """
    Pypi name available.

    Examples:
        >>> assert pypifree('common') is False
        >>> assert pypifree('sdsdsdsd') is True

    Args:
        name: package.
        stdout: stdout.

    Returns:
        bool: True if available.
    """
    r = requests.get(f'https://pypi.org/pypi/{name}/json')

    if r:
        if stdout:
            print(False)
        return False
    else:
        if stdout:
            print(True)
        return True


@decorator.decorator
def runwarning(func: typing.Callable, *args: Any, **kwargs: Any) -> Any:
    with warnings.catch_warnings(record=False):
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        warnings.showwarning = lambda *_args, **_kwargs: None
        rv = func(*args, **kwargs)
        return rv


def splitsep(sep: str = '_') -> dict[str, str]: return dict(sep=sep) if sep else dict()


def to_camel(text: str, replace: bool = True) -> str:
    # noinspection PyCallingNonCallable
    """
    Convert to Camel

    Examples:
        >>> from bapy import N
        >>> to_camel(N.IGNORE_ATTR())
        'IgnoreAttr'
        >>> to_camel(N.IGNORE_ATTR(), replace=False)
        '__Ignore_Attr__'

    Args:
        text: text to convert.
        replace: remove '_'  (default: True)

    Returns:
        Camel text.
    """
    rv = ''.join(map(str.title, toiter(text, '_')))
    return rv.replace('_', '') if replace else rv


def toiter(data: Any, always: bool = False, split: str = ' '
           ) -> Union[typing.Sized, MutableMapping, typing.Sequence, typing.MutableSequence]:
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


def varname(index: int = 2, lower: bool = True, sep: str = '_') -> Optional[str]:
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
                return (var.lower() if lower else var).split(**splitsep(sep))[0]


@app.command(name='version')
def _version() -> None:
    """Version"""
    print(__version__)


def yield_if(data: Any, pred: typing.Callable = lambda x: True if x else False, split: str = ' ',
             apply: Union[Callable, tuple[Callable, ...]] = None) -> typing.Generator:
    """
    Yield value if condition is met and apply function if predicate.

    Examples:
        >>> assert list(yield_if([True, None])) == [True]
        >>> assert list(yield_if('test1.test2', pred=lambda x: x.endswith('2'), split='.')) == ['test2']
        >>> assert list(yield_if('test1.test2', pred=lambda x: x.endswith('2'), split='.', \
        apply=lambda x: x.removeprefix('test'))) == ['2']
        >>> assert list(yield_if('test1.test2', pred=lambda x: x.endswith('2'), split='.', \
        apply=(lambda x: x.removeprefix('test'), lambda x: int(x)))) == [2]


    Args:
        data: data
        pred: predicate (default: if value)
        split: split char for str.
        apply: functions to apply if predicate is met.

    Returns:
        Yield values if condition is met and apply functions if provided.
    """
    for item in toiter(data, split=split):
        if pred(item):
            if apply:
                for func in toiter(apply):
                    item = func(item)
            yield item


def yield_last(data: Any, split: str = ' ') -> Iterator[tuple[bool, Any, Optional[Any]]]:
    """
    Yield value if condition is met and apply function if predicate.

    Examples:
        >>> assert list(yield_last([True, None])) == [(False, True, None), (True, None, None)]
        >>> assert list(yield_last('first last')) == [(False, 'first', None), (True, 'last', None)]
        >>> assert list(yield_last('first.last', split='.')) == [(False, 'first', None), (True, 'last', None)]
        >>> assert list(yield_last(dict(first=1, last=2))) == [(False, 'first', 1), (True, 'last', 2)]


    Args:
        data: data.
        split: split char for str.

    Returns:
        Yield value and True when is the last item on iterable
    """
    data = toiter(data, split=split)
    mm = isinstance(data, MutableMapping)
    total = len(data)
    count = 0
    for i in data:
        count += 1
        yield count == total, *(i, data.get(i) if mm else None,)


# Classes
class EnumBase(enum.Enum):
    """Enum Base Class."""

    def __call__(self, *args, **kwargs) -> Union[str, Any]:
        """Returns Value."""
        return self.value

    def __hash__(self): return hash(self._name_)

    def _generate_next_value_(self, start, count, last_values) -> Union[str, Any]:
        return self.lower()

    @classmethod
    def asdict(cls) -> DictStrAny:
        return {key: value._value_ for key, value in cls.__members__.items()}

    @classmethod
    def attrs(cls) -> list[str, ...]: return list(cls.__members__)

    @classmethod
    def default(cls) -> Union[_T, enum.Enum]: return cls._member_map_[cls._member_names_[0]]

    @classmethod
    def default_attr(cls) -> str: return cls.attrs()[0]

    @classmethod
    def default_dict(cls) -> dict[str, Union[_T, enum.Enum]]: return {cls.default_attr(): cls.default_value()}

    @classmethod
    def default_value(cls) -> Any: return cls[cls.default_attr()]

    @property
    def describe(self) -> tuple[str, Union[_T, enum.Enum]]:
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


# Classes
class AllAttr(metaclass=abc.ABCMeta):
    """ __all__ Type. """
    __slots__ = ()
    __all__ = ()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AllAttr:
            return N.ALL.has(C)
        return NotImplemented


class CmdError(Exception):
    """Thrown if execution of cmd command fails with non-zero status code."""
    def __init__(self, rv: subprocess.CompletedProcess) -> None:
        command = rv.args
        rc = rv.returncode
        stderr = rv.stderr
        stdout = rv.stdout
        super().__init__(f'{command=}', f'{rc=}', f'{stderr=}', f'{stdout=}')


class CmdAioError(CmdError):
    """Thrown if execution of aiocmd command fails with non-zero status code."""
    def __init__(self, rv: subprocess.CompletedProcess) -> None:
        super().__init__(rv)


class getter(typing.Callable[[Any], Union[Any, typing.Tuple[Any, ...]]]):
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

    def __init__(self, attr: Union[str, typing.Iterable[str]], *attrs: str, default: Any = None) -> None:
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

    def __call__(self, obj: Any) -> Union[Any, tuple[Any, ...]]: return self._call(obj)
    def __reduce__(self): return self.__class__, self._attrs
    def __repr__(self) -> str: return f'{self.__class__}({self._attrs})'


class Missing:
    name = 'MISSING'
    __slots__ = ()
    def __hash__(self): return hash((self.__class__, self.name,))
    def __reduce__(self): return self.__class__, (self.name,)
    def __repr__(self): return f'<{self.name}>'


MISSING = Missing()
DictStrMissingAny = dict[str, Union[Missing, Any]]


class NParser:
    __slots__ = ('data', 'default', )
    def __init__(self, data: str = '', default: Any = None) -> None: self.data, self.default = data, default
    def __repr__(self): return f'{self.__class__.__name__}({self.asdict()})'
    def asdict(self): return getprops(self)

    @property
    def domain(self) -> Union[furl.furl, Any]:
        if self.data:
            if noexc(socket.gethostbyname, self.data):
                return furl.furl(host=self.data)
        return self.default

    @property
    def email(self) -> Union[furl.furl, Any]:
        if self.data:
            if rv := noexc(marshmallow.validate.Email(), self.data, default_=self.default):
                value = rv.split('@')
                return furl.furl(host=value[1], username=value[0])
        return self.default

    @property
    def environ(self) -> Union[furl.furl, str, IPv, int, pathlib.Path, Any]:
        if self.true is not None:
            return self.true
        if self.integer is not None:
            return self.integer
        if self.email is not None:
            return self.email
        if self.domain is not None:
            return self.domain
        if self.url is not None:
            return self.url
        if self.ip is not None:
            return self.ip
        if self.path is not None:
            return self.path
        return self.data

    @property
    def integer(self) -> Union[int, Any]:
        if self.data:
            return noexc(marshmallow.fields.Integer().deserialize, self.data, default_=self.default)
        return self.default

    @property
    def ip(self) -> Union[IPv, Any]:
        if self.data:
            return noexc(ipaddress.ip_address, self.data, default_=self.default)
        return self.default

    @property
    def log_level(self) -> Union[str, Any]:
        if self.data:
            rv = self.data.upper()
            if hasattr(logging, rv):
                return rv
        return self.default

    @property
    def log_value(self) -> Union[int, Any]:
        if self.data:
            if rv := self.log_level:
                return getattr(logging, rv, self.default)
            elif self.integer:
                level = self.data.upper()
                if hasattr(logging, self.data) and isinstance(getattr(logging, level), int):
                    return getattr(logging, level)
        return self.default

    @property
    def path(self) -> Union[pathlib.Path, Any]:
        if self.data:
            if any([self.domain, self.email, self.integer, self.ip, self.true, self.url]):
                return self.default
            if NEWLINE not in self.data and '*' not in self.data and '$' not in self.data and '/' in self.data:
                return pathlib.Path(self.data)
        return self.default

    @property
    def true(self) -> Union[bool, Any]:
        if self.data:
            return noexc(marshmallow.fields.Boolean().deserialize, self.data, default_=self.default)
        return self.default

    @property
    def url(self) -> Union[furl.furl, Any]:
        if self.data:
            if rv := noexc(marshmallow.validate.URL(), self.data):
                return furl.furl(rv)
        return self.default


class NBase(EnumBase):
    def __call__(self, *args, **kwargs) -> Union[str, Any]:
        """Returns Value or Has."""
        if args:
            return self.has(*args)
        return self.value

    def _generate_next_value_(self, start, count, last_values) -> Union[str, Any]:
        if self.isupper():
            if self in os.environ:
                return os.environ[self]
            return f'__{self.lower()}__'
        return self.removesuffix('_')

    def get(self, obj: Any, default: Any = None) -> Any:
        """
        Get key/attr value.

        Args:
            obj: object.
            default: default value (default: None).

        Returns:
            Value.
        """
        return hasget(obj, name=self.value, default=default)

    def getset(self, obj: Any, default: Any = None, setvalue: bool = True) -> Any:
        """
        Get key/attr value and sets if does not exists.

        Args:
            obj: object.
            default: default value (default: None).
            setvalue: setattr in object if AttributeError (default: True).

        Returns:
            Value.
        """
        return getset(obj, name=self.value, default=default, setvalue=setvalue)

    @property
    def getter(self) -> getter: return getter(self.value)

    def has(self, obj: Any) -> bool:
        # noinspection PyUnresolvedReferences,PyCallingNonCallable
        """
        Checks if object/dict has attr/key.

        >>> from bapy import N
        >>> class Test:
        ...     __repr_newline__ = True
        >>>
        >>> assert N.REPR_NEWLINE(Test()) is True
        >>> assert N.REPR_EXCLUDE(Test()) is False
        >>> assert N.MODULE(tuple) is True
        >>> assert N.NAME(tuple) is True
        >>> assert N.FILE(tuple) is False
        >>> assert N.FILE(asyncio) is True

        Args:
            obj: object.

        Returns:
            True if object/dict has attr/key.
        """
        return has(obj, self.value)

    def hasget(self, obj: Any, default: Any = None) -> Any:
        return hasget(obj, self.value, default=default)

    def hasgetany(self, obj: Any, default: Any = None) -> Any:
        return hasgetany(obj, self.value, default=default)

    def parse(self) -> NParser: return NParser(self())


class N(NBase):
    ABOUT = enum.auto()
    ABSTRACTMETHODS = enum.auto()
    AUTHOR = enum.auto()
    ADAPT = enum.auto()
    ALL = enum.auto()
    ALLOC = enum.auto()
    ANNOTATIONS = enum.auto()
    ARGS = enum.auto()
    ASDICT = enum.auto()
    ATTRIBUTES = enum.auto()
    BASE = enum.auto()
    BASICSIZE = enum.auto()
    BUILD_CLASS = enum.auto()
    BUILTINS = enum.auto()
    CACHE_CLEAR = enum.auto()
    CACHE_INFO = enum.auto()
    CACHED = enum.auto()
    CLASS = enum.auto()
    CODE = enum.auto()
    CONFORM = enum.auto()
    CONTAINS = enum.auto()
    CREDITS = enum.auto()
    COPY = enum.auto()
    COPYRIGHT = enum.auto()
    CVSID = enum.auto()
    DATACLASS_FIELDS = enum.auto()
    DATACLASS_PARAMS = enum.auto()
    DATE = enum.auto()
    DECIMAL_CONTEXT = enum.auto()
    DEEPCOPY = enum.auto()
    DELATTR = enum.auto()
    DICT = enum.auto()
    DICTOFFSET = enum.auto()
    DIR = enum.auto()
    DOC = enum.auto()
    DOCFORMAT = enum.auto()
    EMAIL = enum.auto()
    EQ = enum.auto()
    EXCEPTION = enum.auto()
    FILE = enum.auto()
    FLAGS = enum.auto()
    FUNC = enum.auto()
    GET = enum.auto()
    GETATTRIBUTE = enum.auto()
    GETFORMAT = enum.auto()
    GETINITARGS = enum.auto()
    GETITEM = enum.auto()
    GETNEWARGS = enum.auto()
    GETSTATE = enum.auto()
    HASH = enum.auto()
    HASH_EXCLUDE = enum.auto()
    IGNORE_ATTR = enum.auto()
    IGNORE_COPY = enum.auto()
    IGNORE_HASH = enum.auto()
    IGNORE_INIT = enum.auto()
    IGNORE_KWARG = enum.auto()
    IGNORE_REPR = enum.auto()
    IGNORE_STATE = enum.auto()
    IGNORE_STR = enum.auto()
    IMPORT = enum.auto()
    INIT = enum.auto()
    INIT_SUBCLASS = enum.auto()
    INITIALIZING = enum.auto()
    ISABSTRACTMETHOD = enum.auto()
    ITEMSIZE = enum.auto()
    LEN = enum.auto()
    LIBMPDEC_VERSION = enum.auto()
    LOADER = enum.auto()
    LTRACE = enum.auto()
    MAIN = enum.auto()
    MEMBERS = enum.auto()
    METHODS = enum.auto()
    MODULE = enum.auto()
    MP_MAIN = enum.auto()
    MRO = enum.auto()
    NAME = enum.auto()
    NEW = enum.auto()
    NEW_MEMBER = enum.auto()
    NEW_OBJ = enum.auto()
    NEW_OBJ_EX = enum.auto()
    OBJ_CLASS = enum.auto()
    OBJCLASS = enum.auto()
    PACKAGE = enum.auto()
    POST_INIT = enum.auto()
    PREPARE = enum.auto()
    QUALNAME = enum.auto()
    REDUCE = enum.auto()
    REDUCE_EX = enum.auto()
    REPR = enum.auto()
    REPR_EXCLUDE = enum.auto()
    REPR_NEWLINE = enum.auto()
    REPR_PPROPERTY = enum.auto()
    RETURN = enum.auto()
    SELF_CLASS = enum.auto()
    SETATTR = enum.auto()
    SETFORMAT = enum.auto()
    SETSTATE = enum.auto()
    SIGNATURE = enum.auto()
    SIZEOF = enum.auto()
    SLOTNAMES = enum.auto()
    SLOTS = enum.auto()
    SPEC = enum.auto()
    STATE = enum.auto()
    STATUS = enum.auto()
    STR = enum.auto()
    SUBCLASSHOOK = enum.auto()
    TEST = enum.auto()
    TEXT_SIGNATURE = enum.auto()
    THIS_CLASS = enum.auto()
    TRUNC = enum.auto()
    VERSION = enum.auto()
    WARNING_REGISTRY = enum.auto()
    WEAKREF = enum.auto()
    WEAKREFOFFSET = enum.auto()
    WRAPPED = enum.auto()
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
    asdict_ = enum.auto()
    attr = enum.auto()
    attrs_ = enum.auto()
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
    default_ = enum.auto()
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
    self_ = enum.auto()
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
    values_ = enum.auto()
    values_dict = enum.auto()
    vars = enum.auto()
    venv = enum.auto()
    AMARILLO = enum.auto()
    ANSIBLE = enum.auto()
    ANSIBLE_SUDO_PASSWORD = enum.auto()
    APPLICATIONS = enum.auto()
    ATHENS_GONOSUM_PATTERNS = enum.auto()
    AZUL = enum.auto()
    AZULCLARO = enum.auto()
    BAPY = enum.auto()
    BASH_RC_DIR = enum.auto()
    BASH_RC_NAME = enum.auto()
    BASH_RC_PATH = enum.auto()
    BASH_RC_PROJECT = enum.auto()
    BREW = enum.auto()
    BREWFILE = enum.auto()
    CACHES = enum.auto()
    CLONES = enum.auto()
    CLT = enum.auto()
    CONFLUENCE_SERVER_PASS = enum.auto()
    DARWIN = enum.auto()
    DATA = enum.auto()
    DEBIAN = enum.auto()
    DEFAULT_CA_BUNDLE_PATH = enum.auto()
    DEFAULT_KALI_USER = enum.auto()
    DEVOPS_HOST = enum.auto()
    DEVOPS_SLD = enum.auto()
    DOCK = enum.auto()
    DOCKER_HOST = enum.auto()
    DOMAINED_DIR = enum.auto()
    DOMAINED_PATH = enum.auto()
    EDITOR = enum.auto()
    EXAMPLES = enum.auto()
    FILES = enum.auto()
    GEMFILE = enum.auto()
    GEOLOCATION_KEY = enum.auto()
    GITHUB_DESKTOP = enum.auto()
    GITHUB_DESKTOP_PROCESS = enum.auto()
    GITHUB_DOMAIN = enum.auto()
    GITHUB_EMAIL = enum.auto()
    GITHUB_ORGANIZATION = enum.auto()
    GITHUB_ORGANIZATION_CLONE_PREFIX_HTTP = enum.auto()
    GITHUB_ORGANIZATION_CLONE_PREFIX_SSH = enum.auto()
    GITHUB_ORGANIZATION_EMAIL = enum.auto()
    GITHUB_ORGANIZATION_ID = enum.auto()
    GITHUB_ORGANIZATION_ID_CLONE_PREFIX_SSH = enum.auto()
    GITHUB_ORGANIZATION_PASSWORD = enum.auto()
    GITHUB_ORGANIZATION_USERNAME = enum.auto()
    GITHUB_PRIVATE_URL = enum.auto()
    GITHUB_SECRETS_PATH = enum.auto()
    GITHUB_SECRETS_URL = enum.auto()
    GITHUB_URL = enum.auto()
    GITHUB_USERNAME = enum.auto()
    GIT_COMMAND = enum.auto()
    GIT_PREFIX = enum.auto()
    GIT_STORE = enum.auto()
    GO111MODULE = enum.auto()
    GOHOME = enum.auto()
    GOPATH = enum.auto()
    HOME = enum.auto()
    ICLOUD = enum.auto()
    ICLOUD_BASENAME = enum.auto()
    ICLOUD_NICK = enum.auto()
    INFOPATH = enum.auto()
    INTERNET = enum.auto()
    INTERNET_HASH = enum.auto()
    INVERSO = enum.auto()
    JETBRAINS = enum.auto()
    JETBRAINS_NAME = enum.auto()
    KALI = enum.auto()
    KEYNOTE = enum.auto()
    LANG = enum.auto()
    LATEST = enum.auto()
    LC_ALL = enum.auto()
    LIBRARY = enum.auto()
    LIBRARY_NICK = enum.auto()
    LOG = enum.auto()
    LOGNAME = enum.auto()
    LOG_BASENAME = enum.auto()
    MACDEV = enum.auto()
    MACDEV_BASENAME = enum.auto()
    MACDEV_NICK = enum.auto()
    MACKUP_ENGINE = enum.auto()
    MACROOT = enum.auto()
    MNOPI = enum.auto()
    MOBILE = enum.auto()
    MORADO = enum.auto()
    MSF_DATABASE_CONFIG = enum.auto()
    NPM = enum.auto()
    NPMFILE = enum.auto()
    NUMBERS = enum.auto()
    OPAMFILE = enum.auto()
    ORG = enum.auto()
    ORG_ATLAS_PASSWORD = enum.auto()
    ORG_BASENAME = enum.auto()
    ORG_GROUP_DEFAULT = enum.auto()
    ORG_HOST = enum.auto()
    ORG_SERVER = enum.auto()
    ORG_SLD = enum.auto()
    PACKAGES = enum.auto()
    PACKAGES_BASENAME = enum.auto()
    PAGES = enum.auto()
    PASSWD_PATH = enum.auto()
    PASSWORD = enum.auto()
    PATH = enum.auto()
    PEN = enum.auto()
    PEN_GIT = enum.auto()
    PEN_NICK = enum.auto()
    PREFS = enum.auto()
    PYCHARM = enum.auto()
    PYCHARM_NAME = enum.auto()
    PYCHARM_OPTIONS = enum.auto()
    PYCHARM_PLUGINS = enum.auto()
    PYCHARM_SCRATCHES = enum.auto()
    PYCHARM_VERSION = enum.auto()
    PYTHON39 = enum.auto()
    PYTHON39_HOME = enum.auto()
    PYTHON39_PACKAGES = enum.auto()
    PYTHONASYNCIODEBUG = enum.auto()
    PYTHONDONTWRITEBYTECODE = enum.auto()
    PYTHONNOUSERSITE = enum.auto()
    PYTHONUNBUFFERED = enum.auto()
    REALNAME = enum.auto()
    REPO_DEFAULT_ADMIN_PASSWORD = enum.auto()
    REPO_DEFAULT_ADMIN_USERNAME = enum.auto()
    REPO_DEFAULT_API_URL = enum.auto()
    REPO_DEFAULT_API_VERSION = enum.auto()
    REPO_DEFAULT_HOST = enum.auto()
    REPO_DEFAULT_HOSTNAME = enum.auto()
    REPO_DEFAULT_PASSWORD = enum.auto()
    REPO_DEFAULT_SCHEME = enum.auto()
    REPO_DEFAULT_URL = enum.auto()
    REPO_DEFAULT_USERNAME = enum.auto()
    REQUESTS_CA_BUNDLE = enum.auto()
    REQUIREMENTS = enum.auto()
    ROJO = enum.auto()
    SAVED = enum.auto()
    SCALEWAY_ACCESS_KEY = enum.auto()
    SCALEWAY_ENDPOINT = enum.auto()
    SCALEWAY_ORGANIZATION_ID = enum.auto()
    SCALEWAY_SECRET_KEY = enum.auto()
    SCHEME = enum.auto()
    SCRATCHES = enum.auto()
    SCRATCHES_NAME = enum.auto()
    SCRIPTS = enum.auto()
    SCRIPTS_BASENAME = enum.auto()
    SCW_TOKEN = enum.auto()
    SECRETS_PATH = enum.auto()
    SECRETS_REPO = enum.auto()
    SERVERS = enum.auto()
    SERVERS_HOST = enum.auto()
    SERVERS_SLD = enum.auto()
    SHELL = enum.auto()
    SHELLCHECK_OPTS = enum.auto()
    SHLVL = enum.auto()
    SSH_AUTH_SOCK = enum.auto()
    SSH_PRIVATE_KEY = enum.auto()
    SSL_CERT_FILE = enum.auto()
    SUPPORT = enum.auto()
    SYNTHETIC = enum.auto()
    TERM = enum.auto()
    TERM_PROGRAM = enum.auto()
    TMPDIR = enum.auto()
    UBUNTU = enum.auto()
    USB = enum.auto()
    USER = enum.auto()
    USERFILE = enum.auto()
    USERHOME = enum.auto()
    USERNAME = enum.auto()
    VERDE = enum.auto()
    VIRTUAL_ENV = enum.auto()
    VISUAL = enum.auto()
    VULTR_API_KEY = enum.auto()
    VULTR_API_TIMEOUT = enum.auto()
    XPC_SERVICE_NAME = enum.auto()


class Re(EnumBase):
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

    def findall(self, string: Union[bytes, str]) -> list[Any]:
        """Return a list of all non-overlapping matches in the string.

        If one or more capturing groups are present in the pattern, return
        a list of groups; this will be a list of tuples if the pattern
        has more than one group.

        Empty matches are included in the result."""
        return self.value.findall(string=string)

    def finditer(self, string: Union[bytes, str]) -> MatchIterator:
        """Return an iterator over all non-overlapping matches in the
        string.  For each match, the iterator returns a Match object.

        Empty matches are included in the result."""
        return self.value.finditer(string=string)

    def fullmatch(self, string: AnyStr) -> MatchOptional:
        """Try to apply the pattern to all of the string, returning
        a Match object, or None if no match was found."""
        return self.value.fullmatch(string=string)

    def match(self, string: AnyStr) -> MatchOptional:
        """Try to apply the pattern at the start of the string, returning
        a Match object, or None if no match was found."""
        return self.value.match(string=string)

    def search(self, string: AnyStr) -> MatchOptional:
        """Scan through string looking for a match to the pattern, returning
        a Match object, or None if no match was found."""
        return self.value.search(string=string)

    def sub(self, repl: MatchCallableUnion, string: AnyStr, count: int = 0) -> tuple[AnyStr, int]:
        """Return the string obtained by replacing the leftmost
        non-overlapping occurrences of the pattern in string by the
        replacement repl.  repl can be either a string or a callable;
        if a string, backslash escapes in it are processed.  If it is
        a callable, it's passed the Match object and must return
        a replacement string to be used."""
        return self.value.sub(repl=repl, string=string, count=count)

    def subn(self, repl: MatchCallableUnion, string: AnyStr, count: int = 0) -> tuple[AnyStr, int]:
        """Return a 2-tuple containing (new_string, number).
        new_string is the string obtained by replacing the leftmost
        non-overlapping occurrences of the pattern in the source
        string by the replacement repl.  number is the number of
        substitutions that were made. repl can be either a string or a
        callable; if a string, backslash escapes in it are processed.
        If it is a callable, it's passed the Match object and must
        return a replacement string to be used."""
        return self.value.subn(repl=repl, string=string, count=count)


# Init
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
