# oasis-hurricane

A Python command-line utility for Linux that computes the economic loss for hurricanes in Florida and in the Gulf states



## Installation
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

## Basic usage
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

The utility has **5 different implementations** of the proposed Monte Carlo hurricane losses model, which can be selected 
with the `-s` or `--simulator` option by providing the `id` of the simulator. The implementations achieve different levels
of acceleration w.r.t. the baseline pure-`python` implementation.

The implementations are:

| ID  | Simulator          | Description |
| --- | ------------------ | ----------- |
| 0   | `python`           | a pure Python implementation of the algorithm outlined in the test sheet. Used as a reference for accuracy and performance benchmarks.       |
| 1   | `jit`              | the same algorithm as in `python`, with `numba` just-in-time compilation   |
| 2   | `jit-parallel`     | the same algorithm as in `python`, with `numba` just-in-time compilation **and** `numba` automatic         |
| 3   | `jit-noloops`      | a `numpy`-only algorithm with **no explicit loops**, with `numba` just-in-time compilation   |
| 4   | `python-noloops`   | a pure Python`numpy`-only algorithm with **no explicit loops**          |

## Examples

#### Example 21: get started with `gethurricanlosses`
`gethurricaneloss` is easy to use, e.g.:
```bash
$ gethurricaneloss 10 2 0.001 30 1 0.000001 -n 1000

********************************************************************************
** Welcome! You are using gethurricaneloss by Marco Tazzari.                  **
**                                                                            **
** gethurricaneloss is a Python command-line utility for Linux that computes  **
** the economic loss for hurricanes in Florida and in the Gulf states.        **
**                                                                            **
********************************************************************************

[2021-11-04 15:57:24]   INFO Validated parameters:
[2021-11-04 15:57:24]   INFO          florida_landfall_rate =   10.00000
[2021-11-04 15:57:24]   INFO                   florida_mean =    0.69315
[2021-11-04 15:57:24]   INFO                 florida_stddev =    0.00100
[2021-11-04 15:57:24]   INFO             gulf_landfall_rate =   30.00000
[2021-11-04 15:57:24]   INFO                      gulf_mean =    0.00000
[2021-11-04 15:57:24]   INFO                    gulf_stddev =    0.00000
[2021-11-04 15:57:24]   INFO Using simulator: python
[2021-11-04 15:57:24]   INFO Setting the random number generator with seed:None
[2021-11-04 15:57:24]   INFO Starting main loop over desired 1000 Monte Carlo samples
[2021-11-04 15:57:24]   INFO End of main loop. Elapsed time: 0:00:00.107569 (h:m:s)
[2021-11-04 15:57:24]   INFO MEAN LOSS: 49.75181159464964
```
#### Example 2: run `gethurricanlosses` with different simulators


### Logging
Logging is handled with the `logging` Python module:

- the **console** shows a concise and easy-to-read log;
- a **development logfile** stores the debug-level logs (typically named `gethurricaneloss_dev.log.x`);
- a **production logfile** stores a production-level (info and above) logs (typically named `gethurricaneloss.log.x`).

The numerical `.x` suffix (e.g., `.1`, `.2`, ...) in the log filenames allows for a rotating log file handling, for logs
of large volume.

### Testing
Testing uses `pytest` and is performed automatically with GitHub Actions on every push on any branch.

Note that GitHub Actions is free for an unlimited amount of compute-minutes for open source projects.

I implemented three tests, with a matrix of parametrizations:

| test name                          | test description                                            |
| ---------------------------------- | ----------------------------------------------------------- |
| test_simulators_accuracy           | Test if the different simulators return mean losses that agree within a relative tolerance `rtol` and an absolute tolerance `atol`. |
| test_simulator_selection           | Test exceptions if the chosen simulator_id doesn't exist.    |
| test_input_parameter_values        | Test exceptions if input data has forbidden values.         |

All the three tests use `pytest.mark.parametrize`, which allows repeating the same test with different
input parameters, handy to test the validity of a test under different scenarios.

Additional tests that it would be easy to implement:

- a test against analytical expected values for the mean loss, considering that the expectation values for
  the Poissonian is the `mean` (i.e., `florida_landfall_rate`) and the expected values for the LogNormal is
  again the `mean` (i.e., `florida_mean`).

- a test to check the CLI usage from a shell (e.g., using `subprocess`).

- additional convergence checks.

## Accuracy checks
Accuracy is checked in the tests,

In particular, `test_simulators_consistency` checks that the 5 implementations of the hurricane loss model return mean loss
values within a given accuracy. To have relatively quick checks, the threshold accuracy is now set to 1%, but it can be
made smaller (i.e. tighter constraint), at the cost of longer CI tests.

## Performance checks

## Author

- [Marco Tazzari](https://github.com/mtazzari)

## License
**oasishurricane** is free software licensed under the BSD-3 License. For more details see
the [LICENSE](https://github.com/mtazzari/oasishurricane/blob/main/LICENSE).

© Copyright 2021 Marco Tazzari.

