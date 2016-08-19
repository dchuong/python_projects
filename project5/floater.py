# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


#
#from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


#they are displayed as images (a UFO icon) and they move in a strange way. Ensure the user can add
#Floaters to the simulation. Initially, each Floater moves at 5 pixels/second, and is moving at a random angle.
class Floater(Prey):
    def __init__(self, x , y , r = 5):
        self.r = r
        Prey.__init__(self, x, y, r* 2, r* 2, 0 , 5)
        self.randomize_angle()
    
    # 30% chance to change 
    #The speed is changed by a random value betwen -.5 and +.5, 
    #but never drops below 3 pixels/update or rises above 7 pixels/update;
    # and the angle is changed by a random value betwen -.5 and +.5 radians.

    def update(self, model):
        chance = random() - 0.1
        if 0 <= chance <= 0.3:
            #random return  0 <= n <     1.0.
            randomSpeed = random() - 0.5
            speed = self.get_speed() + randomSpeed
            while speed < 3 or speed > 7 :
                randomSpeed = random() - 0.5
                speed = self.get_speed() + randomSpeed
            angle = self.get_angle() + (random() -0.5)
            self.set_velocity(speed, angle)
        self.move()
        
    #using a radius 5, but as red circles; you might want to implement floaters this way first
    def display(self,canvas):
        r = self.r
        canvas.create_oval(self._x - r, self._y - r, 
                           self._x + r, self._y + r,
                            fill = 'red')