# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).


from prey import Prey


# from prey class  def __init__(self,x,y,width,height,angle,speed):
# each Ball is blue, has radius 5, moves at 5 pixels/second, and starts moving at a random angle.
#each Ball is blue,
#. Hint: 3 methods (__init__, update, and display),
class Ball(Prey):
    def __init__(self, x, y, r = 5):
        self.r = r
        d = r*2
        Prey.__init__(self, x, y, d, d, 0, 5)
        self.randomize_angle()
        
    def update(self, model):
        self.move()
        
    def display(self, canvas):
        r = self.r
        canvas.create_oval(self._x - r, self._y - r, 
                           self._x + r, self._y + r,
                           fill = 'blue')