from html import parser
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
   
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

   
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    client = genai.Client(api_key=api_key)
    
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]   
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = messages, 
        config=config,)
    if response.usage_metadata is None:
        raise RuntimeError("Response does not contain usage metadata")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    
    if not response.function_calls:
        print("Response:", response.text)
    else:
        for function_call in response.function_calls:
            print (f"Calling function: {function_call.name}({function_call.args})")
            
if __name__ == "__main__":
    main()
