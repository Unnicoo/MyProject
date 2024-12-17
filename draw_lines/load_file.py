import os
import re
from typing import List
from pathlib import Path


cur_dir = Path(__file__).parent
# print(cur_dir)

# file_name = 'time_x_y_a_v'
# file_name = '-0.05===-0.55'
file_name = '-0.1===-0.5'

file_path = cur_dir / 'data' / file_name


def open_points_file():
    with open(file_path, 'r', encoding='utf-8') as f:
        data = {}
        current_title = None
        for line in f:
            line = line.strip()

            if '~' in line:
                if current_title is not None:
                    data[current_title] = current_data

                if line.endswith('：'):
                    current_title = line[:-1]
                else:
                    current_title = line
                current_data = []
            elif current_title is not None:
                if line:
                    current_data.append(line)

        if current_title is not None:
            data[current_title] = current_data

    return data


data = open_points_file()
titles = [x for x in data]
# print(data)
# print(len(data))
# print(titles)


for info in data.values():
    for i in range(len(info)):
        pattern = r'(\w+):\s*(-?\d*\.?\d*)'
        matches = re.findall(pattern, info[i])

        data_dict = {}
        for _key, _value in matches:
            if _key == 'timestamp':
                data_dict[_key] = int(_value)
            else:
                data_dict[_key] = float(_value)

        info[i] = data_dict     # noqa


def get_x_y_values(data_name):
    x_coordinates = []
    y_coordinates = []
    for i in range(len(data_name)):
        x_coordinates.append(data_name[i]['x'])
        y_coordinates.append(data_name[i]['y'])

    return x_coordinates, y_coordinates


def get_time_a_v_values(data_name: List[dict]):
    time_stamps = []
    a_values = []
    v_values = []

    def __get_relative_time(index):
        # 获取相对第一帧的时间
        return data_name[index]['timestamp'] - data_name[0]['timestamp']

    def __get_v(index):
        return data_name[index]['v']

    delta_num = 5
    for i in range(delta_num, len(data_name)-delta_num):
        # 得到相对第一帧的时间
        relative_time = __get_relative_time(i)
        time_stamps.append(relative_time)

        # 取前后5帧的时间计算当前点的加速度
        a = (__get_v(i+delta_num) - __get_v(i-delta_num)) / (__get_relative_time(i+delta_num) - __get_relative_time(i-delta_num))
        a_values.append(a)

        # 得到当前点的速度
        v_values.append(__get_v(i))
    return time_stamps, a_values, v_values


def calculate_a_dv_values(data: list, delta_num=5):
    time_stamp, _, v_values = get_time_a_v_values(data)
    assert len(time_stamp) == len(v_values), '时间和速度的个数不等'
    dv_values = []
    a_values = []
    for i in range(delta_num, len(v_values)-5):
        dv = v_values[i] - v_values[i-delta_num]
        da = (v_values[i] - v_values[i-delta_num]) / (time_stamp[i+delta_num] - time_stamp[i-delta_num])
        dv_values.append(dv)
        a_values.append(da)
    return dv_values, a_values


def select_v_a_t_values(data: list, min_v_value: float, max_v_value: float):
    time_stamps, a_values, v_values = get_time_a_v_values(data)
    _selected_v_values = []
    _selected_a_values = []
    time_values = []
    for i in range(len(time_stamps)):
        if min_v_value <= time_stamps[i] <= max_v_value:
            _selected_v_values.append(v_values[i])
            _selected_a_values.append(a_values[i])
            time_values.append(time_stamps[i])
    assert len(_selected_v_values) == len(_selected_a_values) == len(time_values)
    return _selected_v_values, _selected_a_values, time_values


def get_delta_v(target_v: float, v_values: list):
    delta_v_values = []
    for i in range(len(v_values)):
        delta_v = target_v - v_values[i]
        delta_v_values.append(delta_v)
    # print(len(delta_v_values))
    return delta_v_values


def get_initial_v(title: str):
    return abs(float(title.strip().split('~')[0]))


def get_target_v(title: str):
    return abs(float(title.strip().split('~')[1]))


def get_same_delta_data(_data: dict, delta):
    appointed_data = {}
    for title in _data:
        if round(get_target_v(title) - get_initial_v(title), 2) == delta:
            appointed_data[title] = _data[title]
    return appointed_data


if __name__ == '__main__':
    # print(get_time_a_v_values(data[titles[0]]))
    pass
