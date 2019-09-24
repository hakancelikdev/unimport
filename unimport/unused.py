from unimport.dedect import DetectUnusedImport

def get_unused(source):
    "Yield unused imports."
    dedect = DetectUnusedImport(source)
    for imp in dedect.imports:
        len_dot = len(imp["name"].split("."))
        for name in dedect.names:
            if ".".join(name.split(".")[:len_dot]) == imp["name"]:
                break
        else:
            yield imp
