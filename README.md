# oasis-hurricane

A Python command-line utility for Linux that computes the economic loss for hurricanes in Florida and in the Gulf states



Installation
------------
As easy as

```bash
pip git+https://github.com/mtazzari/OasisHurricane.git
```

or, if you prefer to have the code locally, first clone the github repo and then install it with:

```bash
git clone https://github.com/mtazzari/OasisHurricane.git
cd OasisHurricane
pip install .
```

Basic usage
-----------
Once installed, the requested Python command line utility has the following interface:
```bash
$ gethurricaneloss -h
usage: use "gethurricaneloss --help" for more information

positional arguments:
  florida_landfall_rate
                        [float] annual rate of landfalling hurricanes in Florida.
  florida_mean          [float] mean of the economic loss of landfalling hurricane in Florida.
  florida_stddev        [float] std deviation of the economic loss of landfalling hurricane in Florida.
  gulf_landfall_rate    [float] annual rate of landfalling hurricanes in Gulf states.
  gulf_mean             [float] mean of the economic loss of landfalling hurricane in Gulf states.
  gulf_stddev           [float] std deviation of the economic loss of landfalling hurricane in Gulf states.

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_MONTE_CARLO_SAMPLES, --num_monte_carlo_samples NUM_MONTE_CARLO_SAMPLES
                        [int] number of monte carlo samples, i.e. years. (default=10)
  -s SIMULATOR_ID, --simulator SIMULATOR_ID
                        [int] simulator id. Implemented simulators: (id:name)
                        0: python
                        1: jit
                        2: jit-parallel
                        3: jit-noloops
                        4: python-noloops
```
The positional parameters are required for execution. 

The utility has 5 different implementations of the proposed Monte Carlo hurricane losses model, which can be selected 
with the `-s` or `--simulator` option by providing the `id` of the simulator.

The implementations:

| ID  | Simulator          | Description |
| --- | ------------------ | ----------- |
| 0   | `python`           | a pure Python implementation of the algorithm outlined in the test sheet. Used as a reference for accuracy and performance benchmarks.       |
| 1   | `jit`              | the same algorithm as in `python`, with `numba` just-in-time compilation   |
| 2   | `jit-parallel`     | the same algorithm as in `python`, with `numba` just-in-time compilation **and** `numba` automatic         |
| 3   | `jit-noloops`      | a `numpy`-only algorithm with **no explicit loops**, with `numba` just-in-time compilation   |
| 4   | `python-noloops`   | a pure Python`numpy`-only algorithm with **no explicit loops**          |

Author
------

- [Marco Tazzari](https://github.com/mtazzari)

License
-------
**oasishurricane** is free software licensed under the BSD-3 License. For more details see
the [LICENSE](https://github.com/mtazzari/oasishurricane/blob/main/LICENSE).

© Copyright 2021 Marco Tazzari.

