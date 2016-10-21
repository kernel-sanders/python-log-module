#!/usr/bin/env python

import argparse
from log import log, set_logging_level, levels

def main(args, log_level):

    # set our custom logger to the user supplied level
    set_logging_level(log_level)
    # demo
    log('Default INFO level message')
    log('log.py allows for custom colors', color='red', background='blue', style='bright')    
    log('Plus predefined prefixes and colors', levels.PLUS)
    log('Bang!', levels.BANG)
    log('Asterisk', levels.ASTERISK)
    log('Minus', levels.MINUS)
    log('Some informative warning', levels.WARNING)
    log('A descriptive error occurred', levels.ERROR)
    log('Helpful debug statement', levels.DEBUG)

def parse_args():
    """ Parse the user supplied arguments and return an arg object to the user """
    parser = argparse.ArgumentParser( 
                                    description = 'A small demo of log.py. Requires colorama',
                                    epilog = 'Bad Sector Labs - 2016')
    parser.add_argument(
                      '-v',
                      '--verbose',
                      help='increase output verbosity',
                      action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    """ Called as a stand-alone script, parse args and call main """
    args = parse_args()  

    # Set log level
    if args.verbose:
        log_level = levels.DEBUG
    else:
        log_level = levels.INFO
  
    main(args, log_level)