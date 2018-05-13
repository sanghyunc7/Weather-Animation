#Dan Choi
from tkinter import *
from time import *
from math import *
from random import *
import colorsys
tk = Tk()
s = Canvas(tk, width=1600,height=600, background="black")
s.pack()

#background
buildingheight=[]
buildingwidth=[]
for i in range(7):
    buildingheight.append(randint(0,300))
    buildingwidth.append(randint(50,200))
    
environment=[]    
def buildings():
    for i in range(len(environment)):#this prevents the computer from looping through an array that could potentially grow very large
        s.delete(environment[i])
    ybottom=500
    #ground
    environment.append(s.create_rectangle(0,ybottom, 1600, 600, fill='black'))
    #building 
    for i in range(7):
  
        wallposition=i*200                      
        environment.append(s.create_line(wallposition, buildingheight[i], wallposition, ybottom, width=15))#left wall
        environment.append(s.create_line(wallposition+buildingwidth[i], buildingheight[i], wallposition+buildingwidth[i], ybottom, width=15))

        for x in range((500-buildingheight[i])//20):
            floor=buildingheight[i]+50*(x)
            environment.append(s.create_line(wallposition-7.5, floor, wallposition+buildingwidth[i]+7.5, floor, width=10))


#create tornado animation
numtclouds=500
ydif=1
xwidth=10
ywidth=10
topwidth=200
xoval=[]
yoval=[]
oval=[]
for i in range(numtclouds):
    xoval.append(xwidth) #tornado's tiny particles
    yoval.append(i*ydif)
    oval.append(0)
    

t=0
t1=0

def Tornado(): #make tornado animation
    global f, xmove, xpos, t, t1
    xmovement=60*cos(f)+xmove #move in irregular fashion in terms of x
    xmove+=5
    f+=0.3
    for i in range(numtclouds):
        xpos=20*sin(i*0.03+t1)+xmovement #swirly motion, in addition to xmovement
        x=(topwidth-topwidth*i/numtclouds)*sin(i+t)+xpos #inverse pyramidal shape-tornado
        oval[i]=(s.create_oval(x,yoval[i], x+xoval[i], yoval[i]+5, fill='black', outline=''))
    t+=0.1
    t1+=0.3
    s.update()
    sleep(0.03)
    for i in range(numtclouds):
        s.delete(oval[i])
        
#make lightning animation
class Stick:
        def __init__(self, x1, y1, x2, y2):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
        def addStick(self, xChange, yChange):#update old x,y with new x,y
            return Stick(self.x2, self.y2, self.x2 + xChange, self.y2 + yChange)
        def drawStick(self, lineWidth):#draw individual lightning paths
            return [s.create_line(self.x1, self.y1, self.x2, self.y2, fill='white', width=lineWidth)]
        def background(self):
            backgroundelement = []
            val=0
            hue=choice([0, 310, 300, 290, 280, 270, 260, 250, 240])/360
            sat = 1
            for i in range(500): #lightning flashes: colourful circles on top of larger darker ones
                rgb = colorsys.hsv_to_rgb(hue%1,sat,val)
                col = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*225), int(rgb[2]*225))
                backgroundelement.append(s.create_oval(self.x1-(500-i), self.y1-(500-i),self.x1+(500-i), self.y1+(600-i), fill=col, outline=''))
                val+=1/600 #colour turns to black
            buildings()
            s.update()
            return backgroundelement

class Lightning:
    def __init__(self):
        self.sticks = [] #for keeping track of where to make lightning paths/branches
        self.elements = [] #used to store graphics, then delete all of them in a loop
        self.lineWidth=7 #lightning width
    def createLightning(self):
        startx=randint(100,1500) #random starting point of lightning
        starty=randint(50,100)
        self.sticks.append([Stick(startx, starty, startx, starty)])
        for i in range(10):
            endSticks = self.sticks[-1]
            nextSticks = []
            for j in range(len(endSticks)):
                for k in range(choice([0, 0, 1, 1, 1, 1, 2, 2])):#random choice of whether current end will branch into 2, continue as one path, or stop 
                    nextStick = endSticks[j].addStick(randint(-100, 100), randint(10, 100)) #xchange between -100 and 100, but ychange must be between 20 and 100
                    nextSticks.append(nextStick) #the new end of the lightning's branch will be referenced to start a new branch on the next iteration 
            self.sticks.append(nextSticks) #organize the new branches into one package, then store in main array
    def drawLightning(self):
        self.elements.append(self.sticks[0][0].background())
        for i in range(len(self.sticks)):
            for j in range(len(self.sticks[i])):
                self.elements.append(self.sticks[i][j].drawStick(self.lineWidth))
        s.update()
    def deleteLightning(self):
        for i in range(len(self.elements)):
            for j in range(len(self.elements[i])):
                s.delete(self.elements[i][j])
        s.update()

def Storm():
    lightning = Lightning()
    lightning.createLightning()
    for f in range(2):
        lightning.drawLightning()
        Tornado()#such that tornado animation looks more smooth
        lightning.deleteLightning()
        sleep(0.03)
#make animation        
def Main():
    for i in range(100):    
        Storm()

print("Warning! May cause seizure from flashing light patterns!")
print("Viewer discretion is advised.") #backwards slash shows up as \
sleep(3)
      
while True:
    xpos=400#reset tornado position
    xmove=0
    f=0
    Main()



