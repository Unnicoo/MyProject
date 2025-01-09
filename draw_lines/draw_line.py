import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.load_file import *
from typing import List

data = data_utils.data
titles = data_utils.titles
data_len = len(titles)
# print(titles)


class GenerateImage:
    def __init__(self):
        raise TypeError

    @ staticmethod
    def __draw_scatter_image(x_values, y_values, pic_title, x_label='x', y_label='y'):
        assert len(x_values) == len(y_values)

        plt.figure()

        plt.scatter(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.title(pic_title)
        plt.show()

    @ staticmethod
    def __draw_scatter_images_by_group(images_type: callable, max_group_count=6, _data=data):
        sum_count = 0
        _titles = [x for x in _data]
        while sum_count < len(_titles):
            count = 1
            data_group = {}
            while count <= max_group_count:
                title = _titles[sum_count]
                data_group[title] = _data[title]
                count += 1
                sum_count += 1

                if sum_count == len(_titles):
                    images_type(data_group)
                    return

            images_type(data_group)

    @ staticmethod
    def draw_x_y_image(title):
        """
            单独画一条x-y散点图
        """
        group = data[title][:]
        x_coord, y_coord = DataProcessing.get_x_y_values(group)

        pic_title = f'{title}, y-x image'
        GenerateImage.__draw_scatter_image(x_coord, y_coord, pic_title)

    @ staticmethod
    def draw_a_t_image(title):
        """
            单独画一条a-t散点图
        """
        group = data[title][:]
        t_values, _, a_values = DataProcessing.get_t_v_a_values(group, title)

        pic_title = f'{title}, a-t image'
        GenerateImage.__draw_scatter_image(t_values, a_values, pic_title, x_label='t', y_label='a')
        # plt.plot(time_stamps, a_values, color='blue', linestyle='-', marker='o')

    @ staticmethod
    def draw_a_v_image(title):
        group = data[title][:]
        _, v_values, a_values = DataProcessing.get_t_v_a_values(group, title)

        pic_title = f'{title}, a-v image'
        GenerateImage.__draw_scatter_image(v_values, a_values, pic_title, x_label='v', y_label='a')

    @ staticmethod
    def draw_v_t_image(title):
        """
            单独画一条v-t散点图
        """
        group = data[title][:]
        t_values, v_values, _ = DataProcessing.get_t_v_a_values(group, title)

        GenerateImage.draw_v_t_image_with_data(t_values, v_values, title)

    @ staticmethod
    def draw_v_t_image_with_data(t_values, v_values, title):
        """
            根据输入的数据绘制图像
        """
        pic_title = f'{title}, v-t image'
        GenerateImage.__draw_scatter_image(t_values, v_values, pic_title, x_label='t', y_label='v')

    @ staticmethod
    def draw_accelerating_part(title, t_values, v_values, time_values, selected_v_values):
        """
            在原 v-t 图像上画出挑选的加速部分
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.scatter(t_values, v_values)
        ax.scatter(time_values, selected_v_values, color='r')
        ax.set_xlabel('t')
        ax.set_ylabel('v')
        plt.title(f'{title} v - t line')
        plt.show()

    @ staticmethod
    def _draw_all_vt_images(_data=data):
        """
            画出所有 v-t 图像
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        _titles = [x for x in _data]

        for i in range(len(_data)):
            title = _titles[i]
            group = _data[title][:]

            t_values, v_values, a_values = DataProcessing.get_t_v_a_values(group, title)

            ax.scatter(t_values, v_values, label=title)

            plt.xlabel('t')
            plt.ylabel('v')

            plt.title(f'all v - t line')

        ax.legend()
        plt.show()

    @ staticmethod
    def draw_v_t_images(max_group_count=6, _data=data):
        """
            分组画出所有 v-t 线
        """
        GenerateImage.__draw_scatter_images_by_group(GenerateImage._draw_all_vt_images, max_group_count=max_group_count, _data=_data)

    @ staticmethod
    def get_same_start_v_images():
        """
            获取相同初始速度的 v-t 图像
        :return:
        """

        def get_ini_speed(_title):
            return _title.split('~')[0]

        start_speed = get_ini_speed(titles[0])
        # print(start_speed)
        data_group = {}
        for i in range(len(titles)):
            title = titles[i]
            if get_ini_speed(title) == start_speed:
                data_group[title] = data[title]

                if i == len(titles) - 1:
                    # get_all_image(data_group)
                    GenerateImage._draw_all_vt_images(data_group)
                    return
            else:
                # get_all_image(data_group)
                GenerateImage._draw_all_vt_images(data_group)
                start_speed = title.split('~')[0]
                data_group.clear()
                data_group[title] = data[title]
                continue

    @ staticmethod
    def get_same_diff_v_images(delta):
        """
            获取相同初末速度差值的 v-t 图像
        """
        _data = DataProcessing.get_same_delta_v_data(delta)
        GenerateImage.draw_v_t_images(_data=_data)

    @ staticmethod
    def draw_a_delta_v_image(group, title, min_t, max_t):
        """
            获取单张 a-delta_v 图像
        """
        _, selected_v_values, selected_a_values = DataProcessing.select_t_v_a_values(group, title, min_t, max_t)
        target_v = DataProcessing.get_target_v(title)
        delta_v_values = DataProcessing.get_delta_v(float(target_v), selected_v_values)

        pic_title = f'{title}, a-delta_v image'
        GenerateImage.__draw_scatter_image(delta_v_values, selected_a_values, pic_title)

    @ staticmethod
    def draw_a_delta_v_images(_data: dict = data, acc_t_ranges=data_utils.acc_t_ranges, max_group_count=6):
        """
            获取所有 a-delta_v 图像
        """
        count = 0
        while count < len(_data):
            fig, ax = plt.subplots(figsize=(10, 10))

            for _ in range(max_group_count):
                acc_t_range = acc_t_ranges[count]
                title = titles[acc_t_range[0]]
                target_v = DataProcessing.get_target_v(title)
                _, selected_v_values, selected_a_values = DataProcessing.select_t_v_a_values(_data[title], title,
                                                                                             acc_t_range[1],
                                                                                             acc_t_range[2])
                delta_v_values = DataProcessing.get_delta_v(float(target_v), selected_v_values)

                ax.plot(delta_v_values, selected_a_values, label=f'{title}')
                ax.set_title(f'a - delta_v when {title} accelerating')
                count += 1

                if count == len(_data):
                    break

            plt.xlabel('delta_v')
            plt.ylabel('a')
            ax.legend()
            plt.show()

    @ staticmethod
    def draw_a_delta_v_images_with_same_diff_v(diff_v, max_group_count=6):
        """
            获取初末速度差值相等的 a-delta_v 图像
        """
        same_diff_v_data = DataProcessing.get_same_delta_v_data(diff_v)
        acc_t_ranges = []
        for title in same_diff_v_data:
            index = titles.index(title)
            acc_t_ranges.append(data_utils.acc_t_ranges[index])
        GenerateImage.draw_a_delta_v_images(same_diff_v_data, acc_t_ranges, max_group_count)

    @ staticmethod
    def draw_a_delta_v_images_with_same_ini_v(ini_v, max_group_count=6):
        """
            获取初速度相等的 a-delta_v 图像
        """
        same_ini_v_data = {}
        acc_t_ranges = []
        for title in data:
            if DataProcessing.get_initial_v(title) == ini_v:
                index = titles.index(title)
                same_ini_v_data[title] = data[title]
                acc_t_ranges.append(data_utils.acc_t_ranges[index])
        GenerateImage.draw_a_delta_v_images(same_ini_v_data, acc_t_ranges, max_group_count)


def get_all_image(_data: dict):
    """
        画出所有x-y、a-t、v-t图
    :param _data: 包含几组不同速度的数据，格式大致为{'0.1-0.2': [..], '0.1-0.3': [..]}
    :return:
    """
    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(5, 3)

    ax_list = []
    for i in range(5):
        for j in range(3):
            ax = fig.add_subplot(gs[i, j])
            ax_list.append(ax)

    ax_count = 0
    for title in _data:
        group = _data[title][:]

        x_coordinates, y_coordinates = DataProcessing.get_x_y_values(group[:])
        ax_list[ax_count].scatter(x_coordinates, y_coordinates, label=title)
        ax_list[ax_count].set_xlabel('x')
        ax_list[ax_count].set_ylabel('y')
        ax_list[ax_count].set_title(f'part {title}, y - x line')
        ax_count += 1

        time_stamps, v_values, a_values = DataProcessing.get_t_v_a_values(group, title)
        # print(time_stamps)
        # print(a_values)
        ax_list[ax_count].scatter(time_stamps, a_values, label=title)
        ax_list[ax_count].set_xlabel('t')
        ax_list[ax_count].set_ylabel('a')
        ax_list[ax_count].set_title(f'part {title}, a - t line')
        ax_count += 1

        ax_list[ax_count].scatter(time_stamps, v_values, label=title)
        ax_list[ax_count].set_xlabel('t')
        ax_list[ax_count].set_ylabel('v')
        ax_list[ax_count].set_title(f'part {title}, v - t line')
        ax_count += 1

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # for i in range(len(titles)):
        # get_single_x_y_line(i)
        # get_single_a_t_line(i)
        # get_single_v_t_line(i)
        # pass

    # GenerateImage._draw_all_vt_images()
    # GenerateImage.draw_v_t_images()
    # GenerateImage.get_same_start_v_images()

    # 调整delta的数值以获取速度差为delta的v-t图组
    GenerateImage.get_same_diff_v_images(0.1)

    pass
