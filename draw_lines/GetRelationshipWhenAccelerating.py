from draw_lines.Utils.deal_with_data import DataProcessing
from draw_lines.load_file import *
from draw_lines.draw_line import *


if __name__ == '__main__':
    data = data_utils.data
    titles = data_utils.titles
    acc_t_ranges = data_utils.acc_t_ranges

    # 这部分会自动处理数据，不用管，只需要更改下面执行哪些函数
    for i in range(len(acc_t_ranges)):
        title = titles[acc_t_ranges[i][0]]
        group = data[title]
        min_t = acc_t_ranges[i][1]
        max_t = acc_t_ranges[i][2]
        _data = DataProcessing.get_same_delta_v_data(0.1)

        # 画出全部过程中的vt图
        # GenerateImage.draw_v_t_image(title)

        # 画出经过时间限制的vt图，也就是说你只能看到加速部分的vt图像
        # GenerateImage.draw_random_v_t_images(selected_t_values, selected_v_values, title)

        # 画出加速部分在全部过程中的部分的vt图
        # GenerateImage.draw_accelerating_part(title, min_t, max_t)

        # 画出全部过程中的at图
        # GenerateImage.draw_a_t_image(title)

        # 画出全部过程中的av图
        # GenerateImage.draw_a_v_image(title)

        # 画出a-delta_v图像
        # GenerateImage.draw_a_delta_v_image(group, title, min_t, max_t)

    # 六个一组画出a-delta_v图像
    # GenerateImage.draw_a_delta_v_images()

    # 把速度差相等的a-delta_v图画在一起，可以调整delta来更改速度差
    diff_v = 0.1
    # GenerateImage.draw_a_delta_v_images_with_same_diff_v(diff_v)

    # 把初速度相等的a-delta_v图画在一起，可以调整delta来更改初速度值
    ini_v = 0.1
    # GenerateImage.draw_a_delta_v_images_with_same_ini_v(ini_v)
