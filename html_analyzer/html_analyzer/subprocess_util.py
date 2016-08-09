# Author: Junqi Ma on 7/17/16

import shutil
import os
import subprocess
import time
from multiprocessing import Process


def generate_sample(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions):
    subprocess.call([versions_dir + "/" + version, "-p", output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".pprof", "-l", loops, samples_dir + "/" + sample],
                    shell=False)


def generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions):
    elapsed = ""
    for repetition in range(int(repetitions)):
        start = time.time()
        generate_sample(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)
        if elapsed == "":
            elapsed = str((time.time()) - start)
        else:
            elapsed = elapsed + "-" + str((time.time()) - start)
    write_file(output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".time", elapsed)


def generate_multiple_samples(loops, versions_dir, output_dir, repetitions, samples_dir):
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    if len(versions_list) != 0 and len(samples_list) != 0:
        for version in versions_list:
            for sample in samples_list:
                generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


def generate_particular_onesample(loops, versions_dir, output_dir, repetitions, sample, versions):
    pieces = sample.split('/')
    index = len(pieces)
    samples_dir = ""
    for i in range(1, index - 1):
        samples_dir += "/" + pieces[i]
    samples_dir += "/"
    sample = pieces[index - 1]
    for version in versions:
        generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


def generate_all_onesample(loops, versions_dir, output_dir, repetitions, sample):
    pieces = sample.split('/')
    index = len(pieces)
    samples_dir = ""
    for i in range(1, index - 1):
        samples_dir += "/" + pieces[i]
    samples_dir += "/"
    sample = pieces[index - 1]
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    for version in versions_list:
        generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


# useless
# some versions running through all datasets
def generate_particular_samples_threads(loops, versions_dir, output_dir, repetitions, samples_dir, versions):
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    # we will use versions instead of versions_list
    if len(versions) != 0 and len(samples_list) != 0:
        threads = []
        print len(versions), " processes are running.... "
        for version in versions:
            p = Process(target=generate_samples_run,
                        args=(versions_dir, version, output_dir, samples_list, samples_dir, loops, repetitions,))
            threads.append(p)
    for i in range(0, len(versions)):
        threads[i].start()
    for i in range(0, len(versions)):
        threads[i].join()


# some versions running through all datasets
def generate_particular_samples(loops, versions_dir, output_dir, repetitions, samples_dir, versions):
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    # we will use versions instead of versions_list
    if len(versions) != 0 and len(samples_list) != 0:
        for version in versions:
            for sample in samples_list:
                generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


# useless
# all versions running through all datasets
def generate_multiple_samples_threads(loops, versions_dir, output_dir, repetitions, samples_dir):
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    if len(versions_list) != 0 and len(samples_list) != 0:
        threads = []
        print len(versions_list), " processes are running.... "
        for version in versions_list:
            p = Process(target=generate_samples_run,
                        args=(versions_dir, version, output_dir, samples_list, samples_dir, loops, repetitions,))
            threads.append(p)
    for i in range(0, len(versions_list)):
        threads[i].start()
    for i in range(0, len(versions_list)):
        threads[i].join()

# all versions running through all datasets
def generate_multiple_samples(loops, versions_dir, output_dir, repetitions, samples_dir):
    versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    if len(versions_list) != 0 and len(samples_list) != 0:
        for version in versions_list:
            for sample in samples_list:
                generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


def generate_samples_run(versions_dir, version, output_dir, samples_list, samples_dir, loops, repetitions):
    for sample in samples_list:
        generate_sample_repetitions(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions)


def pre_process(output_dir, versions_dir, samples_dir):
    generate_dir(output_dir)
    versions_list = get_allfiles(versions_dir)
    samples_list = get_allfiles(samples_dir)

    return versions_list, samples_list


def get_allfiles(dir):
    return os.listdir(dir)


def generate_dir(dir):
    try:
        os.mkdir(dir)
    except:
        shutil.rmtree(dir)
        os.mkdir(dir)


def write_file(dir, content):
    if content != "":
        f = open(dir, "w+")
        f.write(content)
        f.close()
