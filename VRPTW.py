# -*- coding: utf-8 -*-

# Vehicle Routing Problem with Time Windows

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

import datetime


global coordinate_array, Distance_Matrix, Time_Matrix

# Global Data

coordinate_list = [
 '家', 114.748125, 37.750201,
 '宋城', 114.903234,37.85197,
 '赵刀寺', 114.72869,37.781231,
 '东阳台', 114.740252,37.823862,
 '常洋', 114.803039,37.776488,
 '小马圈', 114.804022,37.851744,
 '豆腐庄', 114.851979,37.843736,
 '前大章', 114.865526,37.865367,
 '梅花', 114.8317,37.891582, # 梅花
 '永安', 114.77435,37.83808,
 '乡官', 114.797613,37.867981,
 '曹古疃', 114.779879,37.808557,
 '鲁家庄', 114.767719,37.845097, # 栾城区
 '安王村', 114.71166,37.798524,
 '北何庄', 114.8197,37.804607,
 '大马', 114.887135,37.868492,
 '投头庄', 114.840102,37.855959,
 '贾店村', 114.726521,37.801013,
 '石家庄', 114.890489,37.824124,
 '范村', 114.698397,37.79639,
 '北解疃', 114.795109,37.7917,
 '西罗村', 114.871172,37.853288,
 '仪停', 114.782591,37.832019,
 '后大章', 114.865834,37.867755,
 '彭家庄', 114.792664,37.804643,
 '林子', 114.910071,37.805321,
 '四德', 114.851108,37.87908,
 '东罗村', 114.882305,37.853451,
 '北轮城', 114.70097,37.788896,
 '肖庄', 114.770207,37.791428,
 '高庄', 114.902043,37.730501,
 '各南', 114.910162,37.817456,
 '泥沟', 114.833553,37.800309,
 '台兴庄', 114.751193,37.812218,
 '马谷庄', 114.762469,37.810494,
 '双庙', 114.78777,37.843918,
 '各子', 114.8928,37.837465, # 一村 二村 三村？
 '大吕村', 114.831951,37.823025,
 '齐家庄', 114.817472,37.846462,
 '北辛庄', 114.866827,37.81841,
 '王家庄', 114.806625,37.835115,
 '尚庄', 114.875416,37.889713, #藁城区
 '固德', 114.772933,37.858432,
 '徐家庄', 114.871728,37.836585,
 '新宅店', 114.726219,37.820187, #村居委会
 '黎村', 114.821105,37.790131,
 '史家庄', 114.798944,37.81971,
 '小吕村', 114.840012,37.816629
]

coordinate_array = np.array(coordinate_list).reshape(48,3)

Distance_Matrix = pd.read_csv("Distance.csv", header = None)
Time_Matrix = pd.read_csv("Time.csv", header = None)

# End of Global Data

# Input Data For Each Time of Use
# test data: depot + duplicate depot + 8 random locations
Locations = [0, 0, 10, 11, 14, 29, 32, 37, 43, 46]
Demands = [0, 0, 2, 5, 10, 3, 5, 7, 5, 4]
Time_Windows = [(0, 0), (10800, 18000),
                (0, 32400), (0, 32400),
                (0, 32400), (0, 32400),
                (0, 32400), (0, 32400),
                (0, 32400), (0, 32400)]


def create_data_model(Locations, Demands, TimeWindows):

    data = {}
    data["locations"] = Locations
    data['name_locations'] = [str(coordinate_array[nl][0]) for nl in Locations]
    data['coordinates'] = [(float(coordinate_array[coor][1]),
                            float(coordinate_array[coor][2])) for coor in Locations]
    data['num_locations'] = len(data['coordinates'])
    data["num_vehicles"] = 1
    data["depot"] = 0
    data["demands"] = Demands
    data["vehicle_capacities"] = [100] # >> sum of test data (unlimited for testing)
    data["time_per_demand_unit"] = 200 # approximate / guessed value, just for testing
    #
    # TimeWindows = [(0, 0), (10800, 18000)]
    # while len(TimeWindows) < len(data['coordinates']):
    #     TimeWindows.append((0, 32400))

    data["time_windows"] = TimeWindows

    return data


# # Visualisation
#
# def exp_data_plot(Locations, Demands):
#
#     base = [114.748125, 37.750201]
#     fig = plt.figure(figsize = (15, 10))
#     ax1 = fig.add_subplot(111)
#
#     lats = np.asarray(coordinate_array[:, 1], dtype=float)
#     lngs = np.asarray(coordinate_array[:, 2], dtype=float)
#
#     vis_lats = np.asarray(list(coordinate_array[lat, 1] for lat in Locations[:]), dtype = float)
#     vis_lngs = np.asarray(list(coordinate_array[lng, 2] for lng in Locations[:]), dtype = float)
#
#     ax1.set_title('Locations in North ZhaoXian')
#     plt.xlabel('lats')
#     plt.ylabel('lngs')
#
#     ax1.scatter(lats, lngs, c = 'r',marker = 'o')
#     ax1.scatter(vis_lats, vis_lngs, c = 'b',marker = 'o')
#     ax1.scatter(base[0], base[1], c = 'g',marker = 'o')
#
#     for i, d in enumerate(Demands):
#         ax1.annotate(d, (vis_lats[i], vis_lngs[i]))
#
#     plt.show()
#
# exp_data_plot(Locations, Demands)


StartTime = datetime.datetime.now()

# Constraints

def create_distance_callback(data):

    def distance_callback(from_node, to_node):
        return Distance_Matrix.iloc[from_node, to_node]

    return distance_callback

def create_time_callback(data):

    def travel_time_callback(from_node, to_node):
        return Time_Matrix.iloc[from_node, to_node]

    def service_time_callback(node):
        return data["demands"][node] * data["time_per_demand_unit"]

    def time_callback(from_node, to_node):
        service_time = service_time_callback(from_node)
        travel_time = travel_time_callback(from_node, to_node)
        total_time = travel_time + service_time
        return total_time

    return time_callback


def add_time_window_constraints(routing, data, time_callback):

    time = "Time"
    horizon = 32400 # Max. Time per Vehicle per Day (9 hours)
    routing.AddDimension(
        time_callback,
        horizon, # allow waiting time
        horizon, # maximum time per vehicle
        False,
        time)

    time_dimension = routing.GetDimensionOrDie(time)
    for location_node, location_time_window in enumerate(data["time_windows"]):
        index = routing.NodeToIndex(location_node)
        time_dimension.CumulVar(index).SetRange(location_time_window[0],
                                                location_time_window[1])


# Print Functions

def print_solution(data, routing, assignment):

    time_dimension = routing.GetDimensionOrDie('Time')
    total_dist = 0
    time_matrix = 0

    for vehicle_id in range(data["num_vehicles"]):

        index = routing.Start(vehicle_id)
        plan_output = '\n路径规划： {0}号车:\n'.format(vehicle_id+1)
        route_dist = 0

        while not routing.IsEnd(index):
            node_index = routing.IndexToNode(index)
            next_node_index = routing.IndexToNode(assignment.Value(routing.NextVar(index)))
            route_dist += routing.GetArcCostForVehicle(node_index,
                                                       next_node_index,
                                                       vehicle_id)
            time_var = time_dimension.CumulVar(index)
            time_min = assignment.Min(time_var)
            time_max = assignment.Max(time_var)
            plan_output += ' {0}    ' \
                           '距离：{1:.2f}千米, ' \
                           '驾车时长：{2:.0f}分钟， ' \
                           '最早到达时间：+{3:.0f}分钟， ' \
                           '最晚离开时间：+{4:.0f}分钟 ->\n'.format(
                coordinate_array[data["locations"][node_index]][0],
                Distance_Matrix.iloc[node_index][next_node_index]/1000,
                Time_Matrix.iloc[node_index][next_node_index]/60,
                time_min/60,
                time_max/60,)
            index = assignment.Value(routing.NextVar(index))

        node_index = routing.IndexToNode(index)
        time_var = time_dimension.CumulVar(index)
        route_time = assignment.Value(time_var)
        time_min = assignment.Min(time_var)
        time_max = assignment.Max(time_var)
        total_dist += route_dist
        time_matrix += route_time
        plan_output += ' {0}    ' \
                       '最早到达时间：+{1:.0f}分钟， ' \
                       '最晚离开时间：+{2:.0f}分钟\n'.format(
            coordinate_array[data["locations"][node_index]][0],
            time_min/60,
            time_max/60)

        plan_output += '\n总路程: {0} 千米\n'.format(route_dist/1000)
        plan_output += '总时长 {:.2f} 小时\n'.format(route_time/3600)
        print(plan_output)
        print("-"*100)

    print('\n所有车辆总路程: {0} 千米'.format(total_dist/1000))
    print('所有车辆总时间 {:.2f} 小时\n'.format(time_matrix/3600))


# Main Functions

def Main():

    data = create_data_model(Locations, Demands, Time_Windows)

    # Create Routing Model
    routing = pywrapcp.RoutingModel(data["num_locations"], data["num_vehicles"], data["depot"])

    # Define weight of each edge
    distance_callback = create_distance_callback(data)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
    # Add Time Window constraint

    time_callback = create_time_callback(data)
    add_time_window_constraints(routing,
                                data,
                                time_callback)

    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        printer = print_solution(data, routing, assignment)


Main()



EndTime = datetime.datetime.now()
processing_time = (EndTime - StartTime).seconds

print("="*100)
print("\n程序运行时间： %d 秒\n" % processing_time)
