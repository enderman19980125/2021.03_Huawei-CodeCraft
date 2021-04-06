from _VM import SingleVM, DoubleVM
from _Server import Server
from typing import Union, Optional


class VMOperation:
    def __init__(self, day: int, vm: Union[SingleVM, DoubleVM]):
        self.__day = day
        self.__vm = vm

    def get_day(self) -> int:
        return self.__day

    def get_vm(self) -> Union[SingleVM, DoubleVM]:
        return self.__vm


class SingleVMOperation(VMOperation):
    def __init__(self, day: int, vm: SingleVM, server: Optional[Server] = None, node: Optional[str] = None):
        super().__init__(day=day, vm=vm)
        self.__server = server
        self.__node = node

    def get_server(self) -> Optional[Server]:
        return self.__server

    def get_node(self) -> Optional[str]:
        return self.__node

    def set_server(self, server: Server) -> None:
        self.__server = server

    def set_node(self, node: str) -> None:
        self.__node = node


class DoubleVMOperation(VMOperation):
    def __init__(self, day: int, vm: DoubleVM, server: Optional[Server] = None):
        super().__init__(day=day, vm=vm)
        self.__server = server

    def get_server(self) -> Optional[Server]:
        return self.__server

    def set_server(self, server: Server) -> None:
        self.__server = server


class RemoveVMOperation(VMOperation):
    pass


class DeploySingleVMOperation(SingleVMOperation):
    pass


class MigrateSingleVMOperation(SingleVMOperation):
    pass


class RemoveSingleVMOperation(RemoveVMOperation):
    pass


class DeployDoubleVMOperation(DoubleVMOperation):
    pass


class MigrateDoubleVMOperation(DoubleVMOperation):
    pass


class RemoveDoubleVMOperation(RemoveVMOperation):
    pass


class PurchaseServerOperation:
    def __init__(self, day: int, server: Server):
        self.__day = day
        self.__server = server

    def get_day(self) -> int:
        return self.__day

    def get_server(self) -> Server:
        return self.__server
