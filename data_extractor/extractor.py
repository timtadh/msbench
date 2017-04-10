# Author: Junqi Ma on 3/7/17

import matrix_generator
import os

def commandline():
    '''
    these two dirs needs to be changed everytime
    '''

    programs_dir = "/home/majunqi/research/msbench/examples/html-ex-exp-pfm-versions/"
    pprofs_dir = "/home/majunqi/research/result/html1500_automation/html_large1500_new/"

    workspace_dir = "/home/majunqi/research/result/test_automation_test/"
    if not os.path.isdir(workspace_dir):
        os.mkdir(workspace_dir)

    dest_dir_profdata = workspace_dir + "profdata_pfm_largesize/"

    # profdata_pfm_all = "/home/majunqi/research/result/test_automation/profdata_pfm_largesize/"
    profdata_pfm_all = dest_dir_profdata
    profdata_pfm_classified = workspace_dir + "profdata_pfm_largesize_classified/"

    # folders_dir = "/home/majunqi/research/result/test_automation/profdata_pfm_largesize_classified/"
    folders_dir = profdata_pfm_classified

    dest_dir_processed = workspace_dir + "processed_data_largesize/"
    dest_dir_processed_flat = workspace_dir + "processed_data_largesize_flat/"

    # matrix_generator.extract_dir_setup(programs_dir, pprofs_dir, dest_dir_profdata)
    # matrix_generator.files_divider(profdata_pfm_all, profdata_pfm_classified)
    matrix_generator.load_all_files(folders_dir, dest_dir_processed, True)
    matrix_generator.load_all_files(folders_dir, dest_dir_processed_flat, False)

if __name__ == '__main__':
    commandline()
