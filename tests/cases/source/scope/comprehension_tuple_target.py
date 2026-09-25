import os


def f(items):
    names = [os for os, x in items]
    return os.getcwd(), names
