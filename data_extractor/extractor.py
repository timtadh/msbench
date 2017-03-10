# Author: Junqi Ma on 3/7/17

import os
import glob
import subprocess


def extract(program_dir, pprof_dir=""):
    pieces = pprof_dir.split('/')
    # file name is in the last index and get rid of '.pprof'
    filename = pieces[len(pieces) - 1].partition(".")[0]

    dest_dir = "/home/majunqi/research/result/profdata_pfm/"
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    # print "go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir
    # subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir], shell=False)
    subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir + filename + ".txt", "-nodecount=1000000", "-nodefraction=0", program_dir, pprof_dir], shell=False)


def build_matrix(dir):
    print "TODO"


def normalize():
    print "TODO"


def build_matrix_setup():
    texts_dir = "/home/majunqi/research/result/profdata_pfm/"
    text_list = os.listdir(texts_dir)

    data = dict()
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
                    data.update({name: list()})
                    # print flat_percentage + " " +name
    f.close()

    # this for loop is used to add data into the dict
    # index is used to indicate the file number
    index = 0
    for text in text_list:
        f = open(texts_dir + text, "r")
        count = 1

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
                flat_percentage = pieces[1]
                flat_percentage = flat_percentage[0: len(flat_percentage) - 1]
                name = pieces[5]

                value = data.get(name)
                value.append(flat_percentage)
                data.update({name: value})

                # print flat_percentage + " " +name
        if count == 5:
            for key in data.keys():
                if len(data.get(key)) < index:
                    value = data.get(key)
                    value.append('0')
                    data.update({key: value})
            index += 1

    f.close()
    # print data

    f = open("/home/majunqi/research/result/data.txt", "w")
    for key in data.keys():
        f.write(key + " ")
        f.write(' '.join(data.get(key)))
        f.write('\n')

    f.close()

def extract_dir_setup():
    # program_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/html-ex-567e3e3050d01c08ea02bf4865faaa6fb42bf64f"
    # pprof_dir = "/home/majunqi/research/result/result_pfm/html-ex-567e3e3050d01c08ea02bf4865faaa6fb42bf64f-61-100.pprof"
    programs_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/"
    pprofs_dir = "/home/majunqi/research/result/result_pfm/"

    programs_list = os.listdir(programs_dir)
    for program in programs_list:
        # glob means get all the file using regular expression '*'
        pprof_dir_list = glob.glob(pprofs_dir + program + "*.pprof")
        pprof_dir_list.sort()
        for pprof_dir in pprof_dir_list:
            extract(programs_dir + program, pprof_dir)


def commandline():
    # extract_dir_setup()
    build_matrix_setup()


if __name__ == '__main__':
    commandline()
