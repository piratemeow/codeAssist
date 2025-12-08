
import os
from .config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory, file_name):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,file_name))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_name}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_name}"'
    
    file_content_string = ""
    try:
        with open(abs_file_path,"r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >=MAX_CHARS:
                file_content_string+= f'[...File "{file_name}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: An Exception {e} has occured while opening {abs_file_path}"

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within the working directory, truncated to 10,000 characters if too long. Ensures file path security by restricting access to the working directory only.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to read (e.g., 'script.py', 'README.md', 'data.txt'). Must be a regular file within the working directory. Paths like '../outside.txt' are blocked for security.",
            ),
        },
        required=["file_name"],
    ),
)


# print(get_file_content("calculator","lorem.txt"))