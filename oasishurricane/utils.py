#!/usr/bin/env python
# coding=utf-8

import functools
import time
import os


# TODO: pass named arguments to the core functions to improve formatting of the logfile
def timer(func):
    """
    Decorator that times the decorated function.
    If TIMEIT_LOGFILE is defined in the shell, it prints the timing to file, else to stdout.

    :param func: decorated function
    :return: the evaluated function
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic

        if kwargs.get("timeit_discard", False):
            return value

        # timeit_msg = f"Elapsed time: {elapsed_time:0.4f} seconds"
        timeit_msg = "\t".join([f"{arg:>10.6f}" for arg in args])
        timeit_msg += "\t" + f"{elapsed_time:5.4f}"
        timeit_msg += " \n"
        if 'TIMEIT_LOGFILE' in os.environ:
            with open(os.environ['TIMEIT_LOGFILE'], "a") as f:
                f.write(timeit_msg)
        else:
            print(timeit_msg)

        return value

    return wrapper_timer
