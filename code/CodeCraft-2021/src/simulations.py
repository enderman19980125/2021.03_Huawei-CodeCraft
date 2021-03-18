import numpy as np
import heapq
import data
import operations
from typing import Tuple, List, Optional

R = 10


def buy_server_randomly(vm: data.VM) -> data.Server:
    n_server_types = len(data.Server_Config_Dict)
    server_types_list = list(data.Server_Config_Dict.keys())
    while True:
        k = np.random.randint(0, n_server_types)
        k = server_types_list[k]
        server_config = data.Server_Config_Dict[k]
        if operations.has_capacity(server_config=server_config, server_node='A', vm=vm):
            server_id = operations.purchase_server(server_config=server_config)
            server = data.Server_Dict[server_id]
            return server


class ServerHeap:
    def __init__(self, heap_type: str, ratio_list: List[int]) -> None:
        if heap_type not in ['single', 'double']:
            raise ValueError('"heap_type" must be "single" or "double".')
        self.heap_type = heap_type
        self.heap_dict = {k: [] for k in ratio_list}  # {-1: [(s1, 'A'), (s1, 'B'), (s2, 'A'), (s2, 'B')], 1: []}

    def __get_heap_key(self, server: data.Server = None, vm: data.VM = None) -> int:
        if server:
            cpu, memory = server.config.cpu, server.config.memory
        else:
            cpu, memory = vm.config.cpu, vm.config.memory

        ratio = cpu / memory * R if cpu > memory else -memory / cpu * R
        abs_list = [abs(ratio - k) for k in self.heap_dict.keys()]
        min_abs = min(abs_list)
        heap_index = abs_list.index(min_abs)
        heap_key = list(self.heap_dict.keys())[heap_index]
        return heap_key

    @staticmethod
    def __key(server_node_tuple: Tuple[data.Server, str]) -> int:
        server, node = server_node_tuple
        return server.A_cpu_rest if node != 'B' else server.B_cpu_rest

    @staticmethod
    def __swap_server(heap: List[Tuple[data.Server, str]], s1: int, s2: int) -> None:
        t = heap[s1]
        heap[s1] = heap[s2]
        heap[s2] = t

    @staticmethod
    def __push_into_heap(heap: List[Tuple[data.Server, str]], server: data.Server, node: str) -> None:
        heap.append((server, node))
        return

        p_cnt = len(heap) - 1
        p_fa = (p_cnt - 1) // 2

        while p_cnt > 0 and ServerHeap.__key(heap[p_fa]) < ServerHeap.__key(heap[p_cnt]):
            ServerHeap.__swap_server(heap, p_fa, p_cnt)
            p_cnt = p_fa

    @staticmethod
    def __pop_from_heap(heap: List[Tuple[data.Server, str]]) -> Tuple[Optional[data.Server], str]:
        snt_list = heapq.nlargest(1, heap, key=lambda snt: ServerHeap.__key(snt))
        if snt_list:
            return snt_list[0]
        else:
            return None, ''

        if heap is []:
            return None

        top_server_node = heap[0]
        heap[0] = heap.pop()
        p_cnt = 0
        while p_cnt < len(heap):
            p_s1 = p_cnt * 2 + 1
            p_s2 = p_cnt * 2 + 2
            if p_s1 >= len(heap):
                break
            elif p_s2 == len(heap) and ServerHeap.__key(heap[p_cnt]) < ServerHeap.__key(heap[p_s1]):
                ServerHeap.__swap_server(heap, p_cnt, p_s1)
                break
            elif p_s2 == len(heap) and ServerHeap.__key(heap[p_cnt]) >= ServerHeap.__key(heap[p_s1]):
                break
            p_s = p_s1 if ServerHeap.__key(heap[p_s1]) >= ServerHeap.__key(heap[p_s2]) else p_s2
            if ServerHeap.__key(heap[p_cnt]) < ServerHeap.__key(heap[p_s]):
                ServerHeap.__swap_server(heap, p_cnt, p_s)
                p_cnt = p_s
            else:
                break

        return top_server_node

    def push(self, server: data.Server, node: str) -> None:
        heap_key = self.__get_heap_key(server=server)
        heap = self.heap_dict[heap_key]
        ServerHeap.__push_into_heap(heap, server, node)

    def pop_for_vm(self, vm: data.VM) -> Tuple[Optional[data.Server], str]:
        heap_key = self.__get_heap_key(vm=vm)
        heap = self.heap_dict[heap_key]
        return ServerHeap.__pop_from_heap(heap)


Ratio_ServerConfig_List = []


def purchase_server_for_vm(vm: data.VM) -> data.ServerConfig:
    cpu, memory = vm.config.cpu, vm.config.memory
    ratio = cpu / memory * R if cpu > memory else -memory / cpu * R
    abs_list = [(i, abs(ratio - server_ratio), server_config) for i, (server_ratio, server_config) in enumerate(Ratio_ServerConfig_List)]
    abs_list.sort(key=lambda x: x[1])
    for i, _, server_config in abs_list:
        if operations.has_capacity(server_config=server_config, server_node='A', vm=vm):
            return server_config
    raise ValueError('Cannot purchase a Server for the specific VM.')


def start():
    global Ratio_ServerConfig_List
    Ratio_ServerConfig_List = [(server_config.cpu / server_config.memory * R, server_config) for server_config in data.Server_Config_Dict.values()]
    Ratio_ServerConfig_List.sort(key=lambda x: x[0])

    ratio_list = list(range(-800, -10 + 1)) + list(range(10, 800))
    single_server_heap_class = ServerHeap(heap_type='single', ratio_list=ratio_list)
    double_server_heap_class = ServerHeap(heap_type='double', ratio_list=ratio_list)

    for day_id, day_request_list in enumerate(operations.day_request_generator()):
        for request in day_request_list:
            vm = request.vm

            if request.operation == 'add':

                if vm.config.is_double:
                    server, _ = double_server_heap_class.pop_for_vm(vm=vm)
                    if server is None or not operations.has_capacity(server=server, server_node='AB', vm=vm):
                        server_config = purchase_server_for_vm(vm=vm)
                        server_id = operations.purchase_server(server_config=server_config)
                        server = data.Server_Dict[server_id]
                        double_server_heap_class.push(server, 'AB')
                    operations.deploy_vm(vm=vm, server=server, server_node='AB')

                else:
                    server, server_node = single_server_heap_class.pop_for_vm(vm=vm)
                    if server is None or not operations.has_capacity(server=server, server_node=server_node, vm=vm):
                        server_config = purchase_server_for_vm(vm=vm)
                        server_id = operations.purchase_server(server_config=server_config)
                        server = data.Server_Dict[server_id]
                        single_server_heap_class.push(server, 'A')
                        single_server_heap_class.push(server, 'B')
                        operations.deploy_vm(vm=vm, server=server, server_node='A')
                    else:
                        operations.deploy_vm(vm=vm, server=server, server_node=server_node)

            else:
                operations.delete_vm(vm=vm)

        if data.IS_DEBUG:
            cpu_rest = []
            memory_rest = []

            for server in data.Server_Dict.values():
                cpu_rest.append((server.A_cpu_rest, server.B_cpu_rest))
                memory_rest.append((server.A_memory_rest, server.B_memory_rest))
                # print(f'Sever #{server.id:<5s}    type={server.config.type}    '
                #       f'A_rest=({server.A_cpu_rest:3d}C,{server.A_memory_rest:3d})    '
                #       f'B_rest=({server.B_cpu_rest:3d}C,{server.B_memory_rest:3d})')

            n_servers = len(data.Server_Dict)

            total_cpu_rest = sum([c[0] + c[1] for c in cpu_rest])
            total_memory_rest = sum(m[0] + m[1] for m in memory_rest)
            print(f'day={day_id}\t'
                  f'n_servers={n_servers}\t'
                  f'total_cpu_rest={total_cpu_rest}\t'
                  f'total_memory_rest={total_memory_rest}\t'
                  f'total_cost={data.COST_TOTAL}\t')
