from multiprocessing import Pool, cpu_count
from calc_line import calcline_stability
import argparse
from clog import log
from tqdm import tqdm
from clog import log_str
import os
from uuid import uuid4
import numpy as np
from param_update_politics import Politics
from existance_zones.existance_zones import M as M_function
from calc_line import calcline_stats

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='Total number of elements', required=True)
    parser.add_argument('-a', '--alpha' ,type=float, help='Number of elements', required=True)
    parser.add_argument('--omega', type=float, help='Omega', required=True)

    parser.add_argument('--mass_top_boarder' ,type=float, help='Top boarder', required=True)
    parser.add_argument('--h_mass', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_alpha', type=float, help='Total number of elements', required=True)

    parser.add_argument('--t_end', type=float, help='Time to calculate state', required=True)
    parser.add_argument('--iterations', type=int, help='iterations per point', required=True)


    parser.add_argument('--folder_for_data', type=str, help='folder for data', required=True)

    parser.add_argument('--n_cpu', type=int, help='parallel workers', nargs='?', const=cpu_count(), default=cpu_count())
    args = parser.parse_args()

    return args

MASS_TOP_BOARDER = get_args().mass_top_boarder

def inside_args_area(N, M, Alpha, K):
    return M > M_function(Alpha, K, N) and M < MASS_TOP_BOARDER

def alpha_updater_left(N, M, Alpha, K, h, reverse=False):
    if reverse:
        Alpha += h
    else:
        Alpha -= h
    return N, M, Alpha, K

def main():
    ARGS = get_args()
    log(f"ARGS {ARGS}", 'okcyan')

    FOLDER_TO_PUSH = f"stats-{str(uuid4()).split('-').pop()}"

    if not os.path.exists(f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}"):
        os.makedirs(f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}")

    WORKERS_COUNT = ARGS.n_cpu
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} WORKERS", 'header')
    log(f"DATA OUTPUT {ARGS.folder_for_data}/{FOLDER_TO_PUSH}", 'okcyan')


    with Pool(WORKERS_COUNT) as pool:
        tasks = []

        for m_i in np.arange(M_function(ARGS.alpha, 2, ARGS.n), ARGS.mass_top_boarder, ARGS.h_mass):
            params = ARGS.t_end, ARGS.iterations, ARGS.n, m_i, ARGS.alpha, ARGS.omega
            filemane_to_dump_left=f'{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/horizontal-line-{round(m_i, 5)}-left.pickle'
            filemane_to_dump_right=f'{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/horizontal-line-{round(m_i, 5)}-right.pickle'

            args_left = params, Politics(h=ARGS.h_alpha,
                                         inside_args_area=inside_args_area,
                                         args_updater=alpha_updater_left,
                                         bar_title="horizontal-left",
                                         Reverse=False,
                                         ), filemane_to_dump_left

            args_right = params, Politics(h=ARGS.h_alpha,
                                          inside_args_area=inside_args_area,
                                          args_updater=alpha_updater_left,
                                          bar_title="horizontal-right",
                                          Reverse=True,
                                          ), filemane_to_dump_right 

            tasks.append(pool.apply_async(calcline_stats,
                                          args=args_left,
                                          error_callback=lambda e: print(e)))
            tasks.append(pool.apply_async(calcline_stats,
                                          args=args_right,
                                          error_callback=lambda e: print(e)))


        pbar = tqdm(total=len(tasks))
        i = 0
        for t in tasks:
            t.wait(); i += 1
            pbar.set_description(log_str(f"{i}/{len(tasks)} tasks", "okgreen"))
            pbar.update(1)

        log(f"WAIT POOL", 'header')
        pool.close(); pool.join()
        log(f"DONE", 'header')

if __name__ == "__main__":
    main()
