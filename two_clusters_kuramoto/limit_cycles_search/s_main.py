from multiprocessing import Pool, cpu_count
from calc_line import calcline_stability
import argparse
from clog import log
from tqdm import tqdm
from clog import log_str
import os
import sys
from uuid import uuid4

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder_for_data_with_limit_cycles', type=str, help='folder for data with limit cycles', required=True)
    parser.add_argument('--folder_for_store_data', type=str, help='folder for data', required=True)
    parser.add_argument('--n_cpu', type=int, help='parallel workers', nargs='?', const=cpu_count(), default=cpu_count())

    args = parser.parse_args()
    return args

def main():
    ARGS = get_args()
    log(f"ARGS {ARGS}", 'okcyan')

    FOLDER_WITH_LIMIT_CYCLES = ARGS.folder_for_data_with_limit_cycles
    FOLDER_TO_PUSH = f"stability-{FOLDER_WITH_LIMIT_CYCLES.split('/').pop()}-{str(uuid4()).split('-').pop()}"

    if not os.path.exists(f"{ARGS.folder_for_store_data}/{FOLDER_TO_PUSH}"):
        os.makedirs(f"{ARGS.folder_for_store_data}/{FOLDER_TO_PUSH}")
    
    if not os.path.exists(f"{FOLDER_WITH_LIMIT_CYCLES}"):
        print(f"Not found {FOLDER_WITH_LIMIT_CYCLES}")
        exit(1)

    WORKERS_COUNT = ARGS.n_cpu
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} workers", 'header')
    log(f"data output {ARGS.folder_for_store_data}/{FOLDER_TO_PUSH}", 'okcyan')

    files = os.listdir(f"{FOLDER_WITH_LIMIT_CYCLES}")

    with Pool(WORKERS_COUNT) as pool:
        tasks = [pool.apply_async(calcline_stability,
                                  args=(f"{FOLDER_WITH_LIMIT_CYCLES}/{f}", f"{ARGS.folder_for_store_data}/{FOLDER_TO_PUSH}/{f}"),
                                  error_callback=lambda e: print(e)) for f in files]

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
