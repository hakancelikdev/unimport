def foo():
    from x import y, z

    try:
        import t
        print(t)
    except ImportError as exception:
        pass

    return math.pi
