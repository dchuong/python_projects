# Submitter: chuongd(Chuong, Derrick)

from goody import type_as_str
import inspect
from types import LambdaType

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # set name to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Decode the annotation and check it 
        
        def c_inner():
            if len(annot) == 1:
                for val in value:
                    self.check(param, annot[0], val, check_history)
            else:
                if not len(annot) == len(value):
                    assert False
          
                for i in range(len(annot)):
                    self.check(param, annot[i], value[i], check_history)
                    
        def c_dict():
            if len(annot) == 1:
                for key in value:
                    #print(key, value[key])
                    self.check(param, annot, key, check_history)
            else:
                raise AssertionError
        
        #value is not a set
        #annot has more than one value: this is actually a bad/illegal annotation, not a failed annotation
        #annot has one value, and any value in the value set fails the value-annotation check
        def c_set():
            if len(annot) == 1:
                for anno in annot:
                    continue
                for val in value:
                    self.check(param, anno, val, check_history)
            else:
                raise AssertionError
            
        
        if annot is None:
            pass
        elif isinstance(annot, type):
            assert isinstance(value, annot)
        elif isinstance(annot, list):
            assert isinstance(value, list)
            c_inner()
        elif isinstance(annot, tuple):
            assert isinstance(value, tuple)    
            c_inner()
        elif isinstance(annot, dict):
            assert isinstance(value, dict)
            c_dict()
        elif isinstance(annot, set):
            assert isinstance(value, set)
            c_set()
        elif isinstance(annot, frozenset):
            assert isinstance(value, frozenset)
            c_set()
        elif isinstance(annot, LambdaType):
            #we can determine the number of parameters in a function/lambda object 
            #by accessing its __code__.co_varnames attribute.
            assert len(annot.__code__.co_varnames) == 1
            try:
                annot(value)
            except:
                raise AssertionError
            assert annot(value)
        #annot is a class whose __check_annotation__ method is called (test by using Check_All_OK/Check_Any_OK)
        else:
            #There is no __check_annotation__ method in the class: e.g., 
            #calling the __check_annotation__ method raises the AttributeError 
            #exception (the object was not constructed from a class that supports the annotation checking protocol):
            # this is actually a bad/illegal annotation, not a failed annotation
            #calling its __check_annotation__ method fails
            #calling its __check_annotation__ method raises any other exception
        
            try:
                #__check_annotation__(self, check, param, value, check_history):
                self.__check_annotation__(self.check, param, value, check_history)
            except:
                raise AssertionError
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        if not (self.checking_on and Check_Annotation.checking_on):
            return self._f(*args, **kargs)
        
        self._parameters = param_arg_bindings()
        anno = self._f.__annotations__
        
        try:
            # Check the annotation for every parameter (if there is one)
            for p in self._parameters:
                if p in anno:
                    self.check(p, anno[p], self._parameters[p])        
            # Compute/remember the value of the decorated function
            dec_v = self._f(*args, **kargs)
            
            if 'return' in anno:
                self.check('return', anno['return'], dec_v)
            return dec_v
            # If 'return' is in the annotation, check it
            
            # Return the decorated answer
            
            #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #    print(l.rstrip())
            #print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
   # def f(x:int): pass
    #f = Check_Annotation(f)
   # f(3)
    #f('a')
           
    import driver
    driver.driver()
