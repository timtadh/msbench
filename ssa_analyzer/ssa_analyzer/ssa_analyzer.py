# Author: Junqi Ma on 8/3/16

import sys
from optparse import OptionParser
import subprocess_util
import time
import tempfile
import os
import subprocess


def main():
    versions_dir = "/home/majunqi/research/msbench/examples/ssa-ex-versions"
    version = "ssa-ex-1634796cc3a3ee4b3cc216d256b5614f74a43ef4"
    output_dir = "/tmp/aaa/"
    sample = "bufio"
    loops = "3"
    repetitions = "5"

    # print versions_dir + "/" + version, "-p", output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".pprof", "-l", loops, samples_dir + "/" + sample
    subprocess_util.generate_multiple_onesample_threads(loops, versions_dir, output_dir, repetitions, sample)


if __name__ == '__main__':
    main()
