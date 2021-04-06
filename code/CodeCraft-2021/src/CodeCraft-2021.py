import time
from _Reader import Reader
from _Writer import Writer
from _Environment import Environment
import DataIO
# import SimulationNaive as Simulation
import SimulationFewServers as Simulation


def main(is_debug: bool = False, read_mode: str = 'console', filename: str = '',
         is_write_day_info: bool = False, is_write_day_operation: bool = True) -> int:
    r = Reader(mode=read_mode, filename=filename)
    w = Writer(is_console=True, is_file=False)
    e = Environment()
    e.set_debug(is_debug=is_debug)

    DataIO.read_server_config(r=r, e=e)
    DataIO.read_vm_config(r=r, e=e)
    num_total_days, num_next_days = map(int, next(r.get_next_line).split(' '))
    day_data_id = 0
    for day_data_id in range(1, num_next_days + 1):
        DataIO.read_day_request(r=r, e=e, day=day_data_id)

    Simulation.init(e=e)

    for day_id in range(1, num_total_days + 1):
        Simulation.simulate_current_day(e=e, day=day_id)
        e.finish_current_day()

        if is_write_day_info:
            DataIO.write_day_info(w=w, e=e, day=day_id)
        if is_write_day_operation:
            DataIO.write_day_operation(w=w, e=e, day=day_id)

        day_data_id += 1
        if day_data_id <= num_total_days:
            DataIO.read_day_request(r=r, e=e, day=day_data_id)

    return e.eval_get_accumulated_total_cost()


def main_submit() -> None:
    main()


def main_run() -> None:
    time_start = time.time()
    cost_1 = main(read_mode='file', filename='../../../data/training-1.txt')
    time_finish = time.time()
    time_1 = time_finish - time_start

    time_start = time.time()
    cost_2 = main(read_mode='file', filename='../../../data/training-2.txt')
    time_finish = time.time()
    time_2 = time_finish - time_start

    cost_total = cost_1 + cost_2
    print(f'Time_1 = {time_1:.2f}s\tCost_1 = {cost_1}')
    print(f'Time_2 = {time_2:.2f}s\tCost_2 = {cost_2}')
    print(f'Total Cost = {cost_total}')


def main_debug() -> None:
    time_start = time.time()
    cost_1 = main(is_debug=True, read_mode='file', filename='../../../data/training-1.txt',
                  is_write_day_info=True, is_write_day_operation=True)
    time_finish = time.time()
    time_1 = time_finish - time_start

    time_start = time.time()
    cost_2 = main(is_debug=True, read_mode='file', filename='../../../data/training-2.txt',
                  is_write_day_info=True, is_write_day_operation=True)
    time_finish = time.time()
    time_2 = time_finish - time_start

    cost_total = cost_1 + cost_2
    print(f'Time_1 = {time_1:.2f}s\tCost_1 = {cost_1}')
    print(f'Time_2 = {time_2:.2f}s\tCost_2 = {cost_2}')
    print(f'Total Cost = {cost_total}')


if __name__ == "__main__":
    # main_submit()
    # main_run()
    main_debug()
