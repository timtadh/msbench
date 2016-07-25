"""
Demo of the histogram (hist) function with multiple data sets.

Plot histogram with multiple sample sets and demonstrate:

    * Use of legend with multiple sample sets
    * Stacked bars
    * Step curve with a color fill
    * Data sets of different sample sizes
"""
import matplotlib.pyplot as plt
import calcu_util


def plot_box(name_list, result_list, f_oneway):
    name_list = [name[:10] for name in name_list]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dic_return = ax.boxplot(x=result_list)

    ax.set_title("f_oneway: " + str(f_oneway))

    ax.set_xlabel("versions")
    ax.set_ylabel("time: ms")

    # ax.set_xlabel(name)
    xtickname = plt.setp(ax, xticklabels=name_list)
    plt.setp(xtickname, rotation=45)
    print "standard deviation of medians:", std_medians(dic_return, name_list)
    print "standard deviation of numbers of points beyond whiskers (lower, upper):", std_points_in_outliers(dic_return, name_list)
    print "standard deviation of quartiles (lower, upper):", std_quartiles(dic_return, name_list)
    print "standard deviation of whiskers (lower, upper):", std_whiskers(dic_return, name_list)
    plt.show()


def plot(x_multi=[[1, 11, 21], [2, 12, 22], [3, 13, 23], [4, 14, 24], [5, 15, 25], [6, 16, 26]], label=['a', 'b', 'c', 'd', 'e']):
    plt.hist(x_multi, histtype='bar', label=label)
    plt.legend(prop={'size': 10})
    plt.show()


def std_points_in_outliers(dic_return, name_list):
    i = 0
    numbers_lower_outliers_list = []
    numbers_upper_outliers_list = []
    for name in name_list:
        numbers_upper_outliers_list.append(len(dic_return['fliers'][i].get_data()[1]))
        numbers_lower_outliers_list.append(len(dic_return['fliers'][i + 1].get_data()[1]))
        i += 2;
    return calcu_util.calculate_standarddeviation(numbers_lower_outliers_list), calcu_util.calculate_standarddeviation(numbers_upper_outliers_list)


def std_medians(dic_return, name_list):
    i = 0
    std_medians_list = []
    for name in name_list:
        std_medians_list.append(dic_return['medians'][i].get_data()[1][1])
        i += 1
    return calcu_util.format_number(calcu_util.calculate_standarddeviation(std_medians_list))


def std_quartiles(dic_return, name_list):
    i = 0
    std_upper_quartiles_list = []
    std_lower_quartiles_list = []
    for name in name_list:
        std_upper_quartiles_list.append(dic_return['boxes'][i].get_data()[1][3])
        std_lower_quartiles_list.append(dic_return['boxes'][i].get_data()[1][4])
        i += 1
    return calcu_util.format_number(calcu_util.calculate_standarddeviation(std_upper_quartiles_list)), calcu_util.format_number(calcu_util.calculate_standarddeviation(std_lower_quartiles_list))


def std_whiskers(dic_return, name_list):
    i = 0
    std_smallest_list = []
    std_largest_list = []
    for name in name_list:
        std_smallest_list.append(dic_return['whiskers'][i].get_data()[1][1])
        std_largest_list.append(dic_return['whiskers'][i + 1].get_data()[1][1])
        i += 2
    return calcu_util.format_number(calcu_util.calculate_standarddeviation(std_smallest_list)), calcu_util.format_number(calcu_util.calculate_standarddeviation(std_largest_list))
