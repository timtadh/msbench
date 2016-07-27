# Author: Junqi Ma on 7/16/16

import sys
from optparse import OptionParser
import subprocess_util
import time
import tempfile
import os

'''
command:
python html_analyzer.py -l 100 -v /home/majunqi/research/msbench/examples/html-ex-versions -r 5 -o /tmp/test/ /home/majunqi/research/cc-sample
python html_analyzer.py -l 100 -p /home/majunqi/research/msbench/examples/html-ex-versions/... -p /home/majunqi/research/msbench/examples/html-ex-versions/... -r 5 -o /tmp/test/ /home/majunqi/research/cc-sample

'''


def main():
    usage = "usage: %prog -l <int> -v <versions_dir>| -p <version_dir> -p <version_dir> -r <repetitions> -o <output_dir> <samples_dir>"
    parser = OptionParser(usage)
    parser.add_option(
        "-l", "--loops", dest="loops", type="string",
        help="define the loops"
    )
    parser.add_option("-v", "--versions_dir", dest="versions_dir")
    parser.add_option(
        "-o", "--output_dir", dest="output_dir", type="string", default=tempfile.gettempdir(),
        help="path to write output"
    )
    parser.add_option(
        "-r", "--repetitions", dest="repetitions", type="string",
        help="specify how many timing repetitions to run"
    )
    parser.add_option(
        "-p", "--particular", dest="particular", type="string", action="append",
        help="use particular versions "
    )

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "You must provide a directory for the datasets"
        print >> sys.stderr, "got: %s" % ', '.join(args)
        parser.print_help()
        sys.exit(1)

    samples_dir = os.path.abspath(args[0])
    if not os.path.exists(samples_dir):
        print >> sys.stderr, "The directory %s does not exist!" % samples_dir
        parser.print_help()
        sys.exit(1)

    output_dir = os.path.abspath(options.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print >> sys.stderr, "directory %s" % output_dir, "has been created"

    if options.loops:
        if options.output_dir:
            if options.repetitions:
                if options.versions_dir and options.particular:
                    print >> sys.stderr, "You must can provide a argument for the versions_dir or particular version"
                    parser.print_help()
                    sys.exit(1)
                elif options.versions_dir:
                    start_all(options.loops, options.versions_dir, options.output_dir, options.repetitions, args[0])
                elif options.particular:
                    dirs = options.particular
                    pieces = dirs[0].split('/')
                    index = len(pieces)

                    version_dir = ""
                    particular = []

                    for i in range(1,index-1):
                        version_dir += "/" + pieces[i]
                    for dir in dirs:
                        particular.append(dir.split('/')[index - 1])

                    start_particular(options.loops, version_dir, options.output_dir, options.repetitions, args[0], particular)
                else:
                    print >> sys.stderr, "You must provide a argument for the versions_dir or particular version"
                    parser.print_help()
                    sys.exit(1)
            else:
                print >> sys.stderr, "You must provide a argument for the repetitions"
                parser.print_help()
                sys.exit(1)
        else:
            print >> sys.stderr, "You must provide a argument for the output_dir"
            parser.print_help()
            sys.exit(1)
    else:
        print >> sys.stderr, "You must provide a argument for the loops"
        parser.print_help()
        sys.exit(1)


def start_all(loops, versions_dir, output_dir, repetitions, samples_dir):
    start = time.time()
    subprocess_util.generate_multiple_samples_threads(loops, versions_dir, output_dir, repetitions, samples_dir)
    print time.time() - start


def start_particular(loops, versions_dir, output_dir, repetitions, samples_dir, versions):
    start = time.time()
    subprocess_util.generate_particular_samples_threads(loops, versions_dir, output_dir, repetitions, samples_dir, versions)
    print time.time() - start


if __name__ == '__main__':
    main()
