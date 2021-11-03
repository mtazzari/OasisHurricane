#!/usr/bin/env python
# coding=utf-8

import sys
import argparse

# TODO: logging


from .model import simulate


def main(*args, **kwargs):
    simulate(*args, **kwargs)

    pass


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--florida_landfall_rate", action="store", dest="florida_landfall_rate",
                   default=1.,
                   help="florida_landfall_rate", type=float)
    p.add_argument("--florida_mean", action="store", dest="florida_mean", help="florida_mean",
                   type=float)
    p.add_argument("--florida_stddev", action="store", dest="florida_stddev", help="florida_stddev",
                   type=float)
    p.add_argument("--gulf_landfall_rate", action="store", dest="gulf_landfall_rate",
                   help="gulf_landfall_rate", type=float)
    p.add_argument("--gulf_mean", action="store", dest="gulf_mean", help="gulf_mean", type=float)
    p.add_argument("--gulf_stddev", action="store", dest="gulf_stddev", help="gulf_stddev",
                   type=float)
    p.add_argument("-n", "--num_monte_carlo_samples", action="store",
                   dest="num_monte_carlo_samples", help="num_monte_carlo_samples", type=int)

    # p.add_argument("--astrokit-git-hash", action="store", dest="astrokit_git_hash", type=str,
    #                help="astrokit's commit hash to be checked out.")
    # p.add_argument("--cfg-file", action="store", dest="cfg_file", default=None,
    #                help="Configuration file (JSON)")
    # p.add_argument("--cfg-dict", action="store", dest="cfg_dict", default="{}",
    #                help="Configuration dictionary (JSON)", type=json.loads)
    # p.add_argument("--local", action="store_true", dest="local", default=False,
    #                help="Execute in local mode: don't download astrokit but use the system one.")
    args = p.parse_args()

    # TODO: input checking/validation

    # TODO: logging

    main(
        florida_landfall_rate=args.florida_landfall_rate,
        florida_mean=args.florida_mean,
        florida_stddev=args.florida_stddev,
        gulf_landfall_rate=args.gulf_landfall_rate,
        gulf_mean=args.gulf_mean,
        gulf_stddev=args.gulf_stddev,
        num_monte_carlo_samples=args.num_monte_carlo_samples,
    )

    sys.exit(0)
