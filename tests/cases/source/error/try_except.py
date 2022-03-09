try:
    import x
except Exception:
    pass

try:
    import x
except BaseException:
    pass

try:
    import x
except OSError:
    pass

try:
    import x
except (OSError, AttributeError):
    pass
