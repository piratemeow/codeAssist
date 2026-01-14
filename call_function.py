from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


working_directory = "./calculator"

functions_dict = {
    "get_file_content" : get_file_content,
    "get_files_info" : get_files_info,
    "run_python_file" : run_python_file,
    "write_file" : write_file

}


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        # print(function_call_part.args)
        # print(f" - Calling function: {function_call_part.name}   {function_call_part.args}")
        if function_call_part.name == 'get_files_info':
            if 'directory' in function_call_part.args:
                print(f" - Getting the contents of {working_directory}/{function_call_part.args['directory']} directory")
            else:
                print(f" - Getting the contents of {working_directory} directory")
        elif function_call_part.name == 'run_python_file':
            print(f" - Executing {working_directory}/{function_call_part.args['file_path']} file")
        elif function_call_part.name == 'write_file':
            print(f" - Writing to {working_directory}/{function_call_part.args['file_path']} file")
        elif function_call_part.name == 'get_file_content':
            print(f" - Reading the contents of {working_directory}/{function_call_part.args['file_name']} file")

    
    if function_call_part.name not in functions_dict:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

    else:
        function_result = functions_dict[function_call_part.name](working_directory,**function_call_part.args)
        # print(function_result)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )

