import os
import re
from pathlib import Path


cur_dir = Path(__file__).parent
# print(cur_dir)

# file_name = 'time_x_y_a_v'
# file_name = '-0.05===-0.55'
file_name = 'data/-0.1===-0.5'

file_path = cur_dir / file_name


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
print(data)
print(len(data))


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


def get_time_a_v_values(data_name):
    time_stamps = []
    a_values = []
    v_values = []
    for i in range(len(data_name)):
        time_stamps.append(data_name[i]['timestamp'] - data_name[0]['timestamp'])
        a_values.append(data_name[i]['a'])
        v_values.append(data_name[i]['v'])

    return time_stamps, a_values, v_values
