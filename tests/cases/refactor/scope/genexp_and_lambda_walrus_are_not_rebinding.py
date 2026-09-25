from os import sep

n = sum(1 for sep in ["a", "b"])
f = lambda: (sep := "x")
print(n, f, sep)
