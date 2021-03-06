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


def write_day_operation(w: Writer, e: Environment) -> None:
    content_list = []

    server_dict = {}
    for purchase_server_operation in e.get_current_day_info().get_purchase_server_operation_list():
        server_id = purchase_server_operation.get_server().get_server_id()
        server_type = purchase_server_operation.get_server().get_server_type()
        if server_type in server_dict.keys():
            server_dict[server_type].append(server_id)
        else:
            server_dict[server_type] = [server_id]

    # w.write(content=f'(purchase, {len(server_dict)})')
    content_list.append(f'(purchase, {len(server_dict)})')
    for server_type, server_id_list in server_dict.items():
        # w.write(content=f'({server_type}, {len(server_id_list)})')
        content_list.append(f'({server_type}, {len(server_id_list)})')
        for server_id in server_id_list:
            w.set_mapped_server_id(server_id=server_id)

    # w.write(content=f'(migration, {len(e.get_current_day_info().get_migrate_vm_operation_list())})')
    content_list.append(f'(migration, {len(e.get_current_day_info().get_migrate_vm_operation_list())})')
    for op in e.get_current_day_info().get_migrate_vm_operation_list():
        vm_id = op.get_vm().get_vm_id()
        server_id = op.get_server().get_server_id()
        if op.get_vm().is_double():
            # w.write(content=f'({vm_id}, {server_id})')
            content_list.append(f'({vm_id}, {server_id})')
        else:
            node = op.get_node()
            # w.write(content=f'({vm_id}, {server_id}, {node})')
            content_list.append(f'({vm_id}, {server_id}, {node})')

    for op in e.get_current_day_info().get_request_operation_list():
        if isinstance(op, DeploySingleVMOperation):
            mapped_server_id = w.get_mapped_server_id(server_id=op.get_server().get_server_id())
            # w.write(content=f'({mapped_server_id}, {op.get_node()})')
            content_list.append(f'({mapped_server_id}, {op.get_node()})')
        elif isinstance(op, DeployDoubleVMOperation):
            mapped_server_id = w.get_mapped_server_id(server_id=op.get_server().get_server_id())
            # w.write(content=f'({mapped_server_id})')
            content_list.append(f'({mapped_server_id})')

    content = '\n'.join(content_list)
    w.write(content=content)
    w.flush()


def write_day_info_header(w: Writer) -> None:
    content_list = [
        'day',
        '|',

        'accumulated_total_cost',
        'accumulated_purchase_cost',
        'accumulated_running_cost',
        '|',

        'current_day_total_cost',
        'current_day_purchase_cost',
        'current_day_running_cost',
        '|',

        'num_total_vm',
        'num_deployed_vm',
        'num_idle_vm',
        '|',

        'num_total_servers',
        'num_deployed_servers',
        'num_idle_servers',
        'num_purchased_servers',
        '|',

        'num_add_vm_operation',
        'num_del_vm_operation',
        '|',

        'num_migrations',
        '|',
    ]
    content = ','.join(content_list)
    w.write(content=content)


def write_day_info(w: Writer, e: Environment) -> None:
    content_list = [
        e.get_current_day(),
        '|',

        e.eval_get_accumulated_total_cost(),
        e.eval_get_accumulated_purchase_cost(),
        e.eval_get_accumulated_running_cost(),
        '|',

        e.get_current_day_info().eval_get_total_cost(),
        e.get_current_day_info().eval_get_purchase_cost(),
        e.get_current_day_info().eval_get_running_cost(),
        '|',

        len(e.get_deployed_vm_dict()) + len(e.get_non_deployed_vm_dict()),
        len(e.get_deployed_vm_dict()),
        len(e.get_non_deployed_vm_dict()),
        '|',

        len(e.get_deployed_server_dict()) + len(e.get_non_deployed_server_dict()),
        len(e.get_deployed_server_dict()),
        len(e.get_non_deployed_server_dict()),
        len(e.get_current_day_info().get_purchase_server_operation_list()),
        '|',

        e.get_current_day_info().get_num_add_vm_operation(),
        e.get_current_day_info().get_num_del_vm_operation(),
        '|',

        len(e.get_current_day_info().get_migrate_vm_operation_list()),
        '|',
    ]
    content_list = map(str, content_list)
    content = ','.join(content_list)
    w.write(content=content)
