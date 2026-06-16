import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from google.genai import types

def main():
    load_dotenv()
   
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #create a gemini client using the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    client = genai.Client(api_key=api_key)
    
    #creates ca conversation history
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]   
    #creates a config for the model 
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
    #loop that continues until a final response is generated or the maximum number of iterations is reached
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents = messages, 
            config=config,)
        
        #check if the response contains candidates and append their content to the conversation history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        #check if the response contains usage metadata and print token counts if verbose flag is set
        if response.usage_metadata is None:
            raise RuntimeError("Response does not contain usage metadata")
        else:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        #  check if the response contains function calls and handle them accordingly
        if not response.function_calls:
            print("Response:", response.text)
            return 
        
        # if the response contains function calls, call the functions and append their responses to the conversation history
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            
            # check if the function call result contains parts and a function response with a response field, and raise an error if any of these are missing
            if not function_call_result.parts:
                raise RuntimeError("Function call result does not contain parts")
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Function call result part does not contain function response")  
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Function call result part does not contain response field")
            
            # append the response from the function call to the list of function responses 
            function_responses.append(function_call_result.parts[0])
    
            # if verbose flag is set, print the response from the function call
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_responses))

    # if the loop completes without returning, it means the maximum number of iterations has been reached without a final response, so we print a message and exit with an error code
    print("Maximum iterations reached")
    sys.exit(1)
      
    


if __name__ == "__main__":
    main()

