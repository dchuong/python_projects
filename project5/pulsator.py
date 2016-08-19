# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


# For every object a Pulsator eats, its dimension (both width and length)
# grows by 1 and its "time between meals" counter is reset; whenever it is goes 30 
#updates without eating anything, its dimension (both width and length) shrinks by 1; 
#and if the dimesions ever shrink to 0, the object starves and removes itself from the simulation.
class Pulsator(Black_Hole):
    # Each Pulsator behaves and initially looks like a Black_Hole
    def __init__ (self, x, y, r = 10):
        self.num = 0
        self.r = r
        Black_Hole.__init__(self, x , y)
        
        
    def update(self, model):
        newset = Black_Hole.update(self, model)
        self.num += 1
        # (both width and length) grows by 1 and its "time between meals" counter is reset; whenever it is goes 30 
        if newset:
            self.num = 0
            length = len(newset)
            self.change_dimension(length, length)
            
        elif self.num == 30:
            self.num = 0
            #whenever it is goes 30 
            #updates without eating anything, its dimension (both width and length) shrinks by 1;
            self.change_dimension(-1, -1)
            ##and if the dimesions ever shrink to 0, the object starves and removes itself from the simulation.
            w,h = self.get_dimension()
            if w == 0 and h ==0:
                model.remove(self)

            
        return newset