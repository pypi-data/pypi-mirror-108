#!/usr/bin/env python3
from .args import get_magcluster_parser
from .controller import controller

def main():
    # global args
    args = get_magcluster_parser()
    controller(args, subparser_name=args.subparser_name)

#############################################
if __name__ == '__main__':
    main()