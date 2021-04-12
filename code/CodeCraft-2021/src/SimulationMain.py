from _ServerConfig import ServerConfig
from _Environment import Environment
from _Operation import *
from typing import Tuple, List


# --------------------------------    initialize    --------------------------------

def init(**kwargs) -> None:
    pass


# --------------------------------    migrate    --------------------------------

def migrate_vm(e: Environment, vm: Union[SingleVM, DoubleVM], current_server: Server,
               available_server_list: List[Server]) -> int:
    if isinstance(vm, SingleVM):
        for server in available_server_list:
            if server == current_server:
                continue
            if server.has_capacity_for_single_vm(vm=vm, node='A'):
                e.op_migrate_single_vm(vm=vm, new_server=server, node='A')
                return 1
            if server.has_capacity_for_single_vm(vm=vm, node='B'):
                e.op_migrate_single_vm(vm=vm, new_server=server, node='B')
                return 1

    if isinstance(vm, DoubleVM):
        for server in available_server_list:
            if server == current_server:
                continue
            if server.has_capacity_for_double_vm(vm=vm):
                e.op_migrate_double_vm(vm=vm, new_server=server)
                return 1

    return 0


def migrate_current_day(e: Environment, **kwargs) -> None:
    server_dict_dict = {
        server: {
            'server': server,
            'num_del_op': 0,
            'num_vm': server.get_num_vm_of_node_a() + server.get_num_vm_of_node_b(),
            'key': server.get_used_cpu_of_node_a() + server.get_used_cpu_of_node_b() + \
                   server.get_used_memory_of_node_a() + server.get_used_memory_of_node_b(),
        }
        for server in e.get_deployed_server_dict().values()
    }

    for remove_op in e.get_current_day_info().get_del_vm_operation_list():
        server_dict_dict[remove_op.get_vm().get_server()]['num_del_op'] += 1

    for server, server_dict in server_dict_dict.items():
        server_dict_dict[server]['key'] += server.get_num_vm_of_node_a() + server.get_num_vm_of_node_b() + \
                                           -server_dict_dict[server]['num_del_op']

    server_dict_list = list(server_dict_dict.values())
    server_dict_list.sort(key=lambda sd: sd['key'], reverse=False)

    num_total_vm = sum([sd['num_vm'] for sd in server_dict_list])
    num_migrations = 0
    max_migrations = num_total_vm * 3 // 100
    available_server_list = [sd['server'] for sd in server_dict_list]
    available_server_list.reverse()

    for server_dict in server_dict_list:
        server = server_dict['server']
        available_server_list.remove(server)

        for vm in server.get_vm_dict_of_node_a().copy().values():
            num_migrations += migrate_vm(e=e, vm=vm, current_server=server, available_server_list=available_server_list)
            if num_migrations == max_migrations:
                return

        for vm in server.get_vm_dict_of_node_b().copy().values():
            num_migrations += migrate_vm(e=e, vm=vm, current_server=server, available_server_list=available_server_list)
            if num_migrations == max_migrations:
                return


# --------------------------------    position    --------------------------------

def server_cost_s(vm: SingleVM, server: Server, node: str) -> float:
    p = 1.0

    # if node == 'A':
    #     return p * server.get_rest_cpu_of_node_a() + server.get_rest_memory_of_node_a() + \
    #            - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()
    # elif node == 'B':
    #     return p * server.get_rest_cpu_of_node_b() + server.get_rest_cpu_of_node_b() + \
    #            - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()
    # else:
    #     raise KeyError(f'"node" must be "A" or "B".')

    if node == 'A':
        return server.get_rest_cpu_of_node_a() + server.get_rest_memory_of_node_a()
    elif node == 'B':
        return server.get_rest_cpu_of_node_b() + server.get_rest_cpu_of_node_b()
    else:
        raise KeyError(f'"node" must be "A" or "B".')


def server_cost_d(vm: DoubleVM, server: Server) -> float:
    p = 1.0

    # return p * min(server.get_rest_cpu_of_node_a(), server.get_rest_cpu_of_node_b()) + \
    #        min(server.get_rest_memory_of_node_a(), server.get_rest_memory_of_node_b()) + \
    #        - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()

    return server.get_rest_cpu_of_node_a() + server.get_rest_cpu_of_node_b() + \
           server.get_rest_memory_of_node_a() + server.get_rest_memory_of_node_b()


def select_running_server_for_single_vm(e: Environment, vm: SingleVM) -> Tuple[Optional[Server], Optional[str]]:
    target_server = None
    target_node = None

    for server in e.get_deployed_server_dict().values():
        if server.has_capacity_for_single_vm(vm=vm, node='A'):
            if target_server is None or server_cost_s(vm, server, 'A') < server_cost_s(vm, target_server, 'A'):
                target_server, target_node = server, 'A'
        if server.has_capacity_for_single_vm(vm=vm, node='B'):
            if target_server is None or server_cost_s(vm, server, 'B') < server_cost_s(vm, target_server, 'B'):
                target_server, target_node = server, 'B'

    return target_server, target_node


def select_idle_server_for_single_vm(e: Environment, vm: SingleVM) -> Tuple[Optional[Server], Optional[str]]:
    target_server = None
    target_node = None

    for server in e.get_non_deployed_server_dict().values():
        if server.has_capacity_for_single_vm(vm=vm, node='A'):
            if target_server is None or server_cost_s(vm, server, 'A') < server_cost_s(vm, target_server, 'A'):
                target_server, target_node = server, 'A'

    return target_server, target_node


def select_running_server_for_double_vm(e: Environment, vm: DoubleVM) -> Optional[Server]:
    target_server = None

    for server in e.get_deployed_server_dict().values():
        if server.has_capacity_for_double_vm(vm=vm):
            if target_server is None or server_cost_d(vm, server) < server_cost_d(vm, target_server):
                target_server = server

    return target_server


def select_idle_server_for_double_vm(e: Environment, vm: DoubleVM) -> Optional[Server]:
    target_server = None

    for server in e.get_non_deployed_server_dict().values():
        if server.has_capacity_for_double_vm(vm=vm):
            if target_server is None or server_cost_d(vm, server) < server_cost_d(vm, target_server):
                target_server = server

    return target_server


# --------------------------------    purchase    --------------------------------

def server_config_cost(e: Environment, server_config: ServerConfig) -> float:
    return server_config.get_cost_purchase() + \
           server_config.get_cost_everyday() * (e.get_total_days() - e.get_current_day())

    # if e.get_current_day() / e.get_total_days() < 0.2:
    #     return server_config.get_cost_everyday()
    # elif e.get_current_day() / e.get_total_days() < 0.8:
    #     return server_config.get_cost_purchase() + \
    #            server_config.get_cost_everyday() * (e.get_total_days() - e.get_current_day())
    # else:
    #     return server_config.get_cost_purchase()


def purchase_the_best_server(e: Environment, vm: Union[SingleVM, DoubleVM]) -> Server:
    target_server_config = None

    for server_config in e.get_server_config_dict().values():
        if server_config not in vm.get_vm_config().get_capable_server_type_dict().values():
            continue
        if target_server_config is None:
            target_server_config = server_config
            continue
        if server_config_cost(e=e, server_config=server_config) < \
                server_config_cost(e=e, server_config=target_server_config):
            target_server_config = server_config

    server = e.op_purchase_server(server_config=target_server_config)
    return server


# --------------------------------    simulate    --------------------------------

def simulate_current_stage(e: Environment,
                           deploy_operations_list: List[Union[DeploySingleVMOperation, DeployDoubleVMOperation]],
                           **kwargs) -> None:
    deploy_operations_list.sort(
        key=lambda op: op.get_vm().get_cpu_of_one_node() + op.get_vm().get_memory_of_one_node(),
        reverse=True
    )

    for op in deploy_operations_list:
        vm = op.get_vm()

        if isinstance(op, DeploySingleVMOperation):
            server, node = select_running_server_for_single_vm(e=e, vm=vm)
            if server:
                e.op_deploy_single_vm(op=op, server=server, node=node)
                continue

            server, node = select_idle_server_for_single_vm(e=e, vm=vm)
            if server:
                e.op_deploy_single_vm(op=op, server=server, node=node)
                continue

            server = purchase_the_best_server(e=e, vm=vm)
            e.op_deploy_single_vm(op=op, server=server, node='A')

        elif isinstance(op, DeployDoubleVMOperation):
            server = select_running_server_for_double_vm(e=e, vm=vm)
            if server:
                e.op_deploy_double_vm(op=op, server=server)
                continue

            server = select_idle_server_for_double_vm(e=e, vm=vm)
            if server:
                e.op_deploy_double_vm(op=op, server=server)
                continue

            server = purchase_the_best_server(e=e, vm=vm)
            e.op_deploy_double_vm(op=op, server=server)


def simulate_current_day(e: Environment, **kwargs) -> None:
    deploy_operations_list = []

    for op in e.get_current_day_info().get_request_operation_list():
        if isinstance(op, RemoveSingleVMOperation) or isinstance(op, RemoveDoubleVMOperation):
            simulate_current_stage(e=e, deploy_operations_list=deploy_operations_list)
            deploy_operations_list.clear()
            e.op_remove_vm(op=op)
        else:
            deploy_operations_list.append(op)

    simulate_current_stage(e=e, deploy_operations_list=deploy_operations_list)
