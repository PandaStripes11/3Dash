from Graphics import *
from Robots import *
from Game import *

def drawBackground(backgroundColor,floorColor):
   setColor(backgroundColor)
   fillRectangle(0,0,1300,700) #Background
   setColor(floorColor)
   fillRectangle(0,425,1300,700) #floor

def drawRinkPart1(ringColor):
   setColor(ringColor)
   #back posts
   fillRectangle(150,175,175,475)   
   fillRectangle(1250,175,1275,475)
   #back bands
   y = 300
   for k in range(4):
      for k in range(5):
         drawLine(50,y,150,y - 75)
         drawLine(1150,y,1250,y - 75)
         drawLine(1250,y-75,150,y-75)
         y += 1  
      y += 68.75
        
def drawRinkPart2(ringColor):
   #front bands
   setColor(ringColor)
   y = 300
   for k in range(4):
      fillRectangle(50,y,1150,y + 5)
      y += 68.75
   #front posts
   fillRectangle(50,275,75,550)
   fillRectangle(1150,275,1175,550)
   # circle things
   fillCircle(1162.5,265,25)
   fillCircle(1262.5,165,25)
   fillCircle(162.5,165,25)
   fillCircle(62.5,265,25)
   
def beginningScene(backgroundColor, floorColor, ringColor, player1Color, player2Color):
   drawBackground(backgroundColor,floorColor)
   drawRinkPart1(ringColor)
   drawRobot(300,225,"right",player1Color)
   drawRobot(1000,225,"left",player2Color)
   drawRinkPart2(ringColor)
   setColor("white")
   
   scene()
   render()

def drawPlayerNames():
   setColor("white")
   drawString(player2Name,950,500,"Arial",20)
   drawString(player1Name,250,500,"Arial",20)
   delay(3000)
   clear()
   beginningScene()
