#!/usr/bin/env python
# coding=utf-8

import sys
import argparse
import numpy as np
import copy
import logging
import logging.config

from .logs import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("cli")

from .model import Simulator


def parse_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser()

    # parser = parser.add_argument_group('parser arguments')

    parser.add_argument("florida_landfall_rate",
                        action="store",
                        help="[float] florida_landfall_rate",
                        type=float)
    parser.add_argument("florida_mean",
                        action="store",
                        help="[float] florida_mean",
                        type=float)
    parser.add_argument("florida_stddev",
                        action="store",
                        help="[float] florida_stddev",
                        type=float)
    parser.add_argument("gulf_landfall_rate",
                        action="store",
                        help="[float] gulf_landfall_rate",
                        type=float)
    parser.add_argument("gulf_mean",
                        action="store",
                        help="[float] gulf_mean",
                        type=float)
    parser.add_argument("gulf_stddev",
                        action="store",
                        help="[float] gulf_stddev",
                        type=float)
    parser.add_argument("-n", "--num_monte_carlo_samples",
                        action="store",
                        help="[int] num_monte_carlo_samples (default=10)",
                        type=int,
                        dest="num_monte_carlo_samples",
                        default=10)
    parser.add_argument("-s", "--simulator",
                        action="store",
                        help="",
                        type=int,
                        dest="simulator_id",
                        default=0)

    args = vars(parser.parse_args())  # convert to dict for ease of use

    return args


def validate_args(args):
    """

    :param args:
    :return:
    """
    assert args['florida_mean'] > 0, \
        f"Expect florida_mean>0, got {args['florida_mean']}"

    assert args['gulf_mean'] > 0, \
        f"Expect gulf_mean>0, got {args['gulf_mean']}"

    assert args['simulator_id'] >= 0, \
        f"Expect simulator_id>=0, got {args['simulator_id']}"

    # deepcopy ensures mutable items are copied too
    validated_args = copy.deepcopy(args)

    # validate parameters
    # compute natural log of the LogNormal means
    validated_args.update({
        "florida_mean": np.log(args['florida_mean']),
        "gulf_mean": np.log(args['gulf_mean']),
    })

    logger.info("Validated parameters: ")
    for arg_k, arg_v in validated_args.items():
        logger.info(f"{arg_k:>30s} = {arg_v:>10.5f}")

    return validated_args


def main():
    args = parse_args()

    validated_args = validate_args(args)

    sim = Simulator(validated_args["simulator_id"])
    sim.simulate(**validated_args)

    sys.exit(0)


if __name__ == "__main__":
    main()
