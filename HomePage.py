#Home Page Library

from Graphics import *
from LevelsMenu import *
from Game import *

def drawHomeBackground():
   setBackground("blue")
   setColor("yellow") #stars
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
   setColor("blue")
   drawString("<= Back" ,62.5,65,"Arial",20)

def drawSkinsButton():
   setColor("white")
   fillRectangle(25,500,225,650) #skins button
   setColor("blue")
   drawString("Skins",45,600,"Arial",45, "bold") 

def drawSkinPage():
   setColor("green")
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
   setColor("blue")
   drawString("?",1125,625,"Arial",60, "bold")

def drawQuestionPage():
   setColor("purple")
   fillRectangle(0,0,1300,700)
   setColor("white")
   drawString("Controls",450,200,"Arial",70)
   drawBackButton()
   y = 200
   sideLength = 50
   buttons = ["w", "a", "d", "space"]
   for k in range(4):
      y += sideLength + 10
      setColor("white")
      fillRegularPolygon(500,y,sideLength,4)
      if k == 3: fillRectangle(480,y+23,625,y-36)
      setColor("black")
      drawString(buttons[k],487,y+17,"Arial", 32, "bold")
      setColor("purple")
      y += sideLength + 10
      fillRegularPolygon(500,y,sideLength,4)
   setColor("white")
   drawString("moves forward",600,280,"Arial",35)
   drawString("moves left",600,400,"Arial",35)
   drawString("moves right",600,520,"Arial",35)
   drawString("jumps",675,640,"Arial",35)
      
def drawBackgroundColorsButton():   
   setColor("white")
   fillRectangle(425,500,850,650) #background button
   setColor("blue")
   drawString("Backgrounds",447,600,"Arial",45,"bold") 
   
def drawBackgroundColorPage():
   setColor("orange")
   fillRectangle(0,0,1300,700)
   enterBackgroundColor()

backgroundColor = "white"
floorColor = "grey"

def enterBackgroundColor():
   global backgroundColor
   global floorColor
   backgroundColor = textinput("Background","Please enter a background color. ----->" )
   floorColor = textinput(floor,"Please enter a floor color. ----->" )
   backgroundColor = backgroundColor.lower()
   floorColor = floorColor.lower()
   drawHomeBackground()

levelsMenuIsActive = False
def locate(x,y):
   global levelsMenuIsActive
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
   elif inside(x,y,450,500,850,650): #background page
      clear()
      drawBackgroundColorPage()
      drawHomeBackground()
   elif inside(x,y,475,350,800,450): #play
      clear()
      drawLevels() 
      drawBackButton()
      levelsMenuIsActive = True
   elif inside(x,y,100,100,300,300) and levelsMenuIsActive:
      drawLevel1()
   elif inside(x,y,400,100,600,300) and levelsMenuIsActive:
      drawLevel2()
   elif inside(x,y,700,100,900,300) and levelsMenuIsActive:
      drawLevel3()
   elif inside(x,y,1000,100,1200,300) and levelsMenuIsActive:
      drawLevel4()

def drawLevel1():
   clear()
   render(scene, cubeColor)
   clear()
   drawLevels()
   drawBackButton()
def drawLevel2():
   clear()
   render(scene, cubeColor)
   clear()
   drawLevels()
   drawBackButton()
def drawLevel3():
   clear()
   render(scene, cubeColor)
   clear()
   drawLevels()
   drawBackButton()
def drawLevel4():
   clear()
   render(scene, cubeColor)
   clear()
   drawLevels()
   drawBackButton()

onscreenclick(locate)
