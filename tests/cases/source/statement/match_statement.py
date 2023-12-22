# pytest.mark.skipif(not PY310_PLUS, reason: "this statement is supported above python 3.10")

# https://github.com/hakancelikdev/unimport/issues/291

match sort_by:
    case 'date': sort_by = ' updated DESC,'
    case _:      sort_by = ''
