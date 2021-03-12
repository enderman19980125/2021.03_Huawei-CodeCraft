import numpy as np
import data
import operations


def buy_server_randomly(vm: data.VM) -> data.Server:
    n_server_types = len(data.Server_Config_Dict)
    server_types_list = list(data.Server_Config_Dict.keys())
    while True:
        k = np.random.randint(0, n_server_types)
        k = server_types_list[k]
        server_config = data.Server_Config_Dict[k]
        if operations.has_capacity(server_config=server_config, server_node='A', vm=vm):
            server_id = operations.purchase_server(server_config=server_config)
            server = data.Server_Dict[server_id]
            return server


def start():
    if data.IS_DEBUG:
        print('Start simulations ...')

    capable_servers_list = []

    total_capacity_list = [0]

    for day_id, day_request_list in enumerate(operations.day_request_generator()):
        if data.IS_DEBUG and day_id % 50 == 0:
            print(f'Start day {day_id} ...')
            print(f'Money = {data.Total_Cost}')

        capacity = 0
        for request in day_request_list:
            vm = request.vm
            capacity += vm.config.cpu * vm.config.memory
            if request.operation == 'add':
                is_ok = False
                while True:
                    for server in capable_servers_list:
                        if operations.has_capacity(server=server, server_node='A', vm=vm):
                            operations.deploy_vm(vm=vm, server=server, server_node='A')
                            is_ok = True
                        elif operations.has_capacity(server=server, server_node='B', vm=vm):
                            operations.deploy_vm(vm=vm, server=server, server_node='B')
                            is_ok = True
                        else:
                            capable_servers_list.remove(server)
                    if is_ok:
                        break
                    else:
                        server = buy_server_randomly(vm)
                        capable_servers_list.append(server)
            else:
                operations.delete_vm(vm=vm)

        total_capacity_list.append(capacity)

    min_basic_unit_cost = min([s.cost_basic / s.cpu / s.memory for s in data.Server_Config_Dict.values()])
    min_day_unit_cost = min([s.cost_day / s.cpu / s.memory for s in data.Server_Config_Dict.values()])
    total_cost = 0
    for i in range(1, len(total_capacity_list)):
        if total_capacity_list[i - 1] < total_capacity_list[i]:
            total_cost += min_basic_unit_cost * (total_capacity_list[i] - total_capacity_list[i - 1])
        total_cost += min_day_unit_cost * total_capacity_list[i]
    print()
