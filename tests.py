import matplotlib.pyplot as plt
Numberofvisit = [300]
sales = [100]
conversion = [0.37]
plt.scatter(x=Numberofvisit,y=sales,c=conversion,cmap="jet")
cbar=plt.colorbar(label="conversion", orientation="vertical")
cbar.set_ticks([0,0.2, 0.4, 0.6, 0.8,1.0])
cbar.set_ticklabels(["A","A", "B", "C", "D","E"])

plt.show()