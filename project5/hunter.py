# A Hunter is both a Mobile_Simulton and a Pulsator; it updates
#   like a Pulsator, but it also moves (either in a straight line
#   or in pursuit of Prey), and displays as a Pulsator.


from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from prey import Prey
from math import atan2
from pip import locations

#Each Hunter behaves and initially looks like a Pulsator, except for the following additional behavior.
class Hunter(Pulsator,Mobile_Simulton):
    #moves at 5 pixels/second, 
    #Use the find method in the model module to locate all objects that are instance of Prey 
    #(or any of its subclasses no matter how many are added later) and whose locations are within a distance of 200 
    def __init__(self, x , y , r = 10, d = 200):
        self.d = d
        Pulsator.__init__(self, x, y, r)
        w, h = self.get_dimension()
        Mobile_Simulton.__init__(self, x, y, w, h, 0, 5)
        self.randomize_angle()
        
    def update(self, model):
        newset = Pulsator.update(self, model)
        #if any are seen, find the closest one and set the hunter's angle to point at that simulton: to hunt it. 
        #find/return a set of simultons that each satisfy predicate p    
        find = model.find(lambda x: self.distance(x.get_location()) < 200 and isinstance(x, Prey))
        if find:
            temp = []
            for s in find:
                #temp = list(find)
                #print(temp)
                # need distance and the ball object relate to it
                temp.append( 
                            ( s , self.distance(s.get_location()) ) 
                            )
                temp = sorted(temp, key = lambda x: x[1])

                nmex, nmey = temp[0][0].get_location()
                huntx,hunty = self.get_location()
                self.set_angle( atan2(nmey - hunty, nmex - huntx)     )
            
        self.move()
        return newset
            #find the closest one and set the hunter's angle to point at that simulton: to hunt it. 
                
            #just call the math.atan2 function (with these differences as separate arguments)
            # to determine the angle the Hunter should move to head towards the prey.
            # By using math.atan2 and avoiding the division, 
        