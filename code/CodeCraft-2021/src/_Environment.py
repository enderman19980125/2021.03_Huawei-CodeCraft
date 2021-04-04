from _VMConfig import VMConfig
from _ServerConfig import ServerConfig
from _VM import SingleVM, DoubleVM
from _Operation import *
from typing import Dict


class Environment:
    def __init__(self):
        self.__blank_server_config = ServerConfig(server_type='0', cpu=0, memory=0, cost_purchase=0, cost_everyday=0)
        self.__blank_server = Server(server_id='0', server_config=self.__blank_server_config)

        self.__vm_config_dict = {}

        self.__non_deployed_vm_dict = {}
        self.__deployed_vm_dict = {}

        self.__server_config_dict = {'0': self.__blank_server_config}
        self.__server_dict = {'0': self.__blank_server}

        self.__current_day = 0
        self.__current_day_operation = DayOperation(day=0)
        self.__day_operation_dict = {0: DayOperation(day=0)}

    def get_current_day(self) -> int:
        return self.__current_day

    def get_current_day_operation(self) -> DayOperation:
        return self.__current_day_operation

    def get_day_operation_by_day(self, day: int) -> DayOperation:
        return self.__day_operation_dict[day]

    def get_vm_config_by_type(self, vm_type: str) -> VMConfig:
        vm_config = self.__vm_config_dict.get(vm_type)
        if vm_config is None:
            raise KeyError(f"The VMConfig[{vm_type}] doesn't exist.")
        return vm_config

    def get_vm_by_id(self, vm_id: str) -> Union[SingleVM, DoubleVM]:
        vm = self.__deployed_vm_dict.get(vm_id)
        if vm is None:
            vm = self.__non_deployed_vm_dict.get(vm_id)
        if vm is None:
            raise KeyError(f"The VM[{vm_id}] doesn't exist.")
        return vm

    def get_server_config_by_id(self, server_config_id: str) -> ServerConfig:
        server_config = self.__vm_config_dict.get(server_config_id)
        if server_config is None:
            raise KeyError(f"The ServerConfig[{server_config_id}] doesn't exist.")
        return server_config

    def get_server_by_id(self, server_id: str) -> Server:
        server = self.__server_dict.get(server_id)
        if server is None:
            raise KeyError(f"The Server[{server_id}] doesn't exist.")
        return server

    def get_vm_config_dict(self) -> Dict[str, VMConfig]:
        return self.__vm_config_dict

    def get_deployed_vm_dict(self) -> Dict[str, Union[SingleVM, DoubleVM]]:
        return self.__deployed_vm_dict

    def get_server_config_dict(self) -> Dict[str, ServerConfig]:
        return self.__server_config_dict

    def get_server_dict(self) -> Dict[str, Server]:
        return self.__server_dict

    def start_next_day(self) -> None:
        self.__current_day += 1
        self.__current_day_operation = self.__day_operation_dict[self.__current_day]

    def add_request_operation(self, day: int, op: Union[DeploySingleVMOperation, DeployDoubleVMOperation,
                                                        RemoveSingleVMOperation, RemoveDoubleVMOperation]):
        if day not in self.__day_operation_dict.keys():
            self.__day_operation_dict[day] = DayOperation(day=day)
        self.__day_operation_dict[day].add_request_operation(op=op)
        # if isinstance(op, DeploySingleVMOperation) or isinstance(op, DeployDoubleVMOperation):
        #     self.__day_operation_dict[day].add_deploy_vm_operation(op=op)
        # elif isinstance(op, RemoveSingleVMOperation) or isinstance(op, RemoveDoubleVMOperation):
        #     self.__day_operation_dict[day].add_remove_vm_operation(op=op)
        # else:
        #     raise KeyError(f"The operation is invalid.")

    def add_vm_config(self, vm_config: VMConfig) -> None:
        if vm_config.get_vm_type() in self.__vm_config_dict.keys():
            raise KeyError(f"The VMConfig[{vm_config.get_vm_type()}] already exists.")
        self.__vm_config_dict[vm_config.get_vm_type()] = vm_config

        for server_type, server_config in self.__server_config_dict.items():
            try:
                server_config.add_capable_vm_type(vm_config=vm_config)
                vm_config.add_capable_server_type(server_config=server_config)
            except KeyError:
                pass

    def add_server_config(self, server_config: ServerConfig) -> None:
        if server_config.get_server_type() in self.__server_config_dict.keys():
            raise KeyError(f"The ServerConfig[{server_config.get_server_type()}] already exists.")
        self.__server_config_dict[server_config.get_server_type()] = server_config

        for vm_type, vm_config in self.__vm_config_dict.items():
            try:
                server_config.add_capable_vm_type(vm_config=vm_config)
                vm_config.add_capable_server_type(server_config=server_config)
            except KeyError:
                pass

    def add_non_deployed_vm(self, vm: VM) -> None:
        if vm.get_vm_id() in self.__non_deployed_vm_dict.keys():
            raise KeyError(f"The VM[{vm.get_vm_id()}] already exists.")
        self.__non_deployed_vm_dict[vm.get_vm_id()] = vm

    def op_purchase_server(self, server_config: ServerConfig) -> Server:
        server_id = f'S{len(self.__server_dict)}'
        server = Server(server_id=server_id, server_config=server_config)
        self.__server_dict[server_id] = server
        server_config.add_server(server=server)

        op = PurchaseServerOperation(day=self.get_current_day(), server=server)
        server.add_operation(op=op)
        self.__current_day_operation.add_purchase_server_operation(op=op)

        return server

    def op_deploy_single_vm(self, op: DeploySingleVMOperation, server: Server, node: str) -> None:
        vm = op.get_vm()
        self.__non_deployed_vm_dict.pop(vm.get_vm_id())
        self.__deployed_vm_dict[vm.get_vm_id()] = vm

        server.deploy_single_vm_with_check(vm=vm, node=node)
        vm.deploy(server=server, node=node)

        op.set_server(server=server)
        op.set_node(node=node)
        vm.add_operation(op=op)

    def op_deploy_double_vm(self, op: DeployDoubleVMOperation, server: Server) -> None:
        vm = op.get_vm()
        self.__non_deployed_vm_dict.pop(vm.get_vm_id())
        self.__deployed_vm_dict[vm.get_vm_id()] = vm

        server.deploy_double_vm_with_check(vm=vm)
        vm.deploy(server=server)

        op.set_server(server=server)
        vm.add_operation(op=op)

    def op_migrate_single_vm(self, vm: SingleVM, new_server: Server, node: str) -> None:
        if vm.get_vm_id() not in self.__vm_dict.keys():
            raise KeyError(f"The VM[{vm.get_vm_id}] doesn't exist.")
        if vm.get_server_id() == new_server.get_server_id() and vm.get_node() == node:
            raise KeyError(f"The VM[{vm.get_vm_id()}] can't migrate to the original place.")
        old_server = vm.get_server()
        old_server.op_remove_vm(vm=vm)
        new_server.deploy_single_vm_with_check(vm=vm, node=node)
        vm.deploy(server=new_server, node=node)

        op = MigrateSingleVMOperation(day=self.get_current_day(), vm=vm, server=new_server, node=node)
        vm.add_operation(op=op)
        self.__current_day_operation.add_migrate_vm_operation(op=op)

    def op_migrate_double_vm(self, vm: DoubleVM, new_server: Server) -> None:
        if vm.get_vm_id() not in self.__vm_dict.keys():
            raise KeyError(f"The VM[{vm.get_vm_id}] doesn't exist.")
        if vm.get_server_id() == new_server.get_server_id():
            raise KeyError(f"The VM[{vm.get_vm_id()}] can't migrate to the original place.")
        old_server = vm.get_server()
        old_server.op_remove_vm(vm=vm)
        new_server.deploy_double_vm_with_check(vm=vm)
        vm.deploy(server=new_server)

        op = MigrateDoubleVMOperation(day=self.get_current_day(), vm=vm, server=new_server)
        vm.add_operation(op=op)
        self.__current_day_operation.add_migrate_vm_operation(op=op)

    def op_remove_vm(self, op: Union[RemoveSingleVMOperation, RemoveDoubleVMOperation]) -> None:
        vm = op.get_vm()
        self.__deployed_vm_dict.pop(vm.get_vm_id())
        self.__non_deployed_vm_dict[vm.get_vm_id()] = vm

        server = vm.get_server()
        server.remove_vm(vm=vm)
        vm.remove_from_server()

        vm.add_operation(op=op)
