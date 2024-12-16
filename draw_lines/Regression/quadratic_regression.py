import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from draw_lines.load_file import *

for i in range(len(titles)):
    title = titles[i]
    file = data[title]
    _, a_values, v_values = get_time_a_v_values(file)
    target_v = get_target_v(title)
    delta_v_values = get_delta_v(target_v, v_values)
    delta_v = np.array(delta_v_values)  # 你的delta_v数据点
    a = np.array(a_values)        # 你的a数据点

    # 定义拟合函数
    def cubic_fit(x, a0, a1, a2, a3):
        return a0 + a1*x + a2*x**2 + a3*x**3

    # 拟合数据
    params, _ = curve_fit(cubic_fit, delta_v, a)    # noqa

    # 使用拟合参数生成拟合曲线
    delta_v_fit = np.linspace(min(delta_v), max(delta_v), 100)
    a_fit = cubic_fit(delta_v_fit, *params)

    # 绘制原始数据和拟合曲线
    plt.scatter(delta_v, a, label='Data')
    plt.plot(delta_v_fit, a_fit, 'r-', label='Cubic Fit')
    plt.xlabel('delta_v')
    plt.ylabel('a')
    plt.title('Cubic Polynomial Fit')
    plt.legend()
    plt.show()
    print(f"Fitted parameters: {params}")
