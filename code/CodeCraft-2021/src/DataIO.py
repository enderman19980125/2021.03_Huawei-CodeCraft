from _VMConfig import VMConfig
from _ServerConfig import ServerConfig
from _Reader import Reader
from _Writer import Writer
from _Environment import Environment
from _Operation import *


def read_server_config(r: Reader, e: Environment) -> None:
    n = int(next(r.get_next_line))
    for _ in range(n):
        server_config_list = next(r.get_next_line).strip('(').strip(')').split(',')
        server_type, cpu, memory, cost_purchase, cost_everyday = server_config_list
        server_config = ServerConfig(
            server_type=server_type.strip(' '),
            cpu=int(cpu),
            memory=int(memory),
            cost_purchase=int(cost_purchase),
            cost_everyday=int(cost_everyday)
        )
        e.add_server_config(server_config=server_config)


def read_vm_config(r: Reader, e: Environment) -> None:
    n = int(next(r.get_next_line))
    for _ in range(n):
        vm_config_list = next(r.get_next_line).strip('(').strip(')').split(', ')
        vm_type, cpu, memory, is_double = vm_config_list
        vm_config = VMConfig(
            vm_type=vm_type.strip(' '),
            cpu=int(cpu),
            memory=int(memory),
            is_double=is_double == '1'
        )
        e.add_vm_config(vm_config=vm_config)


def read_day_request(r: Reader, e: Environment, day: int) -> None:
    n = int(next(r.get_next_line))
    for _ in range(n):
        request_list = next(r.get_next_line).strip('(').strip(')').split(', ')
        if request_list[0] == 'add':
            vm_type = request_list[1]
            vm_id = request_list[2]
            vm_config = e.get_vm_config_by_type(vm_type=vm_type)
            if vm_config.is_double():
                vm = DoubleVM(vm_id=vm_id, vm_config=vm_config)
                op = DeployDoubleVMOperation(day=day, vm=vm)
            else:
                vm = SingleVM(vm_id=vm_id, vm_config=vm_config)
                op = DeploySingleVMOperation(day=day, vm=vm)
            e.add_non_deployed_vm(vm=vm)
            e.add_request_operation(day=day, op=op)
        elif request_list[0] == 'del':
            vm_id = request_list[1]
            vm = e.get_vm_by_id(vm_id=vm_id)
            if vm.is_double():
                op = RemoveDoubleVMOperation(day=day, vm=vm)
            else:
                op = RemoveSingleVMOperation(day=day, vm=vm)
            e.add_request_operation(day=day, op=op)


def write_day_operation(w: Writer, e: Environment, day: int) -> None:
    day_operation = e.get_day_info_by_day(day=day)

    server_dict = {}
    for purchase_server_operation in day_operation.get_purchase_server_operation_list():
        server_id = purchase_server_operation.get_server().get_server_id()
        server_type = purchase_server_operation.get_server().get_server_type()
        if server_type in server_dict.keys():
            server_dict[server_type].append(server_id)
        else:
            server_dict[server_type] = [server_id]

    w.write(content=f'(purchase, {len(server_dict)})')
    for server_type, server_id_list in server_dict.items():
        w.write(content=f'({server_type}, {len(server_id_list)})')
        for server_id in server_id_list:
            w.set_mapped_server_id(server_id=server_id)

    w.write(content=f'(migration, 0)')

    for op in day_operation.get_request_operation_list():
        if isinstance(op, DeploySingleVMOperation):
            mapped_server_id = w.get_mapped_server_id(server_id=op.get_server().get_server_id())
            w.write(content=f'({mapped_server_id}, {op.get_node()})')
        elif isinstance(op, DeployDoubleVMOperation):
            mapped_server_id = w.get_mapped_server_id(server_id=op.get_server().get_server_id())
            w.write(content=f'({mapped_server_id})')

    w.flush()


def write_day_info(w: Writer, e: Environment, day: int) -> None:
    content_list = [
        f'----------------    Day = {day}    ----------------',
        f'Accumulated Cost = {e.eval_get_accumulated_total_cost()}'
    ]
    content = '\n'.join(content_list)
    w.write(content=content)
