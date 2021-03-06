from _Environment import Environment
from _Operation import *


def init(**kwargs) -> None:
    pass


def migrate_current_day(**kwargs) -> None:
    pass


def simulate_current_day(e: Environment, **kwargs) -> None:
    for op in e.get_current_day_info().get_request_operation_list():
        vm = op.get_vm()

        if isinstance(op, DeploySingleVMOperation):
            server_config_dict = vm.get_vm_config().get_capable_server_type_dict()
            server_config = list(server_config_dict.values())[0]
            server = e.op_purchase_server(server_config=server_config)
            e.op_deploy_single_vm(op=op, server=server, node='A')

        elif isinstance(op, DeployDoubleVMOperation):
            server_config_dict = vm.get_vm_config().get_capable_server_type_dict()
            server_config = list(server_config_dict.values())[0]
            server = e.op_purchase_server(server_config=server_config)
            e.op_deploy_double_vm(op=op, server=server)

        elif isinstance(op, RemoveSingleVMOperation):
            e.op_remove_vm(op=op)

        elif isinstance(op, RemoveDoubleVMOperation):
            e.op_remove_vm(op=op)
