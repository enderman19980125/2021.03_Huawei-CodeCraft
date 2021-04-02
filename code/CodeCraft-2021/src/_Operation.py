from _VM import VM
from _Server import Server
from typing import List, Union, Optional


class VMOperation:
    def __init__(self, day: int, vm: VM):
        self.__day = day
        self.__vm = vm

    def get_day(self) -> int:
        return self.__day

    def get_vm(self) -> VM:
        return self.__vm


class SingleVMOperation(VMOperation):
    def __init__(self, day: int, vm: VM, server: Server, node: str):
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
    def __init__(self, day: int, vm: VM, server: Server):
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


class DayOperation:
    def __init__(self, day: int):
        self.__day = day
        self.__purchase_server_operation_list = []
        self.__migrate_vm_operation_list = []
        self.__deploy_vm_operation_list = []
        self.__remove_vm_operation_list = []
        self.__deploy_and_remove_vm_operation_list = []

    def get_day(self) -> int:
        return self.__day

    def get_purchase_server_operation(self) -> List[PurchaseServerOperation]:
        return self.__purchase_server_operation_list

    def get_migrate_vm_operation(self) -> List[Union[MigrateSingleVMOperation, MigrateDoubleVMOperation]]:
        return self.__migrate_vm_operation_list

    def get_deploy_and_remove_vm_operation(self) -> List[Union[DeploySingleVMOperation, DeployDoubleVMOperation,
                                                               RemoveSingleVMOperation, RemoveDoubleVMOperation]]:
        return self.__deploy_and_remove_vm_operation_list

    def add_purchase_server_operation(self, op: PurchaseServerOperation) -> None:
        self.__purchase_server_operation_list.append(op)

    def add_deploy_vm_operation(self, op: Union[DeploySingleVMOperation, DeployDoubleVMOperation]) -> None:
        self.__deploy_vm_operation_list.append(op)
        self.__deploy_and_remove_vm_operation_list.append(op)

    def add_migrate_vm_operation(self, op: Union[MigrateSingleVMOperation, MigrateDoubleVMOperation]) -> None:
        self.__migrate_vm_operation_list.append(op)

    def add_remove_vm_operation(self, op: Union[RemoveSingleVMOperation, RemoveDoubleVMOperation]) -> None:
        self.__remove_vm_operation_list.append(op)
        self.__deploy_and_remove_vm_operation_list.append(op)
