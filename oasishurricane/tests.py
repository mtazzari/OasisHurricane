#!/usr/bin/env python
# coding=utf-8

# mean loss for florida_mean and Gulf_mean =0
# gethurricaneloss 10 0.0001 0.001 20 0.0001 0.0001 -n 1000
# should be 0

import numpy as np

SEED = 123456789


def test_simulate_zero_losses():
    from .model import simulate

    res = simulate(florida_landfall_rate=10, florida_mean=-10, florida_stddev=1e-14,
             gulf_landfall_rate=10, gulf_mean=-10, gulf_stddev=1e-14,
             num_monte_carlo_samples=10000,
             rng_seed=SEED)

    np.testing.assert_allclose(res, 0., atol=1e-3, rtol=0)
