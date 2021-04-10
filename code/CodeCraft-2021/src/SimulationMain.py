from _ServerConfig import ServerConfig
from _Environment import Environment
from _Operation import *
from typing import Tuple, List


# --------------------------------    initialize    --------------------------------

def init(**kwargs) -> None:
    pass


# --------------------------------    migrate    --------------------------------

def migrate_vm(e: Environment, vm: Union[SingleVM, DoubleVM], current_server: Server) -> int:
    if isinstance(vm, SingleVM):
        for server in e.get_deployed_server_dict().values():
            if server == current_server:
                continue
            if server.has_capacity_for_single_vm(vm=vm, node='A'):
                e.op_migrate_single_vm(vm=vm, new_server=server, node='A')
                return 1
            if server.has_capacity_for_single_vm(vm=vm, node='B'):
                e.op_migrate_single_vm(vm=vm, new_server=server, node='B')
                return 1

    if isinstance(vm, DoubleVM):
        for server in e.get_deployed_server_dict().values():
            if server == current_server:
                continue
            if server.has_capacity_for_double_vm(vm=vm):
                e.op_migrate_double_vm(vm=vm, new_server=server)
                return 1

    return 0


def migrate_current_day(e: Environment, **kwargs) -> None:
    return
    # server_id_num_vm_list = [(server.get_server_id(), server.get_num_vm_of_both_nodes())
    #                          for server in e.get_deployed_server_dict().values()]
    #
    # server_id_num_vm_list.sort(key=lambda t: t[1])
    #
    # num_total_vm = sum([t[1] for t in server_id_num_vm_list])
    # num_migrations = 0
    # max_migrations = num_total_vm * 3 // 100
    #
    # for server_id, num_vm in server_id_num_vm_list:
    #     server = e.get_server_by_id(server_id=server_id)
    #     for vm in server.get_vm_dict_of_node_a().copy().values():
    #         num_migrations += migrate_vm(e=e, vm=vm, current_server=server)
    #         if num_migrations == max_migrations:
    #             break
    #     if num_migrations == max_migrations:
    #         break


# --------------------------------    position    --------------------------------

def server_cost_s(vm: SingleVM, server: Server, node: str) -> float:
    p = 1.0
    if node == 'A':
        return p * server.get_rest_cpu_of_node_a() + server.get_rest_memory_of_node_a() + \
               - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()
    else:
        return p * server.get_rest_cpu_of_node_b() + server.get_rest_cpu_of_node_b() + \
               - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()


def server_cost_d(vm: DoubleVM, server: Server) -> float:
    p = 1.0
    return p * max(server.get_rest_cpu_of_node_a(), server.get_rest_cpu_of_node_b()) + \
           max(server.get_rest_memory_of_node_a(), server.get_rest_memory_of_node_b()) + \
           - p * vm.get_cpu_of_one_node() - vm.get_memory_of_one_node()


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
    if e.get_current_day() / e.get_total_days() < 0.2:
        return server_config.get_cost_everyday()
    elif e.get_current_day() / e.get_total_days() < 0.8:
        return server_config.get_cost_purchase() + \
               server_config.get_cost_everyday() * (e.get_total_days() - e.get_current_day())
    else:
        return server_config.get_cost_purchase()


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
