import os

import argparse

"""
- README.md: file_size=1032 bytes, is_dir=False
- src: file_size=128 bytes, is_dir=True
- package.json: file_size=1234 bytes, is_dir=False
"""

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working_dir,directory))

    # print(abs_working_dir,abs_directory)
    # print(os.path.isdir(abs_directory))

    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
        

    if not abs_directory.startswith(abs_working_dir):
        # print("/".join([abs_working_dir,directory]),abs_directory)
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    contents = os.listdir(abs_directory)
    final_response = ""
    for content in contents:
        content_path = "/".join([abs_directory,content])
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        final_response+= f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"
    
    return final_response



# parser = argparse.ArgumentParser()
# parser.add_argument("working_directory",type=str,help="give me working directory")
# parser.add_argument("directory",type=str,help="give me directory")
# args = parser.parse_args()

# response = get_files_info(args.working_directory,args.directory)

# print(response)
    


    