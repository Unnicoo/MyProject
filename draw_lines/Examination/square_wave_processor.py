import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from pylab import mpl

from draw_lines.draw_line import GenerateImage
from draw_lines.load_file import data_utils
from draw_lines.Utils.deal_with_data import DataProcessing as DP

mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']

omega_n = 4.75593398699244
zeta = 1.0577697080793695


def overdamped_second_order_response(t, omega_n, zeta, ini_v, target_v):
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

# 两端目标速度的测试
# tar_v_param = [ini_v] * acc_t[0][1]
# acc_t_len = (acc_t[0][2] - acc_t[0][1])// 2
# trash = [target_v] * (acc_t_len)
# tar_v_param.extend(trash)
# trash = [target_v + 0.05] * (acc_t_len)
# tar_v_param.extend(trash)
# pprint(tar_v_param)


if __name__ == '__main__':
    titles = data_utils.titles
    data = data_utils.data

    for title in titles:
        group = data[title]
        t_values, v_values, a_values = DP.get_t_v_a_values(group, title)

        ini_v = 0.00981379
        # tar_v = DP.get_target_v(title)
        # diff_v = DP.get_diff_v(title)

        # 获取传入的目标速度序列
        targetV = DP.get_targetV(group)                                      # 1774
        max_t = t_values[-1]

        average_t = np.linspace(0, max_t - 1, max_t)
        average_t = np.rint(average_t)
        t_step = 0.001

        target_v_values = np.array([])
        keep_v = 0

        for t in range(len(average_t)):
            if t in targetV:
                keep_v = targetV[t]
            target_v_values = np.append(target_v_values, [keep_v])

        pred_v = []
        for t in average_t:
            t = int(t)
            if t == 0:
                org_tar_v = ini_v
                start_t_index = t
                calculated_v = [0.0] * 1000
                cur_v = ini_v
                start_v = ini_v
                pred_v.append(cur_v)
                continue

            tar_v = target_v_values[t]

            if tar_v == org_tar_v:
                cur_v = start_v + calculated_v[t - start_t_index]
                pred_v.append(cur_v)
            else:
                start_v = cur_v
                calculated_v = overdamped_second_order_response(average_t * t_step, omega_n, zeta, cur_v, tar_v)
                start_t_index = t - 1
                cur_v = start_v + calculated_v[t - start_t_index]
                pred_v.append(cur_v)

            org_tar_v = tar_v

        plt.plot(average_t, pred_v, color='red', linestyle='solid', marker='o', alpha=0.01, label='预期曲线')

        t = np.array(t_values)
        v = np.array(v_values)

        # 对齐起点
        # if v[0] != ini_v:
        #     v -= (v[0] - ini_v)

        plt.plot(t, v, color='blue', linestyle='-', marker='o', alpha=0.2, label='实际曲线')
        plt.title(f'{title}  v-t图')
        plt.legend()
        plt.grid(True)
        plt.show()
