# Author: Junqi Ma on 7/18/16

import calcu_util
import plot_figure
import anova_oneway
import command_line_util


def get_allresults():
    check, dir = command_line_util.command_line_args()
    # dir1 = "/home/majunqi/PycharmProjects/version_cmp/test"
    # check = "plot"
    # dir = "/home/majunqi/research/test/"
    if check == "mean":
        name_list, mean_list = calcu_util.calculate_allfiles_mean(dir)
        return name_list, mean_list
    if check == "std":
        name_list, result_list = calcu_util.calculate_allfiles_mean(dir)
        std_list = calcu_util.calculate_allfiles_standarddeviation(result_list)
        return name_list, std_list
    if check == "plot":
        name_list, result_list = calcu_util.calculate_allfiles_mean(dir)
        plot(name_list, result_list, get_f_oneway(result_list))


def plot(name_list, result_list, f_oneway):
    plot_figure.plot_box(name_list, result_list, f_oneway)


def get_f_oneway(result_list):
    return anova_oneway.anova_f_oneway(result_list)


if __name__ == '__main__':
    if get_allresults() != None:
        print get_allresults()
