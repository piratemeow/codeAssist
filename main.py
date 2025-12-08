import os 
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


"""
list the contents of the pkg directory. there you will find the instructions test file. read the instructions from the file.  make a new main.py file and write the code as per instructed in the instructions file and then run the code
"""
def model_init() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key
    # print(api_key)

def model_request_response(api_key:str, prompt:str):
    client = genai.Client(api_key=api_key)

    """ To find the available models"""
    # for m in client.models.list():
    #     print(f"Name: {m.name}")
    #     print(f"Display: {m.display_name}")
    #     print("---")

    system_prompt = """
            You are a helpful AI coding agent that fixes python codes.

            When a user asks a question or makes a request, make a function call plan.
            You may need to make multiple function calls to perform on a single prompt.
            If one of the parameters is missing from the context, the prompt or you don't
            understand clearly. Just ask for the parameter or as about your confusions.
             
            You can perform the following operations:

            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
            """
    messsages = [
        types.Content(role="user",parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
        function_declarations = [schema_get_files_info,
                                 schema_get_file_content,
                                 schema_run_python_file,
                                 schema_write_file],
    )
    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = messsages,
        config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )
    return response

def print_response(response: types.GenerateContentResponse):
    if response:
        print(response.text)
    else:
        print("Response Not Found")
        return
    
def dev_related_stuff(prompt:list, response : types.GenerateContentResponse):
    

    if response is None:
        print("Response Not Found")
        return
    if response.usage_metadata is None:
        print("Response Metadata Not Found")
        return
    
    response_text = response.text

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f'Response: {response_text}')
    print(f"Response tokens: {response_tokens}")

    if response.function_calls is None:
        print("No function calls made by the LLM")
        return
    
    function_calls = response.function_calls

    for function_call_part in function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


def args_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt",type=str,help="Give your prompt")
    parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
    args = parser.parse_args()

    prompt = args.prompt
    verbose = args.verbose
    # print(verbose)

    return prompt,verbose



def main():

    # print(prompt)
    api_key = model_init()
    prompt,verbose = args_parser()
    response = model_request_response(api_key,prompt)

    if verbose:
        dev_related_stuff(prompt,response)
    
    else :
        print_response(response)




main()