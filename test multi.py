import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

plt.figure(figsize=(12,8))
plt.subplots_adjust(left=0.06, right=0.95, top=0.9, bottom=0.1)
t1 = np.arange(0.0, 3.0, 0.01)

ax1 = plt.subplot(211)
ax1.margins(0.05)           # Default margin is 0.05, value 0 means fit
ax1.plot(t1, f(t1))

ax2 = plt.subplot(427)
ax2.margins(2, 2)           # Values >0.0 zoom out
ax2.plot(t1, f(t1))
ax2.set_title('Zoomed out')

ax3 = plt.subplot(428)
ax3.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center
ax3.plot(t1, f(t1))
ax3.set_title('Zoomed in')

plt.show()