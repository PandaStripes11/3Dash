from Graphics import *
from Setting import *
from Robots import *

beginGrfx(1300,700)

def drawPlayButton():
   setColor("red")
   fillRectangle(475,350,800,450) #play button
   setColor("yellow")
   drawString("PLAY!",525,450,"Arial",60)
   
def drawBackButton():
   setColor("white")
   fillRectangle(50,25,175,75) #back button
   setColor("black")
   drawString("<-- Back" ,62.5,65,"Arial",20)

def drawSkinsButton():
   setColor("red")
   fillRectangle(25,500,225,650) #skins button
   setColor("yellow")
   drawString("Skins",50,600,"Arial",45) 

def drawQuestionsButton():
   setColor("red")
   fillRectangle(1050,500,1250,650) #questions button
   setColor("yellow")
   drawString("?",1125,625,"Arial",60)

def drawNamesButton():
   setColor("red")
   fillRectangle(25,325,225,475) #names button
   setColor("yellow")
   drawString("Player", 50,412.5,"Arial",30) 
   drawString("Names", 50,450,"Arial",30)
   
def drawBackgroundColorsButton():   
   setColor("red")
   fillRectangle(1050,325,1250,475) #background button
   setColor("yellow")
   drawString("Background",1075,400,"Arial",20) 
   drawString("Colors",1075,450,"Arial",20)

player1Color = "firebrick"
player2Color = "blue"

def enterSkinColor():
   global player1Color
   global player2Color
   player1Color = textinput(player1Name,"Please enter robot color. ----->")      
   player2Color = textinput(player2Name,"Please enter robot color. ----->")
   player1Color = player1Color.lower()
   player2Color = player2Color.lower()
   
player1Name = "Player 1"
player2Name = "Player 2"

def enterPlayerNames():
   global player1Name
   global player2Name
   player1Name = textinput(player1Name,"Please enter your name. ----->")      
   player2Name = textinput(player2Name,"Please enter your name. ----->")
   
backgroundColor = "light blue"
floorColor = "dark blue"
ringColor = "yellow"

def enterBackgroundColor():
   global backgroundColor
   global floorColor
   global ringColor
   backgroundColor = textinput("Background","Please enter a background color. ----->" )
   floorColor = textinput(floor,"Please enter a floor color. ----->" )
   ringColor = textinput(floor,"Please enter a ring color. ----->" )
   backgroundColor = backgroundColor.lower()
   floorColor = floorColor.lower()
   ringColor = ringColor.lower()
   
def drawSkinPage():
   setColor("green")
   fillRectangle(0,0,1300,700)
   enterSkinColor()

def drawNamePage():
   setColor("red")
   fillRectangle(0,0,1300,700)
   enterPlayerNames()

def drawBackgroundColorPage():
   setColor("orange")
   fillRectangle(0,0,1300,700)
   enterBackgroundColor()

def drawQuestionPage():
   setColor("purple")
   fillRectangle(0,0,1300,700)
   setColor("yellow")
   drawString("Controls",200,150,"Arial",70)
   drawBackButton()
   
def drawHomeBackground():
   setBackground("dark blue")
   setColor("yellow") #stars
   for k in range(50):
      x = randint(0,1300)
      y = randint(0,700)
      fillStar(x,y,20,5)
   drawRobot(100,50,"right")
   drawRobot(1200,50,"left","blue")
   drawPlayButton()
   drawSkinsButton()
   drawQuestionsButton()
   drawNamesButton()  
   drawBackgroundColorsButton()
   drawString("Game Name",320,225,"Arial",90) #title

def displayPlayerNames():
   drawString(player2Name,950,500,"Arial",20)
   drawString(player1Name,250,500,"Arial",20)
   delay(3000)
   clear()
   drawBackground(backgroundColor,floorColor)
   drawRinkPart1(ringColor)
   drawRobot(300,225,"right",player1Color)
   drawRobot(1000,225,"left",player2Color)
   drawRinkPart2(ringColor)   
   drawBackButton()
  
def locate(x,y):
   if inside(x,y,25,500,225,650): #skin page
      clear()
      drawSkinPage()  
      drawHomeBackground()
   elif inside(x,y,1075,500,1275,650): #question page
      clear()
      drawQuestionPage()
   elif inside(x,y,50,25,175,75): #back
      clear()
      drawHomeBackground()
   elif inside(x,y,475,350,800,450): #play
      clear()
      print(backgroundColor, floorColor, ringColor, player1Color, player2Color)
      beginningScene(backgroundColor, floorColor, ringColor, player1Color, player2Color)
      drawBackButton()
      displayPlayerNames()      
   elif inside(x,y,25,325,225,475): #name page
      clear()
      drawNamePage()
      drawHomeBackground()
   elif inside(x,y,1050,325,1250,475): #background/floor page
      clear()
      drawBackgroundColorPage()
      drawHomeBackground()

      

drawHomeBackground()
onscreenclick(locate)
endGrfx()
