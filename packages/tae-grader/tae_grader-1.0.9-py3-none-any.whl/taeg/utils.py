"""
Utilities for Tae-Grader
"""

import os
import sys
import pathlib
import random
import string

from contextlib import contextmanager, redirect_stdout, AbstractContextManager
from IPython import get_ipython
import builtins

from io import StringIO
from unittest.mock import patch
from datetime import datetime
from pytz import timezone
import pytz
import inspect

@contextmanager
def block_print():
    """
    Context manager that disables printing to stdout.
    """
    with open(os.devnull, "w") as f, redirect_stdout(f):
        yield

def flush_inline_matplotlib_plots():
    """
    Flush matplotlib plots immediately, rather than asynchronously
    
    Basically, the inline backend only shows the plot after the entire cell executes, which means we 
    can't easily use a context manager to suppress displaying it. See https://github.com/jupyter-widgets/ipywidgets/issues/1181/ 
    and https://github.com/ipython/ipython/issues/10376 for more details. This function displays flushes 
    any pending matplotlib plots if we are using the inline backend. Stolen from 
    https://github.com/jupyter-widgets/ipywidgets/blob/4cc15e66d5e9e69dac8fc20d1eb1d7db825d7aa2/ipywidgets/widgets/interaction.py#L35
    """
    if 'matplotlib' not in sys.modules:
        # matplotlib hasn't been imported, nothing to do.
        return

    try:
        import matplotlib as mpl
        from ipykernel.pylab.backend_inline import flush_figures
    except ImportError:
        return
    # except KeyError:
    #     return

    if mpl.get_backend() == 'module://ipykernel.pylab.backend_inline':
        flush_figures()

@contextmanager
def hide_outputs():
    """
    Context manager for hiding outputs from ``display()`` calls. IPython handles matplotlib outputs 
    specially, so those are supressed too.
    """
    ipy = get_ipython()
    if ipy is None:
        # Not running inside ipython!
        yield
        return
    old_formatters = ipy.display_formatter.formatters
    ipy.display_formatter.formatters = {}
    try:
        yield
    finally:
        # flush_inline_matplotlib_plots()
        ipy.display_formatter.formatters = old_formatters

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Used to generate a dynamic variable name for grading functions

    This function generates a random name using the given length and character set.
    
    Args:
        size (``int``): length of output name
        chars (``str``, optional): set of characters used to create function name
    
    Returns:
        ``str``: randomized string name for grading function
    """
    return ''.join(random.choice(chars) for _ in range(size))

def get_variable_type(obj):
    """Returns the fully-qualified type string of an object ``obj``

    Args:
        obj (object): the object in question

    Returns:
        ``str``: the fully-qualified type string
    """
    return type(obj).__module__ + "." + type(obj).__name__

def get_relpath(src, dst):
    """
    Returns the relative path from ``src`` to ``dst``

    Args:
        src (``pathlib.Path``): the source directory
        dst (``pathlib.Path``): the destination directory

    Returns:
        ``pathlib.Path``: the relative path
    """
    # osrc = src
    ups = 0
    while True:
        try:
            dst.relative_to(src)
            break
        except ValueError:
            src = src.parent
            ups += 1
    return pathlib.Path(("../" * ups) / dst.relative_to(src))

def get_source(cell):
    """
    Returns the source code of a cell in a way that works for both nbformat and JSON
    
    Args:
        cell (``nbformat.NotebookNode``): notebook cell
    
    Returns:
        ``list`` of ``str``: each line of the cell source stripped of ending line breaks
    """
    source = cell.source
    if isinstance(source, str):
        return source.split('\n')
    elif isinstance(source, list):
        return [line.strip('\n') for line in source]
    raise ValueError(f'unknown source type: {type(source)}')

def run_assignment(target, user_input):
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        with patch('builtins.input', side_effect=user_input) as mock_input:
            target()
    result = mock_stdout.getvalue().strip()
    return result

pac_timezone = timezone('US/Pacific')
def pac_now():
    date = datetime.now(tz=pytz.utc)
    return date.astimezone(pac_timezone).replace(tzinfo=None)


class redirect_input(AbstractContextManager):

    _stream = "input"

    def __init__(self, new_target):
        self._new_target = lambda x="": new_target.readline()
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(builtins, self._stream))
        setattr(builtins, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(builtins, self._stream, self._old_targets.pop())


def run_main(user_input, target=None):
    if not target:
        target = inspect.currentframe().f_back.f_globals['main']

    sout = StringIO()
    with redirect_input(StringIO(user_input)):
        with redirect_stdout(sout):
            target()
    result = sout.getvalue().strip()
    return result
