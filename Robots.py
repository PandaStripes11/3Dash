from Graphics import *

class Robot():
   def __init__(self, headCenter, armSide = "right", color"firebrick"):
      self.headCenter = headCenter
      self.armSide = armSide
      self.color = color

   def drawRobot(headCenterX, headCenterY, armSide="right", color="firebrick"):
       setColor(color)
       
       # Head
       headCenter = (headCenterX, headCenterY)
       fillCircle(*headCenter, 50)
       
       # Body
       bodyStart = (headCenter[0], headCenter[1]+90)
       for i in range(50):
         fillCircle(bodyStart[0], bodyStart[1]+i, 40)
       
       # Arm
       if armSide == "right":
          for i in range(25):
            fillCircle(bodyStart[0]+40+i, bodyStart[1]-(i//2), 25)
       else:
         for i in range(25):
            fillCircle(bodyStart[0]-40-i, bodyStart[1]-(i//2), 25)
       
       # Legs
       legsStart = (bodyStart[0]-20, bodyStart[1]+110)
       for i in range(25):
         fillCircle(legsStart[0]-(i//2), legsStart[1]+i, 25)
         fillCircle(legsStart[0]+40+(i//2), legsStart[1]+i, 25)
         
   def controls():
      self.headCenter += 5
      self.headCenter -= 5
      
   