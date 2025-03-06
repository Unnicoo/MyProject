import os
import re
from pathlib import Path

# from draw_lines.data.accelerating_part_t_values import accelerating_t_values
from draw_lines.data.try_t_part import accelerating_t_values

cur_dir = Path(__file__).parent
data_path = cur_dir / 'data'
file_names = [f for f in os.listdir(data_path) if f.endswith('.txt')]
# file_names = [
#     '-0.05~-0.55以及-0.1~-0.5倒车.txt',      # index:0
#     '-0.05~-0.55倒车.txt',                  # index:1
#     '-0.1~-0.5倒车.txt',                    # index:2
#     '-0.55~0.55_10度.txt',                  # index:3
#     '-0.55~0.55_18度.txt',                  # index:4
#     '0.05~0.55正向.txt',                    # index:5
#     '0.05~0.55正向两组.txt',                 # index:6
#     '0.1~0.5正向两组.txt',                   # index:7
#     '0.1~0.6正向.txt'                       # index:8
#     'sin曲线-0.55~0.55.txt.txt'             # index:9
#     'sin曲线0.35~0.55.txt.txt'              # index:10
#     'telecontrol1.txt'                      # index:11
#     'telecontrol2.txt'                      # index:12
#     'telecontrol3.txt'                      # index:13
# ]
# print(file_names)
DEFAULT_INDEX = 12
APPLY_FILTER = True


class DataUtils:
    def __init__(self):
        self.file_name = file_names[DEFAULT_INDEX]
        self.data = self.__read_raw_data()
        self.titles = [x for x in self.data]
        self.accelerating_data = self.data
        self.acc_t_ranges = self.__get_accelerating_t_ranges()

    def __read_raw_data(self):
        """
            读取文件
        :return: data的格式为{'0.1-0.2': [], ...}
        """
        file_path = cur_dir / 'data' / self.file_name
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

                    info[i] = data_dict  # noqa
        if APPLY_FILTER:
            for title, group in data.items():
                i = 0
                while i < len(group):
                    if group[i]['v'] > 0.8:                                                # noqa
                        print(f'速度采样有误,数值为{group[i]["v"]},已去除该点')                # noqa
                        group.pop(i)
                    elif group[i]['targetV'] > 0.8:                                        # noqa
                        print(f'目标速度采样有误,数值为{group[i]["targetV"]},已去除该点')       # noqa
                        group.pop(i)
                    else:
                        i += 1
        return data
    # 文件格式：data = {'v1-v2': [{'timestamp': t1, 'x': x1, 'y': y1, 'a': a1, 'v': v1}, {第二帧信息}...], {'v2-v3'}: [...]}
    # print(data)

    def __get_accelerating_t_ranges(self):
        try:
            accelerating_t_range = accelerating_t_values[self.file_name[:-4]]
        except:
            print("thers's no accelerating_t_ranges")
            accelerating_t_range = []
        return accelerating_t_range

    def reset_file(self, index):
        self.file_name = file_names[index]
        self.data = self.__read_raw_data()
        self.titles = [x for x in self.data]
        self.acc_t_ranges = self.__get_accelerating_t_ranges()


data_utils = DataUtils()
