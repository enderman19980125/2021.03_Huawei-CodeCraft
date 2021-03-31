import data
import operations


def start():
    day_capacity_list = [0]

    for day_id, day_request_list in enumerate(operations.day_request_generator()):
        day_capacity = 0
        for request in day_request_list:
            vm = request.vm
            day_capacity += vm.config.cpu * vm.config.memory
        day_capacity_list.append(day_capacity)

    total_cost = 0
    min_basic_unit_cost = min([s.cost_basic / s.cpu / s.memory for s in data.Server_Config_Dict.values()])
    min_day_unit_cost = min([s.cost_day / s.cpu / s.memory for s in data.Server_Config_Dict.values()])

    for i in range(1, len(day_capacity_list)):
        yesterday_capacity = day_capacity_list[i - 1]
        today_capacity = day_capacity_list[i]
        if yesterday_capacity < today_capacity:
            total_cost += min_basic_unit_cost * (today_capacity - yesterday_capacity)
        total_cost += min_day_unit_cost * today_capacity

    formatted_min_basic_unit_cost = round(min_basic_unit_cost, 10)
    formatted_min_day_unit_cost = round(min_day_unit_cost, 10)
    formatted_total_cost = format(int(total_cost), ',')
    print(f'Minimum cost of purchasing one unit (1C+1GB) is {formatted_min_basic_unit_cost}.')
    print(f'Minimum cost of running one unit (1C+1GB) everyday is {formatted_min_day_unit_cost}.')
    print(f'Theory minimum cost is {formatted_total_cost}.')
