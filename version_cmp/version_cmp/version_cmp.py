# Author: Junqi Ma on 7/18/16

import sys

import calcu_util
import plot_figure
import anova_oneway
import sys
import os
import tempfile
from optparse import OptionParser


def main():
    usage = "%prog -o <output-path> [--plot-all|--plot-dataset=<dataset>|--stats] <datasets>"
    # usage = "usage: %prog -c <samples_dir> or \n %prog -t <samples_dir> -n <int>"
    parser = OptionParser(usage)
    parser.add_option(
        '-o', "--output", dest="output", type="string", default=tempfile.gettempdir(),
        help="output directory where results are written",
    )
    parser.add_option(
        '-a', "--plot-all", dest="plot_all", action="store_true", default=False,
        help="plot all of the figures for all versions and datasets",
    )
    parser.add_option(
        '-d', "--plot-dataset", dest="plot_dataset", type="string", default=None,
        help="plot figures for the specified dataset",
    )
    parser.add_option(
        '-s', "--stats", dest="stats", action="store_true", default=False,
        help="compute descriptive statistics: mean, stddev",
    )
    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "You must provide a directory for the datasets"
        print >> sys.stderr, "got: %s" % ', '.join(args)
        parser.print_help()
        sys.exit(1)

    datasets = os.path.abspath(args[0])
    if not os.path.exists(datasets):
        print >> sys.stderr, "The directory %s does not exist!" % datasets
        parser.print_help()
        sys.exit(1)

    output_dir = options.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print >> sys.stderr, "writing output to: %s" % output_dir

    if options.stats:
        stats(output_dir, datasets)
    elif options.plot_all:
        plot_all(output_dir, datasets)
    elif options.plot_dataset is not None:
        plot_dataset(output_dir, datasets, str(options.plot_dataset))
    else:
        print >> sys.stderr, "you must supply one of: --stats, --plot-all, --plot-dataset"
        parser.print_help()
        sys.exit(1)


def stats(output_dir, dataset_dir):
    name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic = calcu_util.calculate_allfiles_mean_std(dataset_dir)
    i, dir = calcu_util.write_allfiles(name_list, result_mean_list, result_std_list, output_dir)
    print "write " + str(i) + " files to the directory: " + dir


def plot_all(output_dir, dataset_dir):
    name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic = calcu_util.calculate_allfiles_mean_std(dataset_dir)
    plot(name_list, result_mean_list, get_f_oneway(result_mean_list), output_dir)


def plot_dataset(output_dir, dataset_dir, dataset_number):
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_number)
    plot_one(name_list, result_list, dataset_number, output_dir)


def plot(name_list, result_list, f_oneway, output_dir):
    plot_figure.plot_box(name_list, result_list, f_oneway, output_dir)


def plot_one(name_list, result_list, number, output_dir):
    dir = plot_figure.plot_one(name_list, result_list, number, output_dir)
    print "figure was saved in: " + dir


def get_f_oneway(result_list):
    return anova_oneway.anova_f_oneway(result_list)


if __name__ == '__main__':
    main()