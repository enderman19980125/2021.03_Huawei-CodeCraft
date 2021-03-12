import data


def get_line_from_file() -> str:
    with open('../../../data/training-1.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        yield line


def get_line_from_console() -> str:
    while True:
        line = input()
        yield line


get_line = get_line_from_file()


def clear_data():
    data.Servers_Parameter_Dict = {}
    data.VM_Parameter_Dict = {}
    data.Requests_List = []
    data.VM_Info_Dict = {}
    data.Machines_Info_List = []
    data.Operations_List = []


def read_data():
    data.Server_Config_Dict = {}
    n_servers = int(next(get_line))
    for _ in range(n_servers):
        server_str = next(get_line).strip('(').strip(')').replace(' ', '')
        server_item_list = server_str.split(',')
        server_type = server_item_list[0]
        data.Server_Config_Dict[server_type] = data.ServerConfig(
            server_type=server_type,
            cpu=int(server_item_list[1]),
            memory=int(server_item_list[2]),
            cost_basic=int(server_item_list[3]),
            cost_day=int(server_item_list[4]),
        )

    data.VM_Config_Dict = {}
    n_vm = int(next(get_line))
    for _ in range(n_vm):
        vm_str = next(get_line).strip('(').strip(')').replace(' ', '')
        vm_item_list = vm_str.split(',')
        vm_type = vm_item_list[0]
        data.VM_Config_Dict[vm_type] = data.VMConfig(
            vm_type=vm_type,
            cpu=int(vm_item_list[1]),
            memory=int(vm_item_list[2]),
            is_double=bool(int(vm_item_list[3])),
        )

    data.Request_List = []
    n_days = int(next(get_line))
    for _ in range(n_days):
        requests_day_list = []
        n_requests = int(next(get_line))
        for _ in range(n_requests):
            request_str = next(get_line).strip('(').strip(')').replace(' ', '')
            request_item_list = request_str.split(',')
            operation = request_item_list[0]
            if operation == 'add':
                vm_type = request_item_list[1]
                vm_id = request_item_list[2]
                requests_day_list
                request_item = {
                    'op': request_item_list[0],
                    'vm_type': vm_type,
                    'vm_id': vm_id,
                }
                data.VM_Info_Dict[vm_id] = {
                    'vm_type': vm_type,
                    'machine_id': -1,
                    'node': '',
                }
            else:
                vm_id = request_item_list[1]
                requests_day_list.append(data.Request(
                    operation=operation,
                    vm_id=vm_id,
                ))
        data.Request_List.append(requests_day_list)
