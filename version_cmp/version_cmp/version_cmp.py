# Author: Junqi Ma on 7/18/16

import sys

import calcu_util
import plot_figure
import anova_oneway
import sys
import os
import tempfile
import anova_oneway
from optparse import OptionParser


def main():
    usage = "%prog -o <output-path> [--plot-all|--plot-dataset=<dataset>|--stats] <datasets>"
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
    parser.add_option(
        '-t', "--t-test", dest="t_test", type="string", action="append",
        help="name the versions to tun the t-test"
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
    elif options.plot_dataset:
        # plot particular versions
        if options.t_test:
            # calculate_t_test()
            plot_dataset_versions(options.output, datasets, str(options.plot_dataset), options.t_test)
        # plot all versions
        else:
            # calculate_t_test()
            plot_dataset_allversions(output_dir, datasets, str(options.plot_dataset))
    else:
        print >> sys.stderr, "you must supply one of: --stats, --plot-all, --plot-dataset, [-n, -t]"
        parser.print_help()
        sys.exit(1)


def stats(output_dir, dataset_dir):
    name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic = calcu_util.calculate_allfiles_mean_std(dataset_dir)
    i, dir = calcu_util.write_allfiles(name_list, result_mean_list, result_std_list, output_dir)
    print "write " + str(i) + " files to the directory: " + dir


def plot_all(output_dir, dataset_dir):
    name_list, result_mean_list, result_std_list, result_mean_dic, result_std_dic = calcu_util.calculate_allfiles_mean_std(dataset_dir)
    plot(name_list, result_mean_list, get_f_oneway(result_mean_list), output_dir)


def plot_dataset_allversions(output_dir, dataset_dir, dataset_number):
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_number)
    print anova_oneway.anova_f_oneway(result_list)
    plot_one(name_list, result_list, dataset_number, output_dir)


def plot_dataset_versions(output_dir, dataset_dir, dataset_number, version_list):
    version_list = [version[:10]+"-"+dataset_number for version in version_list]
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_number)
    samples_list=[]
    i = 0
    for name in name_list:
        if name in version_list:
            samples_list.append(result_list[i])
        i += 1
    print anova_oneway.anova_f_oneway(samples_list)
    plot_one(version_list, samples_list, dataset_number, output_dir)



def plot(name_list, result_list, f_oneway, output_dir):
    plot_figure.plot_box(name_list, result_list, f_oneway, output_dir)


def plot_one(name_list, result_list, number, output_dir):
    dir = plot_figure.plot_one(name_list, result_list, number, output_dir)
    print "figure was saved in: " + dir


def get_f_oneway(result_list):
    return anova_oneway.anova_f_oneway(result_list)


if __name__ == '__main__':
    main()
