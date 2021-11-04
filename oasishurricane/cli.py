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

from .model import Simulator, SIMULATORS


def parse_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter  # for multi-line help text
    )

    # parser = parser.add_argument_group('parser arguments')

    parser.add_argument("florida_landfall_rate",
                        action="store",
                        help="[float] annual rate of landfalling hurricanes in Florida.",
                        type=float)
    parser.add_argument("florida_mean",
                        action="store",
                        help="[float] mean of the economic loss of landfalling hurricane in Florida.",
                        type=float)
    parser.add_arguent("florida_stddev",
                        action="store",
                        help="[float] std deviation of the economic loss of landfalling hurricane in Florida.",
                        type=float)
    parser.add_argument("gulf_landfall_rate",
                        action="store",
                        help="[float] annual rate of landfalling hurricanes in Gulf states.",
                        type=float)
    parser.add_argument("gulf_mean",
                        action="store",
                        help="[float] mean of the economic loss of landfalling hurricane in Gulf states.",
                        type=float)
    parser.add_argument("gulf_stddev",
                        action="store",
                        help="[float] std deviation of the economic loss of landfalling hurricane in Gulf states.",
                        type=float)
    parser.add_argument("-n", "--num_monte_carlo_samples",
                        action="store",
                        help="[int] number of monte carlo samples, i.e. years. (default=10)",
                        type=int,
                        dest="num_monte_carlo_samples",
                        default=10)
    parser.add_argument("-s", "--simulator",
                        action="store",
                        help="[int] simulator id. Implemented simulators: (id:name) \n" + \
                             "\n".join([f"{k}: {v['desc']}" for k, v in SIMULATORS.items()]),
                        type=int,
                        dest="simulator_id",
                        default=0)

    args = vars(parser.parse_args())  # convert to dict for ease of use

    return args


def validate_args(args):
    """
    Validate parameters (args) passed in input through the CLI.
    If necessary, perform transformations of parameter values to the simulation space.

    :param args: [dict] Parsed arguments.

    :return: [dict] Validated arguments.

    """
    # note: input data types are already checked by the parser object.

    # here we check input values
    if args['florida_landfall_rate'] <= 0:
        raise ValueError(f"Expect florida_landfall_rate>0, got {args['florida_landfall_rate']}")

    if args['florida_mean'] <= 0:
        raise ValueError(f"Expect florida_mean>0, got {args['florida_mean']}")

    if args['florida_stddev'] <= 0:
        raise ValueError(f"Expect florida_stddev>0, got {args['florida_stddev']}")

    if args['gulf_landfall_rate'] <= 0:
        raise ValueError(f"Expect gulf_landfall_rate>0, got {args['gulf_landfall_rate']}")

    if args['gulf_mean'] < 0:
        raise ValueError(f"Expect gulf_mean>0, got {args['gulf_mean']}")

    if args['gulf_stddev'] < 0:
        raise ValueError(f"Expect gulf_stddev>0, got {args['gulf_stddev']}")

    if args['simulator_id'] < 0:
        raise ValueError(f"Expect simulator_id>=0, got {args['simulator_id']}")

    # deepcopy ensures mutable items are copied too
    validated_args = copy.deepcopy(args)

    # validate parameters
    # compute natural log of the LogNormal means
    validated_args.update({
        "florida_mean": np.log(args['florida_mean']),
        "gulf_mean": np.log(args['gulf_mean']),
    })

    # log validated parameter values
    logger.info("Validated parameters: ")

    numerical_args = [
        "florida_landfall_rate",
        "florida_mean",
        "florida_stddev",
        "gulf_landfall_rate",
        "gulf_mean",
        "gulf_stddev",
    ]

    for arg_k in numerical_args:
        logger.info(f"{arg_k:>30s} = {validated_args[arg_k]:>10.5f}")

    return validated_args


def main(args=None):
    """
    Main function, called through the shell entrypoint.
    # TODO: IMPROVE DOCS

    """
    as_CLI = False

    if not args:
        # the code is used as a CLI, parse the arguments
        as_CLI = True
        args = parse_args()

    # validate (and transform, if necessary) arguments
    validated_args = validate_args(args)

    # use the desired simulator
    sim = Simulator(validated_args["simulator_id"])

    # run the simulation
    mean_loss = sim.simulate(**validated_args)

    if as_CLI:
        sys.exit(0)
    else:
        return mean_loss


if __name__ == "__main__":
    main()
