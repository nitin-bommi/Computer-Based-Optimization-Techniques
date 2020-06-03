# Revised simplex 

To find the inverse of intermediate matrices, two approaches are used with time compexities __O(n)__ and __O(n<sup>2</sup>)__ respectively.

### Libraries used

+ ```time```
+ ```sympy``` (sub-modules)

__SymPy__ is a Python library for symbolic mathematics. Since a number of variables are used (x<sub>1</sub>, x<sub>2</sub>...) this library provides efficient way of interpreting the variales for computation. It supports formatted matrix printing, easy interpretation of matrices, its inverse and sub-matrices. 

The time is started after all the libraries are imported and before the function definition. It is stopped at the end of the program after some interations. The overall time is interpreted in *milli-seconds* as it is an interpretable scale for such computations.

### How the input is taken?

The input file can be viewed [here.](https://github.com/Yashi1011/Computer-Based-Optimization-Techniques/blob/master/input.txt)

The text under '\*\*\*' is viewed as comment and it represents the format of the input with some examples (along with solutions). 
The code checkes for the type of the problem (i.e., minimisation or maximisation) and then computes the result. 

The problem to be solved has to be appended below the final '\*\*\*'. And it should contain the type of the problem and the constraints.

Once the file is read, it checks for the lines below the final '\*\*\*' and then converts that into matrices form by a library ```linear_eq_to_matrix``` on which computations are performed. This library takes input in the form of equations and converts them into matrices of coefficients.

### Output 

With the help of SymPy, the out is formatted in matrix form. 

When the input is taken as:

Maximize:
z = 5x<sub>1</sub>+4x<sub>2</sub>
      
s.t.

6x<sub>1</sub> + 4x<sub>2</sub> &le; 24

x<sub>1</sub> + 2x<sub>2</sub> &le; 6

-x<sub>1</sub> + x<sub>2</sub> &le; 1

x<sub>2</sub> &le; 2

The matrices A, b, c are printed as:

<img src="https://github.com/Yashi1011/Computer-Based-Optimization-Techniques/blob/master/samples/abc.PNG" height = 500>

The output and intermediate matrix after each iteration is printed:

<img src="https://github.com/Yashi1011/Computer-Based-Optimization-Techniques/blob/master/samples/output.PNG" height = 500>

### Time complexity

When we found the inverse using both the functions on the same matrix. The following results were obtained:

+ Elementary method:

```python
def inverse1(mat,entering,leaving):
    
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
```

The execution time was `0.9977817 ms`

+ Gauss Jordan method:

```python
def inverse2(A):
    
    size = A.shape[0]
    
    B = eye(size)
    
    for x in range(0,size):
        V = B*A.col(x)
        W = V*1
        item = V[x]
        for y in range(0,size):
            if item != 0:
                if y == x:
                    W[y] = 1/item
                else:
                    W[y] =- V[y]/item
                    
        T = B*1
        T.row_del(x)
        T = T*1
        B = T.row_insert(x,zeros(1,size)) + (W*B.row(x))
        
    return B
```

The execution time was `3.027201 ms`

i.e., Elementary method is ~3.1 times faster.

Justification - In elementary method, we used a single for loop whereas in gauss jordan method we used two for loops. (O(n) vs O(n<sup>2</sup>))
