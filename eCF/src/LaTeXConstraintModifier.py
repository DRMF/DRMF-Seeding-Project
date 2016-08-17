
__author__ = 'Kevin Chen'
__status__ = 'Development'

import os
import argparse

parser = argparse.ArgumentParser(
    description='Receive .tex file with constraints and convert'
                ' them to lines using flushright and flushright.')
parser.add_argument('PATHR', type=str,
                    help='path of input .tex file, with the current'
                         ' directory as the starting point',)
parser.add_argument('PATHW', type=str,
                    help='path of file to be outputted to, with the current'
                         ' directory as the starting point')
args = parser.parse_args()

PATHR = args.PATHR
PATHW = args.PATHW
DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../data/'


def combine_percent(lines):
    # (list) -> list
    """
    Description

    :param lines:
    :return:
    """

    pass


def main():
    #
    """

    :return:
    """
    pass


if __name__ == '__main__':
    main()
