# Submitter: chuongd(Chuong, Derrick)

# Define a special exception for use with the Graph class methods
# Use like any exception: e.g., raise GraphError('Graph.method...error indication...')
from _ast import Dict
from test.test_itertools import errfunc
from pip._vendor.requests.compat import basestring
 
class GraphError(Exception):
     # Inherit all methods, including __init__
    def __init__(self):
        pass
class Graph:

    # HELPER METHODS: used for checking legal arguments to methods below

    def legal_tuple2(self,t):
        return type(t) is tuple and len(t) == 2 and\
               type(t[0]) is str and type(t[1]) is str

    def legal_tuple3(self,t):
        return type(t) is tuple and len(t) == 3 and\
               type(t[0]) is str and type(t[1]) is str and self.is_legal_edge_value(t[2])
        
 
    # __str__ and many bsc tests use the name self.edges for the outer/inner-dict.
    # So __init__ should use self.edges for the name for this dictionary
    # self should store NO other attributes: compute all results from self.edges ONLY
    # Each value in the edges tuple can be either a 
    #   (a) str = origin node
    #   (b) 3-tuple = (origin node, destination node, edge value) 

    def __init__(self,legal_edge_value_predicate,*edges):
        self.edges = dict()
        self.is_legal_edge_value = legal_edge_value_predicate
        
        for e in edges:
            #if single value is int = wrong
            if isinstance(e,int):
                raise GraphError()          
            #if tuple and value doesn't match = wrong  
            if len(e) == 3 and not self.is_legal_edge_value(e[2]):
                raise GraphError()
            if isinstance(e, basestring) and len(e) == 1:
                #if it already exist in the dictionary
                if e[0] in self.edges:
                    raise GraphError()
                self.edges[e[0]] = {}
            if self.legal_tuple3(e):
                #key and dest already exist {a : {b :1}}
                if e[0] in self.edges and e[1] in self.edges.get(e[0]):
                    raise GraphError()
                if self.edges.get(e[1]) == None:
                    self.edges[e[1]] = {}
                if self.edges.get(e[0]) == None:
                    self.edges[e[0]] = {e[1]:e[2]}
                else:
                    self.edges[e[0]].update({e[1]:e[2]})
            if self.legal_tuple2(e):
                print('')
                raise GraphError()
        
    def get_legal_func(self):
        return self.is_legal_edge_value
    # Put all other methods here
    
    def __str__(self) -> 'string':
        temp_string = '\nGraph:'
        
        for k, v in sorted(self.edges.items()):
            count = 1
            if len(v) > 0 :
                temp_string = temp_string + '\n  '+ k + ': '
            else:
                temp_string = temp_string + '\n  ' + k + ':'
            for key ,value in sorted(v.items()):
                temp_string = temp_string + '{}({})'.format(key, value)
                if count != len(v):
                    temp_string = temp_string + ', '
                count += 1
        return temp_string
    
    def __getitem__(self, key) -> {'key : value'}:
        if isinstance(key, int):
            raise GraphError()
        if self.edges.get(key) != None:
            return self.edges[key]
        if len(key) == 2:
            if not isinstance(key[1], basestring):
                raise GraphError()
            inner_dict = self.edges.get(key[0])
            if inner_dict == None or inner_dict.get(key[1]) == None:
                raise GraphError()
            return inner_dict.get(key[1])
        raise GraphError()

    def __setitem__(self, key, item) -> '[key] = value':

        if  not self.is_legal_edge_value(item):
            raise GraphError()
        if self.edges.get(key[1]) == None:
            self.edges[key[1]] = {}
        if self.edges.get(key[0]) == None:
            self.edges[key[0]] = {key[1]:item}
        else:
            self.edges[key[0]].update({key[1]:item})
    
    def node_count(self):
        return len(self.edges)
    
    def __len__(self):
        count = 0
        for k , v in self.edges.items():
            for value in v.values():
                if len(v) != 0:
                    count +=1
        return count
    
    def out_degree(self, key):
        if not isinstance(key, basestring):
            raise GraphError()
        if key not in self.edges:
            raise GraphError()
        return len(self.edges[key])
    
    def in_degree(self, key):
        if key not in self.edges:
            raise GraphError()
        if not isinstance(key,basestring):
            raise GraphError()
        count = 0
        for v in self.edges.values():
            if key in v:
                count += 1
        return count
    
    def __contains__(self, item):
        if isinstance(item, basestring):
            if item in self.edges:
                return True
            else:
                return False
        if self.legal_tuple2(item):
            if self.edges.get(item[0]).get(item[1]):
                return True
            else:
                return False
        if self.legal_tuple3(item):
            if self.edges.get(item[0]).get(item[1]) == item[2]:
                return True
            else:
                return False
        raise GraphError()
    
    def __delitem__(self, item):
        if isinstance(item, basestring):
            if item in self.edges:
                del self.edges[item]
                #print(self.edges)
                for k, v in self.edges.items():
                    if item in v:
                        self.edges[k].pop(item,0)
            return
        if self.legal_tuple2(item):
            if self.edges.get(item[0]).get(item[1]):
                del self.edges[item[0]][item[1]]
        else:
            raise GraphError()
    
    def __call__(self, item):
        if self.legal_tuple2(item):
            raise GraphError()
        if self.edges.get(item) == None:
            raise GraphError()
        answer_dict = {}
        for k, v in self.edges.items():
            if item in v:
                answer_dict.update({k: v[item]})
        return answer_dict
        
    def clear(self):
        self.edges.clear()
        
    def dump(self,file,*spacing):
        variable = list(spacing)
        spacing = variable[0]
        temp_string = ''
        for k,v in sorted(self.edges.items()):
            temp_string += k
            for key, value in sorted(v.items()):
                if len(variable) == 2:
                    temp_string += spacing + key + spacing + variable[1](value)
                else:
                    temp_string += spacing + key + spacing + str(value)
            temp_string += "\n"
        file.write(temp_string)
        file.close()
    
    def load(self, file, spacing, func):
        for line in file:
            parse = line.strip().split(spacing)
            key = parse.pop(0)
            conv = [func(x) for x in parse[1::2]]
            self.edges.update({key : dict(zip(parse[::2],conv))})
        
    def reverse(self):
        temp = {}
        for k, v in self.edges.items():
            if k not in temp:
                temp[k] = {}
            for key, value in v.items():
                if temp.get(key) == None: 
                    temp[key] = {k: value}
                else:
                    temp[key].update({k : value})
        x = Graph(self.get_legal_func())
        x.edges = temp
        return x
            
    def natural_subgraph(self, *str):
            my_list = list(str)
            temp = {}
            #check if there is any invalid input and create node w/ empty dict
            for node in my_list:
                if not isinstance(node, basestring):
                    raise GraphError()
                if node in self.edges:
                    temp.update({node : {}})
            #go through and update the edges
            for k, v in self.edges.items():
                for key,value in v.items():
                    if key in temp and k in temp:
                        temp[k].update({key : value})
            x = Graph(self.get_legal_func())
            x.edges = temp
            return x
        
    def __iter__(self):
        list = []
        for k, v in sorted(self.edges.items()):
            bool = False
            for key , value in sorted(v.items()):
                list.append((k,key,value))
                yield (k,key,value)
            for tuple in list:
                if k in tuple:
                    bool = True
            if bool == False:
                yield k
    
    def __eq__(self, other):
        return self.edges == other.edges
    
    def __ne__(self,other):
        return not self.edges == other.edges
    
    def __le__(self,other):
        for k, v in self.edges.items():
            if k not in other.edges:
                return False
            for key, value in v.items():
                if key not in other.edges[k]:
                    return False
                if self.edges[k].get(key) > other.edges[k].get(key):
                    return False
        return True
    
    #g['a','b'] = 1
    def __add__(self, item):
        check_case = isinstance(item, basestring) or isinstance(item, tuple) or isinstance(item, Graph)
        if not check_case:
            raise GraphError
        
        x = Graph(self.get_legal_func())
        #deep copy 
        for k,v in self.edges.items():
            x.edges.update({k: {}})
            for key, value in v.items():
                x.edges[k].update({key : value})
        if isinstance(item,basestring):
            x.edges.update({item: {}})
        elif isinstance(item, tuple):
            if not x.is_legal_edge_value(item[2]):
                raise GraphError
            if item[0] in x.edges:
                x.edges[item[0]].update({item[1] : item[2]})
            if item[1] not in x.edges:
                x.edges.update({item[1] : {}})
        elif isinstance(item, Graph):
            for k,v in item.edges.items():
                if len(v) == 0 and k not in self.edges:
                    x.edges[k]= {}
                else:
                    for key,value in v.items():
                        x[k,key] = value
        return x

    def __radd__(self, left):
        return self.__add__(left)

    def __iadd__(self, item):
        return self.__add__(item)
        
    def __setattr__(self,item,value):
        if item == 'edges' or item == 'is_legal_edge_value':
            self.__dict__[item] = value
                
        else:
            raise AssertionError
       

            
if __name__ == '__main__':
    #Put code here to test Graph before doing bsc test; for example
    g = Graph( (lambda x : type(x) is int), ('a','b',1),('a','c',3),('b','a',2),('d','b',2),('d','c',1),'e')
    print(g)
    print(g['a'])
    print(g['a','b'])
    print(g.node_count())
    print(len(g))
    print(g.out_degree('c'))
    print(g.in_degree('a'))
    print('c' in g)
    print(('a','b') in g)
    print(('a','b',1) in g)
    print(g('c'))
    print(g.reverse())
    print(g.natural_subgraph('a','b','c'))
    print()    
    import driver
    #Uncomment the following lines to see MORE details on exceptions
    driver.default_file_name = 'bsc1.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
