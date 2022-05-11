#FinalProject.py
from Graphics import *

beginGrfx(1300, 700)


def drawRobot():
    headCenter = (450, 200)
    # Head
    fillCircle(headCenter[0], headCenter[1], 50)
    # Body
    fillOval(headCenter[0], headCenter[1]+150, 50, 75)
    # Legs
    # Arms
    pass


"""
MAIN
"""
drawRobot()



endGrfx()