# Submitter: chuongd(Chuong, Derrick)

import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable=False):
    def show_listing(s):
        for i, l in enumerate(s.split('\n'),1):
            print('{num: >3} {txt}'.format(num = i, txt = l.rstrip()))


    # put your code here
    
    #check typename
    name = re.compile('^[a-zA-Z]+\w*$')
    #print(name.findall(str(type_name)))
    if name.findall(str(type_name)) == []:
        raise SyntaxError('invalid typename')

    #check field_name
    if not isinstance(field_names, str) and not isinstance(field_names, list):
        raise SyntaxError
    
    str_space = re.compile('\s*,?\s+|\s*')
    fields = []
    if isinstance(field_names, list):
        for field in field_names:
            if field in keyword.kwlist or name.findall(field) == []:
                raise SyntaxError
            fields.append(field)
            
    if isinstance(field_names, str):
        # this will return a list 
        temp = str_space.split(field_names)

        for field in temp:
            #print(field)
            #print(name.findall(field))
            if field in keyword.kwlist or name.findall(field) == []:
                raise SyntaxError
            fields.append(field)
   

    #print(fields)
    
    template = '''\
class {type_name}:
    def __init__(self, {value}):
        {self_args}
        self._fields = {fields}
        self._mutable = {check_mutable}
        
    def __repr__(self):
        return '{type_name}({repr_str})

    {accessor}
    '''
            
            
    getitem = '''
    def __getitem__(self, i):
        if i in self._fields:
            return eval('self.get_{arg}()'.format(arg = i))
        elif isinstance(i, int) and i < len(self._fields):
            return eval('self.get_{}()'.format(self._fields[i]))
        raise IndexError
      
    '''
    
    eq = '''
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        for field in self._fields:
            if self[field] != other[field]:
                return False
        return True
    
    '''
    
      #=========================================================================
      # def _replace(self,**kargs):
      #   ...check for all legal field names
      #   if self._mutable:
      #       ...
      #   else:
      #       ...
      #=========================================================================
    
    replace = '''
    def _replace(self, **kargs):
        for arg in kargs:
            if arg not in self._fields:
                raise TypeError
        if self._mutable:
            for arg in kargs:
                self.__dict__[arg] = kargs[arg]
        else:
            return eval({type_name})
            
            
    '''
    #if the mutable parameter is False, the named tuple will not allow any 
    #instance names to be changed: it will raise an AttributeError
    setattr = '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            if self._mutable == False:
                raise AttributeError
        self.__dict__[name] = value

    '''
    #def get_x(self):
    #    return self.x
    
    # __repr__ return 'Point(x={x},y={y})'.format(x=self.x,y=self.y)
    # bind class_definition (used below) to the string constructed for the class
    class_definition = template.format(type_name = type_name,
                                       value = ','.join(field for field in fields),
                                       self_args = '\n        '.join('self.' + field + ' = ' + field for field in fields),
                                       fields = fields, check_mutable = mutable,
                                       repr_str = ','.join('{x}={y}'.format(x = field, y = '{' + field+'}') for field in fields) + 
                                       ')\'.format(' + 
                                       ','.join('{x}=self.{x}'.format(x=field) for field in fields),
                                       accessor = '\n    '.join('def get_{field}(self):\n       return self.{field}'.format(field = field) for field in fields)
                                       )
    class_definition = class_definition + getitem + eq + replace + setattr


    # For initial debugging, always show the source code of the class
    #show_listing(class_definition)
    
    # Execute the class_definition string in a local namespace and bind the
    #   name source_code in its dictionary to the class_defintion; return the
    #   class object created; if there is a syntax error, list the class and
    #   show the error

    name_space = dict(__name__='pnamedtuple_{type_name}'.format(type_name=type_name))
    try:
        exec(class_definition, name_space)
        name_space[type_name].source_code = class_definition
    except(SyntaxError, TypeError):
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    import driver
    driver.driver()
