import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,file_path))

    # print(abs_working_dir,abs_file_path)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if os.path.splitext(abs_file_path)[1]!= ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        output = subprocess.run(
            ["python3", abs_file_path, *args], 
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True)
        final_string = f"""
                STDOUT: {output.stdout},
                STDERR: {output.stderr}
"""
        if output.stderr=="" and output.stdout=="":
            final_string = "No output produced\n"
        if output.returncode!=0:
            final_string+=f"Process exited with code {output.returncode}"

        return final_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

    
