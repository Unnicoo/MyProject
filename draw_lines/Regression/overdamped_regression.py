import numpy as np
from scipy.optimize import curve_fit
from draw_lines.load_file import *
from draw_lines.data.accelerating_part_t_values import *
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']


def overdamped_second_order(t, omega_n, zeta):
    """
    计算过阻尼二阶系统的响应。

    参数:
    t (float or array-like): 时间向量
    omega_n (float): 自然频率
    zeta (float): 阻尼比 (zeta > 1 表示过阻尼)

    返回:
    float or array-like: 系统的响应
    """

    # 输入验证
    if zeta <= 1:
        raise ValueError("阻尼比 zeta 应大于 1，表示过阻尼系统。")

    # 计算 sigma 和 sqrt_part
    sigma = zeta * omega_n
    sqrt_part = np.sqrt(sigma ** 2 - omega_n ** 2)

    # 计算 A1 和 A2
    A1 = (sigma + sqrt_part) / (2 * sqrt_part)
    A2 = -(sigma - sqrt_part) / (2 * sqrt_part)

    # 避免除零错误
    if np.isclose(sqrt_part, 0.0):
        return 1 - np.exp(-sigma * t) * (1 + sigma * t)

    # 使用 expm1 来提高数值稳定性
    term1 = A1 * np.exp((sqrt_part - sigma) * t)
    term2 = A2 * np.exp(-(sqrt_part + sigma) * t)

    # 避免直接计算大指数
    response = 1 - np.exp(-sigma * t) * (term1 + term2)

    return response


def fit_overdamped_second_order(t_data, v_data, ini_omega_n=1.0, ini_zeta=1.0):
    # 初始参数估计值
    initial_guess = [ini_omega_n, ini_zeta]  # [omega_n, zeta]

    # 设置参数的上下界
    # bounds = ([0.1, 1.01], [10.0, 10.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]
    bounds = ([2.0, 1.0], [10.0, 20.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]

    # 使用 curve_fit 进行拟合，带边界条件
    try:
        params, covariance = curve_fit(overdamped_second_order, t_data, v_data, p0=initial_guess, bounds=bounds)    # noqa
        omega_n_fit, zeta_fit = params
        print(f"拟合得到的自然频率 omega_n: {omega_n_fit}")
        print(f"拟合得到的阻尼比 zeta: {zeta_fit}")
    except RuntimeError as e:
        print(f"拟合失败: {e}")

    # 生成拟合曲线
    t_fit = np.linspace(min(t_data), max(t_data), 100)
    y_fit = overdamped_second_order(t_fit, omega_n_fit, zeta_fit)       # noqa

    # 绘制原始数据和拟合曲线
    import matplotlib.pyplot as plt

    plt.plot(t_data, v_data, 'bo', label='原始数据')
    plt.plot(t_fit, y_fit, 'r-', label='拟合曲线')
    plt.xlabel('时间 t')
    plt.ylabel('系统响应 y(t)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    index_minV_maxV = index_minV_maxV_6

    for i in range(len(index_minV_maxV)):
        title = titles[index_minV_maxV[i][0]]
        file = data[title]
        ini_v = get_initial_v(title)
        tar_v = get_target_v(title)
        diff_v = round(tar_v - ini_v, 1)
        print(f'\n目标速度减去初始速度的差值为{diff_v}')
        # time_values, selected_a_values, selected_v_values,  = get_time_a_v_values(file)
        selected_v_values, selected_a_values, time_values = select_v_a_t_values(file, index_minV_maxV[i][1],
                                                                                index_minV_maxV[i][2])

        target_v = get_target_v(title)

        t_data = np.array(time_values)
        v_data = np.array(selected_v_values)

        t_data = t_data - t_data[0]
        t_data = t_data * 1e-3
        v_data = v_data - v_data[0]
        v_data = v_data / diff_v

        fit_overdamped_second_order(t_data, v_data)
