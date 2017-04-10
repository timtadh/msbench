# Author: Junqi Ma on 3/22/17

import os
import glob
import subprocess
import copy


# extract_dir_setup(): it generates profile messages using programs and .pprof file and stored in txt
# files_divider(): it can classify html into folders based on versions' name
# load_all_files(): read in all profile data
# build_matrix_setup(): using data to build matrix for cluster

def extract(program_dir, pprof_dir="", dest_dir=""):
    pieces = pprof_dir.split('/')
    # file name is in the last index and get rid of '.pprof'
    filename = pieces[len(pieces) - 1].partition(".")[0]

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    # print "go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir
    # subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir], shell=False)
    subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir + filename + ".txt", "-nodecount=1000000", "-nodefraction=0", program_dir, pprof_dir], shell=False)


def extract_dir_setup(programs_dir, pprofs_dir, dest_dir):

    programs_list = os.listdir(programs_dir)
    for program in programs_list:
        # glob means get all the file using regular expression '*'

        # -30.pprof means getting the 30th data, however we should get the average flat% from 50 repetitions
        pprof_dir_list = glob.glob(pprofs_dir + program + "*-30.pprof")
        pprof_dir_list.sort()
        for pprof_dir in pprof_dir_list:
            extract(programs_dir + program, pprof_dir, dest_dir)


def load_all_files(folders_dir, dest_dir, is_percentage):

    for folder in os.listdir(folders_dir):
        build_matrix_setup(folders_dir+folder+"/", dest_dir, is_percentage)
        # print folders_dir+folder+"/"

def build_matrix_setup(texts_dir, dest_dir, is_percentage):
    # texts_dir = "/home/majunqi/research/result/profdata_pfm/"
    # texts_dir = "/home/majunqi/research/result/testtest/"
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
                    flat = flat[0: len(flat) - 1]
                    flat_data = flat

                # method name
                name = pieces[5]

                #value_of_htmlname is a map
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
                # data.update({name: value_of_htmlname})

                # print flat_percentage + " " +name
        # if count == 5:
        #     for key in data.keys():
        #         value_of_htmlname = data.get(key)
        #         for key_html in value_of_htmlname:
        #             # index_value = find_index_htmlname(value_of_htmlname, key_html)
        #             # value = value_of_htmlname[index_value].get(html_name)
        #             value = key_html.get(key_html.keys()[0])
        #             if len(value) == 0:
        #                 value.append('0')
        #             elif len(value) != 0:
        #                 print value
                        # value_of_htmlname.updata({key_html: value})
                # data.update({key: value_of_htmlname})

    # append 0 to the method which is not used in this version
    for key in data.keys():
        value_of_htmlname = data.get(key)
        for key_html in value_of_htmlname:
            # index_value = find_index_htmlname(value_of_htmlname, key_html)
            # value = value_of_htmlname[index_value].get(html_name)
            value = key_html.get(key_html.keys()[0])
            if len(value) == 0:
                value.append('0')
        # if count == 5:
        #     for key in data.keys():
        #         if len(data.get(key)) < index:
        #             value = data.get(key)
        #             value.append('0')
        #             data.update({key: value})
        #     index += 1
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
        index +=1

    return -1


def files_divider(profdata_pfm_all, profdata_pfm_classified):

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
        if not os.path.isdir(profdata_pfm_classified+key):
            os.mkdir(profdata_pfm_classified+key)
        for file_name in names.get(key):
            os.rename(profdata_pfm_all+file_name, profdata_pfm_classified+key+"/"+file_name)