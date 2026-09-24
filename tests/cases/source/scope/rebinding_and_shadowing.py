import b1
b1 = "x"
print(b1)

import b2
def f2():
    b2 = {}
    return b2

import b3
def f3(b3):
    return b3

import b4
def f4(b4):
    def g():
        return b4
    return g

import b5
def f5():
    for b5 in []:
        print(b5)

import b6
def f6():
    import b6
    return b6
