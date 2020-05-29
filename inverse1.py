# Importing the libraries.
import time
from sympy import linear_eq_to_matrix, symbols, pprint

# Starting the time count.
start = time.time()

# Defining inverse method.
def inverse(mat,entering,leaving):
    
    dim = mat.shape[0]
    
    X = mat.row(leaving)/mat.row(leaving)[entering]
    mat.row_del(leaving)
    mat = mat.row_insert(leaving,X)
    
    for j in range(dim):
        if(leaving!=j):
            con=mat.row(j)[entering]
            X = mat.row(j)-mat.row(leaving)*con
            mat.row_del(j)
            mat = mat.row_insert(j,X)
            
    return mat

# Counting the iterations.
iteration = 1

# Reading from file.
flag =0
lines =[]
f = open("input.txt", "r")
count_cmt=0

# The following code stores the data starting from min or max ignoring rest of the multiline comments.
for line in f:
    if(flag==1):
        lines.append(line)
    if(line.strip()=="***"):
        count_cmt+=1
    if(count_cmt==2):
        flag=1

new_line = [lines[i].strip() for i in range(len(lines)) if(lines[i].strip()!='')]

# Calculating the number of constraints.
no_constraints = len(new_line)-2          

# Storing the problem type.
min_or_max = new_line[0].lower()[:3]
z = new_line[1].replace(' ', '')
z = z.replace('z=', "")
initial = z.count('x')
n = no_constraints + initial
eqns = new_line[2:]

# Removing the spaces.
for i in range(no_constraints):
    eqns[i] = eqns[i].replace(' ','')
symbs=[]

# Creating the variables and introducing slack variables.
j=0
for i in range(1, n+1):
    globals()['x%s' % i] = symbols('x'+str(i))    
    symbs.append('x'+str(i))
    if(i>initial):
        eqns[j] = eqns[j].replace('<=', '+x'+str(i)+'-')     
        j+=1

# Typecasting the variables into symbols.
symbs = symbols(symbs)

# Storing the coefficients in matrix form.
A, b = linear_eq_to_matrix(eqns,symbs)          
c, rhs = linear_eq_to_matrix([z], symbs)
c = c.T

# Printing the matrices.
print('\nA:\n')
pprint(A)
print('\nb:\n')
pprint(b)
print('\nc:\n')
pprint(c)

# Finding the transpose.
c_trans = c.T

# Assigning the number of variables and equations.
(m, n) = A.shape

# List of indices to be taken.
index =[x for x in range((n-m),n)]

# Constructing the required matrices.
B_inv = A[:, n-m:]
X = B_inv * b
z = c_trans[:, index] * X

print('\nB:')
print("\nIteration:",iteration)
pprint(A)

# Using dictiories to find the key - index, value - value to find the entering and leaving variables.
enter, leave = {}, {}
    
# Finding the entering variable.
for i in range(n):
    if i not in index:
        enter[i] = (((c_trans[:, index] * B_inv) * A[:, [i]])[0] - c_trans[i])

# Determining whether to use min or max approach.
if(min_or_max=="max"):
    entering_index = min(enter.keys(), key=(lambda k: enter[k]))
else:
    entering_index = max(enter.keys(), key=(lambda k: enter[k]))

    
# Checking for optimal solution.
if(min_or_max=="max"):
    determine = enter[entering_index]>=0
else:
    determine = enter[entering_index]<=0
    
if(determine):
    print("\nOptimal solution reached")
    print("Optimal values: ")
    for i in range(len(index)):
        if c[index[i]][0] != 0:
            print("x{a} = {b}".format(a=index[i]+1, b=round(X[i][0],3)))
    exit()

# Copy of A.
A1 = A[:,:]

# Iterating for optimal solution.
while(True):
    
    count=0
    
    # num = B_inv * b, den = B_inv * P[i].
    num, den = B_inv * b, B_inv * A[:, [entering_index]]
    
    # Finding the leaving variable.
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
    
    
    # Finding the index value of leaving variable 
    for i in range(len(index)):
        if(leaving_index==index[i]):
            leaving=i
            break
            
    # Updating the index list.
    for i,j in enumerate(index):
        if(j==leaving_index):
            index[i]=entering_index
            
    # Next iteration.
    iteration += 1
            
    # Updating the matrices.
    A1 = inverse(A1,entering_index,leaving)
    B_inv = A1[:, n-m:]
    X = B_inv * b
    z = c_trans[:, index] * X
    enter, leave = {}, {}
    
    print("\nIteration:",iteration)
    pprint(A1)
    
    # Finding the entering variable.
    for i in range(n):
        if i not in index:
            enter[i] = (((c_trans[:, index] * B_inv) * A[:, [i]])[0] - c_trans[i])
   
    # Determining whether to use min or max approach
    if(min_or_max=="max"):
        entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    else:
        entering_index = max(enter.keys(), key=(lambda k: enter[k]))
    
    # Checking for optimal solution.
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

# Ending the time count.
end = time.time()

# Printing the time taken in ms.
print("Time: " + str((end-start)*1000) + "ms")
