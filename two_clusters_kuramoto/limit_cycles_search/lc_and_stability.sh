#!/bin/bash
set -e
N=7
K=2
N_CPU=2

echo "STEP 1 - LIMIT CYCLES"

poetry run python3 l_c_main.py -n $N -k $K --mass 4.9 -a 1.57 --ic '0, 0.5' -t 11.4 \
        --h_mass 0.2 --h_mass_divide_limit 1e-1 --h_alpha 1e-1 --h_alpha_divide_limit 1e-2 \
        --mass_top_boarder 85 --folder_for_data ./data \
        --n_cpu $N_CPU > N-$N-K-$K-limit_cycles.txt 2>&1

STABILITY_FOLDER=$(ls data | grep limit-cycle-N-$N-K-$K | head -n 1)

echo "STEP 2 - STABILITY"
echo $STABILITY_FOLDER

poetry run python3 s_main.py --folder_for_store_data ./data \
    --folder_for_data_with_limit_cycles ./data/$STABILITY_FOLDER \
    --n_cpu $N_CPU > N-$N-K-$K-stability.txt 2>&1
