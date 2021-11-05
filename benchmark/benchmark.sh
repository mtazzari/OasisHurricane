# s0

TIMINGS_LOGS_DIR="timings"

export TIMEIT=1
export TIMEIT_CYCLES=100
export TIMEIT_LOGFILE="${TIMINGS_LOGS_DIR}/timings_s0.txt"

gethurricaneloss 10 2 0.001 30 1 0.000001 -n 10 -s0
gethurricaneloss 10 2 0.001 30 1 0.000001 -n 100 -s0
gethurricaneloss 10 2 0.001 30 1 0.000001 -n 1000 -s0
export TIMEIT_CYCLES=10
gethurricaneloss 10 2 0.001 30 1 0.000001 -n 100000 -s0
export TIMEIT_CYCLES=4
gethurricaneloss 10 2 0.001 30 1 0.000001 -n 1000000 -s0


export TIMEIT_CYCLES=1000

num_monte_carlo_samples="10 100 1000 10000 100000"   #manca 100000
simulator_ids="1 2 3 4"

for simulator_id in $simulator_ids; do
    for num_monte_carlo_sample in $num_monte_carlo_samples; do
      export TIMEIT_LOGFILE="${TIMINGS_LOGS_DIR}/timings_s${simulator_id}.txt";
      gethurricaneloss 10 2 0.001 30 1 0.000001 -n ${num_monte_carlo_sample} -s${simulator_id};
    done
done

# run the largest MC simulations with reduced TIMEIT_CYCLES
export TIMEIT_CYCLES=50

num_monte_carlo_samples="1000000"
simulator_ids="1 2 3 4"

for simulator_id in $simulator_ids; do
    for num_monte_carlo_sample in $num_monte_carlo_samples; do
      export TIMEIT_LOGFILE="${TIMINGS_LOGS_DIR}/timings_s${simulator_id}.txt";
      gethurricaneloss 10 2 0.001 30 1 0.000001 -n ${num_monte_carlo_sample} -s${simulator_id};
    done
done

# run the largest MC simulations with reduced TIMEIT_CYCLES
export TIMEIT_CYCLES=5

num_monte_carlo_samples="10000000"
simulator_ids="1 2 3 4"

for simulator_id in $simulator_ids; do
    for num_monte_carlo_sample in $num_monte_carlo_samples; do
      export TIMEIT_LOGFILE="${TIMINGS_LOGS_DIR}/timings_s${simulator_id}.txt";
      gethurricaneloss 10 2 0.001 30 1 0.000001 -n ${num_monte_carlo_sample} -s${simulator_id};
    done
done