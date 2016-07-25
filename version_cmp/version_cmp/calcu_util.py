# Author: Junqi Ma on 7/18/16

import os
import shutil
import numpy

skipfile = "skipfile"


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

#get the mean of running time for each versions testing for each samples
def calculate_allfiles_mean(dir):
    times_list = pre_process(dir)
    result_list = []
    name_list = []
    times_list.sort()
    for time in times_list:
        a = read_file(dir + "/" + time)
        if a != skipfile:
            b = convert_string_number(a)
            result = calculate_mean(b)
            if result != None:
                version = time.split("-")
                version = version[2]
                # check if name_list had the name already
                if name_list.__contains__(version):
                    result_list[name_list.index(version)].append(format_number(result * 1))
                else:
                    name_list.append(version)
                    result_list.append([])
                    result_list[name_list.index(version)].append(format_number(result * 1))
    return name_list, result_list


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


def write_file(dir="", content=""):
    if content != "":
        f = open(dir, "a+")
        f.write(content)
        f.close()


def read_file(dir=""):
    if dir.__contains__(".time"):
        f = open(dir, "r+")
        content = str(f.read())
        if content.count("-") > 1:
            times = content.split("-")
            return times
        else:
            content_list = []
            content_list.append(content)
            return content_list
    else:
        return skipfile
