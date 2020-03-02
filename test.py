class A:
    def __init__(self, a):
        self.a = a

    # adding two objects
    def __add__(self, o):
        return self.a + o.a
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


ob1 = A(1)
ob2 = A(2)
ob3 = A("Geeks")
ob4 = A("For")

print(ob1 + ob2)
print(ob3 + ob4)

row1 = sum([ob1, ob2])
print(row1)

