# test_full_unused
from x import y
from x import y
from t import x
import re
import ll
import ll
from c import e
import e

# test_one_used
from x import y
from x import y
from t import x
import re
import ll
import ll
from c import e
import e
from pathlib import Path
from pathlib import Path
p = Path()

# test_two_used
from x import y
from x import y
from t import x
import re
import ll
import ll
from c import e
import e
from pathlib import Path
from pathlib import Path
p = Path()
print(ll)

# test_three_used
from x import y  # 1 - unused
from x import y  # 2 - unused
from t import x  # 3 - unused
import re  # 4 - unused
import ll  # 5 - unused
import ll  # 6
from c import e  # 7 - unused
import e  # 8 -
from pathlib import Path  # 9 - unused
from pathlib import Path  # 10
p = Path()  # 11

print(ll)  # 12

def function(e=e):pass

# test_different_duplicate_unused
from x import z
from y import z

# test_different_duplicate_used
from x import z
from y import z
print(z)

# test_multi_duplicate
from x import y, z, t
import t
from l import t

# test_multi_duplicate_one_used
from x import y, z, t
import t
from l import t
print(t)

# test_one_used_bottom_multi_duplicate
import t
from l import t
from x import y, z, t
print(t)

# test_two_multi_duplicate_one_used
import t
from l import t
from x import y, z, t
from i import t, ii
print(t)
