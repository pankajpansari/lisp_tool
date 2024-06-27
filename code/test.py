import subprocess
import tempfile

def generate_tests(code, file, n) : 
    test_dict = dict()
    for i in range(1, 4) : 
        test_name = f'Test{i}'
        test_code = file.at[n, test_name]
        test_output = f'Res{i}'
        output_res = file.at[n, test_output]
        atom_def = """
        (define atom?
          (lambda (x)
            (and (not (pair? x)) (not (null? x)))))
        """
        scheme_code = atom_def + "\n" + code + "\n" + test_code
        test_dict[scheme_code] = output_res
        
    return test_dict

def run_tests(code, file, n):
    
    test_dict = generate_tests(code, file, n)
    result = True
    
    for code in test_dict.keys() : 
        # temporary file 
        with tempfile.NamedTemporaryFile(delete=False, suffix=".scm") as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name
        
        # run temp file
        result = subprocess.run(["guile", temp_file_path], capture_output=True, text=True)
        
        output = result.stdout
        errors = result.stderr
    
        subprocess.run(["rm", temp_file_path])
        
        print(output)
        print(errors)
        #print(test_dict[code])
        
        if output != test_dict[code] : 
            result = False
        
    return result
