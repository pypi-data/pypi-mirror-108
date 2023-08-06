"""
    
        A not very useful module used in the hgdemo project.

"""
PIE=3.14159

def area(r):
    """Returns the area of the circle with the radius 'r'

    Args:
        r (float): radius of the circle
    """
    A=PIE*r*r
    return A

def peri(r):
    """Returns the perimeter of the circle with the radius 'r'

    Args:
        r (float): radius of the circle
    """
    L=PIE*r*2
    return L
