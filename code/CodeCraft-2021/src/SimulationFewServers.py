from _Environment import Environment
from _Operation import *
import random

All_Capable_Server_Type_List = []


def init(e: Environment) -> None:
    global All_Capable_Server_Type_List
    All_Capable_Server_Type_List = list(e.get_server_config_dict().keys())

    for vm_type, vm_config in e.get_vm_config_dict().items():
        for server_type in All_Capable_Server_Type_List:
            if server_type not in vm_config.get_capable_server_type_dict().keys():
                All_Capable_Server_Type_List.remove(server_type)


def simulate_current_day(e: Environment) -> None:
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
                server_type = random.choice(All_Capable_Server_Type_List)
                server_config = e.get_server_config_by_type(server_type=server_type)
                server = e.op_purchase_server(server_config=server_config)
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
                server_type = random.choice(All_Capable_Server_Type_List)
                server_config = e.get_server_config_by_type(server_type=server_type)
                server = e.op_purchase_server(server_config=server_config)
                e.op_deploy_double_vm(op=op, server=server)

        elif isinstance(op, RemoveSingleVMOperation):
            e.op_remove_vm(op=op)

        elif isinstance(op, RemoveDoubleVMOperation):
            e.op_remove_vm(op=op)
