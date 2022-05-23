#Home Page Library

from Graphics import *
from LevelsMenu import *

def drawHomeBackground():
   setBackground("blue")
   setColor("yellow") #stars
   for k in range(150):
      x = randint(0,1300)
      y = randint(0,700)
      fillRegularPolygon(x,y,5,4)
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
   drawString("<-- Back" ,62.5,65,"Arial",20)

def drawSkinsButton():
   setColor("white")
   fillRectangle(25,500,225,650) #skins button
   setColor("blue")
   drawString("Skins",50,600,"Arial",45) 

def drawSkinPage():
   setColor("green")
   fillRectangle(0,0,1300,700)
   enterSkinColor()

cubeColor = "firebrick"

def enterSkinColor():
   global cubeColor
   cubeColor = textinput("Player Color","Please enter cube color. ----->")
   cubeColor = cubeColor.lower()
   clear()

def drawQuestionsButton():
   setColor("white")
   fillRectangle(1050,500,1250,650) #questions button
   setColor("blue")
   drawString("?",1125,625,"Arial",60)

def drawQuestionPage():
   setColor("purple")
   fillRectangle(0,0,1300,700)
   setColor("white")
   drawString("Controls",450,200,"Arial",70)
   drawBackButton()
   y = 200
   sideLength = 50
   for k in range(4):
      y += sideLength + 10
      setColor("white")
      fillRegularPolygon(500,y,sideLength,4)
      setColor("purple")
      y += sideLength + 10
      fillRegularPolygon(500,y,sideLength,4)
   setColor("white")
   drawString("does this",600,280,"Arial",35)
   drawString("does this",600,400,"Arial",35)
   drawString("does this",600,520,"Arial",35)
   drawString("does this",600,640,"Arial",35)
      
def drawBackgroundColorsButton():   
   setColor("white")
   fillRectangle(540,500,740,650) #background button
   setColor("blue")
   drawString("Background",565,575,"Arial",20) 
   drawString("Colors",600,625,"Arial",20)
   
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
   elif inside(x,y,550,500,750,650): #background page
      clear()
      drawBackgroundColorPage()
      drawHomeBackground()
   elif inside(x,y,475,350,800,450): #play
      clear()
      drawLevels() 
   elif inside(x,y,100,100,300,300):
      drawLevel1()
   elif inside(x,y,400,100,600,300):
      drawLevel2()
   elif inside(x,y,700,100,900,300):
      drawLevel3()
   elif inside(x,y,1000,100,1200,300):
      drawLevel4()

def drawLevel1():
   clear()
   setBackground("green")
def drawLevel2():
   clear()
   setBackground("blue")
def drawLevel3():
   clear()
   setBackground("purple")
def drawLevel4():
   clear()
   setBackground("red")
