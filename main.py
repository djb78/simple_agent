import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    # get api key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("no api key found")
    # setup Client object
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.5-flash' # model to use

    # setup command line parser to bring in user input
    parser = argparse.ArgumentParser(description="ai prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("prompt", type=str, help="prompt for Gemini")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    # agent feedback loop
    for _ in range(20):
        # send request with user prompt
        answer = client.models.generate_content(
            model=model, 
            contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        if answer.candidates:
            for candidate in answer.candidates:
                messages.append(candidate.content)

        if not answer.usage_metadata:
            raise RuntimeError("no response metadata, possible failed API request")
        
        if args.verbose:
            print(f"User prompt: {args.prompt}")
            print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")

        # display response to request
        if answer.function_calls is None:
            print(f"Response: {answer.text}")
            return 0
        else:
            function_results = []
            # calls functions based on LLM response
            for function in answer.function_calls:
                function_result = call_function(function)

                # verifies that some response came back from the function call
                if not function_result.parts:
                    raise Exception("no .parts list associated with function_result")
                if function_result.parts[0].function_response is None:
                    raise Exception("function_result.parts[0].function_response is None")
                if function_result.parts[0].function_response.response is None:
                    raise Exception("function_result.parts[0].function_response.response is None")
                
                function_results.append(function_result.parts[0])

                if args.verbose:
                    print(f"-> {function_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))

    print("agent loop exceeded max iterations")
    sys.exit(1)



if __name__ == "__main__":
    main()