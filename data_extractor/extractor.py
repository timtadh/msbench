# Author: Junqi Ma on 3/7/17

import os
import glob
import subprocess

def extractor(program_dir, pprof_dir=""):
    pieces = pprof_dir.split('/')
    #file name is in the last index and get rid of '.pprof'
    filename = pieces[len(pieces)-1].partition(".")[0]

    dest_dir = "/home/majunqi/research/result/profdata_prm/"
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    #print "go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir
    subprocess.call(["go", "tool", "pprof", "-text", "-output", dest_dir+filename+".txt", program_dir, pprof_dir], shell=False)

def commandline():
    # program_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/html-ex-567e3e3050d01c08ea02bf4865faaa6fb42bf64f"
    # pprof_dir = "/home/majunqi/research/result/result_pfm/html-ex-567e3e3050d01c08ea02bf4865faaa6fb42bf64f-61-100.pprof"
    programs_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/"
    pprofs_dir = "/home/majunqi/research/result/result_pfm/"

    programs_dir_list = os.listdir(programs_dir)
    for program_dir in programs_dir_list:
    #glob means get all the file using regular expression '*'
        pprof_dir_list = glob.glob(pprofs_dir+program_dir+"*.pprof")
        pprof_dir_list.sort()
        for pprof_dir in pprof_dir_list:
            extractor(programs_dir+program_dir, pprof_dir)

if __name__ == '__main__':
    commandline()