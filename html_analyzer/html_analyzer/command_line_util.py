# Author: Junqi Ma on 7/16/16

import sys
from optparse import OptionParser


def command_line_args():
    usage = "usage: %prog -l <int> -v <versions_dir> -r <repetitions> -o <output_dir> <samples_dir>"
    parser = OptionParser(usage)
    parser.add_option("-l", "--loops", dest="loops", help="define the loops", type="string")
    parser.add_option("-v", "--versions_dir", dest="versions_dir")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path to write output", type="string")
    parser.add_option("-r", "--repetitions", dest="repetitions", help="specify how many timing repetitions to run", type="string")
    (options, args) = parser.parse_args()
    if options.loops == None or options.versions_dir == None or options.output_dir == None or options.repetitions == None or len(args) != 1:
        parser.print_help()
        sys.exit()
    else:
        return options.loops, options.versions_dir, options.output_dir, options.repetitions, args[0]
