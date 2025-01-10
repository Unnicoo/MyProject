import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pylab import mpl
from scipy.signal import savgol_filter

from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.draw_line import GenerateImage
from draw_lines.load_file import *

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
        print('为避免除零错误，采用近似拟合')
        return 1 - np.exp(-sigma * t) * (1 + sigma * t)

    term1 = A1 * np.exp(sqrt_part * t)
    term2 = A2 * np.exp(-sqrt_part * t)

    response = 1 - np.exp(-sigma * t) * (term1 + term2)

    return response


def overdamped_second_order_derivative(t: np.array, omega_n: float, zeta: float):
    """
    计算过阻尼二阶系统响应的加速度。

    参数:
    t : 时间向量
    omega_n: 自然频率
    zeta: 阻尼比 (zeta > 1 表示过阻尼)

    返回:
    np.array: 加速度响应
    """
    if zeta <= 1:
        raise ValueError("阻尼比 zeta 应大于 1，表示过阻尼系统。")

    sigma = zeta * omega_n
    sqrt_part = np.sqrt(sigma ** 2 - omega_n ** 2)

    A1 = (sigma + sqrt_part) / (2 * sqrt_part)
    A2 = -(sigma - sqrt_part) / (2 * sqrt_part)

    if np.isclose(sqrt_part, 0.0):
        # 避免除零错误，返回近似表达式
        print('阻尼差较小，采用近似形式')
        return sigma**2 * np.exp(-sigma * t) * (1 + sigma * t)

    # 计算加速度
    term1 = sigma * (A1 * np.exp(sqrt_part * t) + A2 * np.exp(-sqrt_part * t))
    term2 = sqrt_part * (A1 * np.exp(sqrt_part * t) - A2 * np.exp(-sqrt_part * t))
    a = -np.exp(-sigma * t) * (term1 - term2)

    return a


def fit_overdamped_second_order(t_data, v_data, ini_omega_n=1.0, ini_zeta=1.0, is_draw_image=True):
    initial_guess = [ini_omega_n, ini_zeta]  # [omega_n, zeta]

    # bounds = ([0.1, 1.01], [10.0, 10.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]
    bounds = ([1.0, 1.0], [15.0, 20.0])  # [omega_n_min, zeta_min], [omega_n_max, zeta_max]

    try:
        params, covariance = curve_fit(overdamped_second_order, t_data, v_data, p0=initial_guess, bounds=bounds)    # noqa
        omega_n_fit, zeta_fit = params
        print(f"拟合得到的自然频率 omega_n: {omega_n_fit}")
        print(f"拟合得到的阻尼比 zeta: {zeta_fit}")
    except RuntimeError as e:
        print(f"拟合失败: {e}")

    t_fit = np.linspace(min(t_data), max(t_data), len(t_data))
    y_fit = overdamped_second_order(t_fit, omega_n_fit, zeta_fit)       # noqa

    if is_draw_image:
        plt.plot(t_data, v_data, 'bo', label='原始数据')
        plt.plot(t_fit, y_fit, 'r-', label='拟合曲线')
        plt.title(f'{title}')
        plt.xlabel('时间 t')
        plt.ylabel('速度 v')
        plt.legend()
        plt.grid(True)
        plt.show()

    return t_fit, omega_n_fit, zeta_fit


def savgol_derivative(t: np.array, v: np.array, polyorder=3, window_length=51):
    """
    使用 Savitzky-Golay 滤波器计算平滑导数。

    参数:
    t : 时间向量
    v : 速度向量
    polyorder: 多项式阶数
    window_length: 滤波窗口大小 (必须为奇数)

    返回:
    np.array, np.array: 时间向量和加速度向量
    """
    # 确保时间间隔是均匀的，否则需要插值
    dt = np.mean(np.diff(t))
    a = savgol_filter(v, window_length=window_length, polyorder=polyorder, deriv=1, delta=dt)
    return t, a


def compare_a_deltav_images(delta_v_data, a_data, a_fit):
    plt.plot(delta_v_data, a_data, label='实际加速度曲线 (a-delta_v)')
    plt.plot(delta_v_data, a_fit, label='拟合加速度曲线 (a-delta_v)')
    plt.xlabel('速度差值 delta_v')
    plt.ylabel('加速度 a')
    plt.title('加速度关于速度差值的曲线')
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_a_t_images(t_data, a_data, t_fit, a_fit):
    plt.plot(t_data, a_data, label='实际加速度曲线 (a-t)')
    plt.plot(t_fit, a_fit, label='拟合加速度曲线 (a-t)')
    plt.xlabel('时间 t')
    plt.ylabel('加速度 a')
    plt.title('过阻尼二阶系统的加速度响应')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':

    acc_t_ranges = data_utils.acc_t_ranges

    for i in range(len(acc_t_ranges)):
        title = titles[acc_t_ranges[i][0]]
        group = data[title]
        ini_v = DataProcessing.get_initial_v(title)
        tar_v = DataProcessing.get_target_v(title)
        min_t = acc_t_ranges[i][1]
        max_t = acc_t_ranges[i][2]
        diff_v = round(tar_v - ini_v, 2)
        print(f'\n目标速度减去初始速度的差值为{diff_v}')

        t_values, v_values, a_values = DataProcessing.select_t_v_a_values(group, title, acc_t_ranges[i][1], acc_t_ranges[i][2])

        t_data = np.array(t_values)
        v_data = np.array(v_values)

        t_data = t_data - t_data[0]
        t_data = t_data * 1e-3
        start_v = v_data[0]
        v_data = v_data - start_v
        v_data = v_data / diff_v
        v_data_smoothed = savgol_filter(v_data, window_length=25, polyorder=3)

        # 用原始数据拟合vt图
        # t_fit, omega_n_fit, zeta_fit = fit_overdamped_second_order(t_data, v_data, is_draw_image=True)

        # 用经过平滑处理的数据拟合vt图
        t_fit, omega_n_fit, zeta_fit = fit_overdamped_second_order(t_data, v_data_smoothed, is_draw_image=True)

        # 拟合由vt图得到的加速度
        a_fit = abs(overdamped_second_order_derivative(t_fit, omega_n_fit, zeta_fit))
        t_smoothed, a_smoothed = savgol_derivative(t_data, v_data_smoothed, polyorder=3, window_length=11)

        # 绘制at曲线
        # compare_a_t_images(t_smoothed, a_smoothed, t_fit, a_fit)

        # 绘制截取的部分在所有数据中的部分的vt曲线
        # GenerateImage.draw_accelerating_part(title, min_t, max_t)

        # 绘制a-delta_v曲线
        # delta_v_data = tar_v - v_data

        # 绘制a-delta_v对比图像

        # 使用真实速度
        v_data_smoothed = v_data_smoothed * diff_v
        v_data_smoothed = v_data_smoothed + start_v
        delta_v_data = tar_v - v_data_smoothed

        # 令tar_v=1
        # delta_v_data = 1.0 - v_data_smoothed
        compare_a_deltav_images(delta_v_data, a_smoothed, a_fit)
