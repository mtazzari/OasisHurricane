#!/usr/bin/env python
# coding=utf-8

import sys
import argparse

# TODO: logging


from .model import simulate


def parse_args():
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

    args = parser.parse_args()

    # TODO: input checking/validation

    # TODO: logging

    return args


def main():
    args = parse_args()

    simulate(
        florida_landfall_rate=args.florida_landfall_rate,
        florida_mean=args.florida_mean,
        florida_stddev=args.florida_stddev,
        gulf_landfall_rate=args.gulf_landfall_rate,
        gulf_mean=args.gulf_mean,
        gulf_stddev=args.gulf_stddev,
        num_monte_carlo_samples=args.num_monte_carlo_samples,
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
