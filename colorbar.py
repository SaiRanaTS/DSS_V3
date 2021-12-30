import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

x = np.random.randn(60)
y = np.random.randn(60)
z = [np.random.random() for _ in range(60)]

fig = plt.figure()
gs = gridspec.GridSpec(1, 2)

ax0 = plt.subplot(gs[0, 0])
plt.scatter(x, y, s=20)

ax1 = plt.subplot(gs[0, 1])
cm = plt.cm.get_cmap('RdYlBu_r')
plt.scatter(x, y, s=20 ,c=z, cmap=cm)

fig.tight_layout()

cbaxes = inset_axes(ax1, width="30%", height="3%", loc=3)
plt.colorbar(cax=cbaxes, ticks=[0.,1], orientation='horizontal')


plt.show()