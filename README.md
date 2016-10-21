# Python Logging Module

This is a simple python logging module with predefined defaults for use in command line python scripts.

Works on python 2.7+ (including python 3).

Example usage:

~~~python
from log import log, set_logging_level, levels
set_logging_level(levels.DEBUG)
log('Default INFO level message')
log('log.py allows for custom colors', color='red', background='blue', style='bright')    
log('Plus predefined prefixes and colors', levels.PLUS)
log('Bang!', levels.BANG)
log('Asterisk', levels.ASTERISK)
log('Minus', levels.MINUS)
log('Some informative warning', levels.WARNING)
log('A descriptive error occurred', levels.ERROR)
log('Helpful debug statement', levels.DEBUG)
~~~

Output:

![](https://i.imgur.com/suNlCvX.png)
