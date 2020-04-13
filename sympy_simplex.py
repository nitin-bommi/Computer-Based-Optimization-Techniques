import numpy as np
from sympy import linear_eq_to_matrix, symbols, Matrix, init_printing, pprint

iteration = 1

#Declaring the matrices.
A = Matrix([
    [6,4,1,0,0,0],
    [1,2,0,1,0,0],
    [-1,1,0,0,1,0],
    [0,1,0,0,0,1]
])
b = Matrix([[24],[6],[1],[2]])
c = Matrix([[5],[4],[0],[0],[0],[0]])

print('\nA:\n')
pprint(A)
print('\nb:\n')
pprint(b)
print('\nc:\n')
pprint(c)

#Finding the transpose.
c_trans = c.T

#Assigning the number of variables and equations.
(m, n) = A.shape

#List of indices to be taken.
index =[x for x in range((n-m),n)]

#Constructing the required matrices.
B = A[:, index]
B_inv = B ** -1
X = B_inv * b
z = c_trans[:, index] * X

print('\nB:')
print("\nIteration:",iteration)
pprint(B)

#Using dictiories to find the key - index, value - value to find the entering and leaving variables.
enter, leave = {}, {}
    
#Finding the entering variable.
for i in range(n):
    if i not in index:
        enter[i] = (((c_trans[:, index] * B_inv) * A[:, [i]])[0] - c_trans[i])
    
entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
#Checking for optimal solution.
if(enter[entering_index]>0):
    print("\nOptimal solution reached")
    print("Optimal values: ")
    for i in range(len(index)):
        if c[index[i]][0] != 0:
            print("x{a} = {b}".format(a=index[i]+1, b=round(X[i][0],3)))
    exit()

while(True):
    
    #num = B_inv * b, den = B_inv * P[i].
    num, den = B_inv * b, B_inv * A[:, [entering_index]]
    
    #Finding the leaving variable.
    for i in index:
        if int(den[i-(n-m)])>0:
            leave[i] = num[i-(n-m)]/den[i-(n-m)]
            
    leaving_index = min(leave.keys(), key=(lambda k: leave[k]))
    
    #Updating the index list.
    for i,j in enumerate(index):
        if(j==leaving_index):
            index[i]=entering_index
            
    iteration += 1
            
    #Updating the matrices.
    B = A[:, index] 
    B_inv = B ** -1
    X = B_inv * b
    z = c_trans[:, index] * X
    enter, leave = {}, {}
    
    print("\nIteration:",iteration)
    pprint(B)
    
    #Finding the entering variable.
    for i in range(n):
        if i not in index:
            enter[i] = (((c_trans[:, index] * B_inv) * A[:, [i]])[0] - c_trans[i])
    
    entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
    #Checking for optimal solution.
    if(enter[entering_index]>0):
        print("\nOptimal solution reached =", z[0])
        print("Optimal values: ")
        for i in range(len(index)):
            if c[index[i]] != 0:
                print("x{a} = {b}".format(a=index[i]+1, b=round(X[i],3)))
        break
