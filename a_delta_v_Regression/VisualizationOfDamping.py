import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['MicroSoft YaHei']

omega_n = 5.0                                  # 自然频率
t = np.linspace(0, 5, 500)      # 时间范围

# 定义不同阻尼比的系统
systems = {
    'Undamped (ζ=0)': lti([omega_n**2], [1, 0, omega_n**2]),
    'Underdamped (ζ=0.5)': lti([omega_n**2], [1, 2*0.5*omega_n, omega_n**2]),
    'Critically Damped (ζ=1)': lti([omega_n**2], [1, 2*1.0*omega_n, omega_n**2]),
    'Overdamped (ζ=2)': lti([omega_n**2], [1, 2*2.0*omega_n, omega_n**2])
}

# 绘制每个系统的阶跃响应
plt.figure(figsize=(10, 6))
for label, system in systems.items():
    t, y = step(system, T=t)
    plt.plot(t, y, label=label)


plt.title('不同阻尼条件下的系统阶跃响应')
plt.xlabel('时间 [s]')
plt.ylabel('响应')
plt.grid(True)
plt.legend()
plt.show()
