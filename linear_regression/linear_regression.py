import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from sklearn.linear_model import LinearRegression

from draw_lines.data.omegan_zeta import *

mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']


def linear_regression(x, y):

    if len(x) != len(y):
        raise ValueError("自变量和因变量的长度不一致！")

    # 数据
    x = np.array(x).reshape(-1, 1)  # 自变量
    y = np.array(y)  # 因变量

    # 创建线性回归模型
    model = LinearRegression()
    model.fit(x, y)

    # 获取斜率和截距
    m = model.coef_[0]
    b = model.intercept_

    # 绘制拟合线
    plt.scatter(x, y, label='数据点', alpha=0.5)
    plt.plot(x, model.predict(x), color='red', label=f'拟合线: y = {m:.2f}x + {b:.2f}')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.show()
    print(f'斜率：{m:.2f}', f'截距：{b:.2f}')


if __name__=='__main__':
    linear_regression(all_zeta, all_omega_n)
