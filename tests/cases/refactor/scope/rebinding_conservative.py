import a1
if cond:
    a1 = 1
print(a1)

import a2
def f2():
    global a2
    a2 = 1
    return a2

import a3
def f3(a3=a3):
    return a3

import a4
a4 = a4.path

import a5
class A5:
    a5 = a5

import a6
a6 = 1
def f6():
    return a6

import a7
try:
    a7 = x
except Exception:
    pass
print(a7)

import a8
with ctx as a8:
    pass
print(a8)

import a9
(a9 := 1)
print(a9)

import a10
a10: str
print(a10)

import a11
x11 = [a11 for _ in range(3)]

import a12
@a12.decorator
def f12(a12): return a12

import a13
def f13() -> a13.T:
    a13 = 1
    return a13

import a14
a14 += 1

import a15
for a15 in []:
    pass
print(a15)
