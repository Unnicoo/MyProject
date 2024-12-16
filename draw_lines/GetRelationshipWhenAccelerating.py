import matplotlib.pyplot as plt

from draw_lines.load_file import *


index_minV_maxV = [
    # 0, 1000, 1500     # -0.05 ~ -0.15的加速部分
    # 1, 200, 1000      # -0.05 ~ -0.25的加速部分
    # 3, 1000, 2000
    4, 600, 1500
]
speed_range = titles[index_minV_maxV[0]]
file = data[speed_range]
t_values, a_values, _ = get_time_a_v_values(file)
selected_v_values, selected_a_values, time_values = select_v_a_t_values(file, index_minV_maxV[1], index_minV_maxV[2])
delta_v_values = get_delta_v(selected_v_values)

# print(len(selected_a_values))
# print(len(selected_v_values))

# 画出加速阶段的vt图
plt.scatter(time_values, selected_v_values)
plt.title(f'v - t when {speed_range} accelerating')
plt.xlabel('t')
plt.ylabel('v')
plt.show()


# 画出加速阶段的at图
plt.scatter(time_values, selected_a_values)
plt.title(f'a - t when {speed_range} accelerating')
plt.xlabel('t')
plt.ylabel('a')
plt.show()


# 画出加速阶段的av图
plt.scatter(selected_v_values, selected_a_values)
plt.title(f'a - v when {speed_range} accelerating')
plt.xlabel('v')
plt.ylabel('a')
plt.show()

# 画出加速阶段的a-delta_v图
plt.scatter(delta_v_values, selected_a_values[1:])
plt.title(f'a - delta_v when {speed_range} accelerating')
plt.xlabel('delta_v')
plt.ylabel('a')
plt.show()


