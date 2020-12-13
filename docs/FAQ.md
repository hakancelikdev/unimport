# FQA

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

When the same files are scanned, the results are as follows.

### Autoflake

```
68382555 function calls (64595322 primitive calls) in 27.521 seconds

Ordered by: internal time
List reduced from 1305 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  3001189    5.785    0.000   14.671    0.000 /usr/lib/python3.8/tokenize.py:429(_tokenize)
  2851474    2.460    0.000    2.460    0.000 {method 'match' of 're.Pattern' objects}
  2703253    1.436    0.000    2.674    0.000 /usr/lib/python3.8/re.py:289(_compile)
     6052    1.404    0.000    1.404    0.000 {built-in method builtins.compile}
  2999810    1.144    0.000    1.144    0.000 {built-in method __new__ of type object at 0x907780}
1149060/897    1.085    0.000    2.813    0.003 /usr/lib/python3.8/ast.py:365(generic_visit)
12742442/12618738    0.985    0.000    1.017    0.000 {built-in method builtins.isinstance}
941811/82008    0.970    0.000    6.286    0.000 /home/hakan/Desktop/unimport/env/lib/python3.8/site-packages/pyflakes/checker.py:1330(handleNode)
  2701310    0.784    0.000    3.977    0.000 /usr/lib/python3.8/tokenize.py:98(_compile)
  2701379    0.720    0.000    0.996    0.000 /usr/lib/python3.8/types.py:171(__get__)
```

### Unimport

```
77575444 function calls (71914951 primitive calls) in 23.082 seconds

Ordered by: internal time
List reduced from 1844 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     6091    3.701    0.001    3.701    0.001 {built-in method builtins.compile}
  7270946    3.047    0.000    6.098    0.000 /usr/lib/python3.8/ast.py:214(iter_child_nodes)
 16298178    2.920    0.000    3.978    0.000 /usr/lib/python3.8/ast.py:202(iter_fields)
2444156/2125    2.608    0.000    9.965    0.005 /usr/lib/python3.8/ast.py:365(generic_visit)
 12945575    1.599    0.000    1.599    0.000 {built-in method builtins.getattr}
20926736/20921796    1.595    0.000    1.596    0.000 {built-in method builtins.isinstance}
2508573/2125    1.201    0.000    9.970    0.005 /usr/lib/python3.8/ast.py:359(visit)
  2046668    0.895    0.000    4.986    0.000 /usr/lib/python3.8/ast.py:325(walk)
     5187    0.875    0.000    7.782    0.002 /home/hakan/Desktop/unimport/unimport/relate.py:5(relate)
  1976482    0.544    0.000    3.894    0.000 {method 'extend' of 'collections.deque' objects}
```

**As you can see, it's %19.2 faster from the Autoflake, and remember, Unimport's results
are more accurate.**

## Below are some examples that show Unimport works better.

_example.py_

```python
import datetime # unused import
datetime = None
import datetime # unused import
```

The command is run and the results are written below.

### Autoflake

command; `autoflake --in-place --remove-all-unused-imports example.py`

```python
import datetime # unused import
datetime = None
```

> As you can see the wrong result

### Unimport

command; `unimport example.py -r`

```python
datetime = None
```

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
