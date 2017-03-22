# Author: Junqi Ma on 3/7/17

import matrix_generator

def commandline():
    matrix_generator.extract_dir_setup()
    matrix_generator.files_divider()
    matrix_generator.load_all_files()


if __name__ == '__main__':
    commandline()
