# Author: Junqi Ma on 7/18/16

import calcu_util
import plot_figure
import sys
import os
import tempfile
import statistic
from optparse import OptionParser


def main():
    usage = "%prog -o <output-path> [--plot-all|--plot-dataset=<dataset> -t <versionname> -t <versionname>|--stats] <datasets>"
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
    parser.add_option(
        '-r', "--auto-report", dest="report", action="store_true", default=False,
        help="report automatically if there is a pair of versions whose p-value is smaller 5% in t-test"
    )
    parser.add_option(
        "--order", dest="order", type="string",
        help="gives the order of the input for plotting"
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

    if options.order:
        order_path = os.path.abspath(options.order)
        if not os.path.exists(order_path):
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
            plot_dataset_versions(options.output, datasets, options.plot_dataset, options.t_test)
        # plot all versions
        elif options.report:
            report_auto(options.output, datasets, options.plot_dataset)
        else:
            if output_dir:
                if options.order:
                    plot_dataset_allversions(output_dir, datasets, options.plot_dataset, order_path)
                else:
                    plot_dataset_allversions_random(output_dir, datasets, options.plot_dataset)
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
    print len(result_mean_list), len(result_mean_list[0])
    plot(name_list, result_mean_list, get_f_oneway(result_mean_list), output_dir)


def plot_dataset_allversions(output_dir, dataset_dir, dataset_id, order_path):
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_id)
    new_name_list, new_result_list = sort(name_list, result_list, order_path)
    print "anova f one way:", statistic.anova_f_oneway(result_list)
    print "new one", len(new_name_list), len(new_result_list)
    plot_one(new_name_list, new_result_list, dataset_id, output_dir)


def plot_dataset_allversions_random(output_dir, dataset_dir, dataset_id):
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_id)
    print "anova f one way:", statistic.anova_f_oneway(result_list)
    print "old one", len(name_list), len(result_list)
    plot_one(name_list, result_list, dataset_id, output_dir)


def sort(name_list, result_list, order_path):
    help_list_sorted = []
    new_name_list = []
    new_result_list = []
    with open(order_path) as f:
        name_list_ordered = [x.strip('\n') for x in f.readlines()]

    for i in range(len(name_list)):
        for j in range(len(name_list_ordered)):
            if name_list_ordered[j].__contains__(name_list[i].split("-")[0]):
                help_list_sorted.append(j)
    help_list_unsorted = list(help_list_sorted)
    help_list_sorted.sort()
    for i in help_list_sorted:
        for j in range(len(help_list_unsorted)):
            if help_list_unsorted[j] == i:
                new_name_list.append(name_list[j])
                new_result_list.append(result_list[j])
                break
    print len(help_list_sorted), len(help_list_unsorted)
    return new_name_list, new_result_list


# def switch(name_list, return_list):


def report_auto(output_dir, dataset_dir, dataset_id):
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_id)
    num = len(name_list)
    abnormal = []
    for i in range(num):
        for j in range(i + 1, num):
            result = statistic.t_test(result_list[i], result_list[j])
            if result[1] < 0.05:
                content = name_list[i] + name_list[j] + str(result[1])
                abnormal.append(content)
                print content
    if os.path.isfile(output_dir):
        calcu_util.write_file(output_dir, abnormal)


def plot_dataset_versions(output_dir, dataset_dir, dataset_id, version_list):
    version_list = [version[:10] + "-" + dataset_id for version in version_list]
    name_list, result_list = calcu_util.get_onesample_allversions(dataset_dir, dataset_id)
    samples_list = []
    i = 0
    for name in name_list:
        if name in version_list:
            samples_list.append(result_list[i])
        i += 1
    print "t test:", statistic.t_test(samples_list[0], samples_list[1])
    plot_one(version_list, samples_list, dataset_id, output_dir)


def plot(name_list, result_list, f_oneway, output_dir):
    plot_figure.plot_box(name_list, result_list, f_oneway, output_dir)


def plot_one(name_list, result_list, dataset_id, output_dir):
    dir = plot_figure.plot_one(name_list, result_list, dataset_id, output_dir)
    print "figure was saved in: " + dir


def get_f_oneway(result_list):
    return statistic.anova_f_oneway(result_list)


if __name__ == '__main__':
    main()
