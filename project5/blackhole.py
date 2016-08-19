# A Black_Hole is a Simulton; it updates by removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey

#simulton def __init__(self,x,y,width,height):
#s (__init__, update, display), and contains)
class Black_Hole(Simulton):
    #Each Black_Hole is black and has a radius of 10.
    def __init__(self, x, y, r = 10):
        self.r = r
        d = r * 2
        Simulton.__init__(self, x, y, d, d)
        
    # Black_Hole to the center of the object is less than the radius
    # of the Black_Hole. 
    # and whose locations are contained in the circle representing the Black_Hole.
    def update (self , model):
        # Use the find method in the model module to locate all
        # objects that are instances of Prey (or any of its subclasses no matter how many are added later)
        check = model.find (lambda x: self.contains(x.get_location()) and isinstance(x, Prey))
        newset = set()
        for obj in check:
            if  self.contains(obj.get_location()):
                newset.add(obj)
                model.remove(obj)
        return newset
    
     #The update method should return the set of simultons eaten: 
     #this information will be useful when inherited from the Pulsator class (which extends the Black_Hole class). 
     #
    def display(self, the_canvas):  
        w,h = self.get_dimension()
        wrad = w/2
        hrad = h/2
        x = self._x
        y = self._y
        the_canvas.create_oval(x - wrad, y  - hrad,
                               x + wrad, y + hrad, 
                               fill = 'black')
    
    #Override the contains method so that a point is contained in the Black_Hole if the distance from the 
    #center of the Black_Hole to the center of the object is less than the radius of the Black_Hole.
    def contains (self, xy):
        w,h = self.get_dimension()
        return self.distance(xy) < w/2
    
           
        
        