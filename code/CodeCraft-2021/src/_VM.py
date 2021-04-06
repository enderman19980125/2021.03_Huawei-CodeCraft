from _VMConfig import VMConfig
from typing import List, Optional

if __name__ == '__main__':
    from _Server import Server
    from _Operation import VMOperation
else:
    Server = None
    VMOperation = None


class VM:
    def __init__(self, vm_id: str, vm_config: VMConfig):
        self.__vm_id = vm_id
        self.__vm_config = vm_config
        self.__server = None
        self.__node = None
        self.__operation_history_list = []

    def get_vm_id(self) -> str:
        return self.__vm_id

    def get_server_id(self) -> str:
        return self.__server.get_server_id()

    def get_server(self) -> Server:
        return self.__server

    def get_node(self) -> str:
        return self.__node

    def get_vm_config(self) -> VMConfig:
        return self.__vm_config

    def get_vm_type(self) -> str:
        return self.get_vm_config().get_vm_type()

    def is_double(self) -> bool:
        return self.get_vm_config().is_double()

    def get_cpu_of_one_node(self) -> int:
        return self.get_vm_config().get_cpu_of_one_node()

    def get_memory_of_one_node(self) -> int:
        return self.get_vm_config().get_memory_of_one_node()

    def deploy(self, server: Server, node: Optional[str] = None) -> None:
        self.__server = server
        self.__node = node

    def remove_from_server(self) -> None:
        # if self.get_server_id() is None:
        #     raise KeyError(f"The VM[{self.get_vm_id()}] hasn't deployed on any Server.")
        self.__server = None
        self.__node = None

    def add_operation(self, op: VMOperation) -> None:
        self.__operation_history_list.append(op)

    def get_operation_history_list(self) -> List[VMOperation]:
        return self.__operation_history_list


class SingleVM(VM):
    def __init__(self, vm_id: str, vm_config: VMConfig):
        super().__init__(vm_id=vm_id, vm_config=vm_config)

    def deploy_on_server(self, server: Server, node: str) -> None:
        super().deploy(server=server, node=node)


class DoubleVM(VM):
    def __init__(self, vm_id: str, vm_config: VMConfig):
        super().__init__(vm_id=vm_id, vm_config=vm_config)

    def deploy_on_server(self, server: Server) -> None:
        super().deploy(server=server)
