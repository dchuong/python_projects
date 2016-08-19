import controller, sys
import model   #strange, but we need a reference to this module to pass this module to update

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
run = False
update = False
obj = None
simulation = set()
count = 0
#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global run, update, simulation, count
    run = False
    update = False
    simulation = set()
    count = 0


#start running the simulation
def start ():
    global run
    run = True


#stop running the simulation (freezing it)
def stop ():
    global run
    run = False


#The step button stops the simulation after executing one cycle: if it is running, it stops after one more cycle: if it is stopped it starts for one cycle and then stops again.
#step just one update in the simulation
def step ():
    global run
    global update
    run = True
    update = True


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global obj
    obj = kind
    
    
#add the kind of remembered object to the simulation (or remove any objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):

    try: 
        if obj == 'Remove':
            print('here')
            found = find(lambda a: a.contains( (x, y) ))
 
            for k in found:
                simulation.remove(k)
        else:
            pos = obj +'(' + str(x) + ',' + str(y) +')'
            simulation.add(eval(pos))
    except: 
        print('Choose an object')

            
#add simulton s to the simulation
def add(s):
    global simulation
    simulation.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    global simulation
    simulation.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    temp = set()
    for s in simulation:
        if p(s):
            temp.add(s)
    return temp


#call update for every simulton in the simulation
def update_all():
    global run
    global update
    global obj
    global simulation
    global count
    
    if run == True:
        count += 1
        temp = simulation.copy()
        for s in temp:
            s.update(model)
        if update == True:
            run = False
            update = False
            

#delete from the canvas every simulton in the simulation, and then call display for every
#  simulton in the simulation to add it back to the canvas possibly in a new location: to
#  animate it; also, update the progress label defined in the controller
def display_all():
    ##delete from the canvas every simulton in the simulation,
    for simulton in controller.the_canvas.find_all():
        controller.the_canvas.delete(simulton)
    
    #then call display for every simulton
    for ball in simulation:
        ball.display(controller.the_canvas)
        
    #  animate it; also, update the progress label defined in the controller
    #look for all derived class
    bnum= find(lambda x: isinstance(x, Ball))
    fnum = find(lambda x: isinstance(x, Floater))
    tot = len(bnum) + len(fnum)
    controller.the_progress.config(text =  str(count) + "cycles "  + str(tot) + "simultons"  )
    