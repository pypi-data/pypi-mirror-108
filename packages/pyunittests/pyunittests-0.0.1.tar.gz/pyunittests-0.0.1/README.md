# example program:

```
from pyunittests import *

def funcBeingTested(inp):
    return hi
    if inp in [15]:
        return inp*3
    else:
        return inp*2

def raise_test():
    return funcBeingTested(5)

def test1():
    expect(raise_test).toRaise(NameError)

it(f'doubles 5 correctly', test1, 'max')
```
