import matplotlib.pyplot as plt

from draw_lines.load_file import *
# from data.accelerating_part_t_values import *
from data.constant_accelerating_part_t_values import *


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
    index_minV_maxV = index_minV_maxV_3
    for i in range(len(index_minV_maxV)):
        title = titles[index_minV_maxV[i][0]]
        file = data[title]
        t_values, a_values, v_values = get_time_a_v_values(file)
        selected_v_values, selected_a_values, time_values = select_v_a_t_values(file, index_minV_maxV[i][1],
                                                                                index_minV_maxV[i][2])
        target_v = abs(float(title.strip().split('~')[1]))
        delta_v_values = get_delta_v(float(target_v), selected_v_values)

        # draw_v_t_image(t_values, v_values, title)
        # draw_v_t_image(time_values, selected_v_values, title)
        draw_accelerating_part_on_origin(title, t_values, v_values, time_values, selected_v_values)

        # draw_a_t_image(t_values, a_values, title)

        # draw_a_v_image(delta_v_values, a_values, title)

        draw_a_delta_v_image(delta_v_values, selected_a_values, title)
    pass

