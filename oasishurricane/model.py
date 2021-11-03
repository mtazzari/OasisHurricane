#!/usr/bin/env python
# coding=utf-8

# TODO: logging
import numpy as np


def get_rng(seed=None):
    """
    Get a new random number generator.s

    :param seed:
    :return:
    """
    return np.random.default_rng(seed)


def simulate(florida_landfall_rate, florida_mean, florida_stddev,
             gulf_landfall_rate, gulf_mean, gulf_stddev, num_monte_carlo_samples,
             **kwargs):
    """
    Simulate

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
    rng = get_rng(rng_seed)

    tot_loss = 0
    Nyears = 100

    for i in range(num_monte_carlo_samples):
        year_loss = 0

        fl_events = rng.poisson(lam=florida_landfall_rate, size=1)
        for j in range(fl_events):
            year_loss += rng.lognormal(florida_mean, florida_stddev)

        gulf_events = rng.poisson(lam=gulf_landfall_rate, size=1)
        for k in range(gulf_events):
            year_loss += rng.lognormal(gulf_mean, gulf_stddev)

        tot_loss += year_loss

    mean_loss = tot_loss / Nyears

    return mean_loss
