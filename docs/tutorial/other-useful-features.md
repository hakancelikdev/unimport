## Skip Import

Leave '# unimport: skip' or '# noqa' at the end of the line to skip imports **for
example:**

```python
import x # unimport:skip
```

```python
from x import ( # noqa
  t, y,
  f, r
)
```

Unimport support multiple skip like below. _It doesn't matter which line you put the
comment on._

```python
from package import (
    module,
    module1,
)  # unimport:skip
```

or

```python
from package import (
    module, # unimport:skip
    module1,
)
```

---

## File Wide Skips

To skip a file by typing `# unimport: skip_file` anywhere in that file **for example:**

```python
# unimport: skip_file

import x

```

or

```python
import x

# unimport: skip_file

```

---

## Exit code behavior

Exit code 1 if there is a syntax error Exit code 0 if unused import versa and auto
removed for all other cases exit code 1 Exit code 0 if there is no unused import.
