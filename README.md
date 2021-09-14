# creload

Enable autoreloading of C extensions in Python (kind of).

## Usage

```py
from creload import lazyimport
mylib = lazyimport('mylib')
print(mylib.add(3, 4))

# mylib has not been imported into your current environment,
# and yet you were able to use it.
import sys
assert 'mylib' not in sys.modules.keys()
# this means it can be "reimported", circumventing the need to
# restart the Python process to unload the C extension.
```

If you want more control over what is executed inside the subprocess, you can use the subprocess decorator.
```py
from creload import subprocess

@subprocess
def myadd(x, y, z):
    import mylib
    tmp = mylib.add(x, y)
    return float(tmp + z)

print(myadd(3, 4, 5))
```

### Pitfall examples
Sometimes the return value of a function can force a library to be imported. Be vary of this.
```py
from creload import lazyimport
np = lazyimport('numpy')

# This causes numpy to be imported, since the returned data (a numpy array) depends on numpy
print(np.array([1,2,3]))
```

```py
from creload import subprocess

@subprocess
def get_second_element():
    import numpy as np
    a = np.array([1,2,3])
    return a[1]

# This also causes NumPy to be imported, although you might not expect it to
print(get_second_element())
```

Alternative which avoids numpy import:
```py
from creload import subprocess

@subprocess
def get_second_element():
    import numpy as np
    a = np.array([1,2,3])
    return int(a[1])

# Casting creates a new value, which means numpy is no longer imported when the value is returned
print(get_second_element())
```