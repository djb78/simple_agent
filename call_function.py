from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from google import genai
from google.genai import types

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

def call_function(function_call, verbose=False):
    # function_call = types.FunctionCall object
    # verbose = boolean

    # handles verbose flag
    if verbose:
        print(f"Calling Function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # maps functions to string representations of their names
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # ensures function name exists and is a string
    function_name = function_call.name or ""

    # handles unsupported function names
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    
    # creates a shallow copy of function_call.args
    args = dict(function_call.args) if function_call.args else {}

    # sets the hard-coded working directory
    args["working_directory"] = "./calculator"

    # assigns the return value of the function to a variable
    function_result = function_map[function_name](**args)

    # returns function_result via types.Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
