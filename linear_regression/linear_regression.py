from sklearn import linear_model
from pylab import *

from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.load_file import data_utils

data = data_utils.data
titles = data_utils.titles
title = titles[0]

# 设置Matplotlib库的字体
mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']

# X = np.array([[150, 200, 250, 300, 350, 400, 600]]).reshape(7, 1)
# Y = np.array([[6450, 7450, 8450, 9450, 11450, 15450, 18450]]).reshape(7, 1)

time_stamp, a_values, t_values = DataProcessing.get_t_v_a_values(data[title])
X, Y = DataProcessing.calculate_a_dv_values(data[title], delta_num=5)
X = np.array(X).reshape(314, 1)
Y = np.array(Y).reshape(314, 1)

# print(X)
# print(Y)
# print(len(X))
# print(len(Y))

plt.scatter(X, Y, color='blue', label='原始数据点')
plt.show()

# 建立线性回归模型
regr = linear_model.LinearRegression()  # noqa

# 拟合
regr.fit(X, Y)

# 得到直线的斜率，截距
a, b = regr.coef_, regr.intercept_

# 给出预测x，预测y
# area = np.array(X).reshape(-1, 1)

# 作图
# 1.真实数据的点
plt.scatter(X, Y, color='blue', label='原始数据点')

# 拟合的直线
plt.plot(X, regr.predict(X), color='r', linewidth=4, label='拟合线')
plt.xlabel('square_feet')
plt.ylabel('price')
plt.grid()
plt.legend()
plt.show()
