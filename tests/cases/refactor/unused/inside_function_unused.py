def foo():

    try:
        import t
        print(t)
    except ImportError as exception:
        pass

    return math.pi
