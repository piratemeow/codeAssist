import os 
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def model_init():
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
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messsages
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