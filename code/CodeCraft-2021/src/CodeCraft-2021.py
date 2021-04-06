from _Reader import Reader
from _Writer import Writer
from _Environment import Environment
import DataIO
import Simulation
import time


def main(is_debug: bool = False, read_mode: str = 'console', filename: str = '',
         is_write_day_info: bool = False, is_write_day_operation: bool = True):
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

    for day_id in range(1, num_total_days + 1):
        Simulation.simulate(e=e, day=day_id)
        e.finish_current_day()

        if is_write_day_info:
            DataIO.write_day_info(w=w, e=e, day=day_id)
        if is_write_day_operation:
            DataIO.write_day_operation(w=w, e=e, day=day_id)

        day_data_id += 1
        if day_data_id <= num_total_days:
            DataIO.read_day_request(r=r, e=e, day=day_data_id)


if __name__ == "__main__":
    # main()

    if True:
        t1 = time.time()
        main(is_debug=False, read_mode='file', filename='../../../data/training-1.txt',
             is_write_day_info=False, is_write_day_operation=True)
        # main(is_debug=True, read_mode='file', filename='../../../data/training-2.txt',
        #      is_write_day_info=True, is_write_day_operation=True)
        t2 = time.time()
        print(f'Time = {t2 - t1:.2f}s')
