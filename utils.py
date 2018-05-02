def rndstr(len):
    return ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", len))

class obj:
    def __init__(self,  **kw ):
        for k,v in kw.items():
            setattr( self, k, v)

def atoi(s):
    return 0 if s == "" else int(s)
