# Author: Junqi Ma on 7/16/16

import sys
from optparse import OptionParser


def command_line_args():
    usage = "usage: %prog -s <samples_dir> or \n %prog -m <samples_dir> "
    parser = OptionParser(usage)
    parser.add_option("-s", "--standdeviation", dest="standarddeviation", help="calculate the standard deviation", type="string")
    parser.add_option("-m", "--mean", dest="mean", help="calculate the mean", type="string")
    parser.add_option("-p", "--plot", dest="plot", help="plot the figure", type="string")
    (options, args) = parser.parse_args()
    if options.standarddeviation == None and options.mean == None and options.plot == None:
        parser.print_help()
        sys.exit()
    elif options.standarddeviation != None:
        return "std", options.standarddeviation
    elif options.mean != None:
        return "mean", options.mean
    elif options.plot != None:
        return "plot", options.plot
