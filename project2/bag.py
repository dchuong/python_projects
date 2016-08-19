# Submitter: chuongd(Chuong, Derrick)

from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, *list):
    
        self.bag = defaultdict(int) 
        if len(list) != 0:
            for v in list[0]:
                self.bag[v] += 1

    #'\''+v+'\'')
    def __repr__(self):
        temp = 'Bag('
        for k in self.bag:
            for i in range(0, self.bag[k]):
                temp += '\''+  k +'\'' + ','
        if len(self.bag) != 0:
            temp = temp[:-1]
        temp += ')'
        return temp
    

    def __str__(self):
        temp = 'Bag('
        for k,v in sorted(self.bag.items()):
            temp += k +'[' + str(v) +']'
        return temp + ')' 
        
    def __len__(self):
        count = 0
        for k, v in self.bag.items():
            count += v
        return count
    
    def unique(self):
        return len(self.bag)

    def add(self,item):
        self.bag[item] += 1
    
    def __contains__(self, item):
        return item in self.bag

    def count (self, item):
        if item in self.bag:
            return self.bag[item]
        else:
            return 0
    
    def __add__(self, obj):
        if not isinstance(obj, Bag):
            raise TypeError
        temp_bag = Bag()
        for k, v in obj.bag.items():
            temp_bag.bag[k] += v
        for k ,v in self.bag.items():
            temp_bag.bag[k] += v
     
        return temp_bag
       
    def remove(self, item):
        if item in self.bag:
            if self.bag[item] == 1:
                del self.bag[item]
            else:
                self.bag[item] -= 1
        else:
            raise ValueError
    
    def __eq__(self, obj):
        if not isinstance(obj, Bag):
            return False
        for k, v in self.bag.items():
            if k in obj:
                if self.bag[k] != obj.bag[k]:
                    return False
            else:
                return False
        
        return True
    
    def __ne__(self,obj):
        return not self.__eq__(obj)
    
    def __iter__(self):
        for x in self.bag:
            for num in range(0, self.bag[x]):
                yield x
     #   print(new_bag)
        return self
if __name__ == '__main__':
    b = Bag(['d','a','b','d','c','b','d'])

    i = iter(b)
    print([i for i in sorted(b)])
    b.add('d')
    b.remove('a')
    print([i for i in sorted(b)])
    print([i for i in sorted(x for x in i)])
    #driver tests
    import driver
    driver.default_file_name = 'bsc2.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
