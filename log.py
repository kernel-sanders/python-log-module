import logging, inspect
try:
    from colorama import Fore, Back, Style
except ImportError:
    print("""
colorama is required when using log.py
        """)
    import sys
    if sys.hexversion < 0x03000000:
        print('install it with:\npip install colorama')
    else:
        print('install it with:\npip3 install colorama')
    sys.exit(1)
import argparse

class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter to provide the appropriate prefix to logs
    """

    def format(self, record):
        """ Defines the conditional prefix based on logging level """
        if record.levelname == 'DEBUG':
            # This function is quite a ways away from the calling function due to the custom logging module
            func = inspect.currentframe().f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_code
            format = '[DEBUG] {message} ({name} in {file}:{line})'.format(message=record.getMessage(),
                                                                          name=func.co_name,
                                                                          file=func.co_filename,
                                                                          line=func.co_firstlineno)
            return format
        elif record.levelname == 'INFO':
            return '{message}'.format(message=record.getMessage())
        elif record.levelname == 'PLUS':
            prefix = '{color}[+]'.format(color=Fore.GREEN)
        elif record.levelname == 'ASTERISK':
            prefix = '[*]'
        elif record.levelname == 'MINUS':
            prefix = '{style}{color}[-]'.format(color=Fore.YELLOW,
                                                style=Style.DIM)
        elif record.levelname == 'BANG':
            prefix = '{color}[!]'.format(color=Fore.YELLOW)
        elif record.levelname == 'WARNING':
            prefix = '{color}{background}{style}[W]'.format(color=Fore.RED, 
                                                            background=Back.YELLOW,
                                                            style=Style.NORMAL)
        elif record.levelname == 'ERROR':
            prefix = '{color}{background}{style}[E]'.format(color=Fore.YELLOW, 
                                                            background=Back.RED,
                                                            style=Style.NORMAL)
        else:
            prefix = ''

        format = '{prefix} {message}{reset_color}'.format(prefix=prefix,
                                                          message=record.getMessage(),
                                                          reset_color=Style.RESET_ALL)

        # handle an exception
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
            format += '{color}{exc_text}{reset_color}'.format(color=Fore.RED + Back.YELLOW,
                                                              exc_text=record.exc_text,
                                                              reset_color=Style.RESET_ALL)

        return format

class CustomLogger(object):
    """
    The object to maintain the state of our custom logger
    """

    def __init__(self,log_level=20): # default to INFO level

        # Define the level that will be '[+] <message>'
        logging.addLevelName(levels.PLUS, 'PLUS') 
        def plus(self, message, *args, **kws):
            """ The custom check for a level """
            if self.isEnabledFor(levels.PLUS):
                self._log(levels.PLUS, message, args, **kws)
        logging.Logger.plus = plus # add our custom level to the logger

        # Define the level that will be '[*] <message>'
        logging.addLevelName(levels.ASTERISK, 'ASTERISK') 
        def asterisk(self, message, *args, **kws):
            """ The custom check for a level """
            if self.isEnabledFor(levels.ASTERISK):
                self._log(levels.ASTERISK, message, args, **kws)
        logging.Logger.asterisk = asterisk # add our custom level to the logger

        # Define the level that will be '[-] <message>'
        logging.addLevelName(levels.MINUS, 'MINUS') 
        def minus(self, message, *args, **kws):
            """ The custom check for a level """
            if self.isEnabledFor(levels.MINUS):
                self._log(levels.MINUS, message, args, **kws)
        logging.Logger.minus = minus # add our custom level to the logger

        # Define the level that will be '[!] <message>'
        logging.addLevelName(levels.BANG, 'BANG') 
        def bang(self, message, *args, **kws):
            """ The custom check for a level """
            if self.isEnabledFor(levels.BANG):
                self._log(levels.BANG, message, args, **kws)
        logging.Logger.bang = bang # add our custom level to the logger

        # create the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        # create console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(log_level)
        # add our custom formatter to the console handler
        self.console_handler.setFormatter(CustomFormatter())
        # add the console handler to the logger
        self.logger.addHandler(self.console_handler)

    def set_level(self,log_level):
        """ Set a loglevel for all future logging """
        self.logger.setLevel(log_level)
        self.console_handler.setLevel(log_level)

    def log(self, message, level, color, background, style):
        """ 
        Call the logger at the specified level with the specified colors,
        or level defaults
        """
        # set the color prefix
        if color == 'default':
            color_prefix = ''
        elif color.upper() in ['BLACK', 'RED', 'GREEN', 'YELLOW', 
                             'BLUE', 'MAGENTA', 'CYAN', 'WHITE']:
            color_prefix = Fore.__dict__[color.upper()]
        else:
            self.logger.log(levels.ERROR, '{} is not an availbe color'.format(color))
            return

        # set the background prefix
        if background == 'default':
            background_prefix = ''
        elif background.upper() in ['BLACK', 'RED', 'GREEN', 'YELLOW', 
                             'BLUE', 'MAGENTA', 'CYAN', 'WHITE']:
            background_prefix = Back.__dict__[background.upper()]        
        else:
            self.logger.log(levels.ERROR, '{} is not an availbe background color'.format(background))
            return

        # set the style prefix
        if style == 'default':
            style_prefix = ''
        elif style.upper() in ['DIM', 'NORMAL', 'BRIGHT']:
            style_prefix = Style.__dict__[style.upper()]
        else:
            self.logger.log(levels.ERROR, '{} is not an availbe style'.format(style))
            return

        # build the message
        message = '{color_prefix}{background_prefix}{style_prefix}{message}{reset_color}'.format(color_prefix=color_prefix,
                                                  background_prefix=background_prefix,
                                                  style_prefix=style_prefix,
                                                  message=message,
                                                  reset_color=Style.RESET_ALL)
        # log it!
        self.logger.log(level, message) 



# custom logging level globals
# INFO is 20 and DEBUG is 10, to be included in output without a -v, our level must be >20
levels_dict = {'PLUS': 21,
                'ASTERISK': 22,
                'MINUS': 23,
                'BANG': 24,
                # standard levels
                'CRITICAL': 50,
                'ERROR': 40,
                'WARNING': 30,
                'INFO': 20,
                'DEBUG': 10,
                'NOTSET': 0
                }

# make a nice object from our dict
levels = argparse.Namespace(**levels_dict) 

# module global custom logger object
custom_logger = CustomLogger()

def set_logging_level(log_level):
    custom_logger.set_level(log_level)

def log(message, level=20, color='default', background='default', style='default'):
    custom_logger.log(message, level, color, background, style)

        