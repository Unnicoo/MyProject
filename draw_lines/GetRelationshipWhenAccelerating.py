import matplotlib.pyplot as plt

from draw_lines.load_file import *

# 你可以在下面两个文件里面选取你的数据
# 上面那个表示全部加速过程中（包括起步、匀加速过程和终点减速）的数据
# 下面那个表示匀加速过程中（只是肉眼观察，不是真的匀加速）的数据

from data.accelerating_part_t_values import *
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
    # 可以在这里设置使用的哪份数据的范围
    # index_minV_maxV_1 表示第一份数据，也就是5个前进数据
    # index_minV_maxV_2 表示第二份数据，也就是15个前进数据
    # index_minV_maxV_3 表示第三份数据，也就是25个倒车数据
    # 注意：需要配合load_file文件中读取的文件内容，也就是说load_file中读取的第一个文件，那这里就改成index_minV_maxV_1

    index_minV_maxV = index_minV_maxV_3

    # 这部分会自动处理数据，不用管，只需要更改下面执行哪些函数
    for i in range(len(index_minV_maxV)):
        title = titles[index_minV_maxV[i][0]]
        file = data[title]
        t_values, a_values, v_values = get_time_a_v_values(file)
        selected_v_values, selected_a_values, time_values = select_v_a_t_values(file, index_minV_maxV[i][1],
                                                                                index_minV_maxV[i][2])
        target_v = abs(float(title.strip().split('~')[1]))
        delta_v_values = get_delta_v(float(target_v), selected_v_values)

        # 画出全部过程中的vt图
        # draw_v_t_image(t_values, v_values, title)

        # 画出经过时间限制的vt图，也就是说你只能看到加速部分的vt图像
        # draw_v_t_image(time_values, selected_v_values, title)

        # 画出加速部分在全部过程中的部分的vt图
        draw_accelerating_part_on_origin(title, t_values, v_values, time_values, selected_v_values)

        # 画出全部过程中的at图
        # draw_a_t_image(t_values, a_values, title)

        # 画出全部过程中的av图
        # draw_a_v_image(delta_v_values, a_values, title)

        # 画出a-delta_v图像
        draw_a_delta_v_image(delta_v_values, selected_a_values, title)
    pass

