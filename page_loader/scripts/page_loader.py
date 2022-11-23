#!/usr/bin/env python
import logging
import sys

from page_loader import download
from page_loader.cli import parse_args

logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function that starts our project's scripts
    """
    args = parse_args()

    try:
        download(args.url, args.output)
        logging.info("The web page will be shortly downloaded "
                     f"and added to {args.output}")
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
