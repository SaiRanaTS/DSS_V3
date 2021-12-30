import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
x1 = [1,2,3,4,5,6,7]
y1 = [3,4,8,1,2,6,9]
plt.scatter(x1,y1,color="red")

plt.subplot(1,2,2)
x2 = [1,2,3,4,5,6,7]
y2 = [1,2,3,1,2,3,4]
plt.scatter(x2,y2,color="blue")
plt.show()