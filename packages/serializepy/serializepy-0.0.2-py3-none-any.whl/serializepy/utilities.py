from collections import deque
import inspect
import ast
import textwrap

from types import FunctionType, ModuleType
from typing import List, Type, cast

from pydoc import locate

# https://raw.githubusercontent.com/jepperaskdk/pydoctest/main/pydoctest/utilities.py


def get_type_from_module(type_string: str, module: ModuleType) -> Type:
    """Attempts to return the type, given the type_string and module it is extracted from.

    Args:
        type_string (str): String version of a string, e.g. "Optional[str]"
        module (ModuleType): The module the type_string is extracted from.

    Raises:
        Exception: If unable to find the type, we throw an Exception.

    Returns:
        LocateResult: A LocateResult wrapping the type when found.
    """
    # First let pydoc attempt to locate the type
    located_type: Type = cast(Type, locate(type_string))
    if located_type:
        return located_type

    # Try to eval it.
    try:
        # We pass the globals of module to eval, so lookups should work.
        t = eval(type_string, vars(module))
        return t
    except NameError:
        pass

    # Search imported modules in module
    # Inspired by this: https://stackoverflow.com/a/11781721/3717691
    SEARCHES_LEFT = 1_000
    q = deque([module])
    while q and SEARCHES_LEFT > 0:
        m = q.popleft()
        try:
            t = eval(type_string, vars(m))
            return t
        except NameError:
            pass

        for name, item in inspect.getmembers(m):
            if inspect.ismodule(item):
                q.append(item)
            elif inspect.isclass(item) and item.__module__ != module.__name__:
                mod = inspect.getmodule(item)
                if mod:
                    q.append(mod)
        SEARCHES_LEFT -= 1

    # TODO: We should make this configurable in config
    raise Exception(f"Was unable to detect the type of: {type_string} from module: {module.__file__}.\nIf you believe this is a bug, please file it here: https://github.com/jepperaskdk/pydoctest/issues")