# Author: Junqi Ma on 7/18/16

import calcu_util
import plot_figure
import anova_oneway
import command_line_util


def get_allresults():
    check, para = command_line_util.command_line_args()
    if len(para) == 1:
        dir = para[0]
    elif len(para) == 2:
        dir = para[0]
        number = para[1]
    # dir1 = "/home/majunqi/PycharmProjects/version_cmp/test"
    # check = "plotone"
    # number = "200"
    # dir = "/home/majunqi/research/test/"
    name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic = calcu_util.calculate_allfiles_mean_std(dir)
    if check == "calculate":
        i, dir = calcu_util.write_allfiles(name_list, result_mean_list, result_std_list)
        return "write " + str(i) + " files to the directory: " + dir
    if check == "plotall":
        plot(name_list, result_mean_list, get_f_oneway(result_mean_list))
    if check == "plotone":
        name_list, result_list = calcu_util.get_onesample_allversions(dir, number)
        plot_one(name_list, result_list, number)


def plot(name_list, result_list, f_oneway):
    plot_figure.plot_box(name_list, result_list, f_oneway)


def plot_one(name_list, result_list, number):
    plot_figure.plot_one(name_list, result_list, number)


def get_f_oneway(result_list):
    return anova_oneway.anova_f_oneway(result_list)


if __name__ == '__main__':
    if get_allresults() != None:
        print get_allresults()
