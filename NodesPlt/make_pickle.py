import numpy as np
import pickle
import math



arr = np.zeros((50,60,70))

for i in range(0,50):
    for j in range(0,60):
        for k in range(70):
            arr[i, j, k] = i-25 + math.cos(j/20) + k*k/150

print(np.take(arr, 5, 1).shape)
# pickle.dump(arr, open("example.pkl", "wb"))