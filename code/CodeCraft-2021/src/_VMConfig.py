from typing import Dict

if __name__ == '__main__':
    from _VM import VM
    from _ServerConfig import ServerConfig
else:
    VM = None
    ServerConfig = None


class VMConfig:
    def __init__(self, vm_type: str, cpu: int, memory: int, is_double: bool):
        self.__vm_type = vm_type
        self.__is_double = is_double

        if is_double:
            self.__cpu = cpu // 2
            self.__memory = memory // 2
        else:
            self.__cpu = cpu
            self.__memory = memory

        self.__this_type_vm_dict = {}
        self.__capable_server_type_dict = {}

    def get_vm_type(self) -> str:
        return self.__vm_type

    def is_double(self) -> bool:
        return self.__is_double

    def get_cpu_of_one_node(self) -> int:
        return self.__cpu

    def get_memory_of_one_node(self) -> int:
        return self.__memory

    def get_this_type_vm_dict(self) -> Dict[str, VM]:
        return self.__this_type_vm_dict

    def get_capable_server_type_dict(self) -> Dict[str, ServerConfig]:
        return self.__capable_server_type_dict

    def add_vm(self, vm: VM) -> None:
        # if self.get_vm_type() != vm.get_vm_type():
        #     raise KeyError(f"The VM[{vm.get_vm_id()}] isn't an instance of the VMConfig[{self.get_vm_type()}].")
        self.__this_type_vm_dict[vm.get_vm_id()] = vm

    def remove_vm(self, vm: VM) -> None:
        # if vm.get_vm_id() not in self.__this_type_vm_dict.keys():
        #     raise KeyError(f"The VM[{vm.get_vm_id()}] isn't in the instances of the VMConfig[{self.get_vm_type()}].")
        self.__this_type_vm_dict.pop(vm.get_vm_id())

    def add_capable_server_type(self, server_config: ServerConfig) -> None:
        # if server_config.get_cpu_of_one_node() < self.get_cpu_of_one_node() or \
        #         server_config.get_memory_of_one_node() < self.get_memory_of_one_node():
        #     raise KeyError(f"The ServerConfig[{server_config.get_server_type()}] doesn't have enough space for the "
        #                    f"VMConfig[{self.get_vm_type()}].")
        self.__capable_server_type_dict[server_config.get_server_type()] = server_config
