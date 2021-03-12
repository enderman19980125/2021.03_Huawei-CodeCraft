import data
import data_io
import theory
import simulations


def main():
    if data.IS_DEBUG:
        import time
        t1 = time.time()
    data_io.read_data()
    # simulations.start()
    theory.start()

    if data.IS_DEBUG:
        import time
        t2 = time.time()
        print(f'Money = {data.Total_Cost}')
        print(f'Time = {t2 - t1}')
    else:
        data_io.write_data()


if __name__ == "__main__":
    main()
