#encoding:utf-8
import pdb
#class sharebase:
#    def __get__(self, instance, owner):
#        if not hasattr(self, name ):
#            setattr(self,name, -1)
#        val = getattr(self,name)+1
#        setattr(self,name,val)
#        return val
#class share:
#    pass

#if __name__=="__main__": 
#    print("haha!")
#    print(share.abc)
#    print(share.abc)
    

#class C(object):  
#    a = 'abc'  
#    def __getattribute__(self, *args, **kwargs):  
#        print("__getattribute__() is called")  
#        return object.__getattribute__(self, *args, **kwargs)  
#    def __getattr__(self, name):  
#        print("__getattr__() is called ")  
#        return name + " from getattr"  
      
#    def __get__(self, instance, owner):  
#        print("__get__() is called", instance, owner)  
#        return self  
      
#    def foo(self, x):  
#        print(x)  
  
#class C2(object):  
#    d = C()
#    e
#if __name__ == '__main__':  
#    C2.d
#    C2.e



class gen:
    a=0
    def t(self):
        for x in ["测","试","一","步"]:
            gen.__dict__[x](self)

    def 测(self):
        print("t0")
    def 试(self):
        print("t1")
    def 一(self):
        print("t2")
    def 步(self):
        print("t3")

def a():
    print("a")
def b():
    print("b")
def c():
    print("c")

if __name__ == '__main__':
#    print(gen.a)
    ar=[a,b,c]
    ar[0]()