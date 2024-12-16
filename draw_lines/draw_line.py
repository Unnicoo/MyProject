import re
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from draw_lines.load_file import *

data_len = len(titles)
# print(titles)


def get_single_x_y_line(num=0):
    title = titles[num]
    file = data[title]
    # print(file)
    # print(len(file))

    x_coordinates, y_coordinates = get_x_y_values(file[:])

    # print(x_coordinates)
    # print(len(x_coordinates))
    # print(y_coordinates)
    # print(len(y_coordinates))

    plt.figure()

    plt.scatter(x_coordinates, y_coordinates)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.title(f'part {title}, y - x line')
    plt.show()


def get_single_a_t_line(num=0):
    title = titles[num]
    file = data[title]

    time_stamps, a_values, v_values = get_time_a_v_values(file[:])

    plt.figure()

    plt.plot(time_stamps, a_values, color = 'blue', linestyle='-', marker='o')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.title(f'part {title}, y - x line')
    plt.show()


def get_all_x_y_line():
    fig, ax = plt.subplots(figsize=(10, 10))

    for title in titles:
        file = data[title]
        print(file)

        x_coordinates, y_coordinates = get_x_y_values(file[:])
        ax.scatter(x_coordinates, y_coordinates, label=title)

        plt.xlabel('x')
        plt.ylabel('y')

        plt.title(f'all y - x line')

    plt.show()


def get_all_a_t_line():
    plt.figure(figsize=(10, 10))
    fig, ax = plt.subplots()

    for title in titles:
        file = data[title]
        print(file)

        time_stamps, a_values, v_values = get_time_a_v_values(file[:])
        ax.plot(time_stamps, a_values, label=title)

        plt.xlabel('t')
        plt.ylabel('a')

        plt.title(f'all a - t points')

    plt.show()


def get_all_v_t_line(_data):
    fig, ax = plt.subplots(figsize=(10, 10))

    for title in _data:
        file = _data[title]
        print(file)

        time_stamps, a_values, v_values = get_time_a_v_values(file[:])
        ax.scatter(time_stamps, v_values, label=title)

        plt.xlabel('t')
        plt.ylabel('v')

        plt.title(f'all v - t line')

    ax.legend()
    plt.show()


def get_all_image(_data: dict):
    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(5, 3)

    ax_list = []
    for i in range(5):
        for j in range(3):
            ax = fig.add_subplot(gs[i, j])
            ax_list.append(ax)

    ax_count = 0
    for title in _data:
        file = _data[title]

        x_coordinates, y_coordinates = get_x_y_values(file[:])
        ax_list[ax_count].scatter(x_coordinates, y_coordinates, label=title)
        ax_list[ax_count].set_xlabel('x')
        ax_list[ax_count].set_ylabel('y')
        ax_list[ax_count].set_title(f'part {title}, y - x line')
        ax_count += 1

        time_stamps, a_values, v_values = get_time_a_v_values(file[:])
        # print(time_stamps)
        print(a_values)
        ax_list[ax_count].scatter(time_stamps, a_values, label=title)
        ax_list[ax_count].set_xlabel('t')
        ax_list[ax_count].set_ylabel('a')
        ax_list[ax_count].set_title(f'part {title}, a - t line')
        ax_count += 1

        ax_list[ax_count].scatter(time_stamps, v_values, label=title)
        ax_list[ax_count].set_xlabel('t')
        ax_list[ax_count].set_ylabel('v')
        ax_list[ax_count].set_title(f'part {title}, v - t line')
        ax_count += 1

    plt.tight_layout()
    plt.show()


def get_five_images():
    gs = gridspec.GridSpec(5, 2, width_ratios=[3, 3])
    sum_count = 0
    while sum_count < len(titles):
        count = 1
        data_group = {}
        while count <= 5:
            data_group[titles[sum_count]] = data[titles[sum_count]]
            count += 1
            sum_count += 1

            if sum_count == len(titles):
                get_all_image(data_group)
                get_all_v_t_line(data_group)
                return

        get_all_image(data_group)
        get_all_v_t_line(data_group)


def get_same_start_point_images():
    gs = gridspec.GridSpec(5, 2, width_ratios=[3, 3])

    def get_ini_speed(title):
        return title.split('~')[0]
    start_speed = get_ini_speed(titles[0])
    # print(start_speed)
    data_group = {}
    for i in range(len(titles)):
        title = titles[i]
        # print(len(data_group))
        # if len(data_group) >= 5:
        #
        #     if len(data_group) == 10 or get_ini_speed(titles[i + 1]) != start_speed:
        #         get_all_image(dict(list(data_group.items())[:5]))
        #         get_all_v_t_line(dict(list(data_group.items())[:5]))
        #         if len(data_group) > 5:
        #             get_all_image(dict(list(data_group.items())[5:]))
        #             get_all_v_t_line(dict(list(data_group.items())[5:]))
        #         data_group.clear()
        #
        if get_ini_speed(title) == start_speed:
            data_group[title] = data[title]

            if i == len(titles) - 1:
                get_all_image(data_group)
                get_all_v_t_line(data_group)
                return
        else:
            get_all_image(data_group)
            get_all_v_t_line(data_group)
            start_speed = title.split('~')[0]
            data_group.clear()
            data_group[title] = data[title]
            continue


if __name__ == '__main__':
    # get_single_x_y_line(0)
    # get_single_a_t_line(0)

    # get_all_x_y_line()
    # get_all_a_t_line()
    # get_all_v_t_line()

    # get_all_image()
    # get_five_images()

    # get_same_start_point_images()

    a = calculate_a_dv_values(data[titles[0]])
    # plt.plot(a)
    # plt.show()

    pass
