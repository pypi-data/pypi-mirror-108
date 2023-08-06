#magcluster

from maga import maga
from magsc import magsc
from magm import magm

def magcluster(args, subparser_name=None):
    """user args to run magcluster""" 
    if subparser_name:
        if subparser_name == 'maga':
            maga()
        elif subparser_name == 'magsc':
            magsc(args)
        elif subparser_name == 'magm':
            magm()

