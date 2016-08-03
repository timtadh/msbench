# Author: Junqi Ma on 8/3/16


import sys
from optparse import OptionParser
import subprocess_util
import time
import tempfile
import os
import subprocess


def main():
    # versions_dir = "/home/majunqi/research/msbench/examples/ssa-ex-versions"
    # version = "ssa-ex-1634796cc3a3ee4b3cc216d256b5614f74a43ef4"
    # output_dir = "/tmp/aaa/"
    # sample = "bufio"
    # loops = "1"
    # repetitions = "100"
    usage = "usage: %prog -l <int> -v  <versions_dir> -o <output_dir> <samples_dir>"
    parser = OptionParser(usage)
    parser.add_option(
        "-l", "--loops", dest="loops", type="string",
        help="define the loop"
    )
    parser.add_option(
        "-v", "--versions-dir", dest="versions_dir", type="string",
        help="the directory of versions"
    )
    parser.add_option(
        "-r", "--repetitions", dest="repetitions", type="string",
        help="specify how many timing repetitions to run"
    )
    parser.add_option(
        "-o", "--output-dir", dest="output_dir", type="string", default=tempfile.gettempdir(),
        help="path to write output"
    )

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "You must provide a directory for the datasets"
        print >> sys.stderr, "got: %s" % ', '.join(args)
        parser.print_help()
        sys.exit(1)

    sample = args[0]

    output_dir = os.path.abspath(options.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print >> sys.stderr, "directory %s" % output_dir, "has been created\n"

    if options.loops:
        if options.output_dir:
            if options.repetitions:
                if options.versions_dir:
                    start_all_onedataset(options.loops, options.versions_dir, options.output_dir, options.repetitions, sample)
                else:
                    print >> sys.stderr, "You must provide a argument for the versions_dir or particular version"
                    parser.print_help()
                    sys.exit(1)
            else:
                print >> sys.stderr, "You must provide a argument for the repetitions or particular version"
                parser.print_help()
                sys.exit(1)
        else:
            print >> sys.stderr, "You must provide a argument for the output_dir or particular version"
            parser.print_help()
            sys.exit(1)
    else:
        print >> sys.stderr, "You must provide a argument for the loops or particular version"
        parser.print_help()
        sys.exit(1)


def start_all_onedataset(loops, versions_dir, output_dir, repetitions, sample):
    print >> sys.stderr, "program is running....."
    start = time.time()
    subprocess_util.generate_multiple_onedataset(loops, versions_dir, output_dir, repetitions, sample)
    print time.time() - start

if __name__ == '__main__':
    main()