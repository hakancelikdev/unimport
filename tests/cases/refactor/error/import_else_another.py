try:
   import x
except ImportError:
    import y as x

print(x)
