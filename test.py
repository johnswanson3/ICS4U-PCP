"""
***************************************************************************
filename:       mixtape_jump.py
description:    A side scrolling game where the player (mixtape) must navigate through rappers and achieve a high score!
Author:         Wei.K, Miyata.Y, Han.J
Created On:     06/13/2016
***************************************************************************
"""
import kivy
kivy.require('1.7.2')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Canvas
from random import *

#Background color (Black)
Window.clearcolor = (0,0,0,1.)

class WidgetDrawer(Widget):
#This widget is used to draw all of the objects on the screen
#This initializes widget movement, size, positioning
#objects of this class must be initiated with an image string
#with asterisks, Kwargs allow to pass all arguments without needing its parameters
    def __init__(self, imageStr, **kwargs):
        super(WidgetDrawer, self).__init__(**kwargs) #this is part of the **kwargs notation
#if you haven't seen with before, here's a link http://effbot.org/zone/python-with-statement.html
        with self.canvas:
#this line creates a rectangle with the image drawn on top
            self.size = (Window.width*.005*25,Window.height*.005*25)
            self.rect_bg= Rectangle(source=imageStr,pos=self.pos,size = self.size)
#this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
#center the widget
            self.pos = (self.x,self.y)
#center the rectangle on the widget
            self.rect_bg.pos = self.pos

    def update_graphics_pos(self, instance, value):
#if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value
#use this function to change widget size
    def setSize(self,width, height):
        self.size = (width, height)
    def setPos(self,xpos,ypos):
        self.x = xpos
        self.y = ypos


class rapper(WidgetDrawer):
    #rapper class. The flappy mixtape will dodge these
    velocity_x = NumericProperty(0) #initialize velocity_x and velocity_y
    velocity_y = NumericProperty(0) #declaring variables is not necessary in python
 #update the position using the velocity defined here. every time move is called we change the position by velocity_x
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
    def update(self):
#the update function moves the astreoid. Other things could happen here as well (speed changes for example)
        self.move()


class mixtape(WidgetDrawer):
    #mixtape class. This is for the main mixtape object.
    #velocity of mixtape on x/y axis
    def __init__(self, imageStr) :
        WidgetDrawer.__init__(self, imageStr)
        self.impulse = 3 #this variable will be used to move the mixtape up
        self.grav = -0.1 #this variable will be used to pull the mixtape down

        self.velocity_x = 0 #we wont actually use x movement
        self.velocity_y = 0

        self.setSize(50, 30)

    def setSize (self, width, height):
        WidgetDrawer.setSize(self, width, height)

    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

        #don't let the mixtape go too far
        if self.y > Window.height*0.95: #don't let the mixtape go up too high
            self.impulse = -3

    def determineVelocity(self):
        #move the mixtape up and down
        #we need to take into account our acceleration
        #also want to look at gravity
        self.grav = self.grav*1.05  #the gravitational velocity should increase
        #set a grav limit
        if self.grav < -4: #set a maximum falling down speed (terminal velocity)
            self.grav = -4
        #the mixtape has a propety called self.impulse which is updated
        #whenever the player touches, pushing the mixtape up
        #use this impulse to determine the mixtape velocity
        #also decrease the magnitude of the impulse each time its used

        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95*self.impulse #make the upward velocity decay

    def update(self):
        self.determineVelocity() #first figure out the new velocity
        self.move()              #now move the mixtape


class MyButton(Button):
    #class used to get uniform button styles
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
 #all we're doing is setting the font size. more can be done later
        self.font_size = Window.width*0.018


class GUI(Widget):
    #this is the main widget that contains the game.
    rapperList =[] #use this to keep track of rappers
    rapperScore = NumericProperty(0)
    minProb = 1780 #this variable used in spawning rappers
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.score = Label(text = "0")
        self.score.y = Window.height*0.8
        self.score.x = Window.width*0.2
        self.rapperScore = 0
        l = Label(text='Mixtape Jump') #give the game a title
        l.x = Window.width/2 - l.width/2
        l.y = Window.height*0.8
        self.add_widget(l) #add the label to the screen

        #now we create a mixtape object
 #notice how we specify the mixtape image
        self.mixtape = mixtape(imageStr = 'C:\Users\Koven\desktop\photoshopped\mmixtape.png')
        self.mixtape.x = Window.width/4
        self.mixtape.y = Window.height/2
        self.add_widget(self.mixtape)


        def check_score(self,obj):
            #update credits
            self.score.text = str(self.rapperScore)

        self.bind(rapperScore = check_score)
        self.add_widget(self.score)


    def addrapper(self):
        #add an rapper to the screen
        #self.rapper
        imageNumber = randint(1,7)
        imageStr = ('C:\Users\Koven\desktop\photoshopped\image'+str(imageNumber)+'.png')
        tmprapper = rapper(imageStr)
        tmprapper.x = Window.width*0.99
        #randomize y position
        ypos = randint(2,25)
        ypos = ypos*Window.height*.0625
        tmprapper.y = ypos
        tmprapper.velocity_y = 0
        vel = 10
        tmprapper.velocity_x = -0.1*vel
        self.rapperList.append(tmprapper)
        self.add_widget(tmprapper)

    #handle input events
    #kivy has a great event handler. the on_touch_down function is already recognized
    #and doesn't need t obe setup. Every time the screen is touched, the on_touch_down function is called
    def on_touch_down(self, touch):
        self.mixtape.impulse = 3 #give the mixtape an impulse
        self.mixtape.grav = -0.1 #reset the gravitational velocity

    def gameOver(self): #this function is called when the game ends
        #add a restart button
        restartButton = MyButton(text='Press to Restart, your score was ' + str(self.rapperScore))
        def restart_button(obj):
        #this function will be called whenever the reset button is pushed
            print 'restart button pushed'
            #reset game
            for k in self.rapperList:
                self.remove_widget(k)
                self.mixtape.xpos = Window.width*0.25
                self.mixtape.ypos = Window.height*0.5
                self.minProb = 1780
            self.rapperList = []

            self.parent.remove_widget(restartButton)
            #stop the game clock in case it hasn't already been stopped
            Clock.unschedule(self.update)
            #start the game clock
            Clock.schedule_interval(self.update, 1.0/60.0)
        restartButton.size = (Window.width*.3,Window.width*.1)
        restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.5
        #bind the button using the built-in on_release event
        #whenever the button is released, the restart_button function is called
        restartButton.bind(on_release=restart_button)

        #*** It's important that the parent get the button so you can click on it
        #otherwise you can't click through the main game's canvas
        self.parent.add_widget(restartButton)


    def update(self,dt):
        #This update function is the main update function for the game
        #All of the game logic has its origin here
        #events are setup here as well
        #update game objects
        #update mixtape
        self.mixtape.update()
        #update rappers
        #randomly add an rapper
        tmpCount = randint(1,1800)
        print self.minProb
        if tmpCount > self.minProb:
            self.addrapper()
            self.minProb = self.minProb - 0.10
        if self.minProb <= 1750:
            self.minProb = self.minProb + 0.1
        if self.mixtape.y < Window.height * 0.001:
            self.mixtape.impulse = 10
        for k in self.rapperList:
            #check for collision with mixtape
            if k.collide_widget(self.mixtape):
                print 'death'
                #game over routine
                self.gameOver()
                Clock.unschedule(self.update)
                self.rapperScore = 0
                #add reset button
            if k.x < -100:
                self.remove_widget(k)
                self.rapperScore += 1
                tmpRapperList = self.rapperList
                tmpRapperList[:] = [x for x in tmpRapperList if (x.x > - 100)]
                self.RapperList = tmpRapperList
            k.update()

class ClientApp(App):

    def build(self):
        #this is where the root widget goes
        #should be a canvas
        parent = Widget() #this is an empty holder for buttons, etc
        app = GUI()
        #Start the game clock (runs update function once every (1/60) seconds
        Clock.schedule_interval(app.update, 1.0/60.0)
        parent.add_widget(app) #use this hierarchy to make it easy to deal w/buttons
        return parent

if __name__ == '__main__' :
    ClientApp().run()