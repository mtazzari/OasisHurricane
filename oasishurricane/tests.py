#!/usr/bin/env python
# coding=utf-8

# mean loss for florida_mean and Gulf_mean =0
# gethurricaneloss 10 0.0001 0.001 20 0.0001 0.0001 -n 1000
# should be 0

import copy
import numpy as np
import pytest
from pytest import raises

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
        "timeit": False,
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
        "timeit": False,
    },
    {  # test larger losses (requires deeper MC sampling)
        "florida_landfall_rate": 8.,
        "florida_mean": 10.2333,
        "florida_stddev": 1.8345,
        "gulf_landfall_rate": 15.,
        "gulf_mean": 4.33232,
        "gulf_stddev": 1.1344,
        "num_monte_carlo_samples": 1000000,
        "simulator_id": 0,
        "rng_seed": SEED,
        "timeit": False,
    }
]

@pytest.mark.parametrize("test_args",
                         [(args_) for args_ in args],
                         ids=["{}".format(i) for i in range(len(args))])
def test_simulators_accuracy(test_args, rtol=0.01, atol=0.001):
    """
    Test if simulators return mean losses that agree within a relative tolerance `rtol`
    and an absolute tolerance `atol`.
    :param test_args: [dict] test arguments, same format as in the CLI (i.e., before validation)
    :param rtol: relative tolerance of the checks
    :param atol: absolute tolerance of the checks

    """
    Nsimulators = len(SIMULATORS.keys())

    # iterate through simulators and check for consistency
    mean_loss = []
    for id_ in SIMULATORS.keys():
        test_args["simulator_id"] = id_
        mean_loss.append(main(test_args))

    # compare results w.r.t. the python-only version, as a point-of-truth
    np.testing.assert_allclose(mean_loss, np.repeat(mean_loss[0], Nsimulators), atol=atol,
                               rtol=rtol)


@pytest.mark.parametrize("test_args",
                         [(args_) for args_ in args],
                         ids=["{}".format(i) for i in range(len(args))])
def test_simulator_selection(test_args):
    """Test exceptions if the chosen simulator_id doesn't exist. """
    max_simulator_id = int(np.max(list(SIMULATORS.keys())))

    # if simulator_id > max available should return NotImplementedError
    test_args["simulator_id"] = max_simulator_id + 1
    with raises(NotImplementedError,
                match=f"simulator_id={test_args['simulator_id']} is not implemented"):
        main(test_args)

    # if simulator_id < 0 the validation should throw a ValueError
    test_args["simulator_id"] = -1
    with raises(ValueError, match="Expect simulator_id>=0, got -1"):
        main(test_args)

@pytest.mark.parametrize("test_args",
                         [(args_) for args_ in args],
                         ids=["{}".format(i) for i in range(len(args))])
def test_input_parameter_values(test_args):
    """Test exceptions if input data has forbidden values. """

    numerical_args = [
        "florida_landfall_rate",
        "florida_mean",
        "florida_stddev",
        "gulf_landfall_rate",
        "gulf_mean",
        "gulf_stddev",
    ]

    for numerical_arg in numerical_args:
        # turn negative each numerical argument; it should raise a Value Error
        # take a deepcopy of test_args otherwise they are overwritten
        test_args_ = copy.deepcopy(test_args)
        test_args_[numerical_arg] *= -1
        with raises(ValueError,
                    match=f"Expect {numerical_arg}>0, got {test_args_[numerical_arg]}"):
            main(test_args_)

