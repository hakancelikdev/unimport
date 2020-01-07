# This is not unused import, but it is unused import according to unimport.

# CASE 1
from codeop import compile_command

__all__ = ["compile_command"]

# CASE 2; NOTE Its has methods need to be checked
# then they need to be compared to the state of use and then it has to be printed.
from io import __all__ 
# or
from io import * 
