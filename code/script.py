import os
import pandas as pd
from together import Together
from tools import construct_prompt, encode_prompt, decode_output
from test_tools import run_tests

os.environ['TOGETHER_API_KEY'] = '7191a5043c49e74068692dba6a6bded2e7b28e07f0695c94fbf78b02fe509c11'

api_key = os.environ.get("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the TOGETHER_API_KEY environment variable.")
    
file = pd.read_csv('functions.csv')

print(file)
print(file.shape[0])

def LLMCall(file, n):
    # n refers to function number (index in functions.csv)
    
    prompt = encode_prompt(construct_prompt(file, n))
    
    client = Together(api_key=api_key)
    
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    response1 = client.chat.completions.create(
        model="mistralai/Mixtral-8x22B-Instruct-v0.1", #meta-llama/Llama-3-70b-chat-hf
        messages=messages,
        temperature=0.1
    )
    
    response1_content = response1.choices[0].message.content
    #print("Output:", response1_content)
    
    return response1_content

def write(file, i, code):
    file.at[i, 'Definition'] = code
    file.to_csv('functions2.csv', index=False)
    
def write_error(file, i):
    file.at[i, 'Definition'] = 'Unable to generate valid function'
    file.to_csv('functions2.csv', index=False)
    
for i in range(file.shape[0]):
    code = decode_output(LLMCall(file, i))
    print(code + "\n")
    write(file, i, code)

"""for i in range(file.shape[0]):
    samples = 0
    max_samples = 50
    for j in range(max_samples) : 
        code = decode_output(LLMCall(file, i))
        print(code)
        if run_tests(code, file, i) == True : 
            # write definition to functions.csv and break
            write(file, i, code)
            success = True
            break    
    if success == False : 
        write_error(file, i)
        # store failure
"""
