# -*- coding: utf-8 -*-

import numpy as np
from urllib.request import urlopen
import json
import datetime

global coordinate_array

start_time = datetime.datetime.now()
print("Current Progress: 0 %\n")

# Coordinate Data

coordinate_list = [
 'depot', 114.748125, 37.750201,
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

coordinate_array = np.array(coordinate_list).reshape(int(len(coordinate_list)/3), 3)


# API Baidu Maps
# Generate Est. Time & Distance between two points

def MatrixGenerator(coordinate_array):

    distance_list= []
    time_list = []

    for i in range(len(coordinate_array)):

        for j in range(len(coordinate_array)):

            url = r"https://api.map.baidu.com/routematrix/v2/driving?" \
                  r"ak=s9OuW9YnwvNp0p5gvaksv2pWmETkRe7k&" \
                  r"origins=%s,%s&" \
                  r"destinations=%s,%s&" \
                  r"tactics=11&" \
                  r"gps_direction=%d&" \
                  r"speed=%f&" \
                  r"radius=%f&" \
                  r"output=json&" \
                  r"coord_type=bd09ll" \
                  % (coordinate_array[i][2], coordinate_array[i][1],
                     coordinate_array[j][2], coordinate_array[j][1],
                     0, 11.11, 0)

            # origins / destinations = lat,lon ; string
            # tactics = 11 : regular route / 12 (13) : shortest with (without) consideration of traffic
            # gps_direction / radius : does not matter in rural area
            # speed : 40 km/h / 11.11 m/s in this case
            # coord_type = bd09ll : Baidu maps coordinate / wgs84 : gps

            req = urlopen(url, timeout=300)
            res = req.read().decode()
            temp = json.loads(res)

            distance_list.append(temp["result"][0]["distance"]["value"]) # in m
            time_list.append(temp["result"][0]["duration"]["value"]) # in s

        progress = round((i+1)/len(coordinate_array)*100)
        print("Current Progress: " + str(progress) + " % \n")

    distance_matrix = np.array(distance_list).reshape(len(coordinate_array),len(coordinate_array))
    time_matrix = np.array(time_list).reshape(len(coordinate_array),len(coordinate_array))

    return distance_matrix, time_matrix


MatrixGenerator(coordinate_array)


end_time = datetime.datetime.now()
print("="*50)
print("\nRunning Time: %s Mins.\n" % round((end_time - start_time).seconds/60))

