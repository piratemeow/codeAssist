import os
import subprocess
from google.genai import types
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

    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file (.py) within the working directory with optional arguments. Captures STDOUT, STDERR, and exit code. 30-second timeout for preventing infinite loops. Paths outside working directory are blocked for security.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file (.py) relative to working directory (e.g., 'script.py', 'utils/calc.py'). It will only accept a python (.py) file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of command line arguments to pass to the Python script (e.g., ['5', '3', '--verbose']).",
            ),
        },
        required=["file_path"],
    ),
)
