def wrapper(func):
    print("hello")
    func()

@wrapper
def test():
   print("world")