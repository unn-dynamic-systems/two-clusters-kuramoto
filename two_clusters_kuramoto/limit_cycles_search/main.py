import time
from multiprocessing import Pool, cpu_count, Value, Process

from py import process
from config import Config
from existance_zones.existance_zones import M as M_function
from param_update_politics import Politics
from calc_line import calcline
import pickle
from clog import log


def spawn_horizontal_lines(filepath, is_over, pool):
    while True:
        try:
            open(filepath).close()
            break
        except FileNotFoundError:
            if is_over.value == 1: return
            time.sleep(3)

    with open(filepath, "rb") as f:
        while True:
            try:
                d = pickle.load(f)
                args_orig = d.get("system args")
                T = d.get("Limit Cycle Period")
                IC = d.get("Initial Conditions")

                params = IC, T, *args_orig
                filemane_to_dump_left=f'{Config.data_storage}/horizontal-line-{round(args_orig[1], 5)}-left.pickle'
                filemane_to_dump_right=f'{Config.data_storage}/horizontal-line-{round(args_orig[1], 5)}-right.pickle'

                args_down = params, Politics(h=1e-2,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=0.5 * 1e-2,
                                            bar_title="horizontal-left",
                                            Reverse=False,
                                            color='okblue'), filemane_to_dump_left

                args_up = params, Politics(h=1e-2,
                                            inside_args_area=inside_args_area,
                                            args_updater=alpha_updater_left,
                                            h_limit=0.5 * 1e-2,
                                            bar_title="horizontal-right",
                                            Reverse=True,
                                            color='okcyan'), filemane_to_dump_right

                pool.apply_async(calcline, args=args_down)
                pool.apply_async(calcline, args=args_up)

            except EOFError:
                if is_over.value == 1: return
                time.sleep(3)

def calcline_wrap(is_over, args):
        try:
            calcline(*args)
        except BaseException as e:
            print("Error was occured")
            print(e)
        finally:
            is_over.value = 1

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
        M_function(Config.Alpha, Config.K, Config.N) + 1, Config.Alpha, Config.K

    filemane_to_dump_down=f"{Config.data_storage}/verticle-line-down.pickle"
    filemane_to_dump_up=f"{Config.data_storage}/verticle-line-up.pickle"

    args_down = params, Politics(h=1e-1,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=0.5 * 1e-1,
                                bar_title="down",
                                Reverse=False,
                                color='okgreen'), filemane_to_dump_down

    args_up = params, Politics(h=1e-1,
                                inside_args_area=inside_args_area,
                                args_updater=mass_updater_down,
                                h_limit=1e-3,
                                bar_title="up",
                                Reverse=True,
                                color='okgreen'), filemane_to_dump_up

    WORKERS_COUNT = cpu_count()
    log(f"MAIN PROCESS CREATE POOL WITH {WORKERS_COUNT} workers", 'header')

    is_over_down, is_over_up = Value("i", 0), Value("i", 0)

    main_process_down = Process(target=calcline_wrap, args=(is_over_down, args_down))
    main_process_up = Process(target=calcline_wrap, args=(is_over_up, args_up))

    main_process_down.start()
    main_process_up.start()

    with Pool(WORKERS_COUNT) as pool:
        spawn_horizontal_lines(filemane_to_dump_down, is_over_down, pool)
        spawn_horizontal_lines(filemane_to_dump_up, is_over_up, pool)

        main_process_down.join()
        main_process_up.join()

        log(f"WAIT POOL", 'header'); pool.close(); pool.join()
        log(f"DONE", 'header')

if __name__ == "__main__":
    main()
