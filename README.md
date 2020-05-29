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

