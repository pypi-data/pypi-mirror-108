#!/usr/bin/env python3

import args
from magcluster import magcluster

def main():
    global args
    args = args.get_magcluster_parser()
    magcluster(args, subparser_name=args.subparser_name)

#############################################
if __name__ == '__main__':
    main()