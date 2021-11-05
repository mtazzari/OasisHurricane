# oasishurricane

[![image](https://github.com/mtazzari/oasishurricane/actions/workflows/tests.yml/badge.svg)](https://github.com/mtazzari/oasishurricane/actions/workflows/tests.yml)
[![image](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

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

A Python command-line utility for Linux that computes the economic loss for hurricanes in Florida and in the Gulf states.

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
                        [int] simulator id (default=0). Implemented simulators: (id:name)
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
Let us run a series of examples in which the losses are highly peaked around the
mean loss values. Since the events are all independent, the expected mean loss value is 
```bash
florida_landfall_rate * florida_mean + gulf_landfall_rate * gulf_mean
```
it's easy to verify whether the result is about correct.

### Example 1: get started with `gethurricaneloss`
`gethurricaneloss` is easy to use. 

Let us run it with 100k Monte Carlo steps (i.e., years):
```bash
$ gethurricaneloss 10 5 0.00001 30 1 0.00001 -n 100000
[2021-11-04 16:33:01] gethurricaneloss v0.0.1 by Marco Tazzari
[2021-11-04 16:33:01] Validated parameters:
[2021-11-04 16:33:01]          florida_landfall_rate =   10.00000
[2021-11-04 16:33:01]                   florida_mean =    1.60944
[2021-11-04 16:33:01]                 florida_stddev =    0.00001
[2021-11-04 16:33:01]             gulf_landfall_rate =   30.00000
[2021-11-04 16:33:01]                      gulf_mean =    0.00000
[2021-11-04 16:33:01]                    gulf_stddev =    0.00001
[2021-11-04 16:33:01] Using simulator: python
[2021-11-04 16:33:01] Setting the random number generator with seed:None
[2021-11-04 16:33:01] Starting main loop over desired 100000 Monte Carlo samples
[2021-11-04 16:33:12] End of main loop. Elapsed time: 0:00:11.463529 (h:m:s)
[2021-11-04 16:33:12] MEAN LOSS: 79.96644884090169
```
By default, `gethurricaneloss` uses the `python` simulator.

> **Note:**  the `validated parameters` printed in the console/log show the values of the parameters after validation (type- and value-checking), and transformation, if necessary.

> **Note:**  `florida_mean` and `gulf_mean` printed in the console/log are the natural log of the values 
passed in input by the user: the transformation ensures that the expected value of the lognormal distribution
is the value of `florida_mean` passed by the user (as opposed to `exp^florida_mean`). The same applies to `gulf_mean`.

### Example 2: run `gethurricaneloss` with different simulators
Let us now run `gethurricaneloss` using the `python-noloops` simulator (id: 4) by passing the `-s4` option.
```bash
$ gethurricaneloss 10 5 0.00001 30 1 0.00001 -n 100000 -s4
[2021-11-04 16:44:03] gethurricaneloss v0.0.1 by Marco Tazzari
[2021-11-04 16:44:03] Validated parameters:
[2021-11-04 16:44:03]          florida_landfall_rate =   10.00000
[2021-11-04 16:44:03]                   florida_mean =    1.60944
[2021-11-04 16:44:03]                 florida_stddev =    0.00001
[2021-11-04 16:44:03]             gulf_landfall_rate =   30.00000
[2021-11-04 16:44:03]                      gulf_mean =    0.00000
[2021-11-04 16:44:03]                    gulf_stddev =    0.00001
[2021-11-04 16:44:03] Using simulator: python-noloops
[2021-11-04 16:44:03] Setting the random number generator with seed:None
[2021-11-04 16:44:03] Starting main loop over desired 100000 Monte Carlo samples
[2021-11-04 16:44:03] End of main loop. Elapsed time: 0:00:00.174803 (h:m:s)
[2021-11-04 16:44:03] MEAN LOSS: 80.01731942131745
```
This is waaaay faster! 0.17s vs 11.46s compared to the explicit-loop Python version (`python` simulator), a 67x speed-up! 

## Logging
Logging is handled with the `logging` Python module:

- the **console** shows a concise and easy-to-read log;
- a **development logfile** stores the debug-level logs (typically named `gethurricaneloss_dev.log.x`);
- a **production logfile** stores a production-level (info and above) logs (typically named `gethurricaneloss.log.x`).

The numerical `.x` suffix (e.g., `.1`, `.2`, ...) in the log filenames allows for a rotating log file handling, for logs
of large volume.

## Testing
Testing uses `pytest` and is performed automatically with GitHub Actions on every push on any branch.

Note that GitHub Actions is free for an unlimited amount of compute-minutes for open source projects.

I implemented three tests, with a matrix of parametrizations:

| test name                          | test description                                            |
| ---------------------------------- | ----------------------------------------------------------- |
| `test_simulators_accuracy`           | Test if the different simulators return mean losses that agree within a relative tolerance `rtol` and an absolute tolerance `atol`. |
| `test_simulator_selection`           | Test exceptions if the chosen simulator_id doesn't exist.    |
| `test_input_parameter_values`        | Test exceptions if input data has forbidden values.         |

All the three tests use `pytest.mark.parametrize`, which allows repeating the same test with different
input parameters, handy to test the validity of a test under different scenarios.

To keep the tests reproducible, I fix the random seed to the `SEED` defined in `tests.py`.

Additional tests that it would be easy to implement:

- a test against analytical expected values for the mean loss, considering that the expectation values for
  the Poissonian is the `mean` (i.e., `florida_landfall_rate`) and the expected values for the LogNormal is
  again the `mean` (i.e., `florida_mean`).

- a test to check the CLI usage from a shell (e.g., using `subprocess`).

- additional convergence checks for different regimes of the input parameters.

## Accuracy checks
Accuracy is checked in the tests.

In particular, `test_simulators_accuracy` checks that the 5 implementations of the hurricane loss model return mean loss
values within a given accuracy, for 3 sets of input parameters. 

To have relatively quick checks, the threshold accuracy is now set to 1%, but it can be
made smaller (i.e. tighter constraint), at the cost of longer CI tests.

## Performance
In order to test the performance of the implemented simulators I adopt a Factory design patter for the
`Simulator` class, e.g.:
```py
from oasishurricane.model import Simulator
sim = Simulator(simulator_id=1)
```
Regardless of the chosen simulator, the MC simulation is run with:
```py
sim.simulate(**validated_parameters)
```
where `validated_parameters` are the CLI input parameters after validation.

This architecture allows for a modular and quick replacement of the core MC model. 

To properly evaluate the performance of the simulators I defined an ad-hoc decorator `oasishurricane.utils.timer` 
which:

- runs the simulator core function for the desired number of `cycles`, 
- momentarily deactivates the garbage collector, 
- computes the best execution time among the `cycles` execution times. 

For reference: in developing `oasishurricane.utils.timer`, I follow the nomenclature of `timeit.Timer`.

The timing functionality can be activated by setting the `TIMEIT` environment variable, e.g.
```bash
export TIMEIT=1
```
Additional parameters to customize the timing functionality are:

- `TIMEIT_CYCLES`: the number of times the simulator core function is executed. The larger, the better, but
                   for large `num_monte_carlo_samples` it might be handy to reduce it. If not set, `cycles=3`.
- `TIMEIT_LOGFILE`: the filename of the log where to store the timings. If not set, it prints to the console log. 

### Examples
With this setup:
```bash
export TIMEIT=1
export TIMEIT_CYCLES=33
export TIMEIT_LOGFILE=timings_example.txt
```
we obtain the following output in the console:
```bash
$ gethurricaneloss 10 2 0.001 30 1 0.000001 -n 1000 -s3
[2021-11-05 01:25:52] gethurricaneloss v0.0.1 by Marco Tazzari
[2021-11-05 01:25:52] Validated parameters:
[2021-11-05 01:25:52]          florida_landfall_rate =   10.00000
[2021-11-05 01:25:52]                   florida_mean =    0.69315
[2021-11-05 01:25:52]                 florida_stddev =    0.00100
[2021-11-05 01:25:52]             gulf_landfall_rate =   30.00000
[2021-11-05 01:25:52]                      gulf_mean =    0.00000
[2021-11-05 01:25:52]                    gulf_stddev =    0.00000
[2021-11-05 01:25:52] Found TIMEIT and TIMEIT_LOGFILE: timings will be logged in timings_example.txt
[2021-11-05 01:25:52] Using simulator: jit-noloops
[2021-11-05 01:25:52] Setting the random number generator with seed:None
[2021-11-05 01:25:52] Starting main loop over desired 1000 Monte Carlo samples
[2021-11-05 01:25:52] Timings are computed by running 33 times the function.
[2021-11-05 01:25:53] End of main loop. Elapsed time: 0:00:00.478656 (h:m:s)
[2021-11-05 01:25:53] MEAN LOSS: 49.98602443852616
```
This is the content of `timings_example.txt`:
```text
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 1000.000000         33   0.001399  49.986024 
```
where the columns are:

- `florida_landfall_rate` 
- `ln(florida_mean)` 
- `florida_stddev` 
- `gulf_landfall_rate` 
- `ln(gulf_mean)` 
- `gulf_stddev` 
- `num_monte_carlo_samples`
- `cycles`
- `best execution time`
- Mean economic loss

By running multiple times `gethurricaneloss` with the environment variables as above, the timings are appended, e.g.:
```text
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001  10.000000       1000   0.000013  49.966121 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 100.000000       1000   0.000133  50.037439 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 1000.000000       1000   0.001401  49.991665 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 10000.000000       1000   0.014170  50.000415 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 100000.000000       1000   0.144798  49.999268 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 1000000.000000         50   1.464731  50.000486 
 10.000000   0.693147   0.001000  30.000000   0.000000   0.000001 10000000.000000          5  14.800176  50.001481 
```

Timing functionality is deactivated by unsetting `TIMEIT`:
```bash
unset TIMEIT
```

### Results
To quantify the performance of the different implementations I wrote a simple bash script (benchmark/benchmark.sh)
to compute the execution time for all the 5 simulators, each of them for a range of `num_monte_carlo_samples`
between 10 and 10 millions.

All the execution times are in the `benchmark/timings/` folder, e.g. `timings_s0.txt` for `simulator_id=0` (`python`).

In this plot I present the scaling as a function of `num_monte_carlo_samples`:

<p align="center">
   <img width = "600" src="https://github.com/mtazzari/OasisHurricane/blob/readme/benchmark/execution_time_vs_num_monte_carlo_samples.png?raw=true"/>		 
 </p>

**Comments:**

- the scaling is pretty much linear (cf. reference dashed line) for all the implementations.
- the pure `python` implementation is, as expected, the least efficient.
- the `numba.jit` compilation achieves a 75x speed-up when applied to the `python` implementation (`jit`), roughly the same speed-up achieved by implementations with no explicit loops (`jit-noloops`).
- using only numpy functions with no explicit loops achieves a very good acceleration as well (75x w.r.t. `python`),
  without the need of `numba.jit`.
- `numba.jit` with `parallel` option is further 5.7x faster than the `jit` version. Overall, the `jit-parallel` 
  version is 390x faster than pure `python`.

In the following figure I show the convergence of the mean economic losses for increasing `num_monte_carlo_samples`.

<p align="center">
   <img width = "600" src="https://github.com/mtazzari/OasisHurricane/blob/readme/benchmark/mean_loss_vs_num_monte_carlo_samples.png?raw=true"/>		 
 </p>
 
Comments:

- as expected, with increasing `num_monte_carlo_samples`, all the implementations tend towards the 
  same expected value (dashed line at mean loss=50 $B).
- the pure `python` implementation is slightly slower in converging than the others.

## Author

- [Marco Tazzari](https://github.com/mtazzari)

## License
**oasishurricane** is free software licensed under the BSD-3 License. For more details see
the [LICENSE](https://github.com/mtazzari/oasishurricane/blob/main/LICENSE).

© Copyright 2021 Marco Tazzari.

