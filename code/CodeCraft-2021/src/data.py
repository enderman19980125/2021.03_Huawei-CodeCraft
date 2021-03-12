class ServerConfig:
    def __init__(self, server_type: str, cpu: int, memory: int, cost_basic: int, cost_day: int):
        self.type = server_type
        self.cpu = cpu
        self.memory = memory
        self.cost_basic = cost_basic
        self.cost_day = cost_day


class VMConfig:
    def __init__(self, vm_type: str, cpu: int, memory: int, is_double: bool):
        self.type = vm_type
        self.cpu = cpu
        self.memory = memory
        self.is_double = is_double


Server_Config_Dict = {
    'host0Y6DP': ServerConfig(server_type='host0Y6DP', cpu=300, memory=830, cost_basic=141730, cost_day=176),
    'hostHV3A3': ServerConfig(server_type='hostHV3A3', cpu=290, memory=580, cost_basic=111689, cost_day=139),
    'hostD4V30': ServerConfig(server_type='hostD4V30', cpu=418, memory=412, cost_basic=121272, cost_day=152),
}

VM_Config_Dict = {
    'vm38TGB': VMConfig(vm_type='vm38TGB', cpu=124, memory=2, is_double=True),
    'vmMRUNJ': VMConfig(vm_type='vmMRUNJ', cpu=60, memory=2, is_double=True),
    'vmH024K': VMConfig(vm_type='vmH024K', cpu=48, memory=2, is_double=False),
}


class Server:
    def __init__(self, server_id: int, config: ServerConfig):
        self.id = server_id
        self.config = config
        self.status = 'idle'  # 'running', 'idle', 'deleted'
        self.A_cpu_rest = self.config.cpu / 2
        self.B_cpu_rest = self.config.cpu / 2
        self.A_memory_rest = self.config.memory / 2
        self.B_memory_rest = self.config.memory / 2
        self.A_vm = []  # List[VM1, VM2, VM3, ...]
        self.B_vm = []  # List[VM1, VM2, VM3, ...]
        self.AB_vm = []  # List[VM1, VM2, VM3, ...]


class VM:
    def __init__(self, vm_id: str, config: VMConfig):
        self.id = vm_id
        self.config = config
        self.server = None  # Server
        self.node = '-'  # '-', 'A', 'B', 'AB'


VM_Dict = {
    '000000000': VM(vm_id='000000000', config=VM_Config_Dict['vm38TGB']),
    '000000001': VM(vm_id='000000001', config=VM_Config_Dict['vm38TGB']),
    '000000002': VM(vm_id='000000002', config=VM_Config_Dict['vmMRUNJ']),
    '000000003': VM(vm_id='000000003', config=VM_Config_Dict['vmH024K']),
    '000000004': VM(vm_id='000000004', config=VM_Config_Dict['vm38TGB']),
    '000000005': VM(vm_id='000000005', config=VM_Config_Dict['vmMRUNJ']),
    '000000006': VM(vm_id='000000006', config=VM_Config_Dict['vmH024K']),
}

Server_List = [
    Server(server_id=0, config=Server_Config_Dict['host0Y6DP']),
    Server(server_id=1, config=Server_Config_Dict['hostHV3A3']),
]


class Request:
    def __init__(self, operation: str, vm_id: str, vm_type: str = None):
        self.operation = operation
        self.vm_id = vm_id
        self.vm_type = vm_type


Request_List = [
    [
        Request(operation='add', vm_id='000000001', vm_type='vm38TGB'),
        Request(operation='add', vm_id='000000002', vm_type='vmMRUNJ'),
        Request(operation='add', vm_id='000000003', vm_type='vmH024K'),
    ], [
        Request(operation='del', vm_id='000000001'),
        Request(operation='add', vm_id='000000004', vm_type='vmMRUNJ'),
        Request(operation='add', vm_id='000000005', vm_type='vmH024K'),
    ],
]


class Migration:
    def __init__(self, vm: VM, to_server: Server, to_node: str):
        self.vm = vm
        self.from_server = vm.server
        self.from_node = vm.node
        self.to_server = to_server
        self.to_node = to_node


class Deploy:
    def __init__(self, vm: VM, to_server: Server, to_node: str):
        self.vm = VM
        self.to_server = to_server
        self.to_node = to_node


class DayOperation:
    def __init__(self):
        self.purchase = []  # List[Server_1, Server_2, Server_3, ...]
        self.migration = []  # List[Migration_1, Migration_2, Migration_3, ...]
        self.deploy = []  # List[Deploy_1, Deploy_2, Deploy_3, ...]


Operation_List = [
    DayOperation(), DayOperation(), DayOperation(),
]
