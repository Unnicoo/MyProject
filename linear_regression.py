import numpy as np
import matplotlib.pyplot as plt

data = np.array([[32, 31], [53, 68], [61, 62], [47, 71], [59, 87], [55, 78], [52, 79], [39, 59], [48, 75], [52, 71],
                 [45, 55], [54, 82], [44, 62], [58, 75], [56, 81], [48, 60], [44, 82], [60, 97], [45, 48], [38, 56],
                 [66, 83], [65, 118], [47, 57], [41, 51], [51, 75], [59, 74], [57, 95], [63, 95], [46, 79],
                 [50, 83]])

x = data[:, 0]
y = data[:, 1]


# 定义损失函数J(θ)
def cost(theta0, theta1, data):
    total_cost = 0
    M = len(data)
    for i in range(M):
        x = data[i, 0]
        y = data[i, 1]
        total_cost += (y - theta0 * x - theta1) ** 2
    return total_cost / (2 * M)


# 定义模型的超参数
alpha = 0.00001
ini_theta0 = 0
ini_theta1 = 0
num_iter = 1000   # 迭代次数


# 定义梯度下降算法
def grad_desc(data, ini_theta0, ini_theta1, alpha, num_iter):
    theta0 = ini_theta0
    theta1 = ini_theta1
    # 定义一个list保存所有的损失函数值，用来显示下降的过程
    cost_list = []
    for i in range(num_iter):
        cost_list.append(cost(theta0, theta1, data))
        theta0, theta1 = step_grad_desc(theta0, theta1, alpha, data)
    return [theta0, theta1, cost_list]


def step_grad_desc(cur_theta0, cur_theta1, alpha, data):
    sum_grad_theta0 = 0
    sum_grad_theta1 = 0
    M = len(data)

    # 对每个点都代入公式求和
    for i in range(M):
        x = data[i, 0]
        y = data[i, 1]
        sum_grad_theta0 += (cur_theta0 * x + cur_theta1 - y) * x
        sum_grad_theta1 += cur_theta0 * x + cur_theta1 - y

    # 求当前梯度
    grad_theta0 = sum_grad_theta0 / M
    grad_theta1 = sum_grad_theta1 / M

    # 梯度下降，更新参数
    updated_theta0 = cur_theta0 - alpha * grad_theta0
    updated_theta1 = cur_theta0 - alpha * grad_theta1

    return updated_theta0, updated_theta1


# 测试，运行梯度下降算法计算最优的theta0, theta1
theta0, theta1, cost_list = grad_desc(data, ini_theta0, ini_theta1, alpha, num_iter)
print('theta0 is:', theta0)
print('theta1 is:', theta1)
cost = cost(theta0, theta1, data)
print('cost is:', cost)

# 画出拟合曲线
plt.scatter(x, y)
predict_y = theta0 * x + theta1
plt.plot(x, predict_y)
plt.show()
