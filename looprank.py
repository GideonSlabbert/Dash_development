import numpy as np
from numpy import linalg as LA


Connectivity_Matrix = np.array([
                                [0,0,1,1],
                                [1,0,0,0],
                                [1,1,0,1],
                                [1,1,0,0]
                                         ])

back_links_nj = np.sum(Connectivity_Matrix,axis=0)

forward_links_xn = np.sum(Connectivity_Matrix,axis=1)

A_matrix = Connectivity_Matrix / back_links_nj

w,v = LA.eigh(A_matrix)

print("w=",w)
print("v=",v)