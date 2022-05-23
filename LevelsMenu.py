from Graphics import *

def drawPlayButton():
   setColor("white")
   fillRectangle(475,325,800,450) #play button
   setColor("darkslateblue")
   drawString("PLAY!",520,425,"Arial",60, "bold")
   
def drawLevels(completedLevels):
   setBackground("cornflowerblue")
   setColor("white")  
   rectanglePositions = [
      [100,100,300,300],
      [400,100,600,300],
      [700,100,900,300],
      [1000,100,1200,300]
   ]
   for position in rectanglePositions:
      fillRectangle(*position)
      fillRectangle(position[0],400,position[2],600)

   stringPositions = [130,430,730,1030]
   for index, position in enumerate(stringPositions):
      setColor("cornflowerblue")
      drawString("Level \n    "+str(index+1), position, 250, "Arial", 40, "bold")
      drawString("Level \n    "+str(index+5), position, 550, "Arial", 40, "bold")
      if completedLevels[index]:
         setColor("mediumseagreen")
         drawString("✔", position, 285, "Arial", 120, "bold")
      elif completedLevels[index+4]:
         setColor("mediumseagreen")
         drawString("✔", position, 585, "Arial", 120, "bold")
