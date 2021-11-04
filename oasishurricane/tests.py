#!/usr/bin/env python
# coding=utf-8

# mean loss for florida_mean and Gulf_mean =0
# gethurricaneloss 10 0.0001 0.001 20 0.0001 0.0001 -n 1000
# should be 0

import numpy as np
import pytest

from .cli import main
from .model import SIMULATORS

# fix random number generator seed
SEED = 123456789

# mock CLI arguments
args = [
    {  # reference test
        "florida_landfall_rate": 10.,
        "florida_mean": 2,
        "florida_stddev": 0.6,
        "gulf_landfall_rate": 20.,
        "gulf_mean": 0.3,
        "gulf_stddev": 0.1,
        "num_monte_carlo_samples": 20000,
        "simulator_id": 0,
        "rng_seed": SEED,
    },
    {  # test larger rates
        "florida_landfall_rate": 30.,
        "florida_mean": 2,
        "florida_stddev": 0.6,
        "gulf_landfall_rate": 34.,
        "gulf_mean": 0.3,
        "gulf_stddev": 0.1,
        "num_monte_carlo_samples": 20000,
        "simulator_id": 0,
        "rng_seed": SEED,
    },
    {  # test larger losses (requires deeper MC sampling)
        "florida_landfall_rate": 8.,
        "florida_mean": 10.2333,
        "florida_stddev": 2.297,
        "gulf_landfall_rate": 15.,
        "gulf_mean": 4.33232,
        "gulf_stddev": 1.2344,
        "num_monte_carlo_samples": 900000,
        "simulator_id": 0,
        "rng_seed": SEED,
    }
]


@pytest.mark.parametrize("test_args",
                         [(args_) for args_ in args],
                         ids=["{}".format(i) for i in range(len(args))])
def test_simulators_consistency(test_args, rtol=0.01, atol=0.001):
    """
    Test if simulators return mean losses that agree within a relative tolerance `rtol`
    and an absolute tolerance `atol`
    :param test_args: [dict] test arguments, same format as in the CLI (i.e., before validation)
    :param rtol: relative tolerance of the checks
    :param atol: absolute tolerance of the checks

    """
    Nsimulators = len(SIMULATORS.keys())

    # iterate through simulators and check for consistency
    mean_loss = []
    for id in SIMULATORS.keys():
        test_args["simulator_id"] = id
        mean_loss.append(main(test_args))

    # compare results w.r.t. the python-only version, as a point-of-truth
    np.testing.assert_allclose(mean_loss, np.repeat(mean_loss[0], Nsimulators), atol=atol,
                               rtol=rtol)


def test_Simulator_not_implemented():
    pass

# test a not implemented simulator_id
