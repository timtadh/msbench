# Author: Junqi Ma on 3/7/17

import matrix_generator
import os


def commandline():
    '''
    these two dirs needs to be changed everytime
    '''

    programs_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/"
    pprofs_dir = "/home/majunqi/research/result/html1500_automation/html_large1500_new/"

    # workspace_dir = "/home/majunqi/research/result/test_automation_test/"
    workspace_dir = "/home/majunqi/research/result/test_test/"

    if not os.path.isdir(workspace_dir):
        os.mkdir(workspace_dir)

    dest_dir_profdata_tmp = workspace_dir + "profdata_pfm_largesize/"
    dest_dir_profdata = workspace_dir + "profdata_pfm_largesize/"

    # profdata_pfm_all = "/home/majunqi/research/result/test_automation/profdata_pfm_largesize/"
    profdata_pfm_all = dest_dir_profdata
    profdata_pfm_classified = workspace_dir + "profdata_pfm_largesize_classified/"

    # folders_dir = "/home/majunqi/research/result/test_automation/profdata_pfm_largesize_classified/"
    folders_dir = profdata_pfm_classified

    dest_dir_processed = workspace_dir + "processed_data_largesize/"
    dest_dir_processed_flat = workspace_dir + "processed_data_largesize_flat/"

    num_of_repetition = 50

    # because the original file is so big (more than 1 million files), the line below is executed separately from others
    # num_of_html, num_of_repetition = matrix_generator.profile_dir_setup(programs_dir, pprofs_dir, dest_dir_profdata_tmp)

    # the following lins of code can be run simultaneous.
    matrix_generator.avg_prof_data(dest_dir_profdata_tmp, dest_dir_profdata)
    matrix_generator.classify_files_byversions(profdata_pfm_all, profdata_pfm_classified)
    matrix_generator.classify_files_byhtmls(profdata_pfm_classified)
    matrix_generator.load_all_files(folders_dir, dest_dir_processed, True, num_of_repetition)
    matrix_generator.load_all_files(folders_dir, dest_dir_processed_flat, False, num_of_repetition)


if __name__ == '__main__':
    commandline()
