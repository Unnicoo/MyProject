import matplotlib.pyplot as plt

from draw_lines.load_file import *


index_minV_maxV = [
    # 0, 1000, 1500       # -0.05 ~ -0.15的加速部分
    # 1, 200, 1000        # -0.05 ~ -0.25的加速部分
    # 2, 550, 1500        # -0.05 ~ -0.35的加速部分
    # 3, 1000, 2000       # -0.05 ~ -0.45的加速部分
    # 4, 600, 1500        # -0.05 ~ -0.55的加速部分
    # 5, 550, 1000        # -0.15 ~ -0.25的加速部分
    # 6, 550, 1300        # -0.15 ~ -0.35的加速部分
    # 7, 2650, 3800       # -0.15 ~ -0.45的加速部分
    # 8, 700, 2000        # -0.15 ~ -0.55的加速部分
    # 9, 1200, 2000       # -0.25 ~ -0.35的加速部分
    # 10, 500, 1300       # -0.25 ~ -0.45的加速部分
    # 11, 1150, 2000      # -0.25 ~ -0.55的加速部分
    # 12, 0, 0            # -0.35 ~ -0.45的加速部分，用不了，空了一段
    # 13, 1100, 2000      # -0.35 ~ -0.55的加速部分
    # 14, 1200, 2200      # -0.45 ~ -0.55的加速部分

    # 15, 400, 1100       # -0.1 ~ -0.2的加速部分
    # 16, 250, 1000       # -0.1 ~ -0.3的加速部分
    # 17, 900, 1600       # -0.1 ~ -0.4的加速部分
    # 18, 700, 1500       # -0.1 ~ -0.5的加速部分
    # 19, 900, 1500       # -0.2 ~ -0.3的加速部分
    # 20, 950, 1500       # -0.2 ~ -0.4的加速部分
    # 21, 750, 1900       # -0.2 ~ -0.5的加速部分
    # 22, 1200, 2000      # -0.3 ~ -0.4的加速部分
    # 23, 600, 1700       # -0.3 ~ -0.5的加速部分
    # 24, 650, 1500       # -0.4 ~ -0.5的加速部分
]
speed_range = titles[index_minV_maxV[0]]
file = data[speed_range]
t_values, a_values, _ = get_time_a_v_values(file)
selected_v_values, selected_a_values, time_values = select_v_a_t_values(file, index_minV_maxV[1], index_minV_maxV[2])
target_v = abs(float(speed_range.strip().split('~')[1]))
delta_v_values = get_delta_v(float(target_v), selected_v_values)

# print(len(selected_a_values))
# print(len(selected_v_values))


def draw_v_t_image():
    # 画出加速阶段的vt图
    plt.scatter(time_values, selected_v_values)
    plt.title(f'v - t when {speed_range} accelerating')
    plt.xlabel('t')
    plt.ylabel('v')
    plt.show()


def draw_a_t_image():
    # 画出加速阶段的at图
    plt.scatter(time_values, selected_a_values)
    plt.title(f'a - t when {speed_range} accelerating')
    plt.xlabel('t')
    plt.ylabel('a')
    plt.show()


def draw_a_v_image():
    # 画出加速阶段的av图
    plt.scatter(selected_v_values, selected_a_values)
    plt.title(f'a - v when {speed_range} accelerating')
    plt.xlabel('v')
    plt.ylabel('a')
    plt.show()


def draw_a_delta_v_image():
    # 画出加速阶段的a-delta_v图
    plt.scatter(delta_v_values, selected_a_values)
    plt.title(f'a - delta_v when {speed_range} accelerating')
    plt.xlabel('delta_v')
    plt.ylabel('a')
    plt.show()


if __name__=='__main__':
    # draw_v_t_image()
    # draw_a_t_image()
    # draw_a_v_image()
    draw_a_delta_v_image()
    pass

