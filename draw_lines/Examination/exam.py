import matplotlib.pyplot as plt
import numpy as np

from overdamped_second_order_system import OverdampedSecondOrderSystem
from draw_lines.Examination.sine_wave_processor import overdamped_second_order_response
from draw_lines.load_file import data_utils
from draw_lines.Utils.deal_with_data import DataProcessing as DP


data = data_utils.data
titles = data_utils.titles
acc_t = data_utils.acc_t_ranges


omega_n = 4.75593398699244
zeta = 1.0577697080793695
dt = 11/1000

model = OverdampedSecondOrderSystem(zeta=zeta, omega_n=omega_n, dt=dt)


if __name__ == '__main__':
    group = data[titles[0]]
    v_values, t_values = DP.get_v_t_values(group, titles[0])
    v_values = np.array(v_values)
    ini_v = v_values[0]

    targetV = DP.get_targetV(group)

    # 得到时间序列
    time_steps = np.array(list(targetV.keys()))

    # 获取传入的目标速度序列
    v_targets = list(targetV.values())

    # cut_idx = 950
    # v_values = v_values[:cut_idx]
    # v_targets = v_targets[:cut_idx]
    # time_steps = time_steps[:cut_idx]

    v_preds = model.evaluate(v_targets, [v_values[0], 0])

    # v_preds_old = []
    # for i, t in enumerate(time_steps / 1000):
    #     v_target = v_targets[i]
    #     v_t = ini_v + overdamped_second_order_response(t, omega_n, zeta, ini_v, v_target)
    #     v_preds_old.append(v_t)

    marker_size = 6
    plt.scatter(time_steps, v_values, alpha=0.2, label='实际曲线', s=marker_size)
    plt.scatter(time_steps, v_preds, color='red', alpha=0.2, label='预期曲线', s=marker_size)
    # plt.scatter(time_steps, v_preds_old, color='green', alpha=0.2, label='之前预期曲线', s=marker_size)
    plt.xlabel('Time (ms)')
    plt.ylabel('Velocity')
    plt.title(titles[0])
    plt.grid(True)
    plt.legend()
    plt.show()

