# Author: Junqi Ma on 3/22/17

import os
import glob
import subprocess
import copy
import re
from sets import Set
import shutil


# extract_dir_setup(): it generates profile messages using programs and .pprof file and stored in txt
# files_divider(): it can classify htmls into folders based on versions' name
# load_all_files(): read in all profiling data
# build_matrix_setup(): using data to build matrix for cluster

def profile(program_dir, pprof_dir="", dest_dir=""):
    pieces = pprof_dir.split('/')
    # file name is in the last index and get rid of '.pprof'
    filename = pieces[len(pieces) - 1].partition(".")[0]

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    # print "go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir
    # subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir], shell=False)
    subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir + filename + ".txt", "-nodecount=1000000",
                     "-nodefraction=0", program_dir, pprof_dir], shell=False)


def profile_dir_setup(programs_dir, pprofs_dir, dest_dir):
    programs_list = os.listdir(programs_dir)

    num_of_html = -1
    num_of_repetition = -1

    for program in programs_list:
        # glob means get all the file using regular expression '*'
        # -30.pprof means getting the 30th data, however we should get the average flat% from 50 repetitions
        pprof_dir_list = glob.glob(pprofs_dir + program + "*.pprof")
        # pprof_dir_list.sort()
        pprof_dir_list = natural_sort(pprof_dir_list)

        if len(pprof_dir_list) is 0:
            continue

        if num_of_html == -1:
            pieces = pprof_dir_list[len(pprof_dir_list) - 1].split('/')
            html_num = pieces[len(pieces) - 1].split('-')
            num_of_html = html_num[len(html_num) - 3]
            num_of_repetition = html_num[len(html_num) - 2]

        for pprof_dir in pprof_dir_list:
            profile(programs_dir + program, pprof_dir, dest_dir)
    return num_of_html, num_of_repetition

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def load_all_files(folders_dir, dest_dir, is_percentage, num_of_repetition):
    ll = os.listdir(folders_dir)
    for folder in ll:
        # build_matrix_setup(folders_dir + folder + "/", dest_dir, is_percentage)

        # the line below is used for test
        build_matrix_setup_modified(folders_dir + folder + "/", dest_dir, is_percentage, num_of_repetition)
        # print folders_dir+folder+"/"


def align_methodsname(html_folder, text_list):
    method_name_list = Set()
    for text in text_list:
        text = html_folder + "/" + text
        f = open(text, "r")
        count = 0
        for line in f:
            if count < 2:
                count += 1
                continue
            piece = line.split()
            method_name = piece[len(piece) - 1]
            method_name_list.add(method_name)

    method_name_list = list(method_name_list)
    method_name_list.sort()
    return method_name_list


def merge_pprof_txt(htmls_dir, html_folder_list, num_of_repetitions):
    html_folder_list.sort()

    for html_folder in html_folder_list:

        html_idx = html_folder
        html_folder = htmls_dir + html_folder

        txt_list = os.listdir(html_folder)

        method_name_list = align_methodsname(html_folder, txt_list)
        data_flat = dict()
        for method_name in method_name_list:
            data_flat.update({method_name: float()})

        data_flat_percentage = copy.deepcopy(data_flat)

        my_total_time = 0

        for text in txt_list:
            f = open(html_folder + "/" + text, "r")
            count = 0

            for line in f:
                if len(line) == 0:
                    continue
                # line 1: total time
                if count == 0:
                    line_one = line.split()
                    total_time = line_one[0]
                    #   unit is ms
                    if total_time.__contains__('ms'):
                        total_time = total_time[: len(total_time) - 2]
                        total_time = long(total_time) / 1000
                        my_total_time += total_time
                    # unit is s
                    else:
                        total_time = total_time[: len(total_time) - 1]
                        # print html_folder + "/" + text + ' ' + total_time
                        total_time = float(total_time)
                        my_total_time += total_time
                # line 2: labels
                if count == 1:
                    count += 1
                    continue

                # line 3: real data
                if count >= 2:
                    pieces = line.split()

                    method_name = pieces[len(pieces) - 1]

                    flat_percentage = pieces[1]
                    flat_percentage = flat_percentage[0: len(flat_percentage) - 1]
                    flat_percentage = float(flat_percentage)
                    old = data_flat_percentage.get(method_name)
                    new = old + flat_percentage
                    data_flat_percentage.update({method_name: new})

                    # flat
                    flat = pieces[0]
                    if flat.__contains__('ms'):
                        flat = flat[0: len(flat) - 2]
                        flat = long(flat)
                        flat /= 1000
                    elif flat.__contains__('s'):
                        flat = flat[0: len(flat) - 1]
                        flat = float(flat)
                    # if the data is 0, it has no unit
                    else:
                        flat = float(flat)
                    old = data_flat.get(method_name)
                    new = old + flat
                    data_flat.update({method_name: new})

                count += 1
            f.close()

        # because there are 50 files, so the dividend is 50
        repetition = num_of_repetitions

        total_time = my_total_time / repetition

        txt_name = txt_list[0].split('-')
        txt_name = txt_name[0] + '-' + txt_name[1] + '-' + txt_name[2] + '-' + html_idx + '-' + str(repetition) + '.txt';

        if not os.path.exists(htmls_dir + 'data/'):
            os.mkdir(htmls_dir + 'data/')

        filepath = htmls_dir + 'data/' + txt_name

        # in order to avoid repeated calculation, if same file is found, skip it.
        if os.path.exists(filepath):
            # os.remove(filepath)
            continue

        f = open(filepath, 'w')
        f.write(str(total_time) + '\n')

        count = 1
        for method_name in method_name_list:
            flat = data_flat.get(method_name) / repetition
            f.write(str(flat) + '\t')
            # data_flat.update({method_name: flat})
            flat_percentage = data_flat_percentage.get(method_name) / repetition
            f.write(str(flat_percentage) + '\t')
            # data_flat_percentage.update({method_name: flat_percentage})
            f.write(method_name + '\n')
            count += 1
        f.close()
    return method_name_list


def build_matrix_setup_modified(htmls_dir, dest_dir, is_percentage, num_of_repetitions):
    if os.path.exists(htmls_dir + 'data/'):
        shutil.rmtree(htmls_dir + 'data/')

    html_folder_list = os.listdir(htmls_dir)

    method_name_list = merge_pprof_txt(htmls_dir, html_folder_list, num_of_repetitions)

    texts_dir = htmls_dir + 'data/'
    text_list = os.listdir(texts_dir)
    # key of data is method name, value of each key is html_name_list
    data = dict()
    html_name_list = list()
    version_name = text_list[0].split('-')[2]

    # generate a list of map, the key of map is html name, value is a list of execution time
    # [{'68': []}, {'67': []}, {'62': []}, {'64': []}]
    for text in text_list:
        html_name = text.split('-')[3]
        if find_index_htmlname(html_name_list, html_name) == -1:
            html_name_map = dict()
            html_name_map.update({html_name: list()})
            html_name_list.append(html_name_map)
    # html_name_map.append(html_name_map)
    # this for loop is used to add all method into dict data

    for text in text_list:

        f = open(texts_dir + text, "r")
        count = 1

        for line in f:
            if count < 2:
                count += 1
                continue
            else:
                pieces = line.split()
                name = pieces[2]
                if not data.has_key(name):
                    # because every data must have a new html_name_list, so it must be a new object
                    # deepcopy is the method to create a new object with same value
                    new_html_name_list = copy.deepcopy(html_name_list)
                    data.update({name: new_html_name_list})
                    # print flat_percentage + " " +name
        f.close()

    # this for loop is used to add data into the dict
    # index is used to indicate the file number
    index = 0
    for text in text_list:
        f = open(texts_dir + text, "r")
        count = 1

        html_name = text.split('-')[3]

        for line in f:
            if count < 2:
                count += 1
                continue
            else:
                if count == 2:
                    if index == 0:
                        index = 1
                    count += 1
                pieces = line.split()
                if is_percentage:
                    # flat%
                    flat_percentage = pieces[1]
                    flat_data = flat_percentage
                elif not is_percentage:
                    # flat
                    flat = pieces[0]
                    flat_data = flat

                # method name
                name = pieces[2]

                # value_of_htmlname is a map
                value_of_htmlname = data.get(name)

                index_value = find_index_htmlname(value_of_htmlname, html_name)

                # print html_name
                # print value_of_htmlname[0]
                # print index_value

                # value is a map
                value = value_of_htmlname[index_value].get(html_name)
                value.append(flat_data)
                # value_of_htmlname.updata({html_name: value})
        f.close()

    # append 0 to the method which is not used in this version
    for key in data.keys():
        value_of_htmlname = data.get(key)
        for key_html in value_of_htmlname:
            # index_value = find_index_htmlname(value_of_htmlname, key_html)
            # value = value_of_htmlname[index_value].get(html_name)
            value = key_html.get(key_html.keys()[0])
            if len(value) == 0:
                value.append('0')
    # print data

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    f = open(dest_dir + version_name + ".txt", "w")
    f.write("  ")
    html_maps = data.get(data.keys()[0])
    for html_map in html_maps:
        f.write(html_map.keys()[0] + " ")

    f.write('\n')
    for key in data.keys():
        f.write(key + " ")
        html_maps = data.get(key)
        for html_map in html_maps:
            f.write(html_map.values()[0][0] + " ")
        f.write('\n')

    f.close()


# old one. It can be used if there is only one pprof file and it can build matrix directly
def build_matrix_setup(texts_dir, dest_dir, is_percentage):
    text_list = os.listdir(texts_dir)

    data = dict()
    html_name_list = list()
    version_name = text_list[0].split('-')[2]

    # generate a list of map, the key of map is html name, value is a list of execution time
    # [{'68': []}, {'67': []}, {'62': []}, {'64': []}]
    for text in text_list:
        html_name = text.split('-')[3]
        if find_index_htmlname(html_name_list, html_name) == -1:
            html_name_map = dict()
            html_name_map.update({html_name: list()})
            html_name_list.append(html_name_map)
    # html_name_map.append(html_name_map)
    # this for loop is used to add all method into dict data

    for text in text_list:

        f = open(texts_dir + text, "r")
        count = 1

        for line in f:
            if count < 4:
                count += 1
                continue
            else:
                pieces = line.split()
                name = pieces[5]
                if not data.has_key(name):
                    # because every data must have a new html_name_list, so it must be a new object
                    # deepcopy is the method to create a new object with same value
                    new_html_name_list = copy.deepcopy(html_name_list)
                    data.update({name: new_html_name_list})
                    # print flat_percentage + " " +name
        f.close()

    # this for loop is used to add data into the dict
    # index is used to indicate the file number
    index = 0
    for text in text_list:
        f = open(texts_dir + text, "r")
        count = 1

        html_name = text.split('-')[3]

        for line in f:
            if count < 4:
                count += 1
                continue
            else:
                if count == 4:
                    if index == 0:
                        index = 1
                    count += 1
                pieces = line.split()
                if is_percentage:
                    # flat%
                    flat_percentage = pieces[1]
                    flat_percentage = flat_percentage[0: len(flat_percentage) - 1]
                    flat_data = flat_percentage
                elif not is_percentage:
                    # flat
                    flat = pieces[1]
                    if flat.__contains__('ms'):
                        flat = flat[0: len(flat) - 2]
                        flat = long(flat)
                        flat /= 1000
                        flat = str(flat)
                    else:
                        flat = flat[0: len(flat) - 1]
                    flat_data = flat

                # method name
                name = pieces[5]

                # value_of_htmlname is a map
                value_of_htmlname = data.get(name)

                index_value = find_index_htmlname(value_of_htmlname, html_name)

                # print html_name
                # print value_of_htmlname[0]
                # print index_value

                # value is a map
                value = value_of_htmlname[index_value].get(html_name)
                value.append(flat_data)
                # value_of_htmlname.updata({html_name: value})
        f.close()

    # append 0 to the method which is not used in this version
    for key in data.keys():
        value_of_htmlname = data.get(key)
        for key_html in value_of_htmlname:
            # index_value = find_index_htmlname(value_of_htmlname, key_html)
            # value = value_of_htmlname[index_value].get(html_name)
            value = key_html.get(key_html.keys()[0])
            if len(value) == 0:
                value.append('0')
    # print data

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    f = open(dest_dir + version_name + ".txt", "w")
    f.write("  ")
    html_maps = data.get(data.keys()[0])
    for html_map in html_maps:
        f.write(html_map.keys()[0] + " ")

    f.write('\n')
    for key in data.keys():
        f.write(key + " ")
        html_maps = data.get(key)
        for html_map in html_maps:
            f.write(html_map.values()[0][0] + " ")
        f.write('\n')

    f.close()


def find_index_htmlname(value_of_htmlname, html_name):
    index = 0
    for item in value_of_htmlname:
        if html_name == item.keys()[0]:
            return index
        index += 1

    return -1


# it's used to classify files based on htmls
def classify_files_byhtmls(profdata_pfm_classified):
    version_folders = os.listdir(profdata_pfm_classified)


    for version_folder in version_folders:
        names = dict()
        if not os.path.isdir(profdata_pfm_classified + version_folder + "/"):
            continue
        files = os.listdir(profdata_pfm_classified + version_folder + "/")
        for file in files:
            if os.path.isdir(profdata_pfm_classified + version_folder + "/" + file + "/"):
                continue
            html = file.split('-')[3]
            if not html in names.keys():
                names.update({html: []})
            names.get(html).append(file)

        for key in names.keys():
            if not os.path.isdir(profdata_pfm_classified + version_folder + "/" + key):
                os.mkdir(profdata_pfm_classified + version_folder + "/" + key)
            for file_name in names.get(key):
                os.rename(profdata_pfm_classified + version_folder + "/" + file_name, profdata_pfm_classified + version_folder + "/" + key + "/" + file_name)

    # files = os.listdir(profdata_pfm_all)
    # if len(files) == 0:
    #     os.rmdir(profdata_pfm_all)


# it's used to classify files based on versions
def classify_files_byversions(profdata_pfm_all, profdata_pfm_classified):
    if not os.path.isdir(profdata_pfm_classified):
        os.mkdir(profdata_pfm_classified)

    files = os.listdir(profdata_pfm_all)
    names = dict()
    for file in files:
        version = file.split('-')[2]
        if not version in names.keys():
            names.update({version: []})
        names.get(version).append(file)

    for key in names.keys():
        if not os.path.isdir(profdata_pfm_classified + key):
            os.mkdir(profdata_pfm_classified + key)
        for file_name in names.get(key):
            os.rename(profdata_pfm_all + file_name, profdata_pfm_classified + key + "/" + file_name)

            # files = os.listdir(profdata_pfm_all)
            # if len(files) == 0:
            #     os.rmdir(profdata_pfm_all)
