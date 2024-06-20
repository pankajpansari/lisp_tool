import random
import string

def construct_prompt(df, n):
    prompt = """
The programming language we're discussing has a unique syntax that is centred around functional programming and recursion. Here's a breakdown of some key elements:

atoms: An atom is a single, indivisible value such as a number, boolean, or symbol.
lists: A list is a compound data structure that contains an ordered sequence of elements, which can be atoms or other lists.
S-expressions (Symbolic Expressions): S-expressions are the primary syntactic constructs in the language, consisting of atoms or lists enclosed in parentheses.
#t and #f: These represent the boolean values true and false, respectively.

The language uses prefix notation, where the operator or function comes before its operands or arguments, enclosed in parentheses. It also supports recursion, where the function calls itself with a smaller portion of the list until the base case is reached.

Here are some primtive functions in this programming language.

car : gives first S-expression of a list
defined only for non - empty lists, returns a S - expression

cdr : gives list l without (by removing) rac l
defined only for non - empty lists, returns a list

cons : adds an S - expression to the front of a list
takes two arguments, second must be a list. output is a list

null? : checks whether a list is empty list
defined only for lists

atom? : checks whether it is an atom
takes one argument (any S - expression)

eq? : checks if two non numeric atoms are equal

Here are the keywords forming the syntax of the language. 
define: This keyword is used for function definitions. 
lambda: This keyword is used to create anonymous functions and expressions. It takes a list of arguments and a body of expressions to be evaluated.
cond: This keyword is used for conditional branching. It evaluates a series of test expressions and evaluates the corresponding expression for the first test that evaluates to true.
else: This keyword is used in the conditional expression to specify the expression to be evaluated if none of the previous test expressions are true.
(): This represents the empty list, often used as a terminating condition in recursive list operations.

Here is an example for how these keywords form a function : 
    
(define lat?
(lambda (l)
(cond
((null? l) #t )
(( atom? ( car l)) (lat? ( cdr l)))
(else #f )))) 
 
Here are some existing functions and a brief explanation of what they do :
    
"""
    fn_names = list(df['FunctionName'])
    fn_explanations = list(df['Explanation'])
    
    for each in range(n):
        string = fn_names[each] + " : " + fn_explanations[each] + "\n\n"
        prompt = prompt + string
        
    prompt = prompt + "I want to form a function that does the following : \n\n"
    
    fn = fn_names[n] + " : " + fn_explanations[n] + "\n"
    
    prompt = prompt + fn
        
    final_str = """
Help me write the code. Output only the code for the function directly, do not include anything else. Make sure to use the correct keywords like lambda, cond, define and close all brackets correctly.
"""
    prompt = prompt + final_str
    
    return prompt 

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_encodings():
    primitives = ['car', 'cdr', 'cons', 'null', 'atom', 'eq']
    keywords = ['define', 'lambda', 'cond', 'else']
    
    encodings = dict()
    
    for each in primitives : 
        encodings[each] = each[::-1]
        
    for each in keywords:
        encodings[each] = random_string(len(each))
        
    return encodings

def encode_prompt(prompt):
    encode_dict = get_encodings()
    for key in encode_dict:
        prompt = prompt.replace(key, encode_dict[key])
    return prompt
    
def decode_output(txt):
    encode_dict = get_encodings()
    decode_dict = {value: key for key, value in encode_dict.items()}
    for key in decode_dict:
        txt = txt.replace(key, decode_dict[key])
    return txt
