import matplotlib.pyplot as plt

from draw_lines.load_file import *


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


def draw_a_delta_v_image(delta_v_values, a_values, title):
    # 画出加速阶段的a-delta_v图
    plt.scatter(delta_v_values, a_values)
    plt.title(f'a - delta_v when {title} accelerating')
    plt.xlabel('delta_v')
    plt.ylabel('a')
    plt.show()


if __name__=='__main__':
    # draw_v_t_image()
    # draw_a_t_image()
    # draw_a_v_image()
    for title in titles:
        file = data[title]
        t_values, a_values, v_values = get_time_a_v_values(file)
        target_v = get_target_v(title)
        delta_v_values = get_delta_v(target_v, v_values)

        # 在这里选择执行的函数
        # draw_v_t_image(t_values, v_values, title)
        # draw_a_t_image(t_values, a_values, title)
        # draw_a_v_image(v_values, a_values, title)
        # draw_a_delta_v_image(delta_v_values, a_values, title)
    pass

