#!/usr/bin/env python
# coding=utf-8

import functools
import time
import os
import logging

logger = logging.getLogger("timing")


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

        timeit = kwargs.get("timeit", False)

        if not timeit:
            return value

        # timeit_msg = f"Elapsed time: {elapsed_time:0.4f} seconds"
        timeit_msg = " ".join([f"{arg:>10.6f}" for arg in args])
        timeit_msg += " " + f"{elapsed_time:10.6f}"
        timeit_msg += " \n"

        if 'TIMEIT_LOGFILE' in os.environ:
            with open(os.environ['TIMEIT_LOGFILE'], "a") as f:
                f.write(timeit_msg)
        else:
            logger.info("timeit: " + timeit_msg)

        return value

    return wrapper_timer
