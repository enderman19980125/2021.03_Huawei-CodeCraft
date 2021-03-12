import data


def day_request_generator() -> list:
    for day_request_list in data.Request_List:
        if data.IS_DEBUG:
            for server in data.Server_Dict.values():
                data.Total_Cost += server.config.cost_day
        data.Operation_List.append(data.DayOperation())
        yield day_request_list


def has_capacity(server: data.Server = None, server_config: data.ServerConfig = None, server_node: str = None,
                 vm: data.VM = None, vm_config: data.VMConfig = None) -> bool:
    """
    Check whether the Server has capacity for the VM.
    You must pass the value for 'server' or 'server_config'. If both of 'server' and 'server_config' are set, 'server' will be used.
    'vm' and 'vm_config' work for the same principle.
    :param server: A Server instance.
    :param server_config:A ServerConfig instance.
    :param server_node: The server node must be 'A', 'B'. If the VM is deployed on both nodes 'AB', the value will be ignored.
    :param vm: A VM instance.
    :param vm_config: A VMConfig instance.
    :return: Whether the Server has capacity for the VM.
    """
    if vm:
        vm_config = vm.config
    if server is None and server_config is None:
        raise ValueError('You must specify a Server or a ServerConfig.')
    if vm_config is None:
        raise ValueError('You must specify a VM or a VMConfig.')
    if vm_config.is_double:
        server_node = None
    if server_node not in [None, 'A', 'B']:
        raise ValueError('The server node must be "A" or "B".')
    if not vm_config.is_double and server_node not in ['A', 'B']:
        raise ValueError('You must specify the server node.')

    if server:
        if vm_config.is_double:
            return min(server.A_cpu_rest, server.B_cpu_rest) >= (vm_config.cpu / 2) and \
                   min(server.A_memory_rest, server.B_memory_rest) >= (vm_config.memory / 2)
        elif server_node == 'A':
            return server.A_cpu_rest >= vm_config.cpu and server.A_memory_rest >= vm_config.memory
        else:
            return server.B_cpu_rest >= vm_config.cpu and server.B_memory_rest >= vm_config.memory
    else:
        if vm_config.is_double:
            return (server_config.cpu / 2) >= (vm_config.cpu / 2) and (server_config.memory / 2) >= (vm_config.memory / 2)
        else:
            return (server_config.cpu / 2) >= vm_config.cpu and (server_config.memory / 2) >= vm_config.memory


def purchase_server(server_config: data.ServerConfig) -> str:
    """
    Add a new Server with the specific config.
    :param server_config: A ServerConfig instance.
    :return: The server id.
    """
    server_id = f'S{len(data.Server_Dict)}'
    server = data.Server(server_id=server_id, config=server_config)
    data.Server_Dict[server_id] = server
    data.Operation_List[-1].purchase.append(server)
    data.Total_Cost += server.config.cost_basic
    return server_id


def get_first_capable_server(vm: data.VM = None, vm_config: data.VMConfig = None) -> tuple:
    """
    Get the first server which has capacity for the specific VM or VMConfig.
    You must pass the value for 'vm' or 'vm_config'. If both of 'vm' and 'vm_config' are set, 'vm' will be used.
    :param vm: A VM instance.
    :param vm_config: A VMConfig instance.
    :return: A list of capable servers.
    For double-node VM, the return value is like (Server_1, None)
    For single-node VM, the return value is like (Server_1, 'A')
    """
    if vm is None and vm_config is None:
        raise ValueError('You must specify a VM or a VMConfig.')
    if vm:
        vm_config = vm.config

    for server in data.Server_Dict.values():
        if vm.config.is_double:
            if has_capacity(server=server, vm_config=vm_config):
                return server, None
        else:
            if has_capacity(server=server, server_node='A', vm_config=vm_config):
                return server, 'A'
            if has_capacity(server=server, server_node='A', vm_config=vm_config):
                return server, 'B'

    return None, None


def get_all_capable_servers_list(vm: data.VM = None, vm_config: data.VMConfig = None) -> list:
    """
    Get a list of servers which have capacity for the specific VM or VMConfig.
    You must pass the value for 'vm' or 'vm_config'. If both of 'vm' and 'vm_config' are set, 'vm' will be used.
    :param vm: A VM instance.
    :param vm_config: A VMConfig instance.
    :return: A list of capable servers.
    For double-node VM, the return value is like [(Server_1, None), (Server_2, None), (Server_3, None), ...]
    For single-node VM, the return value is like [(Server_1, 'A'), (Server_1, 'B'), (Server_3, 'A'), ...]
    """
    if vm is None and vm_config is None:
        raise ValueError('You must specify a VM or a VMConfig.')
    if vm:
        vm_config = vm.config

    capable_servers_list = []
    for server in data.Server_Dict.values():
        if vm.config.is_double:
            if has_capacity(server=server, vm_config=vm_config):
                capable_servers_list.append((server, None))
        else:
            if has_capacity(server=server, server_node='A', vm_config=vm_config):
                capable_servers_list.append((server, 'A'))
            if has_capacity(server=server, server_node='A', vm_config=vm_config):
                capable_servers_list.append((server, 'B'))

    return capable_servers_list


def deploy_vm(vm: data.VM, server: data.Server, server_node: str = None) -> None:
    """
    Deploy the specific VM on the specific Server.
    :param vm: A VM instance.
    :param server: A Server instance.
    :param server_node: The value must be 'A' or 'B'. If the VM is deployed on both nodes 'AB', the value will be ignored.
    :return: None.
    """
    if not vm.config.is_double and server_node not in ['A', 'B']:
        raise ValueError('You must specify the server node.')
    if not has_capacity(server=server, server_node=server_node, vm=vm):
        raise ValueError('The Server has no capacity for the VM.')

    if vm.config.is_double:
        server.A_cpu_rest -= vm.config.cpu / 2
        server.B_cpu_rest -= vm.config.cpu / 2
        server.A_memory_rest -= vm.config.memory / 2
        server.B_memory_rest -= vm.config.memory / 2
        server.AB_vm.append(vm)
        vm.server = server
        deploy = data.Deploy(vm=vm, to_server=server)
        data.Operation_List[-1].deploy.append(deploy)
    elif server_node == 'A':
        server.A_cpu_rest -= vm.config.cpu
        server.A_memory_rest -= vm.config.memory
        server.A_vm.append(vm)
        vm.server = server
        vm.node = 'A'
        deploy = data.Deploy(vm=vm, to_server=server, to_node='A')
        data.Operation_List[-1].deploy.append(deploy)
    else:
        server.B_cpu_rest -= vm.config.cpu
        server.B_memory_rest -= vm.config.memory
        server.B_vm.append(vm)
        vm.server = server
        vm.node = 'B'
        deploy = data.Deploy(vm=vm, to_server=server, to_node='B')
        data.Operation_List[-1].deploy.append(deploy)


def delete_vm(vm: data.VM) -> None:
    """
    Delete the specific VM.
    :param vm: A VM instance.
    :return: None.
    """
    server = vm.server

    if vm.config.is_double:
        server.A_cpu_rest += vm.config.cpu / 2
        server.B_cpu_rest += vm.config.cpu / 2
        server.A_memory_rest += vm.config.memory / 2
        server.B_memory_rest += vm.config.memory / 2
        server.AB_vm.remove(vm)
    elif vm.node == 'A':
        server.A_cpu_rest += vm.config.cpu
        server.A_memory_rest += vm.config.memory
        server.A_vm.remove(vm)
    else:
        server.B_cpu_rest += vm.config.cpu
        server.B_memory_rest += vm.config.memory
        server.B_vm.remove(vm)

    vm.server = None
    vm.node = None
