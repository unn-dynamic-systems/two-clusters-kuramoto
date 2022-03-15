from multiprocessing import Pool, cpu_count, Value, Process
from config import Config
from calc_line import calcline_stability
from clog import log
from tqdm import tqdm
from clog import log_str
import os


FOLDER = 'stability'

def main():
    if not os.path.exists(f"{Config.data_storage}/{FOLDER}/"):
        os.makedirs(f"{Config.data_storage}/{FOLDER}/")


    WORKERS_COUNT = cpu_count()
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} workers", 'header')

    files = os.listdir(f"{Config.data_storage}/limit_cycle")

    with Pool(WORKERS_COUNT) as pool:
        tasks = [pool.apply_async(calcline_stability,
                                  args=(f"./data/limit_cycle/{f}", f"./data/stability/{f}"),
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
