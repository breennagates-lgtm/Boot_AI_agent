from html import parser
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
        function_responses = []
        for function_call in response.function_calls:

            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call result does not contain parts")

            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function call result part does not contain function response")  
             
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Function call result part does not contain response field")
            
            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()

