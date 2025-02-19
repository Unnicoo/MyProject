import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

from draw_lines.draw_line import GenerateImage
from draw_lines.load_file import data_utils
from draw_lines.Utils.deal_with_data import DataProcessing as DP

mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']

data = data_utils.data
titles = data_utils.titles
acc_t = data_utils.acc_t_ranges

omega_n = 4.75593398699244
zeta = 1.0577697080793695


def overdamped_second_order_response(t, omega_n, zeta, ini_v, target_v):
    """
        速度时间关系
    :param t: 单位是s;可以是时刻，也可以是时间序列，影响得到的结果是数值还是数组
    :param omega_n: 自然频率
    :param zeta: 阻尼比
    :param ini_v: 初始速度（运动过程中最初的速度数值，不会随着时间变化）
    :param target_v: 给定的目标速度
    :return: 给定目标速度下，该时间点的速度值
    """
    sigma = omega_n * zeta
    sqrt_part = np.sqrt(sigma ** 2 - omega_n ** 2)

    A1 = (sigma + sqrt_part) / (2 * sqrt_part)
    A2 = -(sigma - sqrt_part) / (2 * sqrt_part)

    # 避免除零错误
    if np.isclose(sqrt_part, 0.0):
        print('为避免除零错误，采用近似拟合')
        return 1 - np.exp(-sigma * t) * (1 + sigma * t)

    term1 = A1 * np.exp(sqrt_part * t)
    term2 = A2 * np.exp(-sqrt_part * t)

    response = 1 - np.exp(-sigma * t) * (term1 + term2)
    response *= (target_v - ini_v)

    return response


if __name__ == '__main__':
    for title in titles:
        group = data[title]
        v_values, t_values = DP.get_v_t_values(group, title)
        ini_v = v_values[0]

        targetV = DP.get_targetV(group)

        # 得到时间序列
        time_steps = np.array(list(targetV.keys()))

        # 获取传入的目标速度序列
        v_targets = list(targetV.values())

        # 计算实际速度曲线
        pred_v = []
        for i, t in enumerate(time_steps / 1000):
            print(i, t)
            v_target = v_targets[i]
            v_t = ini_v + overdamped_second_order_response(t, omega_n, zeta, ini_v, v_target)
            pred_v.append(v_t)

        # 绘制v-t图
        t_values, v_values, a_values = DP.get_t_v_a_values(group, title)
        t = np.array(t_values)
        v = np.array(v_values)

        plt.scatter(t, v, alpha=0.2, label='实际曲线')
        plt.scatter(time_steps, pred_v, color='red', alpha=0.2, label='预期曲线')
        plt.xlabel('Time (ms)')
        plt.ylabel('Velocity')
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.show()
