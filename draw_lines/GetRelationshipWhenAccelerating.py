import matplotlib.pyplot as plt
from typing import List

from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.load_file import *

# 你可以在下面两个文件里面选取你的数据
# 上面那个表示全部加速过程中（包括起步、匀加速过程和终点减速）的数据
# 下面那个表示匀加速过程中（只是肉眼观察，不是真的匀加速）的数据

# from data.constant_accelerating_part_t_values import *


def draw_v_t_image(t_values, v_values, title):
    # 画出加速阶段的vt图
    plt.scatter(t_values, v_values)
    plt.title(f'v - t when {title} accelerating')
    plt.xlabel('t')
    plt.ylabel('v')

    plt.show()


def draw_a_t_image(t_values, a_values, title):
    # 画出加速阶段的at图
    plt.scatter(t_values, a_values)
    plt.title(f'a - t when {title} accelerating')
    plt.xlabel('t')
    plt.ylabel('a')
    plt.show()


def draw_a_v_image(v_values, a_values, title):
    # 画出加速阶段的av图
    plt.scatter(v_values, a_values)
    plt.title(f'a - v when {title} accelerating')
    plt.xlabel('v')
    plt.ylabel('a')
    plt.show()


def draw_a_delta_v_image(delta_v_values, selected_a_values, title):
    # 画出加速阶段的a-delta_v图
    plt.scatter(delta_v_values, selected_a_values)
    plt.title(f'a - delta_v when {title} accelerating')
    plt.xlabel('delta_v')
    plt.ylabel('a')
    plt.show()


def draw_five_a_delta_v_images(_data: dict[List[dict]], acc_t_ranges: List[List]):
    count = 0
    while count < len(_data):
        fig, ax = plt.subplots(figsize=(10, 10))

        for _ in range(5):
            title = titles[acc_t_ranges[count][0]]
            target_v = DataProcessing.get_target_v(title)
            _, selected_v_values, selected_a_values = DataProcessing.select_t_v_a_values(_data[title], acc_t_ranges[count][1], acc_t_ranges[count][2])
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


def draw_same_delv_a_delta_v_images_by_5(_data: dict[List[dict]], acc_t_ranges: List[List], delta):
    data = DataProcessing.get_same_delta_data(_data, delta)
    # data.pop('-0.15~-0.35')
    _acc_t_ranges = []
    for title in data:
        index = titles.index(title)
        print(index)
        _acc_t_ranges.append(acc_t_ranges[index])
    draw_five_a_delta_v_images(data, _acc_t_ranges)


def get_same_iniv_a_delta_v_images_by_5(_data: dict[List[dict]], acc_t_ranges: List[List], ini_speed):
    appointed_data = {}
    _acc_t_ranges = []
    for title in _data:
        if DataProcessing.get_initial_v(title) == ini_speed:
            index = titles.index(title)
            appointed_data[title] = _data[title]
            _acc_t_ranges.append(acc_t_ranges[index])
    draw_five_a_delta_v_images(appointed_data, _acc_t_ranges)


def draw_accelerating_part_on_origin(title, t_values, v_values, time_values, selected_v_values):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(t_values, v_values)
    ax.scatter(time_values, selected_v_values, color='r')
    ax.set_xlabel('t')
    ax.set_ylabel('v')
    plt.title(f'{title} v - t line')
    # ax.legend()
    plt.show()


if __name__=='__main__':
    data = data_utils.data
    titles = data_utils.titles
    acc_t_ranges = data_utils.acc_t_ranges

    # 这部分会自动处理数据，不用管，只需要更改下面执行哪些函数
    for i in range(len(acc_t_ranges)):
        title = titles[acc_t_ranges[i][0]]
        file = data[title]
        t_values, v_values, a_values = DataProcessing.get_t_v_a_values(file)
        selected_t_values, selected_v_values, selected_a_values = DataProcessing.select_t_v_a_values(file, acc_t_ranges[i][1],
                                                                                                     acc_t_ranges[i][2])
        target_v = DataProcessing.get_target_v(title)
        delta_v_values = DataProcessing.get_delta_v(float(target_v), selected_v_values)
        _data = DataProcessing.get_same_delta_data(data, 0.1)

        # 画出全部过程中的vt图
        # draw_v_t_image(t_values, v_values, title)

        # 画出经过时间限制的vt图，也就是说你只能看到加速部分的vt图像
        # draw_v_t_image(selected_t_values, selected_v_values, title)

        # 画出加速部分在全部过程中的部分的vt图
        # draw_accelerating_part_on_origin(title, t_values, v_values, selected_t_values, selected_v_values)

        # 画出全部过程中的at图
        # draw_a_t_image(t_values, a_values, title)

        # 画出全部过程中的av图
        # draw_a_v_image(delta_v_values, a_values, title)

        # 画出a-delta_v图像
        # draw_a_delta_v_image(delta_v_values, selected_a_values, title)

    # 五个一组画出a-delta_v图像
    # draw_five_a_delta_v_images(data, acc_t_ranges)

    # 把速度差相等的a-delta_v图画在一起，可以调整delta来更改速度差
    # draw_same_delv_a_delta_v_images_by_5(data, acc_t_ranges, 0.2)

    # 把初速度相等的a-delta_v图画在一起，可以调整delta来更改初速度值
    # get_same_iniv_a_delta_v_images_by_5(data, acc_t_ranges, 0.2)
