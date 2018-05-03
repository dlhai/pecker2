from tools import *

#* arg: id,class,style, 
class tag:
    def __init__(self, *arg, **kw,  ):
        for k,v in kw.items():
            setattr( self, k, v)

class doc:
    def __init__(self):
        self.head = tag()
        self.body = tag()
    def build():
        pass
    def addhead():
        pass
    def add():
        pass
