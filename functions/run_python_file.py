import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # get absolute path to target directory
        absp_wdir = os.path.abspath(working_directory)
        absp_target = os.path.normpath( os.path.join(absp_wdir, file_path) )

        # verify that the absolute path of the target directory is valid
        target_valid = os.path.commonpath([absp_wdir, absp_target]) == absp_wdir
        if not target_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # validate file_path exists and points to a regular file
        if not os.path.isfile(absp_target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absp_target]
        if args is not None:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = ''
        if result.returncode == 0:
            output += f'Process exited with code {result.returncode}\n'
        if not result.stdout and not result.stderr:
            output += f'No output produced\n'
        output += f'STDOUT: {result.stdout}\n'
        output += f'STDERR: {result.stderr}\n'

        return output
    except Exception as e:
        return f'Error: executing Python file: {e}'
     
# potential refactorization

#def validate_path(working_directory, target_path):
#    abs_working_dir = os.path.abspath(working_directory)
#    abs_target = os.path.normpath(os.path.join(abs_working_dir, target_path))
#    if os.path.commonpath([abs_working_dir, abs_target]) != abs_working_dir:
#        return abs_working_dir, abs_target, "outside"
#    return abs_working_dir, abs_target, None

# Or even simpler, return a tuple of (abs_working_dir, abs_target, is_valid) so callers can still compose their own error messages.
# If this were a production codebase, you'd absolutely want a shared utility like functions/path_utils.py to house it.
    
# Gemini API schema to describe the function for LLM callers    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs code from a python file with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="relative path from the working directory of the file to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="array containing the command line arguments to be included when running the file at file_path",
                items=types.Schema(
                     type=types.Type.STRING,
                )
            ),
        },
    ),
)