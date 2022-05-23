from Graphics import *

def drawPlayButton():
   setColor("white")
   fillRectangle(475,325,800,450) #play button
   setColor("blue")
   drawString("PLAY!",520,425,"Arial",60, "bold")
   
def drawLevels():
   setBackground("blue")
   setColor("white")  
   fillRectangle(100,100,300,300)
   fillRectangle(400,100,600,300)
   fillRectangle(700,100,900,300)
   fillRectangle(1000,100,1200,300)
   setColor("blue")
   drawString("Level \n    1",130,250,"Arial",40,"bold")
   drawString("Level \n    2",430,250,"Arial",40,"bold")
   drawString("Level \n    3",730,250,"Arial",40,"bold")
   drawString("Level \n    4",1030,250,"Arial",40,"bold")
