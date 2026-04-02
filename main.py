import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    prompts = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    # send request with user prompt
    answer = client.models.generate_content(model=model, contents=prompts)

    # VERBOSE output
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        # display usage data for this request
        if not answer.usage_metadata:
            raise RuntimeError("no response metadata, possible failed API request")
        print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")

    # display response to request
    print(f"Response: {answer.text}")


if __name__ == "__main__":
    main()