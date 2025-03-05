from typing import List

from draw_lines.load_file import data_utils

data = data_utils.data


class DataProcessing:
    def __init__(self):
        raise TypeError('该类是工具类，不能被实例化')

    @ staticmethod
    def get_x_y_values(group: List[dict]):
        """
            取出所有某速度范围下所有的x、y点
        :param group: 相当于data[title]，也就是上面的[{'timestamp': t1, 'x': x1, 'y': y1, 'a': a1, 'v': v1}, {第二帧信息}...]
        :return: x坐标的列表， y坐标的列表
        """
        x_coordinates = []
        y_coordinates = []
        for i in range(len(group)):
            x_coordinates.append(group[i]['x'])
            y_coordinates.append(group[i]['y'])

        return x_coordinates, y_coordinates

    @ staticmethod
    def get_targetV(group: List[dict]):
        try:
            for i in range(len(group)):
                trash = group[i]['targetV']
        except Exception as e:
            print(f'Warning: {e}')
            print("there's no targetV")
        else:
            targetV = {}
            ini_t = group[0]['timestamp']
            for i in range(len(group)):
                targetV[group[i]['timestamp'] - ini_t] = (group[i]['targetV'])
            return targetV

    @ staticmethod
    def get_v_t_values(group: List[dict], title):
        """
            得到所有的t、a、v值
        :param group: 相当于data[title]，也就是上面的[{'timestamp': t1, 'x': x1, 'y': y1, 'a': a1, 'v': v1}, {第二帧信息}...]
        :return: t坐标的列表， a坐标的列表，v坐标的列表
        """
        t_values = []
        v_values = []

        def __get_relative_time(index):
            # 获取相对第一帧的时间
            return group[index]['timestamp'] - group[0]['timestamp']

        def __get_v(index):
            return group[index]['v']

        for i in range(len(group)):
            # 得到当前点的速度
            cur_v = __get_v(i)
            v_values.append(cur_v)

            # 得到相对第一帧的时间
            relative_time = __get_relative_time(i)
            t_values.append(relative_time)

        return v_values, t_values

    @ staticmethod
    def get_t_v_a_values(group: List[dict], title):
        """
            得到所有的t、a、v值
        :param group: 相当于data[title]，也就是上面的[{'timestamp': t1, 'x': x1, 'y': y1, 'a': a1, 'v': v1}, {第二帧信息}...]
        :return: t坐标的列表， a坐标的列表，v坐标的列表
        """
        time_stamps = []
        a_values = []
        v_values = []

        def __get_relative_time(index):
            # 获取相对第一帧的时间
            return group[index]['timestamp'] - group[0]['timestamp']

        def __get_v(index):
            return group[index]['v']

        delta_num = 5
        for i in range(delta_num, len(group)-delta_num):
            # 得到当前点的速度
            cur_v = __get_v(i)
            v_values.append(cur_v)

            # 得到相对第一帧的时间
            relative_time = __get_relative_time(i)
            time_stamps.append(relative_time)

            # 取前后5帧的时间计算当前点的加速度
            a = (__get_v(i+delta_num) - __get_v(i-delta_num)) / (__get_relative_time(i+delta_num) - __get_relative_time(i-delta_num))
            a_values.append(a)

        return time_stamps, v_values, a_values

    @ staticmethod
    def select_t_v_a_values(group: List[dict], title, min_t_value: float, max_t_value: float):
        """
            获取指定的时间范围内的v、a、t列表
        :param group: 相当于data[title]，也就是上面的[{'timestamp': t1, 'x': x1, 'y': y1, 'a': a1, 'v': v1}, {第二帧信息}...]
        :param min_t_value: 最小的 t值
        :param max_t_value: 最大的 t值
        :return: t坐标的列表， a坐标的列表，v坐标的列表
        """
        time_stamps, v_values, a_values = DataProcessing.get_t_v_a_values(group, title)
        selected_v_values = []
        selected_a_values = []
        time_values = []
        for i in range(len(time_stamps)):
            if min_t_value <= time_stamps[i] <= max_t_value:
                selected_v_values.append(v_values[i])
                selected_a_values.append(a_values[i])
                time_values.append(time_stamps[i])
        assert len(selected_v_values) == len(selected_a_values) == len(time_values)
        return time_values, selected_v_values, selected_a_values

    @ staticmethod
    def get_initial_v(title: str):
        """
            获取初始速度
        :param title: 形如'0.1 ~ 0.2'的字符串
        :return: 初始速度
        """
        return abs(float(title.strip().split('~')[0]))

    @ staticmethod
    def get_target_v(title: str):
        """
            获取目标速度
        :param title: 形如'0.1 ~ 0.2'的字符串
        :return: 目标速度
        """
        if ' ' in title:
            title = title.split(' ')[0]
        return abs(float(title.strip().split('~')[1]))

    @ staticmethod
    def get_diff_v(title: str):
        return round(DataProcessing.get_target_v(title) - DataProcessing.get_initial_v(title), 2)

    @ staticmethod
    def get_delta_v(target_v: float, v_values: list):
        """
            获取delta_v，也就是目标速度减去当前速度
        :param target_v: 目标速度
        :param v_values: 房前速度
        :return: 包含所有delta_v的列表
        """
        delta_v_values = []
        for i in range(len(v_values)):
            delta_v = target_v - v_values[i]
            delta_v_values.append(delta_v)
        # print(len(delta_v_values))
        return delta_v_values

    @ staticmethod
    def get_same_delta_v_data(delta):
        """
            获取相同初末速度差值的数据
        """
        appointed_data = {}
        for title in data:
            if DataProcessing.get_diff_v(title) == delta:
                appointed_data[title] = data[title]
        return appointed_data
