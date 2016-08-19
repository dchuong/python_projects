# Submitter: chuongd(Chuong, Derrick)

# Generators must be able to iterate through any iterable.
# hide is present and called to ensure that your generator code works on
#   general iterable parameters (not just on a string, tuple, list, etc.)
# For example, although we can call len(string) we cannot call
#   len(hide(string)), so the generator functions you write should not
#   call len on their parameters
# Leave hide in this file and add code for the other generators.

def hide(iterable):
    for v in iterable:
        yield v


def running_count(iterable,p):
    count = 0
    for v in iterable:
        if p(v) == True:
            count += 1
            yield count
        else:
            yield count
    


        
def n_with_pad(iterable,n,pad=None):
    count = 0
    for v in iterable:
        if count < n:
            yield v
        if count == n:
            break
        count+=1
    
    for num in range(count, n):
        yield pad


def overlap(iterable,n,m=1):
    count = 0
    list= []
    for v in iterable:
        if count == n:
            yield list
            list = list[m:]
            count = len(list)
        list.append(v)
        count += 1
        
    if len(list) == n:
        yield list

def yield_and_skip(iterable):
    skip_num = 0
    for v in iterable:
        if skip_num > 0:
            skip_num -=1
            continue
        if isinstance(v, int):
            yield v
            skip_num = v
        if not isinstance(v, int):
            yield v
        
        

        
def skip_bad_and_next(iterable,p): # predicate p(n) true if n is good
    print_all = True
    count = 1
    for v in iterable:
        if p(v) == True and print_all == True:
            yield v
        else:
            print_all = False
            if p(v) == True and count <= 0:
                yield v
            if p(v) == True:
                count -= 1
            else:
                count = 1
        
 
    
def alternate(*args):
    pos = 0
    total = 0
    counter = 0
    char = 0
    numlist = []
    for tup in args:
        for letter in tup:
            total += 1
            char += 1
    
        numlist.append(char)
        char = 0 

    while total > 0:
        for tup in args:
            if counter == len(args):
                pos += 1
                counter = 0
         
            if pos < numlist[counter]:
                for letter in range(pos,numlist[counter]):
                    temp = list(tup)
                 
                    temp = temp[letter::]
                    character = ""
                    if temp:
                        character = temp.pop(0)
                    yield character
                    total -= 1
                    break
            #print(counter ,  '   ' , len(args))
            counter += 1    


if __name__ == '__main__':
    print('\nTesting running_count')
    for i in running_count('bananastand',lambda x : x in 'aeiou'): # is vowel
        print(i,end=' ')
    print()
    for i in running_count(hide('bananastand'),lambda x : x in 'aeiou'): # is vowel
        print(i,end=' ')
    print()
    

    print('\nTesting n_with_pad')
    for i in n_with_pad('abcdefg',3,None):
        print(i,end=' ')
    print()
    for i in n_with_pad(hide('abcdefg'),3,None):
        print(i,end=' ')
    print()
    for i in n_with_pad(hide('abcdefg'),10):
        print(i,end=' ')
    print()
    for i in n_with_pad(hide('abcdefg'),10,'?'):
        print(i,end=' ')
    print()
    for i in n_with_pad(hide('abcdefg'),10):
        print(i,end=' ')
    print()
    
     
    print('\nTesting overlap')
    for i in overlap('abcdefghijk',3,2):
        print(i,end=' ')
    print()
    for i in overlap(hide('abcdefghijk'),3,2):
        print(i,end=' ')
    print()
    
    
    print('\nTesting yield_and_skip')
    for i in yield_and_skip([1, 2, 1, 3, 'a', 'b', 2, 5, 'c', 1, 2, 3, 8, 'x', 'y', 'z', 2]):
        print(i,end=' ')
    print()
    for i in yield_and_skip(hide([1, 2, 1, 3, 'a', 'b', 2, 5, 'c', 1, 2, 3, 8, 'x', 'y', 'z', 2])):
        print(i,end=' ')
    print()
    
    
    print('\nTesting skip_bad_and_next')
    for i in skip_bad_and_next('abxcdxxefxgxxxxxxxabc',lambda x: x != 'x'):
        print(i,end=' ')
    print()
    for i in skip_bad_and_next(hide('abxcdxxefxgxxxxxxxabc'),lambda x: x != 'x'):
        print(i,end=' ')
    print()
    
    
    print('\nTesting alternate')
    for i in alternate('abcde','fg','hijk'):
        print(i,end=' ')
    print()
    for i in alternate(hide('abcde'),hide('fg'),hide('hijk')):
        print(i,end=' ')
    print()
    
    
    #driver tests
    import driver
    driver.default_file_name = 'bsc3.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
