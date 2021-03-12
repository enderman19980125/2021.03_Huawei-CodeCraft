import data


def get_line_from_file_1() -> str:
    with open('../../../data/training-1.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        yield line


def get_line_from_file_2() -> str:
    with open('../../../data/training-2.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        yield line


def get_line_from_console() -> str:
    while True:
        line = input()
        yield line


def clear_data() -> None:
    data.Server_Config_Dict = {}
    data.VM_Config_Dict = {}
    data.VM_Dict = {}
    data.Server_Dict = {}
    data.Request_List = []
    data.Operation_List = []


def read_data() -> None:
    if data.IS_DEBUG:
        print('Reading data ...')

    clear_data()
    if data.READ_MODE == 'file-1':
        get_line = get_line_from_file_1()
    elif data.READ_MODE == 'file-2':
        get_line = get_line_from_file_2()
    else:
        get_line = get_line_from_console()

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
                vm_config = data.VM_Config_Dict[vm_type]
                vm = data.VM(vm_id=vm_id, config=vm_config)
                data.VM_Dict[vm_id] = vm
                requests_day_list.append(data.Request(
                    operation=operation,
                    vm=vm,
                    vm_config=vm_config
                ))
            else:
                vm_id = request_item_list[1]
                vm = data.VM_Dict[vm_id]
                requests_day_list.append(data.Request(
                    operation=operation,
                    vm=vm,
                ))
        data.Request_List.append(requests_day_list)


def write_data() -> None:
    if data.IS_DEBUG:
        print('Writing data ...')

    server_mapping_dict = {}  # key=server_id:str, value=output_server_id:int

    for day_operation in data.Operation_List:

        server_day_dict = {}  # key=server_type:str, value=[Server_1, Server_2, Server_3, ...]
        for server in day_operation.purchase:
            server_type = server.config.type
            if server_type in server_day_dict.keys():
                server_day_dict[server_type].append(server)
            else:
                server_day_dict[server_type] = [server]

        q = len(server_day_dict)
        print(f'(purchase, {q})')

        for server_type, servers_list in server_day_dict.items():
            for server in servers_list:
                server_id = server.id
                output_server_id = len(server_mapping_dict)
                server_mapping_dict[server_id] = output_server_id
            num_servers = len(servers_list)
            print(f'({server_type}, {num_servers})')

        # TODO: migrate
        w = len(day_operation.migration)
        print(f'(migration, {w})')

        for deploy in day_operation.deploy:
            server_id = deploy.to_server.id
            server_node = deploy.to_node
            output_server_id = server_mapping_dict[server_id]
            if server_node:
                print(f'({output_server_id}, {server_node})')
            else:
                print(f'({output_server_id})')
