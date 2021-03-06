from _VMConfig import VMConfig
from _ServerConfig import ServerConfig
from _Operation import *
from _DayInfo import DayInfo
from typing import Dict


class Environment:
    def __init__(self):
        self.__is_debug = False

        self.__vm_config_dict = {}
        self.__non_deployed_vm_dict = {}
        self.__deployed_vm_dict = {}

        self.__server_config_dict = {}
        self.__non_deployed_server_dict = {}
        self.__deployed_server_dict = {}
        self.__next_server_id = 1

        self.__total_days = 0
        self.__current_day = 0
        self.__day_info_dict = {0: DayInfo(day=0)}

        self.__eval_accumulated_purchase_cost = 0  # enabled only in debug mode
        self.__eval_accumulated_running_cost = 0  # enabled only in debug mode
        self.__eval_accumulated_total_cost = 0  # enabled only in debug mode

    # -------------------------------- get methods --------------------------------

    def is_debug(self) -> bool:
        return self.__is_debug

    def get_total_days(self) -> int:
        return self.__total_days

    def get_current_day(self) -> int:
        return self.__current_day

    def get_current_day_info(self) -> DayInfo:
        return self.__day_info_dict[self.get_current_day()]

    def get_day_info_by_day(self, day: int) -> DayInfo:
        return self.__day_info_dict[day]

    def get_vm_config_by_type(self, vm_type: str) -> VMConfig:
        vm_config = self.__vm_config_dict.get(vm_type)
        # if vm_config is None:
        #     raise KeyError(f"The VMConfig[{vm_type}] doesn't exist.")
        return vm_config

    def get_vm_by_id(self, vm_id: str) -> Union[SingleVM, DoubleVM]:
        vm = self.__deployed_vm_dict.get(vm_id)
        if vm is None:
            vm = self.__non_deployed_vm_dict.get(vm_id)
        # if vm is None:
        #     raise KeyError(f"The VM[{vm_id}] doesn't exist.")
        return vm

    def get_server_config_by_type(self, server_type: str) -> ServerConfig:
        server_config = self.get_server_config_dict().get(server_type)
        # if server_config is None:
        #     raise KeyError(f"The ServerConfig[{server_config_id}] doesn't exist.")
        return server_config

    def get_server_by_id(self, server_id: str) -> Server:
        server = self.__deployed_server_dict.get(server_id)
        if server is None:
            server = self.__deployed_server_dict.get(server_id)
        # if server is None:
        #     raise KeyError(f"The Server[{server_id}] doesn't exist.")
        return server

    def get_vm_config_dict(self) -> Dict[str, VMConfig]:
        return self.__vm_config_dict

    def get_deployed_vm_dict(self) -> Dict[str, Union[SingleVM, DoubleVM]]:
        return self.__deployed_vm_dict

    def get_non_deployed_vm_dict(self) -> Dict[str, Union[SingleVM, DoubleVM]]:
        return self.__non_deployed_vm_dict

    def get_server_config_dict(self) -> Dict[str, ServerConfig]:
        return self.__server_config_dict

    def get_deployed_server_dict(self) -> Dict[str, Server]:
        return self.__deployed_server_dict

    def get_non_deployed_server_dict(self) -> Dict[str, Server]:
        return self.__non_deployed_server_dict

    # -------------------------------- day methods --------------------------------

    def start_next_day(self) -> None:
        self.__current_day += 1

    def finish_current_day(self) -> None:
        if self.is_debug():
            self.get_current_day_info().eval_set_deployed_server_dict(
                deployed_server_dict=self.get_deployed_server_dict().copy()
            )
            self.__eval_accumulated_purchase_cost += self.get_current_day_info().eval_get_purchase_cost()
            self.__eval_accumulated_running_cost += self.get_current_day_info().eval_get_running_cost()
            self.__eval_accumulated_total_cost += self.get_current_day_info().eval_get_total_cost()

    # -------------------------------- set methods --------------------------------

    def set_debug(self, is_debug: bool) -> None:
        self.__is_debug = is_debug

    def set_total_days(self, total_days: int) -> None:
        self.__total_days = total_days

    def add_request_operation(self, day: int, op: Union[DeploySingleVMOperation, DeployDoubleVMOperation,
                                                        RemoveSingleVMOperation, RemoveDoubleVMOperation]):
        if day not in self.__day_info_dict.keys():
            self.__day_info_dict[day] = DayInfo(day=day)
        self.__day_info_dict[day].add_request_operation(op=op)

    def add_vm_config(self, vm_config: VMConfig) -> None:
        # if vm_config.get_vm_type() in self.__vm_config_dict.keys():
        #     raise KeyError(f"The VMConfig[{vm_config.get_vm_type()}] already exists.")
        self.__vm_config_dict[vm_config.get_vm_type()] = vm_config

        for server_type, server_config in self.get_server_config_dict().items():
            if vm_config.get_cpu_of_one_node() <= server_config.get_cpu_of_one_node() and \
                    vm_config.get_memory_of_one_node() <= server_config.get_memory_of_one_node():
                server_config.add_capable_vm_type(vm_config=vm_config)
                vm_config.add_capable_server_type(server_config=server_config)

    def add_server_config(self, server_config: ServerConfig) -> None:
        # if server_config.get_server_type() in self.__server_config_dict.keys():
        #     raise KeyError(f"The ServerConfig[{server_config.get_server_type()}] already exists.")
        self.__server_config_dict[server_config.get_server_type()] = server_config

        for vm_type, vm_config in self.get_vm_config_dict().items():
            if vm_config.get_cpu_of_one_node() <= server_config.get_cpu_of_one_node() and \
                    vm_config.get_memory_of_one_node() <= server_config.get_memory_of_one_node():
                server_config.add_capable_vm_type(vm_config=vm_config)
                vm_config.add_capable_server_type(server_config=server_config)

    def add_non_deployed_vm(self, vm: Union[SingleVM, DoubleVM]) -> None:
        # if vm.get_vm_id() in self.__non_deployed_vm_dict.keys():
        #     raise KeyError(f"The VM[{vm.get_vm_id()}] already exists.")
        self.__non_deployed_vm_dict[vm.get_vm_id()] = vm

    # -------------------------------- operation methods --------------------------------

    def op_purchase_server(self, server_config: ServerConfig) -> Server:
        server_id = f'S{self.__next_server_id}'
        self.__next_server_id += 1
        server = Server(server_id=server_id, server_config=server_config)
        self.__non_deployed_server_dict[server_id] = server
        server_config.add_server(server=server)

        op = PurchaseServerOperation(day=self.get_current_day(), server=server)
        server.add_operation(op=op)
        self.get_current_day_info().add_purchase_server_operation(op=op)

        return server

    def op_deploy_single_vm(self, op: DeploySingleVMOperation, server: Server, node: str) -> None:
        if server.is_idle():
            self.__non_deployed_server_dict.pop(server.get_server_id())
            self.__deployed_server_dict[server.get_server_id()] = server

        vm = op.get_vm()
        self.__non_deployed_vm_dict.pop(vm.get_vm_id())
        self.__deployed_vm_dict[vm.get_vm_id()] = vm

        server.deploy_single_vm(vm=vm, node=node)
        vm.deploy(server=server, node=node)

        op.set_server(server=server)
        op.set_node(node=node)
        vm.add_operation(op=op)

    def op_deploy_double_vm(self, op: DeployDoubleVMOperation, server: Server) -> None:
        if server.is_idle():
            self.__deployed_server_dict[server.get_server_id()] = server
            self.__non_deployed_server_dict.pop(server.get_server_id())

        vm = op.get_vm()
        self.__non_deployed_vm_dict.pop(vm.get_vm_id())
        self.__deployed_vm_dict[vm.get_vm_id()] = vm

        server.deploy_double_vm(vm=vm)
        vm.deploy(server=server)

        op.set_server(server=server)
        vm.add_operation(op=op)

    def op_migrate_single_vm(self, vm: SingleVM, new_server: Server, node: str) -> None:
        # if vm.get_vm_id() not in self.__vm_dict.keys():
        #     raise KeyError(f"The VM[{vm.get_vm_id}] doesn't exist.")
        # if vm.get_server_id() == new_server.get_server_id() and vm.get_node() == node:
        #     raise KeyError(f"The VM[{vm.get_vm_id()}] can't migrate to the original place.")
        old_server = vm.get_server()
        old_server_is_idle = old_server.is_idle()
        new_server_is_idle = new_server.is_idle()

        old_server.remove_vm(vm=vm)
        new_server.deploy_single_vm(vm=vm, node=node)
        vm.deploy(server=new_server, node=node)

        op = MigrateSingleVMOperation(day=self.get_current_day(), vm=vm, server=new_server, node=node)
        vm.add_operation(op=op)
        self.get_current_day_info().add_migrate_vm_operation(op=op)

        if not old_server_is_idle and old_server.is_idle():
            self.__non_deployed_server_dict[old_server.get_server_id()] = old_server
            self.__deployed_server_dict.pop(old_server.get_server_id())

        if new_server_is_idle and not new_server.is_idle():
            self.__deployed_server_dict[new_server.get_server_id()] = new_server
            self.__non_deployed_server_dict.pop(new_server.get_server_id())

    def op_migrate_double_vm(self, vm: DoubleVM, new_server: Server) -> None:
        # if vm.get_vm_id() not in self.__vm_dict.keys():
        #     raise KeyError(f"The VM[{vm.get_vm_id}] doesn't exist.")
        # if vm.get_server_id() == new_server.get_server_id():
        #     raise KeyError(f"The VM[{vm.get_vm_id()}] can't migrate to the original place.")
        old_server = vm.get_server()
        old_server_is_idle = old_server.is_idle()
        new_server_is_idle = new_server.is_idle()

        old_server.remove_vm(vm=vm)
        new_server.deploy_double_vm(vm=vm)
        vm.deploy(server=new_server)

        op = MigrateDoubleVMOperation(day=self.get_current_day(), vm=vm, server=new_server)
        self.get_current_day_info().add_migrate_vm_operation(op=op)
        vm.add_operation(op=op)

        if new_server_is_idle and not new_server.is_idle():
            self.__deployed_server_dict[new_server.get_server_id()] = new_server
            self.__non_deployed_server_dict.pop(new_server.get_server_id())

        if not old_server_is_idle and old_server.is_idle():
            self.__non_deployed_server_dict[old_server.get_server_id()] = old_server
            self.__deployed_server_dict.pop(old_server.get_server_id())

    def op_remove_vm(self, op: Union[RemoveSingleVMOperation, RemoveDoubleVMOperation]) -> None:
        vm = op.get_vm()
        server = vm.get_server()
        server_is_idle = server.is_idle()
        self.__deployed_vm_dict.pop(vm.get_vm_id())
        self.__non_deployed_vm_dict[vm.get_vm_id()] = vm

        server.remove_vm(vm=vm)
        vm.remove_from_server()

        vm.add_operation(op=op)

        if not server_is_idle and server.is_idle():
            self.__non_deployed_server_dict[server.get_server_id()] = server
            self.__deployed_server_dict.pop(server.get_server_id())

    # -------------------------------- evaluation methods --------------------------------

    def eval_get_accumulated_purchase_cost(self) -> int:
        return self.__eval_accumulated_purchase_cost

    def eval_get_accumulated_running_cost(self) -> int:
        return self.__eval_accumulated_running_cost

    def eval_get_accumulated_total_cost(self) -> int:
        return self.__eval_accumulated_total_cost
