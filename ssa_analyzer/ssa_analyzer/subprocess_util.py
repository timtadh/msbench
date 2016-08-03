# Author: Junqi Ma on 8/3/16

import shutil
import os
import subprocess
import time
from multiprocessing import Process


def generate_samples_legacy(versions_dir, version, output_dir, sample, samples_dir, loops, repetitions):
    env = dict(os.environ)
    env["GOPATH"] = samples_dir
    print versions_dir + "/" + version, "-p", output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".pprof", "-l", loops, samples_dir + "/" + sample
    subprocess.call([versions_dir + "/" + version, "-p", output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".pprof", "-l", loops, samples_dir + "/" + sample],
                    shell=False, env=env)


def generate_samples(versions_dir, version, output_dir, sample, loops, repetitions):
    subprocess.call([versions_dir + "/" + version, "-p", output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".pprof", "-l", loops, sample],
                    shell=False)


def generate_samples_repetitions(versions_dir, version, output_dir, sample, loops, repetitions):
    elapsed = ""
    for repetition in range(int(repetitions)):
        start = time.time()
        generate_samples(versions_dir, version, output_dir, sample, loops, repetitions)
        if elapsed == "":
            elapsed = str((time.time()) - start)
        else:
            elapsed = elapsed + "-" + str((time.time()) - start)
    write_file(output_dir + version + "-" + sample.partition(".")[0] + "-" + repetitions + ".time", elapsed)


def generate_multiple_onesample_threads(loops, versions_dir, output_dir, repetitions, sample):
    # versions_list, samples_list = pre_process(output_dir, versions_dir, samples_dir)
    versions_list = get_allfiles(versions_dir)
    samples_list = []

    samples_list.append(sample)
    if len(versions_list) != 0 and len(samples_list) != 0:
        threads = []
        print len(versions_list), " processes are running.... "
        for version in versions_list:
            p = Process(target=generate_samples_run,
                        args=(versions_dir, version, output_dir, samples_list, loops, repetitions,))
            threads.append(p)
    for i in range(0, len(versions_list)):
        threads[i].start()
    for i in range(0, len(versions_list)):
        threads[i].join()


def generate_samples_run(versions_dir, version, output_dir, samples_list, loops, repetitions):
    for sample in samples_list:
        generate_samples_repetitions(versions_dir, version, output_dir, sample, loops, repetitions)


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
        f = open(dir, "a+")
        f.write(content)
        f.close()
