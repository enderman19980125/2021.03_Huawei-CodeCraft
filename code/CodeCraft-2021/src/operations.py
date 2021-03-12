import data


def has_capacity(machine_id: int, machine_node: str, vm_id: str) -> bool:
    vm_info_item = data.VM_Info_Dict[vm_id]
    vm_type = vm_info_item['vm_type']
    vm_parameter_item = data.VM_Parameter_Dict[vm_type]
    machine_info_item = data.Machines_Info_List[machine_id]

    if vm_parameter_item['is_double']:
        return machine_info_item['A_cpu_rest'] >= vm_parameter_item['cpu'] / 2 and \
               machine_info_item['B_cpu_rest'] >= vm_parameter_item['cpu'] / 2 and \
               machine_info_item['A_memory_rest'] >= vm_parameter_item['memory'] / 2 and \
               machine_info_item['B_memory_rest'] >= vm_parameter_item['memory'] / 2
    elif machine_node == 'A':
        return machine_info_item['A_cpu_rest'] >= vm_parameter_item['cpu'] and \
               machine_info_item['A_memory_rest'] >= vm_parameter_item['memory']
    elif machine_node == 'B':
        return machine_info_item['B_cpu_rest'] >= vm_parameter_item['cpu'] and \
               machine_info_item['B_memory_rest'] >= vm_parameter_item['memory']
    else:
        raise KeyError


def add_machine(server_type: str):
    machine_id = len(data.Machines_Info_List)
    server_parameter_item = data.Servers_Parameter_Dict[server_type]
    cpu_per_node = server_parameter_item['cpu'] / 2
    memory_per_node = server_parameter_item['memory'] / 2
    machine_info_item = {
        'machine_id': machine_id,
        'server_type': server_type,
        'A_cpu_rest': cpu_per_node,
        'A_memory_rest': memory_per_node,
        'B_cpu_rest': cpu_per_node,
        'B_memory_rest': memory_per_node,
        'A': [],
        'B': [],
        'AB': [],
    }
    data.Machines_Info_List.append(machine_info_item)
