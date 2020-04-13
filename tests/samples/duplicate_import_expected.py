# test_full_unused

# test_one_used
from pathlib import Path
p = Path()

# test_two_used
import ll
from pathlib import Path
p = Path()
print(ll)

# test_three_used
import ll  # 6
import e  # 8 -
from pathlib import Path  # 10
p = Path()  # 11

print(ll)  # 12

def function(e=e):pass

# test_different_duplicate_unused

# test_different_duplicate_used
from y import z
print(z)

# test_multi_duplicate

# test_multi_duplicate_one_used
from l import t
print(t)

# test_one_used_bottom_multi_duplicate
from x import t
print(t)

# test_two_multi_duplicate_one_used
from i import t
print(t)
