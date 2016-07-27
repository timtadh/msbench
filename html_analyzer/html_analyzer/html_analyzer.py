# Author: Junqi Ma on 7/16/16

import command_line_util
import subprocess_util
import time
'''
command: python html_analyzer.py -l 100 -v /home/majunqi/research/msbench/examples/html-ex-versions -r 5 -o /tmp/test/ /home/majunqi/research/cc-sample

'''

def main():
    (loops, versions_dir, output_dir, repetitions, samples_dir) = command_line_util.command_line_args()
    start = time.time()
    # subprocess_util.generate_multiple_samples(loops, versions_dir, output_dir, repetitions, samples_dir)

    subprocess_util.generate_multiple_samples_threads(loops, versions_dir, output_dir, repetitions, samples_dir)
    print time.time()-start
if __name__ == '__main__':
    main()
