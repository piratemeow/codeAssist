import os 
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function
import time

model = "gemini-2.5-flash"
system_prompt = """
            You are a helpful AI coding agent that fixes python codes.

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
            When the user mentions directory he is refering to the working directory which is hard coded so you do not need to worry about that.
        
            When a user asks a question or makes a request, make a function call plan.
            You may need to make multiple function calls to perform on a single prompt.
            If one of the parameters is missing from the context, the prompt or you don't
            understand clearly. Just ask for the parameter or as about your confusions.
             
            You can perform the following operations:

            - List files and directories
            - Read file contents
            - Execute Python files with optional arguments
            - Write or overwrite files

            When the users ask about code project - they are refering to the working directory. 
            So you should typically start by looking at the project's files and figure out how to
            run the project and its tests. You should always want to test the tests and the actual program
            to verify that behavior is working. Also you should always want to test the code that you have written and
            verify if it is working as it is suppose to work. To test the code you should write test cases if it is more convenient. 

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

    
    messsages = [
        types.Content(role="user",parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
        function_declarations = [schema_get_files_info,
                                 schema_get_file_content,
                                 schema_run_python_file,
                                 schema_write_file],
    )

    max_iter = 20
    response = []
    for iter in range(0,max_iter):
        # time.sleep(20)
        response = client.models.generate_content(
            model = model,
            contents = messsages,
            config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
        )

        if response is None:
            print("Sorry! No Response")
            return
        
        for candidate in response.candidates:

            if candidate is None or candidate.content is None:
                continue
            messsages.append(candidate.content)
        
        if response.function_calls is None:
            return response
        
        
        function_calls = response.function_calls
        function_responses = []
        for function_call_part in function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_response = call_function(function_call_part,False)

            if function_call_response.parts[0].function_response.response is None:
                raise ValueError("There is no response for the function call")
            
            function_responses.append(function_call_response.parts[0])

            #adding the function responses to the context
            messsages.append(function_call_response)
            # print(f"-> {function_call_response.parts[0].function_response.response}")

        # messsages.append(*function_responses)

    
    
    return response

def print_response(response: types.GenerateContentResponse):
    if response:
        print(response.text)
    else:
        print("Response Not Found")
        return
    
def dev_related_stuff(api_key : str,prompt:list):
    client = genai.Client(api_key=api_key)

    """ To find the available models"""
    # for m in client.models.list():
    #     print(f"Name: {m.name}")
    #     print(f"Display: {m.display_name}")
    #     print("---")

    
    messsages = [
        types.Content(role="user",parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
        function_declarations = [schema_get_files_info,
                                 schema_get_file_content,
                                 schema_run_python_file,
                                 schema_write_file],
    )

    max_iter = 20
    response = []
    for iter in range(0,max_iter):

        response = client.models.generate_content(
            model = model,
            contents = messsages,
            config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
        )

        if response is None:
            print("Sorry! No Response")
            return
        
        response_text = response.text

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"Prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f'Response: {response_text}')
        print(f"Response tokens: {response_tokens}")
        
        for candidate in response.candidates:

            if candidate is None or candidate.content is None:
                continue
            messsages.append(candidate.content)
        
        if response.function_calls is None:
            print("No function calls made by the LLM")
            return
        
        
        function_calls = response.function_calls
        function_responses = []
        for function_call_part in function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_response = call_function(function_call_part,True)

            if function_call_response.parts[0].function_response.response is None:
                raise ValueError("There is no response for the function call")
            
            function_responses.append(function_call_response.parts[0])

            #adding the function responses to the context
            messsages.append(function_call_response)
            print(f"-> {function_call_response.parts[0].function_response.response}")

        # messsages.append(*function_responses)



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

    if verbose:
        dev_related_stuff(api_key,prompt)
    
    else :
        response = model_request_response(api_key,prompt)
        print_response(response)




main()