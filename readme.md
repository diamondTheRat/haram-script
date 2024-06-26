# Notes
Focused around a silly syntax because I like rats(hamsters).
Haram script is an esoteric programming language made in 3-4 days with the goal of being hard to read and very verbose.
It's interpreted by python therefore it's dynamic, but it uses braces instead of indentation.

This is an experimental version as I didn't have time to test it too much, everything in the examples directory should work, though.

I know you could make a dictionary where you define the variables and use that instead of `rat` and `swap` for an easier time programming but that would make me sad ;c
# Credits
Made by me because I have no inspiration, no skill, no life, no bitches, only hampter.

# Flow
1. initiate variables
2. select a variable
3. alter it
4. swap rats like they're tetris pieces
5. try not to go insane
6. contemplate your life choices

# Variables
### 1) Define
- supports:
    * lowercase and uppercase English letters
    * digits 0-9
    * underscore '_'

- syntax:
    * single variable: `adopt rat named <name>`
    * multiple variables: `adopt rats named <name1>, <name2>, ...`

- properties:
    * initialized as None
    * dynamic


### 2) Select
Variables can't be used directly. In order to use a variable you must select it.
```
adopt rat named my_variable; # initialize a variable

grab my_variable; # selects this variable
```
The selected variable still can't be used directly, it's referred to as 'rat'


### 3) Assign
To assign a value to a variable you first have to select that variable then give it a value.
```
adopt rat named my_variable; # initialize a variable
grab my_variable; # selects this variable

give <value>; # gives it a value
```


### 4) Types
- from python:
    - int
    - string
    - float
    - list
    - dict

- custom types:
    * block
        A block is a body of code. Unlike functions, blocks directly insert code into your program.
```
grab my_block; # select your variable

# assign code to my_block
give {
    <code>
}; # ALWAYS PUT ; AFTER THIS

rat; # runs <code>
```

### 5) Using multiple variables
In order to use multiple variables you have to grab the 2 variables you want to use.
```
grab a; grab b;
```
After that you can refer to variable 'a' using the keyword 'swap'.
```
give rat + swap; # b + a
```
Keep in mind that swap also grabs the previous variable so 'rat' is now 'a'.
This can be reversed with another swap or grabbing b again.


# Operators
I will write `<expression>` as `<exp>` because I can.
```
# Arithmetic
<exp1> + <exp2>; # addition
<exp1> - <exp2>; # subtraction
<exp1> * <exp2>; # multiplication
<exp1> / <exp2>; # division
<exp1> // <exp2>; # integer division (works like it does in python)
<exp1> % <exp2>; # remainder (works like it does in python)
-<exp>; # negative number thingy yk it

# Bitwise
<exp1> | <exp2>; # bitwise OR
<exp1> & <exp2>; # bitwise AND
<exp1> ^ <exp2>; # bitwise XOR

# Logic
!<exp>: # NOT (!false = true, !true = false)
<exp1> and <exp2>; # AND (<exp2> does NOT get evaluated if <exp1> is false)
<exp1> or <exp2>; # OR (<exp2> does NOT get evaluated if <exp1> is true)
# 'or' can be used as a replacement for ? but thats haram don't do it

# Other
<exp1>[<exp2>]; # indexing
<exp1>.<variable name>; # get attribute
<exp1>(<*args>, <**kwargs>);
```

# Conditionals
An if statement is typed using is using '?'.
```
<condition> ? <code>; # if <condition> is true then the code gets executed
```
The 'else' statement uses similar a syntax.
```
# if the condition inside the <if statement> is false then the entire statement becomes false
# if the <if statement> is false (or !<if statement> is true) we execute other code
!(<if statement>) ? <code>;
```

# Loops
Loops work by using something similar to 'go to'.
```
place cheese <anchor name>; # create an anchor to return to

eat <anchor name>; # go to the anchor u previously created
```
Use a conditional to not have an infinite loop.
```
{
    place cheese <name>; 
    <code>;
    <condition> ? eat <name>;
};
```
You can NOT go to an anchor that's inside a different block.
```
# All of these will result in an error or undefined behavior
place cheese <name>;
{
    eat <name>;
};

{
    place cheese <name>;
};
eat <name>;
```

# Functions
### 1) Defining
```
define <function name>(<arguments>, <keyword arguments>) as <code>;
```
Example:
```
define my_function(a, b, c=4) as {
    grab a;
    grab b;
    give rat + swap; # b = b + a
    
    grab c;
    grab b;
    output rat * swap; # returns (a + b) * c   
};
```

### 2) Running functions
They're run using `()` after the variable.
```
grab <function name>;
rat();
```
Arguments are passed normally
```
rat(<exp1>, <exp2>, ...);
```
Keyword arguments are passed AFTER that.
```
rat(<*arguments>, <name1> = <exp1>, <name2> = <exp2>);
```
### 3) Returning values
Returning is done with the `output` keyword.
```
define <function name>(<arguments>, <keyword arguments>) as {
    <code>;
    output <exp>; # returns whatever is inside the <exp> and stop the function
    <other code>; # this won't get executed
};
```
Placing this keyword outside a function or a block will result in the termination of the program.

### 4) Variable management or something
Functions make a copy of the variables before their creation.
Meaning that if you have a variable `x` and it was 2 when the function was created, but you changed it to 4 after, the function will use 2 as its value.
On top of that the arguments overwrite the variables u had previously defined.

# Importing 
### 1) Syntax
```
import <file1>, <file2>, <file3>, ...;
```
Importing only works for files in the same directory as the one you're running it in.
Do NOT add .haram after the file name.
Example:
```
main.haram:
    import other; # no .haram in the name
    
other.haram:
    <code>;
```
### 2) Using imported files
To do that were going to use `.`.
```
import other;

grab other.my_variable;
grab other.my_function;
# and so on
```

# Python Integration
### 1) Built-in functions
These are already implemented in haram script, you just have to grab them.
```
grab print;
rat("Hello, World!");
```

### 2) Python modules
These can be imported using the `__import__` function
```
grab __import__; 
grab my_module;
give swap("my_module"); 
grab my_moudle; # making sure the current variable is the module
```
Importing modules from libraries is very similar to the code above.
```
grab __import__; 
grab my_module;
give swap("my_library.my_module");
grab my_module; # making sure the current variable is the module
```

### 3) Running python code
This is done using the `exec` function.
```
grab exec;
rat("print('Hello, World!')");
```
If you want to process variables using python you will have to pass the globals to `exec`.
```
adopt rat named globals;
grab globals;
give {
    "my_variable": 2
};
grab exec;
rat("print(f'the variable is {my_variable}')", swap);
```
