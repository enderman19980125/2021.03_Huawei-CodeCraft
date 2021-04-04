from _Reader import Reader
from _Writer import Writer
from _Environment import Environment
import DataIO
import Simulation
import time


def main(is_debug: bool):
    t1 = time.time()

    if is_debug:
        r = Reader(mode='file', filename='../../../data/training-1.txt')
    else:
        r = Reader(mode='console')

    w = Writer(is_console=True, is_file=False)
    e = Environment()

    DataIO.read_server_config(r=r, e=e)
    DataIO.read_vm_config(r=r, e=e)
    num_total_days, num_next_days = map(int, next(r.get_next_line).split(' '))
    day_data_id = 0
    for day_data_id in range(1, num_next_days + 1):
        DataIO.read_day_request(r=r, e=e, day=day_data_id)

    for day_id in range(1, num_total_days + 1):
        day_data_id += 1
        Simulation.simulate(e=e, day=day_id)
        DataIO.write_day_operation(w=w, e=e, day=day_id)
        if day_data_id <= num_total_days:
            DataIO.read_day_request(r=r, e=e, day=day_data_id)

    t2 = time.time()
    if is_debug:
        w.write(content=f'Time = {t2 - t1:.2f}s')


if __name__ == "__main__":
    main(is_debug=False)
