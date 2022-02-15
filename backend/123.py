from lib2to3.pytree import Base

from pyrsistent import b


dict1 = {"a":10}


class test():
    def __init__(self,a,b):
        self.a = a
        self.b = b 

aa = test(**dict1)
print(aa.b)
    