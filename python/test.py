
def f(l=[]):
    print l

l = [1, 2, 3]

f()
f(l)
f()


class A():
    x = 1


class B(A):
    pass


class C(A):
    pass

a = A()
b = B()
c = C()


b.x = 2
print a.x, b.x, c.x
a.x = 3
print a.x, b.x, c.x
