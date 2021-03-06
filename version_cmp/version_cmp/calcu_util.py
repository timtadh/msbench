# Author: Junqi Ma on 7/18/16

import os
import shutil
import numpy

skipfile = "skipfile"


# calculate the standard deviation for one version testing all samples
def calculate_allfiles_standarddeviation(result_list):
    first = len(result_list)
    second = len(result_list[0])
    input_list = []
    std_list = []
    # calculate the std of the same sample from different versions
    for i in range(first):
        for j in range(second):
            input_list.append(result_list[i][j])
        std_list.append(calculate_standarddeviation(input_list))
    return std_list


# get the mean of running time for each versions testing for each samples
def calculate_allfiles_mean_std(dir):
    times_list = pre_process(dir)

    result_mean_list = []
    result_std_list = []
    result_mean_dic = {}
    result_std_dic = {}

    name_list = []
    times_list.sort()
    for time in times_list:
        a = read_file(dir + "/" + time)
        if a != skipfile:
            b = convert_string_number(a)
            result_mean = calculate_mean(b)
            result_std = calculate_standarddeviation(b)
            if result_mean != None:
                versions = time.split("-")
                version = versions[2]
                name = versions[2] + "-" + versions[3]
                # check if name_list had the name already
                if name_list.__contains__(version):
                    result_mean_list[name_list.index(version)].append(format_number(result_mean * 1))
                    result_std_list[name_list.index(version)].append(format_number(result_std * 1))
                    result_mean_dic[name] = format_number(result_mean * 1)
                    result_std_dic[name] = format_number(result_std * 1)
                else:
                    name_list.append(version)
                    result_mean_list.append([])
                    result_std_list.append([])
                    result_mean_list[name_list.index(version)].append(format_number(result_mean * 1))
                    result_std_list[name_list.index(version)].append(format_number(result_std * 1))
                    result_mean_dic[name] = format_number(result_mean * 1)
                    result_std_dic[name] = format_number(result_std * 1)
    return name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic


def get_onesample_allversions(dir, dataset_id):
    allfiles_name_list = pre_process(dir)
    name_list = []
    result_list = []
    times_list = []
    for name in allfiles_name_list:
        if name.__contains__('-' + dataset_id + '-'):
            times_list.append(name)
    times_list.sort()
    for time in times_list:
        a = read_file(dir + "/" + time)
        if a != skipfile:
            versions = time.split("-")
            version = versions[2]
            name = versions[2][:10] + "-" + versions[3]
            name_list.append(name)
            result_list.append(format_number_list(convert_string_number(a)))
    return name_list, result_list


def sort_by_orderfile(name_list, result_list, order_path):
    help_list_sorted = []
    new_name_list = []
    new_result_list = []
    with open(order_path) as f:
        name_list_ordered = [x.strip('\n') for x in f.readlines()]

    for i in range(len(name_list)):
        for j in range(len(name_list_ordered)):
            if name_list_ordered[j].__contains__(name_list[i].split("-")[0]):
                help_list_sorted.append(j)
    help_list_unsorted = list(help_list_sorted)
    help_list_sorted.sort()
    for i in help_list_sorted:
        for j in range(len(help_list_unsorted)):
            if help_list_unsorted[j] == i:
                new_name_list.append(name_list[j])
                new_result_list.append(result_list[j])
                break
    return new_name_list, new_result_list


def calculate_mean(a):
    if len(a) > 0:
        return numpy.mean(a)


def calculate_standarddeviation(a):
    if len(a) > 0:
        return numpy.std(a)


def get_allfiles(dir=""):
    return os.listdir(dir)


def generate_dir(dir=""):
    try:
        os.mkdir(dir)
    except:
        shutil.rmtree(dir)
        os.mkdir(dir)


def format_number_list(result_list):
    result_list = [format(i, '.5f') for i in result_list]
    result_list = [float(i) for i in result_list]
    return result_list


def format_number(result):
    result = format(result, '.5f')
    result = float(result)
    return result


def convert_string_number(a):
    a = [format(float(i), '.5f') for i in a]
    a = [float(i) for i in a]
    return a


def pre_process(times_dir):
    times_list = get_allfiles(times_dir)

    return times_list


def generate_dir(dir):
    try:
        os.mkdir(dir)
    except:
        shutil.rmtree(dir)
        os.mkdir(dir)


def write_allfiles(name_list, result_mean_list, result_std_list, output_dir):
    dir = output_dir + "/mean_std.txt"
    f = open(dir, "w+")
    i = 1
    for i in range(len(name_list)):
        f.write(name_list[i] + "\t" + str(result_mean_list[i]) + "\t" + str(result_std_list[i]) + "\r")
        i += 1
    f.close()
    return i, dir


def write_file(dir="", content=""):
    if content != "":
        f = open(dir, "w+")
        f.write(content)
        f.close()


def read_file(dir=""):
    if dir.__contains__(".time"):
        f = open(dir, "r+")
        content = str(f.read())
        if content.count("-") > 1:
            times = content.split("-")
            new_times = []
            for time in times:
                if len(time) > 1:
                    new_times.append(time)
            return new_times
        else:
            content_list = []
            content_list.append(content)
            return content_list
    else:
        return skipfile
