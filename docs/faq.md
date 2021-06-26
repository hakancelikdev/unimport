# FAQ

## Differences between Autoflake and Unimport

- Autoflake doesn't always remove the duplicate imports when they are on separate lines.

Example:

```py
from os import walk
from os import walk

use(walk)
```

For this snippet, autoflake doesn't change anything, while unimport detects and removes
the _first_ walk import.

- Autoflake replaces unused imports in compound statements with `pass`, while unimport
  detects and imports inside compound statements, if it detects that you are expecting
  an `ImportError`, it doesn't remove that particular import.

```py
try:
    from x import y
except ImportError:
    ...
```

For this snippet autoflake replaces the import statement with `pass.`, while unimport
leaves it as is.

- Autoflake is not accurate when it comes to star import expansions, while unimport can
  detect and expand them accurately.

```py
from math import *

use(RANDOM_VAR)
```

Running autoflake with --expand-star-import flag on the snippet above turns it into

```py
from math import RANDOM_VAR
```

while unimport simple removes the math import because it is not used.

- Autoflake doesn't work with multiple star imports, while unimport does.

from math import _ from os import _

use(walk, cos)

Running unimport on the above snippet with --include-star-imports flag produces the
correct output.

```py
from math import cos
from os import walk

use(walk, cos)
```

while autoflake simply ignores them.

- Our outputs are more useful, try using our --check, --diff or --permission commands.

## Performance

Unimport < 0.6.8 was much slower than Autoflake == 1.4 (current latest version as of
writing this) but Unimport > 0.6.8 is slightly faster.

## Reasons to choose autoflake

- ~~It is faster. When tested, autoflake is 1-4x faster on average.~~ (Unimport is
  slightly faster now)
- It removes unused variables which unimport doesn't support, and is not planning to.
- Has a feature that removes duplicate keys on objects.

## Reasons to choose unimport

- It does more static analysis to increse the accuracy of choosing the correct imports
  to remove.
- Can handle star imports more accurately.(https://github.com/myint/autoflake/pull/18
  describes their approach)
- Works with multiple star imports.
- Removes duplicate imports.
- Has skip_file feature that allows one to skip an entire file.
- Has a feature to remove the unused imports from requirements file.
- Allows configuration via pyproject.toml and setup.cfg files.

## Overall

Even though unimport and autoflake has features that are similar, they are not designed
to do the same thing. When you are including one to your project, it is a good idea to
know what your needs are, and decide accordingly.
