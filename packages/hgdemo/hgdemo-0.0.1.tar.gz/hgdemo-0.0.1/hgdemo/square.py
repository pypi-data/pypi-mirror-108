"""
    
        SQUARE : Another not very useful module used in the hgdemo project.

"""

import numpy as np

def sqarea(r):
    """ Returns the area of the square with the side 'r'

    Args:
        r (float): square side
    """
    A=r*r
    return A

def side(A):
    """ Returns the side of the square with the area 'A''

    Args:
        A (float): square area
    """
    r=np.sqrt(A)
    return r
    