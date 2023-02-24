import os 
a = "/home"

b = os.path.split(a)

print(b)

c = os.path.join(b[0], "test2")

print(c)