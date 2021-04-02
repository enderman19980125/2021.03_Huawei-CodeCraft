from _Server import Server
from _VMConfig import VMConfig
from typing import Dict


class ServerConfig:
    def __init__(self, server_type: str, cpu: int, memory: int, cost_purchase: int, cost_everyday: int):
        self.__server_type = server_type
        self.__cpu = cpu // 2
        self.__memory = memory // 2
        self.__cost_purchase = cost_purchase
        self.__cost_everyday = cost_everyday

        self.__this_type_server_dict = {}
        self.__capable_vm_type_dict = {}

    def get_server_type(self) -> str:
        return self.__server_type

    def get_cpu_of_one_node(self) -> int:
        return self.__cpu

    def get_memory_of_one_node(self) -> int:
        return self.__memory

    def get_cost_purchase(self) -> int:
        return self.__cost_purchase

    def get_cost_everyday(self) -> int:
        return self.__cost_everyday

    def get_this_type_server_dict(self) -> Dict[str, Server]:
        return self.__this_type_server_dict

    def get_capable_vm_type_dict(self) -> Dict[str, VMConfig]:
        return self.__capable_vm_type_dict

    def add_server(self, server: Server) -> None:
        if self.get_server_type() != server.get_server_config().get_server_type():
            raise KeyError(f"The Server[{server.get_server_id()}] isn't an instance of the "
                           f"ServerConfig[{self.get_server_type()}].")
        self.__this_type_server_dict[server.get_server_id()] = server

    def remove_vm(self, server: Server) -> None:
        if server.get_server_id() not in self.__this_type_server_dict.keys():
            raise KeyError(f"The Server[{server.get_server_id()}] isn't in the instances of the "
                           f"ServerConfig[{self.get_server_type()}].")
        self.__this_type_server_dict.pop(server.get_server_id())

    def add_capable_vm_type(self, vm_config: VMConfig):
        if self.get_cpu_of_one_node() < vm_config.get_cpu_of_one_node() or \
                self.get_memory_of_one_node() < vm_config.get_memory_of_one_node():
            raise KeyError(f"The ServerConfig[{self.get_server_type()}] doesn't have enough space for the "
                           f"VMConfig[{vm_config.get_vm_type()}].")
        self.__capable_vm_type_dict[vm_config.get_vm_type()] = vm_config
