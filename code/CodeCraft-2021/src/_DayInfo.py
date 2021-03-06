from _Operation import *
from typing import List, Dict, Union


class DayInfo:
    def __init__(self, day: int):
        self.__day = day
        self.__request_operation_list = []
        self.__purchase_server_operation_list = []
        self.__migrate_vm_operation_list = []

        self.__eval_purchase_cost = 0
        self.__eval_running_cost = 0
        self.__eval_deployed_server_dict = {}

    def get_day(self) -> int:
        return self.__day

    def get_add_vm_operation_list(self) -> List[Union[DeploySingleVMOperation, DeployDoubleVMOperation]]:
        return [op for op in self.__request_operation_list
                if isinstance(op, DeploySingleVMOperation) or isinstance(op, DeployDoubleVMOperation)]

    def get_num_add_vm_operation(self) -> int:
        return len(self.get_add_vm_operation_list())

    def get_del_vm_operation_list(self) -> List[Union[DeploySingleVMOperation, DeployDoubleVMOperation]]:
        return [op for op in self.__request_operation_list
                if isinstance(op, RemoveSingleVMOperation) or isinstance(op, RemoveDoubleVMOperation)]

    def get_num_del_vm_operation(self) -> int:
        return len(self.get_del_vm_operation_list())

    def get_request_operation_list(self) -> List[Union[DeploySingleVMOperation, DeployDoubleVMOperation,
                                                       RemoveSingleVMOperation, RemoveDoubleVMOperation]]:
        return self.__request_operation_list

    def add_request_operation(self, op: Union[DeploySingleVMOperation, DeployDoubleVMOperation,
                                              RemoveSingleVMOperation, RemoveDoubleVMOperation]) -> None:
        self.__request_operation_list.append(op)

    def get_purchase_server_operation_list(self) -> List[PurchaseServerOperation]:
        return self.__purchase_server_operation_list

    def add_purchase_server_operation(self, op: PurchaseServerOperation) -> None:
        self.__purchase_server_operation_list.append(op)
        self.__eval_purchase_cost += op.get_server().get_cost_purchase()

    def get_migrate_vm_operation_list(self) -> List[Union[MigrateSingleVMOperation, MigrateDoubleVMOperation]]:
        return self.__migrate_vm_operation_list

    def add_migrate_vm_operation(self, op: Union[MigrateSingleVMOperation, MigrateDoubleVMOperation]) -> None:
        self.__migrate_vm_operation_list.append(op)

    # def eval_add_running_server(self, server: Server) -> None:
    #     if server.get_server_id() not in self.eval_get_running_server_dict().keys():
    #         self.__eval_running_server_dict[server.get_server_id()] = server
    #         self.__eval_running_cost += server.get_cost_everyday()
    #
    # def eval_remove_running_server(self, server: Server) -> None:
    #     if server.get_server_id() in self.eval_get_running_server_dict().keys():
    #         self.__eval_running_server_dict.pop(server.get_server_id())
    #         self.__eval_running_cost -= server.get_cost_everyday()

    def eval_get_purchase_cost(self) -> int:
        return self.__eval_purchase_cost

    def eval_get_running_cost(self) -> int:
        return self.__eval_running_cost

    def eval_get_total_cost(self) -> int:
        return self.eval_get_purchase_cost() + self.eval_get_running_cost()

    def eval_get_running_server_dict(self) -> Dict[str, Server]:
        return self.__eval_deployed_server_dict

    def eval_set_deployed_server_dict(self, deployed_server_dict: Dict[str, Server]) -> None:
        self.__eval_running_cost = 0
        self.__eval_deployed_server_dict = deployed_server_dict
        for server in self.eval_get_running_server_dict().values():
            self.__eval_running_cost += server.get_cost_everyday()
