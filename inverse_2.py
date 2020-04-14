#Importing the libraries.
import numpy as np

#Declaring the matrices.
A = np.array([
    [6,4,1,0,0,0],
    [1,2,0,1,0,0],
    [-1,1,0,0,1,0],
    [0,1,0,0,0,1]
])
b = np.array([[24],[6],[1],[2]])
c = np.array([[5],[4],[0],[0],[0],[0]])

#Declaring inverse function method-2
def inverse(A):
    size = A.shape[0]
    B = np.identity(size)
    for x in range(0,size):
        V = np.dot(B,A[:, x])
        W = V.copy()
        item=V.item(x)
        for y in range(0,size):
            if item!=0:
                if y==x:
                    W[y] = 1/item
                else:
                    W[y] = -V[y]/item
        T = B.copy()
        T[x]=np.zeros(size)
        B = T + np.dot(W.reshape(size,1),[B[x]])
  
    return B
  
#Finding the transpose.
c_trans = c.transpose()

#Assigning the number of variables and equations.
(m, n) = A.shape

#List of indices to be taken.
index =[x for x in range((n-m),n)]

#Constructing the required matrices.
B = A[:, index]
B_inv = np.linalg.inv(B)
X = np.dot(B_inv, b)
z = np.dot(c_trans[:, index], X)

#Using dictiories to find the key - index, value - value to find the entering and leaving variables.
enter, leave = {}, {}
    
#Finding the entering variable.
for i in range(n):
    if i not in index:
        enter[i] = (np.dot(np.dot(c_trans[:, index], B_inv), A[:, [i]]) - c_trans[0][i])
    
entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
#Checking for optimal solution.
if(enter[entering_index]>0):
    print("Optimal solution reached")
    print("Optimal values: ")
    for i in range(len(index)):
        if c[index[i]][0] != 0:
            print("x{a} = {b}".format(a=index[i]+1, b=round(X[i][0],3)))
    exit()

while(True):

    #Printing the indices taken.
    print(index)
    
    #num = B_inv * b, den = B_inv * P[i].
    num, den = np.dot(B_inv, b), np.dot(B_inv, A[:, [entering_index]])
    
    #Finding the leaving variable.
    for i in index:
        if int(den[i-(n-m)][0])>0:
            leave[i] = num[i-(n-m)][0]/den[i-(n-m)][0]
            
    leaving_index = min(leave.keys(), key=(lambda k: leave[k]))
    
    #Updating the index list.
    for i,j in enumerate(index):
        if(j==leaving_index):
            index[i]=entering_index
            
    #Updating the matrices.
    B = A[:, index] 
    B_inv = inverse(B)
    X = np.dot(B_inv, b)
    z = np.dot(c_trans[:, index], X)
    enter, leave = {}, {}
    
    #Finding the entering variable.
    for i in range(n):
        if i not in index:
            enter[i] = (np.dot(np.dot(c_trans[:, index], B_inv), A[:, [i]]) - c_trans[0][i])
    
    entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
    #Checking for optimal solution.
    if(enter[entering_index]>0):
        print("Optimal solution reached =", z[0][0])
        print("Optimal values: ")
        for i in range(len(index)):
            if c[index[i]][0] != 0:
                print("x{a} = {b}".format(a=index[i]+1, b=X[i][0]))
        break
