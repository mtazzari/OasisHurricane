#!/usr/bin/env python
# coding=utf-8

import functools
import time
import os
import logging
import gc
import numpy as np

logger = logging.getLogger("timing")


# TODO: pass named arguments to the core functions to improve formatting of the logfile
def timer(cycles=3):
    """
    Decorator that times the decorated function.
    If TIMEIT_LOGFILE is defined in the shell, it prints the timing to file, else to stdout.

    :param func: decorated function
    :return: the evaluated function

    """

    def inner_function(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            timeit = bool(os.getenv("TIMEIT"))

            if not timeit:
                value = func(*args, **kwargs)
                return value

            logger.info(f"Timings are computed by running {cycles} times the function.")

            # momentarily disable garbage collector (if enabled)
            gcold = gc.isenabled()
            gc.disable()

            try:
                # use a precise timer for performance benchmark
                _timer = time.perf_counter

                values = []
                times = []
                for _i in range(cycles):
                    t0 = _timer()
                    values.append(func(*args, **kwargs))
                    t1 = _timer()
                    times.append(t1 - t0)

                value = np.mean(values)

                # evaluate the best execution time
                # according to the docstring of `timeit.Timer.repeat`, min(times) is the best number
                # to use as a representation of the best performance. Higher time values are likely
                # affected by variability, and interference with other processes.

                # Note on numba jit-compiled functions:
                # jit compilation takes time, which should be discarded when timing the performance.
                # Since the best execution time is the `min` of all the execution times, the jit
                # compilation time is naturally excluded from the benchmark.
                best_time = np.min(times)

            finally:
                # re-enable garbage collector if it was enabled
                if gcold:
                    gc.enable()

            timeit_msg = " ".join([f"{arg:10.6f}" for arg in args])
            timeit_msg += " " + f"{cycles:10}"
            timeit_msg += " " + f"{best_time:10.6f}"
            timeit_msg += " " + f"{value:10.6f}"

            if 'TIMEIT_LOGFILE' in os.environ:
                with open(os.environ['TIMEIT_LOGFILE'], "a") as f:
                    f.write(timeit_msg + " \n")
            else:
                logger.info("timeit: " + timeit_msg)

            return value

        return wrapper

    return inner_function
