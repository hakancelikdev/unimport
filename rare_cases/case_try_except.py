# This is not unused import, but it is unused import according to unimport.

try:
    import django
except ImportError:
    print("install django")
