from _ServerConfig import ServerConfig
from _Environment import Environment
from _Operation import *


def init(**kwargs) -> None:
    pass


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


def server_config_cost(e: Environment, server_config: ServerConfig) -> float:
    return server_config.get_cost_purchase() + \
           1.0 * server_config.get_cost_everyday() * (e.get_total_days() - e.get_current_day())


def purchase_server(e: Environment, vm: Union[SingleVM, DoubleVM]) -> Server:
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


def simulate_current_day(e: Environment, **kwargs) -> None:
    for op in e.get_current_day_info().get_request_operation_list():
        vm = op.get_vm()

        if isinstance(op, DeploySingleVMOperation):
            for server in e.get_deployed_server_dict().values():
                if server.has_capacity_for_single_vm(vm=vm, node='A'):
                    e.op_deploy_single_vm(op=op, server=server, node='A')
                    break
                if server.has_capacity_for_single_vm(vm=vm, node='B'):
                    e.op_deploy_single_vm(op=op, server=server, node='B')
                    break

            if op.get_server() is None:
                for server in e.get_non_deployed_server_dict().values():
                    if server.has_capacity_for_single_vm(vm=vm, node='A'):
                        e.op_deploy_single_vm(op=op, server=server, node='A')
                        break
                    if server.has_capacity_for_single_vm(vm=vm, node='B'):
                        e.op_deploy_single_vm(op=op, server=server, node='B')
                        break

            if op.get_server() is None:
                server = purchase_server(e=e, vm=vm)
                e.op_deploy_single_vm(op=op, server=server, node='A')

        elif isinstance(op, DeployDoubleVMOperation):
            for server in e.get_deployed_server_dict().values():
                if server.has_capacity_for_double_vm(vm=vm):
                    e.op_deploy_double_vm(op=op, server=server)
                    break

            if op.get_server() is None:
                for server in e.get_non_deployed_server_dict().values():
                    if server.has_capacity_for_double_vm(vm=vm):
                        e.op_deploy_double_vm(op=op, server=server)
                        break
                    if server.has_capacity_for_double_vm(vm=vm):
                        e.op_deploy_double_vm(op=op, server=server)
                        break

            if op.get_server() is None:
                server = purchase_server(e=e, vm=vm)
                e.op_deploy_double_vm(op=op, server=server)

        elif isinstance(op, RemoveSingleVMOperation):
            e.op_remove_vm(op=op)

        elif isinstance(op, RemoveDoubleVMOperation):
            e.op_remove_vm(op=op)
