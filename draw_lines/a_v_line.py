import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from draw_lines.load_file import *

# -0.05 ~ -0.15的加速部分
file = data[titles[0]]
selected_v_values, time_values = select_v_t_values(file, 1000, 1500)

plt.scatter(time_values, selected_v_values)
plt.show()

