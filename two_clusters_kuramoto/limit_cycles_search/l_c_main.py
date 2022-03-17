import time
from multiprocessing import Pool, cpu_count, Value, Process

from config import Config
from existance_zones.existance_zones import M as M_function
from param_update_politics import Politics
from calc_line import calcline_limit_cycle
import pickle
from tqdm import tqdm
from clog import log, log_str
import os
from uuid import uuid4

FOLDER = f'limit-cycle-{str(uuid4()).split("-").pop()}'

def spawn_horizontal_lines(filepath, is_file_writed_stopped, pool):
    tasks = []
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
                filemane_to_dump_left=f'{Config.data_storage}/{FOLDER}/horizontal-line-{round(args_orig[1], 5)}-left.pickle'
                filemane_to_dump_right=f'{Config.data_storage}/{FOLDER}/horizontal-line-{round(args_orig[1], 5)}-right.pickle'

                args_down = params, Politics(h=Config.h_a,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=Config.h_a_limit,
                                            bar_title="horizontal-left",
                                            Reverse=False,
                                            ), filemane_to_dump_left

                args_up = params, Politics(h=Config.h_a,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=Config.h_a_limit,
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
    return M > M_function(Alpha, K, N) and M < Config.Mass_end

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

def main():
    params = Config.IC0, Config.T0, Config.N, \
        Config.Mass_start, Config.Alpha, Config.K

    if not os.path.exists(f"{Config.data_storage}/{FOLDER}"):
        os.makedirs(f"{Config.data_storage}/{FOLDER}")

    filemane_to_dump_down=f"{Config.data_storage}/{FOLDER}/verticle-line-down.pickle"
    filemane_to_dump_up=f"{Config.data_storage}/{FOLDER}/verticle-line-up.pickle"

    args_down = params, Politics(h=Config.h_m,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=Config.h_m_limit,
                                bar_title="down",
                                Reverse=False,
                                color='okcyan',
                                is_need_pgbar=True,
                                ), filemane_to_dump_down

    args_up = params, Politics(h=Config.h_m,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=Config.h_m_limit,
                                bar_title="up",
                                Reverse=True,
                                color='okblue',
                                is_need_pgbar=True
                                ), filemane_to_dump_up


    is_file_writed_stopped_down, is_file_writed_stopped_up = Value("i", 0), Value("i", 0)

    main_processes = [Process(target=calcline_wrap, args=(is_file_writed_stopped_down, args_down)),
                      Process(target=calcline_wrap, args=(is_file_writed_stopped_up, args_up))]

    [p.start() for p in main_processes]

    WORKERS_COUNT = cpu_count()
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} WORKERS", 'header')

    with Pool(WORKERS_COUNT) as pool:

        def spawn_tasks():
            tasks_down = spawn_horizontal_lines(filemane_to_dump_down, is_file_writed_stopped_down, pool)
            tasks_up = spawn_horizontal_lines(filemane_to_dump_up, is_file_writed_stopped_up, pool)
            [p.join() for p in main_processes]
            log(f"MAIN PROCESSES DONE", 'header')
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
