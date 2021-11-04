#!/usr/bin/env python
# coding=utf-8

import numpy as np
import logging
import time
import datetime
from numba import jit, njit, prange

logger = logging.getLogger("model")

from .utils import timer


def get_rng(seed=None):
    """
    Get a new random number generator.s

    :param seed:
    :return:
    """
    return np.random.default_rng(seed)


@timer
def mean_loss_py(florida_landfall_rate, florida_mean, florida_stddev,
                 gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
                 timeit_discard=False):
    """
    Compute mean economic loss in Pure Python.

    :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
    :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
    :param florida_stddev:  [float] std deviation of the economic loss of landfalling hurricane in Florida.
    :param gulf_landfall_rate:  [float] annual rate of landfalling hurricanes in Gulf states.
    :param gulf_mean:  [float] mean of the economic loss of landfalling hurricane in Gulf states.
    :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
    :param num_monte_carlo_samples: [int] Number of monte carlo samples, i.e. years.
    :param timeit_discard: [bool] (optional) If True, @timer does not record the timing. Only used by @timer.

    :return: [float] Mean annual losses.

    """
    tot_loss = 0

    for i in range(num_monte_carlo_samples):
        log_prefix = f"year {i:0>10} "

        fl_events = np.random.poisson(lam=florida_landfall_rate, size=1)[0]
        logger.debug(log_prefix + f"Florida events: {fl_events:0>3}")
        fl_loss = 0
        for j in range(fl_events):
            fl_loss += np.random.lognormal(florida_mean, florida_stddev)
            logger.debug(log_prefix + f"Florida loss: {fl_loss:05.3f}")

        gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=1)[0]
        logger.debug(log_prefix + f"Gulf events: {gulf_events:5.3f}")

        gulf_loss = 0
        for k in range(gulf_events):
            gulf_loss += np.random.lognormal(gulf_mean, gulf_stddev)
            logger.debug(log_prefix + f"Gulf loss: {gulf_loss:05.3f}")

        year_loss = fl_loss + gulf_loss

        tot_loss += year_loss

    return tot_loss / num_monte_carlo_samples


@timer
@jit(nopython=True)
def mean_loss_jit(florida_landfall_rate, florida_mean, florida_stddev,
                  gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
                  timeit_discard=False):
    """
    Compute mean economic loss with explicit loops and jit-compilation with numba.

    :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
    :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
    :param florida_stddev:  [float] std deviation of the economic loss of landfalling hurricane in Florida.
    :param gulf_landfall_rate:  [float] annual rate of landfalling hurricanes in Gulf states.
    :param gulf_mean:  [float] mean of the economic loss of landfalling hurricane in Gulf states.
    :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
    :param num_monte_carlo_samples: [int] Number of monte carlo samples, i.e. years.
    :param timeit_discard: [bool] (optional) If True, @timer does not record the timing. Only used by @timer.

    :return: [float] Mean annual losses.

    """
    fl_events = np.random.poisson(lam=florida_landfall_rate, size=num_monte_carlo_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_monte_carlo_samples)

    tot_loss = 0

    for i in range(num_monte_carlo_samples):

        fl_loss = 0
        for j in range(fl_events[i]):
            fl_loss += np.random.lognormal(florida_mean, florida_stddev)

        gulf_loss = 0
        for k in range(gulf_events[i]):
            gulf_loss += np.random.lognormal(gulf_mean, gulf_stddev)

        year_loss = fl_loss + gulf_loss

        tot_loss += year_loss

    return tot_loss / num_monte_carlo_samples


@timer
@njit(parallel=True)
def mean_loss_jit_parallel(florida_landfall_rate, florida_mean, florida_stddev,
                           gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
                           timeit_discard=False):
    """
    Compute mean economic loss with explicit loops, jit-compilation, and auto-parallelization with numba.

    :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
    :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
    :param florida_stddev:  [float] std deviation of the economic loss of landfalling hurricane in Florida.
    :param gulf_landfall_rate:  [float] annual rate of landfalling hurricanes in Gulf states.
    :param gulf_mean:  [float] mean of the economic loss of landfalling hurricane in Gulf states.
    :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
    :param num_monte_carlo_samples: [int] Number of monte carlo samples, i.e. years.
    :param timeit_discard: [bool] (optional) If True, @timer does not record/print the timing. Only used by @timer.

    :return: [float] Mean annual losses.

    """
    fl_events = np.random.poisson(lam=florida_landfall_rate, size=num_monte_carlo_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_monte_carlo_samples)

    tot_loss = 0
    for i in prange(num_monte_carlo_samples):
        fl_loss = 0
        for j in range(fl_events[i]):
            fl_loss += np.random.lognormal(florida_mean, florida_stddev)

        gulf_loss = 0
        for k in range(gulf_events[i]):
            gulf_loss += np.random.lognormal(gulf_mean, gulf_stddev)

        year_loss = fl_loss + gulf_loss

        tot_loss += year_loss

    return tot_loss / num_monte_carlo_samples


@timer
@jit(nopython=True)
def mean_loss_noloops_jit(florida_landfall_rate, florida_mean, florida_stddev,
                          gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
                          timeit_discard=False):
    """
    Compute mean economic loss with numpy vectorization, no explicit loops, and jit-compilation with numba.

    :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
    :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
    :param florida_stddev:  [float] std deviation of the economic loss of landfalling hurricane in Florida.
    :param gulf_landfall_rate:  [float] annual rate of landfalling hurricanes in Gulf states.
    :param gulf_mean:  [float] mean of the economic loss of landfalling hurricane in Gulf states.
    :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
    :param num_monte_carlo_samples: [int] Number of monte carlo samples, i.e. years.
    :param timeit_discard: [bool] (optional) If True, @timer does not record the timing. Only used by @timer.

    :return: [float] Mean annual losses.

    """
    fl_events = np.random.poisson(lam=florida_landfall_rate, size=num_monte_carlo_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_monte_carlo_samples)
    Nfl_events = np.sum(fl_events)
    Ngulf_events = np.sum(gulf_events)

    fl_loss = np.random.lognormal(florida_mean, florida_stddev, size=(Nfl_events,))

    gulf_loss = np.random.lognormal(gulf_mean, gulf_stddev, size=(Ngulf_events,))

    tot_loss = np.sum(fl_loss) + np.sum(gulf_loss)

    return tot_loss / num_monte_carlo_samples


@timer
def mean_loss_noloops_py(florida_landfall_rate, florida_mean, florida_stddev,
                         gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
                         timeit_discard=False):
    """
    Compute mean economic loss in Pure Python, using numpy vectorization and no explicit loops.

    :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
    :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
    :param florida_stddev:  [float] std deviation of the economic loss of landfalling hurricane in Florida.
    :param gulf_landfall_rate:  [float] annual rate of landfalling hurricanes in Gulf states.
    :param gulf_mean:  [float] mean of the economic loss of landfalling hurricane in Gulf states.
    :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
    :param num_monte_carlo_samples: [int] Number of monte carlo samples, i.e. years.
    :param timeit_discard: [bool] (optional) If True, @timer does not record the timing. Only used by @timer.

    :return: [float] Mean annual losses.

    """

    fl_events = np.random.poisson(lam=florida_landfall_rate, size=num_monte_carlo_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_monte_carlo_samples)
    Nfl_events = np.sum(fl_events)
    Ngulf_events = np.sum(gulf_events)

    fl_loss = np.random.lognormal(florida_mean, florida_stddev, size=(Nfl_events,))

    gulf_loss = np.random.lognormal(gulf_mean, gulf_stddev, size=(Ngulf_events,))

    tot_loss = np.sum(fl_loss) + np.sum(gulf_loss)

    return tot_loss / num_monte_carlo_samples


SIMULATORS = {
    0: {
        'func': mean_loss_py,
        'desc': "python"
    },
    1: {
        'func': mean_loss_jit,
        'desc': "jit"
    },
    2: {
        'func': mean_loss_jit_parallel,
        'desc': "jit-parallel"
    },
    3: {
        'func': mean_loss_noloops_jit,
        'desc': "jit-noloops"
    },
    4: {
        'func': mean_loss_noloops_py,
        'desc': "python-noloops"
    },
}


class Simulator(object):
    def __init__(self, simulator_id):
        """Init the Simulator object by setting the simulator. """
        try:
            self._simulate_core = SIMULATORS[simulator_id]['func']
            self._desc = SIMULATORS[simulator_id]['desc']

        except KeyError:

            raise NotImplementedError(f"simulator_id={simulator_id} is not implemented")

        finally:
            logger.info(f"Simulator set to use: {self._desc}")

    def __str__(self):
        """Description of the simulator engine used."""
        return f"{self._desc:16s}"

    def simulate(self, florida_landfall_rate, florida_mean, florida_stddev,
                 gulf_landfall_rate, gulf_mean, gulf_stddev,
                 num_monte_carlo_samples, **kwargs):
        """
        Simulate losses due to hurricanes making landfall in Florida and in Gulf States.

        The simulation assumes a Poisson distribution for the rate of landfalling hurricanes,
        and a LogNormal distribution for the economic loss.

        The `mean` provided in input for the economic loss is the mean of the normal distribution
        underlying the LogNormal, namely: the expected value E[x] = mean (not exp^mean).
        This makes it easier to interpret the results.

        :param florida_landfall_rate: [float] annual rate of landfalling hurricanes in Florida.
        :param florida_mean: [float] mean of the economic loss of landfalling hurricane in Florida.
        :param florida_stddev: [float] std deviation of the economic loss of landfalling hurricane in Florida.
        :param gulf_landfall_rate: [float] annual rate of landfalling hurricanes in Gulf states.
        :param gulf_mean: [float] mean of the economic loss of landfalling hurricane in Gulf states.
        :param gulf_stddev: [float] std deviation of the economic loss of landfalling hurricane in Gulf states.
        :param num_monte_carlo_samples: [int] number of monte carlo samples, i.e. years.
        :param rng_seed: [int] (optional) Seed of the random number generator.

        :return: [float] Mean annual losses.

        """
        rng_seed = kwargs.get('rng_seed', None)

        # set the random number generator seed
        logger.info(f"Setting the random number generator with seed:{rng_seed}")
        np.random.seed(rng_seed)

        logger.info(
            f"Starting main loop over desired {num_monte_carlo_samples} Monte Carlo samples ")

        # dummy call to jit-compile it
        _ = self._simulate_core(1, 1e-10, 1e-10, 1, 1e-10, 1e-10, 1, timeit_discard=True)

        t0 = time.time()
        mean_loss = self._simulate_core(florida_landfall_rate, florida_mean, florida_stddev,
                                        gulf_landfall_rate, gulf_mean, gulf_stddev,
                                        num_monte_carlo_samples,
                                        )

        t1 = time.time()
        logger.info(
            f"End of main loop. Elapsed time: {datetime.timedelta(seconds=t1 - t0)} (h:m:s)")

        logger.info(f"MEAN LOSS: {mean_loss}")

        return mean_loss
