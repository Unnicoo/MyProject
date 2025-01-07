import numpy as np
from scipy.optimize import curve_fit

from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.load_file import *
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']
data = data_utils.data
titles = data_utils.titles


def overdamped_second_order(t: np.array, omega_n: float, zeta: float):
    """
    计算过阻尼二阶系统的响应。

    参数:
    t : 时间向量
    omega_n: 自然频率
    zeta: 阻尼比 (zeta > 1 表示过阻尼)

    返回:
    np.array: 系统响应
    """

    if zeta <= 1:
        raise ValueError("阻尼比 zeta 应大于 1，表示过阻尼系统。")

    sigma = zeta * omega_n
    sqrt_part = np.sqrt(sigma ** 2 - omega_n ** 2)

    A1 = (sigma + sqrt_part) / (2 * sqrt_part)
    A2 = -(sigma - sqrt_part) / (2 * sqrt_part)

    # 避免除零错误
    if np.isclose(sqrt_part, 0.0):
        return 1 - np.exp(-sigma * t) * (1 + sigma * t)

    term1 = A1 * np.exp((sqrt_part - sigma) * t)
    term2 = A2 * np.exp(-(sqrt_part + sigma) * t)

    response = 1 - np.exp(-sigma * t) * (term1 + term2)

    return response


def fit_overdamped_second_order(t_data, v_data, ini_omega_n=1.0, ini_zeta=1.0):
    initial_guess = [ini_omega_n, ini_zeta]  # [omega_n, zeta]

    # bounds = ([0.1, 1.01], [10.0, 10.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]
    bounds = ([1.0, 1.0], [10.0, 20.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]

    try:
        params, covariance = curve_fit(overdamped_second_order, t_data, v_data, p0=initial_guess, bounds=bounds)    # noqa
        omega_n_fit, zeta_fit = params
        print(f"拟合得到的自然频率 omega_n: {omega_n_fit}")
        print(f"拟合得到的阻尼比 zeta: {zeta_fit}")
    except RuntimeError as e:
        print(f"拟合失败: {e}")

    t_fit = np.linspace(min(t_data), max(t_data), 100)
    y_fit = overdamped_second_order(t_fit, omega_n_fit, zeta_fit)       # noqa

    import matplotlib.pyplot as plt

    plt.plot(t_data, v_data, 'bo', label='原始数据')
    plt.plot(t_fit, y_fit, 'r-', label='拟合曲线')
    plt.xlabel('时间 t')
    plt.ylabel('系统响应 y(t)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    acc_t_ranges = data_utils.acc_t_ranges

    for i in range(len(acc_t_ranges)):
        title = titles[acc_t_ranges[i][0]]
        file = data[title]
        ini_v = DataProcessing.get_initial_v(title)
        tar_v = DataProcessing.get_target_v(title)
        diff_v = round(tar_v - ini_v, 2)
        print(f'\n目标速度减去初始速度的差值为{diff_v}')
        # time_values, selected_v_values, _ = DataProcessing.get_t_v_a_values(file)
        t_values, v_values, _ = DataProcessing.select_t_v_a_values(file, acc_t_ranges[i][1], acc_t_ranges[i][2])

        target_v = DataProcessing.get_target_v(title)

        t_data = np.array(t_values)
        v_data = np.array(v_values)

        t_data = t_data - t_data[0]
        t_data = t_data * 1e-3
        v_data = v_data - v_data[0]
        v_data = v_data / diff_v

        fit_overdamped_second_order(t_data, v_data)
