import sys
import argparse

from phygitalism_config.__main__ import args_parser, main

from phygitalism_logger.config import Graylog

args_parser_logger = argparse.ArgumentParser()
args_parser_logger.add_argument("path", type=str)


def gen():
    args = args_parser_logger.parse_args()
    sys.argv[1] = 'phygitalism_logger.config'
    sys.argv.append('Graylog')
    sys.argv.append(args.path)
    main()


if __name__ == "__main__":
    gen()
