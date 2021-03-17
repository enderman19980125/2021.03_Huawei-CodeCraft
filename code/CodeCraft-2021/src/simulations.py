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
    capable_servers_list = []

    for day_id, day_request_list in enumerate(operations.day_request_generator()):
        for request in day_request_list:
            vm = request.vm
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

        if data.IS_DEBUG:
            print(f'-------------------------------- DAY {day_id} --------------------------------')

            cpu_rest = []
            memory_rest = []

            for server in data.Server_Dict.values():
                cpu_rest.append(f'({server.A_cpu_rest},{server.B_cpu_rest})')
                memory_rest.append(f'({server.A_memory_rest},{server.B_memory_rest})')
                # print(f'Sever #{server.id:<5s}    type={server.config.type}    '
                #       f'A_rest=({server.A_cpu_rest:3d}C,{server.A_memory_rest:3d})    '
                #       f'B_rest=({server.B_cpu_rest:3d}C,{server.B_memory_rest:3d})')

            n_servers = len(data.Server_Dict)
            day_cost_purchase = data.COST_PURCHASE[-1]
            day_cost_maintain = data.COST_MAINTAIN[-1]
            # print(f'n_servers={n_servers}')
            print(f'cpu_rest={",".join(cpu_rest)}')
            print(f'memory_rest={",".join(memory_rest)}')
            # print(f'day_cost_purchase={day_cost_purchase}    day_cost_maintain={day_cost_maintain}    Money = {data.COST_TOTAL}')
            # print(f'{day_id}\t{n_servers}\t{day_cost_purchase}\t{day_cost_maintain}')
