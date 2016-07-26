# Author: Junqi Ma on 7/16/16

import sys
from optparse import OptionParser


def command_line_args():
    usage = "usage: %prog -c <samples_dir> or \n %prog -t <samples_dir> -n <int>"
    parser = OptionParser(usage)
    parser.add_option("-c", "--calculate", dest="calculate", help="calculate the mean and standard deviation", type="string")
    parser.add_option("-p", "--plotall", dest="plotall", help="plot the figure", type="string")
    parser.add_option("-t", "--plotone", dest="plotone", help="plot one figure", type="string")
    parser.add_option("-n", "--number", dest="number", help="which sample to plot", type="string")
    (options, args) = parser.parse_args()
    if options.calculate == None and options.plotall == None and options.plotone == None:
        parser.print_help()
        sys.exit()
    elif options.calculate != None:
        return "calculate", [options.calculate]
    elif options.plotall != None:
        return "plotall", [options.plotall]
    elif options.plotone != None:
        if options.number != None:
            return "plotone", [options.plotone, options.number]
        else:
            parser.print_help()
            sys.exit()
    else:
        parser.print_help()
        sys.exit()