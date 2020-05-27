
from sympy import linear_eq_to_matrix, symbols, Matrix, init_printing, pprint
import sympy as sp
import os
iteration = 1

#Declaring the matrices.

f = open(os.getcwd()+"\\input1.txt", "r")
flag =0
lines =[]
f = open("input1.txt", "r")
count1=0
#The following code makes stores the data starting from min or max ignoring rest of the multiline comments
for line in f:
    if(flag==1):
        lines.append(line)
    if(line.strip()=="***"):
        count1+=1
    if(count1==2):
        flag=1

lines1 = [lines[i].strip() for i in range(len(lines)) if(lines[i].strip()!='')]

no_constraints = len(lines1)-2          #Calculates no_of_constraints
min_or_max = lines1[0].lower()[:3]
z = lines1[1].replace(' ', '')
z=z.replace('z=', "")
initial = z.count('x')
n = no_constraints+initial
eqns = lines1[2:]
for i in range(no_constraints):
    eqns[i] = eqns[i].replace(' ','')    #removes all the spaces
symbs=[]
j=0
for i in range(1, n+1):
    globals()['x%s' % i]=symbols('x'+str(i))     #creates the symbols to be used as variables
    symbs.append('x'+str(i))
    if(i>initial):
        eqns[j]=eqns[j].replace('<=', '+x'+str(i)+'-')      #converting inequalities into equation form by adding slack variables
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
    count=0
    #num = B_inv * b, den = B_inv * P[i].
    num, den = B_inv * b, B_inv * A[:, [entering_index]]
    #Finding the leaving variable.
    for i in index:
        if int(den[i-(n-m)])>0:
            leave[i] = num[i-(n-m)]/den[i-(n-m)]
        elif(int(den[(i-(n-m))])<=0):
            count+=1
    if(count==len(index)):
        print("Solution is unbounded")
        break
    else:
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
        determine = enter[entering_index]>=0
    else:
        determine = enter[entering_index]<=0
    
    if(determine):
        print("\nOptimal solution reached =", z[0])
        print("Optimal values: ")
        for i in range(len(index)):
            if c[index[i]] != 0:
                print("x{a} = {b}".format(a=index[i]+1, b=round(X[i],3)))
        break