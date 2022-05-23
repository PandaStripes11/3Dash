#Home Page Library

from Graphics import *
from LevelsMenu import *
from Game import *
from copy import deepcopy

from threading import Thread
import winsound
def play_music():
    winsound.PlaySound("Kahoot.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

def drawHomeBackground():
   thread = Thread(target=play_music)
   thread.start()
   setBackground("cornflowerblue")
   setColor("gold") #stars
   for k in range(100):
      x = randint(0,1300)
      y = randint(0,700)
      fillStar(x,y,8,4)
   drawPlayButton()
   drawSkinsButton()
   drawQuestionsButton()
   drawBackgroundColorsButton()
   setColor("white")
   drawString("3-DASH",320,250,"Arial",120,"bold") #title
   
def drawBackButton():
   setColor("white")
   fillRectangle(50,25,175,75) #back button
   setColor("cornflowerblue")
   drawString("<= Back" ,62.5,65,"Arial",20)

def drawSkinsButton():
   setColor("white")
   fillRectangle(25,500,225,650) #skins button
   setColor("cornflowerblue")
   drawString("Skins",45,600,"Arial",45, "bold") 

def drawSkinPage():
   setColor("slateblue")
   fillRectangle(0,0,1300,700)
   enterSkinColor()

cubeColor = "cornflowerblue"

def enterSkinColor():
   global cubeColor
   cubeColor = textinput("Player Color","Please enter cube color. ----->")
   cubeColor = cubeColor.lower()
   clear()

def drawQuestionsButton():
   setColor("white")
   fillRectangle(1050,500,1250,650) #questions button
   setColor("cornflowerblue")
   drawString("?",1125,625,"Arial",60, "bold")

def drawQuestionPage():
   setColor("purple")
   fillRectangle(0,0,1300,700)
   setColor("white")
   drawString("Controls",150,200,"Arial",70)
   drawBackButton()
   y = 200
   sideLength = 50
   buttons = ["w", "a", "d", "space", "s"]
   for k in range(5):
      if k == 3: 
         setColor("white")
         fillRegularPolygon(675,255,sideLength,4)
         fillRegularPolygon(740,255,sideLength,4)
         setColor("black")
         drawString(buttons[3],650,280,"Arial",32,"bold")
      if k == 4:
         setColor("white")
         fillRegularPolygon(675,370,sideLength,4)
         setColor("black")
         drawString(buttons[k],665,390,"Arial",32,"bold")
   for k in range(3):
      y += sideLength + 5
      setColor("white")
      fillRegularPolygon(150,y,sideLength,4)
      setColor("black")
      drawString(buttons[k],140,y+20,"Arial", 32, "bold")
      setColor("purple")
      y += sideLength + 10
      fillRegularPolygon(500,y,sideLength,4)
   setColor("white")
   drawString("moves forward",200,280,"Arial",35)
   drawString("moves left",200,400,"Arial",35)
   drawString("moves right",200,520,"Arial",35)
   drawString("jumps",800,280,"Arial",35)
   drawString("hold to reset",720,395,"Arial",35)
      
def drawBackgroundColorsButton():   
   setColor("white")
   fillRectangle(425,500,850,650) #background button
   setColor("cornflowerblue")
   drawString("Backgrounds",447,600,"Arial",45,"bold") 
   
def drawBackgroundColorPage():
   setColor("slateblue")
   fillRectangle(0,0,1300,700)
   enterBackgroundColor()

backgroundColor = "white"
floorColor = "lightslategray"

def enterBackgroundColor():
   global backgroundColor
   global floorColor
   backgroundColor = textinput("Background","Please enter a background color. ----->" )
   floorColor = textinput(floor,"Please enter a floor color. ----->" )
   backgroundColor = backgroundColor.lower()
   floorColor = floorColor.lower()
   drawHomeBackground()

levelsMenuIsActive = False
completedLevels = [False]*8
def locate(x,y):
   global levelsMenuIsActive
   global completedLevels
   if inside(x,y,50,25,175,75): #back
      clear()
      drawHomeBackground()
   if not levelsMenuIsActive:
      if inside(x,y,25,500,225,650): #skin page
         clear()
         drawSkinPage()  
         drawHomeBackground()
      elif inside(x,y,1075,500,1275,650): #question page
         clear()
         drawQuestionPage()
      elif inside(x,y,450,500,850,650): #background page
         clear()
         drawBackgroundColorPage()
         drawHomeBackground()
      elif inside(x,y,475,350,800,450): #play
         clear()
         drawLevels(completedLevels) 
         drawBackButton()
         levelsMenuIsActive = True
   if levelsMenuIsActive:
      if inside(x,y,100,100,300,300):
         drawLevel(1)
      elif inside(x,y,400,100,600,300):
         drawLevel(2)
      elif inside(x,y,700,100,900,300):
         drawLevel(3)
      elif inside(x,y,1000,100,1200,300):
         drawLevel(4)
      elif inside(x,y,100,400,300,600):
         drawLevel(5)
      elif inside(x,y,400,400,600,600):
         drawLevel(6)
      elif inside(x,y,700,400,900,600):
         drawLevel(7)
      elif inside(x,y,1000,400,1200,600):
         drawLevel(8)

def drawLevel(level = 1):
   global completedLevels
   clear()
   render(level=level, playerColor=deepcopy(cubeColor), floorColor=deepcopy(floorColor), backgroundColor=deepcopy(backgroundColor))
   clear()
   completedLevels[level-1] = True
   drawLevels(completedLevels)
   drawBackButton()

onscreenclick(locate)
