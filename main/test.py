#encoding:utf-8
import datetime

def make_counter(): 
    count = 0 
    def counter(): 
        nonlocal count 
        count += 1 
        return count 
    return counter 
       
def make_counter_test(): 
  mc = make_counter() 
  print(mc())
  print(mc())
  print(mc())
 
make_counter_test()