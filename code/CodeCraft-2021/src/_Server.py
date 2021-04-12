from _VM import SingleVM, DoubleVM
from _ServerConfig import ServerConfig
from typing import List, Dict, Union

if __name__ == '__main__':
    from _Operation import PurchaseServerOperation
else:
    PurchaseServerOperation = None


class Server:
    def __init__(self, server_id: str, server_config: ServerConfig):
        self.__server_id = server_id
        self.__server_config = server_config

        self.__a_rest_cpu = server_config.get_cpu_of_one_node()
        self.__a_rest_memory = server_config.get_memory_of_one_node()
        self.__b_rest_cpu = server_config.get_cpu_of_one_node()
        self.__b_rest_memory = server_config.get_memory_of_one_node()

        self.__a_vm_dict = {}
        self.__b_vm_dict = {}

        self.__operation_history_list = []

    def get_server_id(self) -> str:
        return self.__server_id

    def get_server_config(self) -> ServerConfig:
        return self.__server_config

    def get_server_type(self) -> str:
        return self.get_server_config().get_server_type()

    def get_cpu_of_one_node(self) -> int:
        return self.get_server_config().get_cpu_of_one_node()

    def get_memory_of_one_node(self) -> int:
        return self.get_server_config().get_memory_of_one_node()

    def get_cost_purchase(self) -> int:
        return self.get_server_config().get_cost_purchase()

    def get_cost_everyday(self) -> int:
        return self.get_server_config().get_cost_everyday()

    def get_used_cpu_of_node_a(self) -> int:
        return self.get_cpu_of_one_node() - self.get_rest_cpu_of_node_a()

    def get_used_memory_of_node_a(self) -> int:
        return self.get_memory_of_one_node() - self.get_rest_memory_of_node_a()

    def get_rest_cpu_of_node_a(self) -> int:
        return self.__a_rest_cpu

    def get_rest_memory_of_node_a(self) -> int:
        return self.__a_rest_memory

    def get_vm_dict_of_node_a(self) -> Dict[str, Union[SingleVM, DoubleVM]]:
        return self.__a_vm_dict

    def get_num_vm_of_node_a(self) -> int:
        return len(self.get_vm_dict_of_node_a())

    def get_used_cpu_of_node_b(self) -> int:
        return self.get_cpu_of_one_node() - self.get_rest_cpu_of_node_b()

    def get_used_memory_of_node_b(self) -> int:
        return self.get_memory_of_one_node() - self.get_rest_memory_of_node_b()

    def get_rest_cpu_of_node_b(self) -> int:
        return self.__b_rest_cpu

    def get_rest_memory_of_node_b(self) -> int:
        return self.__b_rest_memory

    def get_vm_dict_of_node_b(self) -> Dict[str, Union[SingleVM, DoubleVM]]:
        return self.__b_vm_dict

    def get_num_vm_of_node_b(self) -> int:
        return len(self.get_vm_dict_of_node_b())

    def is_idle(self) -> bool:
        return self.__a_vm_dict == {} and self.__b_vm_dict == {}

    def get_num_vm_of_both_nodes(self) -> int:
        return self.get_num_vm_of_node_a() + self.get_num_vm_of_node_b()

    def add_operation(self, op: PurchaseServerOperation) -> None:
        self.__operation_history_list.append(op)

    def get_operation_history_list(self) -> List[PurchaseServerOperation]:
        return self.__operation_history_list

    def has_capacity_for_single_vm(self, vm: SingleVM, node: str) -> bool:
        if node == 'A':
            if self.get_rest_cpu_of_node_a() < vm.get_cpu_of_one_node() or \
                    self.get_rest_memory_of_node_a() < vm.get_memory_of_one_node():
                return False
            else:
                return True
        elif node == 'B':
            if self.get_rest_cpu_of_node_b() < vm.get_cpu_of_one_node() or \
                    self.get_rest_memory_of_node_b() < vm.get_memory_of_one_node():
                return False
            else:
                return True
        else:
            raise KeyError("The node must be 'A' or 'B'.")

    def has_capacity_for_double_vm(self, vm: DoubleVM) -> bool:
        if self.get_rest_cpu_of_node_a() < vm.get_cpu_of_one_node() or \
                self.get_rest_memory_of_node_a() < vm.get_memory_of_one_node() or \
                self.get_rest_cpu_of_node_b() < vm.get_cpu_of_one_node() or \
                self.get_rest_memory_of_node_b() < vm.get_memory_of_one_node():
            return False
        else:
            return True

    def deploy_single_vm(self, vm: SingleVM, node: str) -> None:
        if node == 'A':
            if self.has_capacity_for_single_vm(vm=vm, node=node):
                self.__a_rest_cpu -= vm.get_cpu_of_one_node()
                self.__a_rest_memory -= vm.get_memory_of_one_node()
                self.__a_vm_dict[vm.get_vm_id()] = vm
                vm.deploy(server=self, node='A')
            else:
                raise KeyError(f"Node A of the Server[{self.get_server_id()}] doesn't have enough space for the "
                               f"VM[{vm.get_vm_id()}].")
        elif node == 'B':
            if self.has_capacity_for_single_vm(vm=vm, node=node):
                self.__b_rest_cpu -= vm.get_cpu_of_one_node()
                self.__b_rest_memory -= vm.get_memory_of_one_node()
                self.__b_vm_dict[vm.get_vm_id()] = vm
                vm.deploy(server=self, node='B')
            else:
                raise KeyError(f"Node B of the Server[{self.get_server_id()}] doesn't have enough space for the "
                               f"VM[{vm.get_vm_id()}].")
        else:
            raise KeyError("The node must be 'A' or 'B'.")

    def deploy_double_vm(self, vm: DoubleVM) -> None:
        if self.has_capacity_for_double_vm(vm=vm):
            self.__a_rest_cpu -= vm.get_cpu_of_one_node()
            self.__a_rest_memory -= vm.get_memory_of_one_node()
            self.__a_vm_dict[vm.get_vm_id()] = vm
            self.__b_rest_cpu -= vm.get_cpu_of_one_node()
            self.__b_rest_memory -= vm.get_memory_of_one_node()
            self.__b_vm_dict[vm.get_vm_id()] = vm
            vm.deploy(server=self)
        else:
            raise KeyError(f"The Server[{self.get_server_id()}] doesn't have enough space for the "
                           f"VM[{vm.get_vm_id()}].")

    def remove_vm(self, vm: Union[SingleVM, DoubleVM]) -> None:
        if vm.get_server_id() != self.get_server_id():
            raise KeyError(f"The VM[{vm.get_vm_id()}] doesn't deployed on the Server[{self.get_server_id()}].")
        if vm.is_double():
            self.__a_rest_cpu += vm.get_cpu_of_one_node()
            self.__a_rest_memory += vm.get_memory_of_one_node()
            self.__a_vm_dict.pop(vm.get_vm_id())
            self.__b_rest_cpu += vm.get_cpu_of_one_node()
            self.__b_rest_memory += vm.get_memory_of_one_node()
            self.__b_vm_dict.pop(vm.get_vm_id())
        elif vm.get_node() == 'A':
            self.__a_rest_cpu += vm.get_cpu_of_one_node()
            self.__a_rest_memory += vm.get_memory_of_one_node()
            self.__a_vm_dict.pop(vm.get_vm_id())
        elif vm.get_node() == 'B':
            self.__b_rest_cpu += vm.get_cpu_of_one_node()
            self.__b_rest_memory += vm.get_memory_of_one_node()
            self.__b_vm_dict.pop(vm.get_vm_id())
        else:
            raise KeyError("The node must be 'A' or 'B'.")
