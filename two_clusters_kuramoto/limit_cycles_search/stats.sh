#!/bin/bash
set -e
N=12
N_CPU=1
Omega=1
export PYTHONWARNINGS="ignore"

poetry run python3 stat_main.py -n $N --alpha 1.57 \
        --h_mass 0.2 --h_alpha 1e-2 --mass_top_boarder 80 \
        --folder_for_data ./data --n_cpu $N_CPU --t_end 4000 \
        --iterations 50 --omega $Omega > N-$N-Omega-$Omega-stats.txt 2>&1
