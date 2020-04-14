
from sympy import linear_eq_to_matrix, symbols, Matrix, init_printing, pprint
import sympy as sp
import os
iteration = 1

#Declaring the matrices.

f = open(os.getcwd()+"\\input1.txt", "r")
eqns=[]
no_constraints = f.readline()
no_constraints = int(no_constraints.rstrip())
min_or_max = f.readline().lower()[:3]
z = f.readline()
z= z.rstrip()       #removes \n from the end
z = z.replace(" ", "") #removesall the spaces
z=z.replace('z=', "")
initial = z.count('x')
n = no_constraints+initial
for i in range(0, no_constraints):
    eqns.append(f.readline().rstrip())
symbs=[]
j=0
for i in range(1, n+1):
    globals()['x%s' % i]=symbols('x'+str(i))
    symbs.append('x'+str(i))
    if(i>initial):
        eqns[j]=eqns[j].replace('<=', '+x'+str(i)+'-')  #converts given inequalities into equation form
        j+=1
A, b=   sp.linear_eq_to_matrix(eqns,symbs)          #storing respective values into the matrices A, b, c
c, rhs=sp.linear_eq_to_matrix([z], symbs)
c = c.T
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
print(index)
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
 #Determining whether to use min or max approach
if(min_or_max=="max"):
    entering_index = min(enter.keys(), key=(lambda k: enter[k]))
else:
    entering_index = max(enter.keys(), key=(lambda k: enter[k]))

    
#Checking for optimal solution.
#Determining whether to use min or max approach
if(min_or_max=="max"):
    determine = enter[entering_index]>0
else:
    determine = enter[entering_index]<0
if(determine):
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
    #Determining whether to use min or max approach
    if(min_or_max=="max"):
        entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    else:
        entering_index = max(enter.keys(), key=(lambda k: enter[k]))
    
    #Checking for optimal solution.
    #Determining whether to use min or max approach
    if(min_or_max=="max"):
        determine = enter[entering_index]>0
    else:
        determine = enter[entering_index]<0
    if(determine):
        print("\nOptimal solution reached =", z[0])
        print("Optimal values: ")
        for i in range(len(index)):
            if c[index[i]] != 0:
                print("x{a} = {b}".format(a=index[i]+1, b=round(X[i],3)))
        break