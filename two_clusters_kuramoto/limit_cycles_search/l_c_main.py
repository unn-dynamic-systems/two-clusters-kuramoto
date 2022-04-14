import time
from multiprocessing import Pool, cpu_count, Value, Process
import argparse
import numpy as np
from existance_zones.existance_zones import M as M_function
from param_update_politics import Politics
from calc_line import calcline_limit_cycle, limit_cycle_find_check
import pickle
from tqdm import tqdm
from clog import log, log_str
import os
from uuid import uuid4

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='Total number of elements', required=True)
    parser.add_argument('-k', type=int, help='Number of elements in small cluster', required=True)
    parser.add_argument('-m', '--mass' ,type=float, help='Number of elements', required=True)
    parser.add_argument('-a', '--alpha' ,type=float, help='Number of elements', required=True)
    parser.add_argument('-i', '--ic',type=str, help='Initial conditions for limit cycle', required=True)
    parser.add_argument('-t', type=str, help='Limit cycle period', required=True)

    parser.add_argument('--mass_top_boarder' ,type=float, help='Top boarder', required=True)
    parser.add_argument('--h_mass', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_alpha', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_mass_divide_limit', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_alpha_divide_limit', type=float, help='Total number of elements', required=True)

    parser.add_argument('--folder_for_data', type=str, help='folder for data', required=True)

    parser.add_argument('--n_cpu', type=int, help='parallel workers', nargs='?', const=cpu_count(), default=cpu_count())
    args = parser.parse_args()

    args.ic = np.fromstring(args.ic, sep=",")
    return args

FOLDER_TO_PUSH = f'limit-cycle-N-{get_args().n}-K-{get_args().k}-{str(uuid4()).split("-").pop()}'
MASS_TOP_BOARDER = get_args().mass_top_boarder

def spawn_horizontal_lines(filepath, is_file_writed_stopped, pool):
    tasks = []
    ARGS = get_args()
    while True:
        try:
            open(filepath).close()
            break
        except FileNotFoundError:
            if is_file_writed_stopped.value == 1:
                return tasks
            time.sleep(3)

    with open(filepath, "rb") as f:
        while True:
            try:
                d = pickle.load(f)
                args_orig = d.get("system args")
                T = d.get("Limit Cycle Period")
                IC = d.get("Initial Conditions")

                params = IC, T, *args_orig
                filemane_to_dump_left=f'{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/horizontal-line-{round(args_orig[1], 5)}-left.pickle'
                filemane_to_dump_right=f'{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/horizontal-line-{round(args_orig[1], 5)}-right.pickle'

                args_down = params, Politics(h=ARGS.h_alpha,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=ARGS.h_alpha_divide_limit,
                                            bar_title="horizontal-left",
                                            Reverse=False,
                                            ), filemane_to_dump_left

                args_up = params, Politics(h=ARGS.h_alpha,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=ARGS.h_alpha_divide_limit,
                                            bar_title="horizontal-right",
                                            Reverse=True,
                                            ), filemane_to_dump_right

                tasks.append(pool.apply_async(calcline_limit_cycle, args=args_down))
                tasks.append(pool.apply_async(calcline_limit_cycle, args=args_up))

            except EOFError:
                if is_file_writed_stopped.value == 1:
                    return tasks
                time.sleep(3)

def calcline_wrap(is_file_writed_stopped, args):
        try:
            calcline_limit_cycle(*args)
        except BaseException as e:
            print("Error was occured")
            print(e)
        finally:
            is_file_writed_stopped.value = 1

def inside_args_area(N, M, Alpha, K):
    return M > M_function(Alpha, K, N) and M < MASS_TOP_BOARDER

def mass_updater_down(N, M, Alpha, K, h, reverse=False):
    if reverse:
        M += h
    else:
        M -= h
    return N, M, Alpha, K

def alpha_updater_left(N, M, Alpha, K, h, reverse=False):
    if reverse:
        Alpha += h
    else:
        Alpha -= h
    return N, M, Alpha, K

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='Total number of elements', required=True)
    parser.add_argument('-k', type=int, help='Number of elements in small cluster', required=True)
    parser.add_argument('-m', '--mass' ,type=float, help='Number of elements', required=True)
    parser.add_argument('-a', '--alpha' ,type=float, help='Number of elements', required=True)
    parser.add_argument('-i', '--ic',type=str, help='Initial conditions for limit cycle', required=True)
    parser.add_argument('-t', type=str, help='Limit cycle period', required=True)

    parser.add_argument('--mass_top_boarder' ,type=float, help='Top boarder', required=True)
    parser.add_argument('--h_mass', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_alpha', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_mass_divide_limit', type=float, help='Total number of elements', required=True)
    parser.add_argument('--h_alpha_divide_limit', type=float, help='Total number of elements', required=True)

    parser.add_argument('--folder_for_data', type=str, help='folder for data', required=True)

    parser.add_argument('--n_cpu', type=int, help='parallel workers', nargs='?', const=cpu_count(), default=cpu_count())
    args = parser.parse_args()

    args.ic = np.fromstring(args.ic, sep=",")
    return args

def main():
    ARGS = get_args()
    log(f"ARGS {ARGS}", 'okcyan')

    params = ARGS.ic, ARGS.t, ARGS.n, ARGS.mass, ARGS.alpha, ARGS.k

    filemane_to_dump_down=f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/verticle-line-down.pickle"
    filemane_to_dump_up=f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}/verticle-line-up.pickle"

    args_down = params, Politics(h=ARGS.h_mass,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=ARGS.h_mass_divide_limit,
                                bar_title="down",
                                Reverse=False,
                                color='okcyan',
                                is_need_pgbar=True,
                                ), filemane_to_dump_down

    args_up = params, Politics(h=ARGS.h_mass,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=ARGS.h_mass_divide_limit,
                                bar_title="up",
                                Reverse=True,
                                color='okblue',
                                is_need_pgbar=True
                                ), filemane_to_dump_up


    is_file_writed_stopped_down, is_file_writed_stopped_up = Value("i", 0), Value("i", 0)

    is_find_first_point = limit_cycle_find_check(params)
    if not is_find_first_point:
        log(f"We didn't find the first point", 'header')
        exit(1)

    log(f"We found the first point", 'header')

    if not os.path.exists(f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}"):
        os.makedirs(f"{ARGS.folder_for_data}/{FOLDER_TO_PUSH}")

    main_processes = [Process(target=calcline_wrap, args=(is_file_writed_stopped_down, args_down)),
                      Process(target=calcline_wrap, args=(is_file_writed_stopped_up, args_up))]

    [p.start() for p in main_processes]

    WORKERS_COUNT = ARGS.n_cpu
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} WORKERS", 'header')
    log(f"data output {ARGS.folder_for_data}/{FOLDER_TO_PUSH}", 'okcyan')

    with Pool(WORKERS_COUNT) as pool:

        def spawn_tasks():
            tasks_down = spawn_horizontal_lines(filemane_to_dump_down, is_file_writed_stopped_down, pool)
            tasks_up = spawn_horizontal_lines(filemane_to_dump_up, is_file_writed_stopped_up, pool)
            [p.join() for p in main_processes]
            log(f"\nMAIN PROCESSES DONE", 'header')
            return tasks_down + tasks_up

        tasks = spawn_tasks()
        total_tasks_count = len(tasks)
        log(f"WAIT TASKS", 'header')
        pbar = tqdm(total=total_tasks_count)
        i = 0
        for t in tasks:
            t.wait(); i += 1
            pbar.set_description(log_str(f"{i}/{total_tasks_count} tasks", "okblue"))
            pbar.update(1)

        log(f"CLOSE POOL", 'header')
        pool.close(); pool.join()        
        log(f"DONE", 'header')

if __name__ == "__main__":
    main()
