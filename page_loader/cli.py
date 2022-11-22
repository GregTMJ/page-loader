import argparse
import os


def parse_args(argv=None):
    """
    Getting the info from client to download the needed content
    :param argv:
    :return: output dir + web page
    """
    parser = argparse.ArgumentParser(
        description='Script that helps downloading a web page with '
                    'its content'
    )
    parser.add_argument('url')
    parser.add_argument(
        '-o',
        '--output',
        default='',
        help=f"output directory (default: '{os.getcwd()}')"
    )
    return parser.parse_args(argv)
