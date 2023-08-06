import dataclasses
import enum
import functools
import inspect
from functools import reduce
from typing import Tuple, Union


# taken from https://stackoverflow.com/questions/3589311/get-defining-class-of-unbound-method-object-in-python-3
def _get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return _get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (
            inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__,
                                                                                                '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


class Self(type):
    """
    This class stands in for the type of the class being defined. Since decorators require evaluation
    before the defintion end of a class, you cannot use a class's type in the @accepts for one of its
    methods. Instead, you should use the type Self. This will be replaced by the class type at runtime.
    This does not make sense for unbound methods (free functions) or static methods and will raise an
    error if passed to such a function or method.

    Example:

        class Vector2D:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

            @accepts(Self)
            def plus(self, other):
                self.x += other.x
                self.y += other.y
                self.z += other.z

         class State:
            registry = {}

            @classmethod
            @accepts((Self, str))
            def get(cls, s):
                if isinstance(s, State):
                    return s
                else:
                    if s not in registry:
                        registry[s] = State(s)
                    return registry[s]

            @accepts(str)
            def __init__(self, name):
                self.name = name
    """
    pass


def _isiterable(t):
    try:
        i = iter(t)
        return True
    except TypeError:
        return False


# from PEP 318 with heavy modifications
def accepts(*types: Union[type, Tuple[type]]):
    """
    Provides a declaration and run-time check of the types accepted by a function or method

    Pass 1 type per argument or, if multiple types are acceptable, 1 tuple of types per argument (as used in isinstance)

    DO NOT PASS A TYPE FOR self OR cls parameters. The parameters 'self' and 'cls' are NEVER CHECKED by if they appear
    as the first parameter in a method.

    :param types: a splat of types or tuples of types to match 1 to 1 against the args to the function
    :return: a decorator which wraps a function and does a run time type check on all arguments against the types
             given EXCEPT for 'self' and 'cls' first args
    """
    def check_accepts(f):
        is_bound = len(f.__code__.co_varnames) > 0 and (
                f.__code__.co_varnames[0] == 'self' or f.__code__.co_varnames[0] == 'cls')
        if is_bound:
            argcount = f.__code__.co_argcount - 1
        else:
            argcount = f.__code__.co_argcount
        assert len(types) == argcount, "Not enough types for arg count, expected {} but got {}".format(argcount,
                                                                                                       len(types))

        @functools.wraps(f)
        def new_f(*args, **kwds):
            if is_bound:
                for_args = args[1:]  # drop self or cls
            else:
                for_args = args
            for (a, t) in zip(for_args, types):
                if _isiterable(t) and not isinstance(t, enum.EnumMeta):
                    t = tuple([_get_class_that_defined_method(f) if i is Self else i for i in t])
                    assert all(i is not None for i in t), "Cannot accept Self on non-bound method {}".format(f.__name__)
                else:
                    t = _get_class_that_defined_method(f) if t is Self else t
                    assert t is not None, "Cannot accept Self on non-bound method {}".format(f.__name__)
                assert isinstance(a, t), "{}: got argument {} (type of {}) but expected argument of type(s) {}".format(
                    f.__name__, a, type(a), t)
            return f(*args, **kwds)

        return new_f

    return check_accepts

def json_serializable(cls):
    """
    Adds a 'to_json' method to the class that it annotates. This method
    uses json.dumps and a JSONEncoder to bundle all the keys and values of the
    classes __dict__ property into a JSON object
    """
    import json
    class MyEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
    def to_json(self) -> str:
        return json.dumps(self.__dict__, cls=MyEncoder)
    setattr(cls, 'to_json', to_json)
    return cls


def spread(times):
    """
    creates a new function that takes the same arguments as the original function
    and runs the original function `times` times storing the result in a list
    each time and then returning the list of all the results back to the caller
    """
    def inner(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            results = []
            for i in times:
                results.append(fn(*args, **kwargs))
            return results

        return wrapper

    return inner


def timed(fn):
    """
    Wraps a function using time.time() in order to time the execution of the function

    Returns the a tuple of original function result and the time elapsed in
    seconds
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        return result, end - start

    return wrapper


def squash(exceptions: Union[Tuple[Type[BaseException]], Callable[[Any], Any]] = (Exception,),
           on_squashed: Optional[Any] = None):

    """
    returns a function that handles exceptions differently.

    if squash is used without calling it, then the decorated function that is
    returned does the following: if the new function raises an
    exception of type Exception or its derivates, it is ignored and None is returned

    If squash is used with parameters, then: 

    If an exception is raised in the function that is not of a type listed in
    the `exceptions` parameter, then the exception is raised normally

    If an exception is raised in the function that IS of a type listed in
    the `exceptions` parameter, then..

        If `on_squashed` is a value (including None) then that is returned
        If `on_squashed` is callable (has a __call__ method) then the
          result of calling `on_squashed` is returned
    """
    if type(exceptions) is types.FunctionType:
        @functools.wraps(exceptions)
        def wrapper(*args, **kwargs):
            try:
                return exceptions(*args, **kwargs)
            except Exception:
                return None

        return wrapper
    else:
        def decor(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except BaseException as e:
                    squashed = exceptions if isinstance(exceptions, Tuple) else tuple(exceptions)
                    if not isinstance(e, squashed):
                        raise
                    else:
                        return on_squashed() if hasattr(on_squashed, '__call__') else on_squashed

            return wrapper

        return decor


# decorator function
def stringable(cls):
    """
    Adds a __str__ method to a class that ties all the items in __dict__ together
    into a nicely formatted string
    """
    def __str__(self):
        items = ['{}={}'.format(k, v) for (k, v) in self.__dict__.items()]
        items_string = ', '.join(items)
        return '{}[{}]'.format(self.__class__.__name__, items_string)

    setattr(cls, '__str__', __str__)
    setattr(cls, '__repr__', __str__)
    return cls



def equatable(cls):
    """
    Adds an __eq__ method that compares all the values in __dict__ in 'self'
    and the other item. Only works on classes of identical type
    """
    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        pairs = zip(self.__dict__.values(), other.__dict__.values())
        return all([i[0] == i[1] for i in pairs])

    setattr(cls, '__eq__', __eq__)
    setattr(cls, '__hash__', None)
    return cls


def hashable(cls):
    """
    Implicitly calls 'equatable' for the class and also generates a __hash__
    method for the class so it can be used in a dictionary
    """
    cls = equatable(cls)

    def hasher(a, i):
        return ((a << 8) | (a >> 56)) ^ hash(i)

    def __hash__(self):
        for (name, value) in self.__dict__.items():
            if type(value).__hash__ is None:
                fmt_str = "value of type {} can't be hashed because the field {}={} (type={}) is not hashable"
                str_format = fmt_str.format(repr(cls.__name__), repr(name), repr(value), repr(type(value).__name__))
                raise TypeError(str_format)
        return super(cls, self).__hash__() ^ reduce(hasher, self.__dict__.values(), 0)

    setattr(cls, '__hash__', __hash__)
    return cls



# decorator function
def dataclass(cls):
    """
    Wraps the built-in dataclass.dataclass annotation in order to also give the
    class a __str__ method
    """
    cls = dataclasses.dataclass(cls, init=True, repr=True, eq=True, frozen=True)
    cls = stringable(cls)
    return cls
