"""
In order to use different styles, call with options.
e.g.:
    python rctest.py vivid web
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys
from tools import set_style

set_style(sys.argv)

# ejemplo
xdatos = np.array([1, 2, 3, 4, 5])

#print(matplotlib.matplotlib_fname())
#print(matplotlib.get_backend())

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot()

for _ in range(5):
    ydatos = np.random.uniform(size=len(xdatos))
    ax.plot(xdatos, ydatos)

ax.plot(xdatos[::-1], ydatos)
plt.show()


