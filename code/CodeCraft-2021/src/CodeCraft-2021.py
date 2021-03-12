import data
import data_io


def main():
    data_io.clear_data()
    data_io.read_data()
    s = data.Servers_Parameter_Dict
    vm = data.VM_Parameter_Dict
    r = data.Requests_List
    print()


if __name__ == "__main__":
    main()
