A = np.array([
    [6,4,1,0,0,0],
    [1,2,0,1,0,0],
    [-1,1,0,0,1,0],
    [0,1,0,0,0,1]
])
b = np.array([[24],[6],[1],[2]])
c = np.array([[5],[4],[0],[0],[0],[0]])
c_trans = c.transpose()
n, m = 6, 4
index =[x for x in range((n-m),n)]
B = A[:, index]
B_inv = np.linalg.inv(B)
X = np.dot(B_inv, b)
z = np.dot(c_trans[:, index], X)
enter, leave = {}, {}
    
for i in range(n):
    if i not in index:
        enter[i] = (np.dot(np.dot(c_trans[:, index], B_inv), A[:, [i]]) - c_trans[0][i])
    
entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
if(enter[entering_index]>0):
    print("Optimal solution reached")

while(True):

    print(index)
    num, den = np.dot(B_inv, b), np.dot(B_inv, A[:, [entering_index]])
    for i in index:
        if int(den[i-(n-m)][0])>0:
            leave[i] = num[i-(n-m)][0]/den[i-(n-m)][0]
            
    leaving_index = min(leave.keys(), key=(lambda k: leave[k]))
    
    for i,j in enumerate(index):
        if(j==leaving_index):
            index[i]=entering_index
            
    B = A[:, index] 
    B_inv = np.linalg.inv(B)
    X = np.dot(B_inv, b)
    z = np.dot(c_trans[:, index], X)
    enter, leave = {}, {}
    
    for i in range(n):
        if i not in index:
            enter[i] = (np.dot(np.dot(c_trans[:, index], B_inv), A[:, [i]]) - c_trans[0][i])
    
    entering_index = min(enter.keys(), key=(lambda k: enter[k]))
    
    if(enter[entering_index]>0):
        print("Optimal solution reached")
        break
