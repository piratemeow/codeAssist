import os
from google.genai import types
def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir)
            except Exception as e:
                return f"Error: Could not create parent directory {parent_dir} exception {e}"
        
    
    try:
        with open(abs_file_path,"w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Faile to make file: {file_path, {e}}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file. Creates necessary parent directories if they don't exist. Overwrites existing files. Access restricted to working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path where the file should be written (e.g., 'data/output.txt', 'script.py'). Relative to working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
