#!/usr/bin/env python
# coding=utf-8

import numpy as np
import logging
import time
import datetime
from alive_progress import alive_bar

logger = logging.getLogger("model")

def get_rng(seed=None):
    """
    Get a new random number generator.s

    :param seed:
    :return:
    """
    return np.random.default_rng(seed)


def simulate_pbar(florida_landfall_rate, florida_mean, florida_stddev,
             gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
             **kwargs):
    """
    Simulate losses

    :param florida_landfall_rate:
    :param florida_mean:
    :param florida_stddev:
    :param gulf_landfall_rate:
    :param gulf_mean:
    :param gulf_stddev:
    :param num_monte_carlo_samples:

    :return: Mean annual losses

    """
    rng_seed = kwargs.get('rng_seed', None)

    # get a new random number generator
    logger.info(f"Setting the random number generator with seed:{rng_seed}")
    rng = get_rng(rng_seed)

    logger.info(f"Starting main loop over desired {num_monte_carlo_samples} Monte Carlo samples ")
    tot_loss = 0

    t0 = time.time()
    with alive_bar(num_monte_carlo_samples) as bar:
        for i in range(num_monte_carlo_samples):
            log_prefix = f"year {i:0>10} "

            fl_events = rng.poisson(lam=florida_landfall_rate, size=1)[0]
            logger.debug(log_prefix + f"Florida events: {fl_events:0>3}")
            fl_loss = 0
            for j in range(fl_events):
                fl_loss += rng.lognormal(florida_mean, florida_stddev)
                logger.debug(log_prefix + f"Florida loss: {fl_loss:05.3f}")

            gulf_events = rng.poisson(lam=gulf_landfall_rate, size=1)[0]
            logger.debug(log_prefix + f"Gulf events: {gulf_events:5.3f}")

            gulf_loss = 0
            for k in range(gulf_events):
                gulf_loss += rng.lognormal(gulf_mean, gulf_stddev)
                logger.debug(log_prefix + f"Gulf loss: {gulf_loss:05.3f}")

            year_loss = fl_loss + gulf_loss

            tot_loss += year_loss
            logger.debug(log_prefix + f"TOTAL LOSS: {tot_loss:05.3f}")

            bar()

    t1 = time.time()
    logger.info(f"End of main loop. Elapsed time: {datetime.timedelta(seconds=t1-t0)} (h:m:s)")
    mean_loss = tot_loss / num_monte_carlo_samples

    logger.info(f"MEAN LOSS: {mean_loss}")

    return mean_loss


def simulate(florida_landfall_rate, florida_mean, florida_stddev,
             gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
             **kwargs):
    """
    Simulate losses
    WITHOUT PROGRESSBAR

    :param florida_landfall_rate:
    :param florida_mean:
    :param florida_stddev:
    :param gulf_landfall_rate:
    :param gulf_mean:
    :param gulf_stddev:
    :param num_monte_carlo_samples:

    :return: Mean annual losses

    """
    rng_seed = kwargs.get('rng_seed', None)

    # get a new random number generator
    logger.info(f"Setting the random number generator with seed:{rng_seed}")
    rng = get_rng(rng_seed)

    logger.info(f"Starting main loop over desired {num_monte_carlo_samples} Monte Carlo samples ")
    tot_loss = 0

    t0 = time.time()
    for i in range(num_monte_carlo_samples):
        log_prefix = f"year {i:0>10} "

        fl_events = rng.poisson(lam=florida_landfall_rate, size=1)[0]
        logger.debug(log_prefix + f"Florida events: {fl_events:0>3}")
        fl_loss = 0
        for j in range(fl_events):
            fl_loss += rng.lognormal(florida_mean, florida_stddev)
            logger.debug(log_prefix + f"Florida loss: {fl_loss:05.3f}")

        gulf_events = rng.poisson(lam=gulf_landfall_rate, size=1)[0]
        logger.debug(log_prefix + f"Gulf events: {gulf_events:5.3f}")

        gulf_loss = 0
        for k in range(gulf_events):
            gulf_loss += rng.lognormal(gulf_mean, gulf_stddev)
            logger.debug(log_prefix + f"Gulf loss: {gulf_loss:05.3f}")

        year_loss = fl_loss + gulf_loss

        tot_loss += year_loss
        logger.debug(log_prefix + f"TOTAL LOSS: {tot_loss:05.3f}")


    t1 = time.time()
    logger.info(f"End of main loop. Elapsed time: {datetime.timedelta(seconds=t1-t0)} (h:m:s)")
    mean_loss = tot_loss / num_monte_carlo_samples

    logger.info(f"MEAN LOSS: {mean_loss}")

    return mean_loss


class Simulator(object):
    def __init__(self, simulator_id):
        if simulator_id == 0:
            self.simulate = simulate_pbar
        elif simulator_id == 1:
            self.simulate = simulate
        else:
            raise NotImplementedError(f"simulator_id={simulator_id} is not implemented")

