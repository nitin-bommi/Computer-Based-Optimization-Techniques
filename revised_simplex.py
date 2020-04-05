# Importing the libraries.
import numpy as np

# Creating a 4-dimentional array.
B = [
     [1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]
    ]

# Creating a 4x1 dimentional array.
b = [[24],[6],[1],[2]]

# Finding the inverse of B.
B_inv = np.linalg.inv(B).astype(int)

# Matrix multiplication.
X = np.dot(B_inv, b)
