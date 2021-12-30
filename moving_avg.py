import  numpy as np

dataset = [1,5,7,6,7,8,2,5,2,6,2,6,13]

def moving_avg (values, window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights)
    return smas

ma = moving_avg(dataset,3)

print(ma)