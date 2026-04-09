
import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
            # get absolute path to target file
            absp_wdir = os.path.abspath(working_directory)
            absp_target = os.path.normpath( os.path.join(absp_wdir, file_path) )

            # verify that the absolute path of the target directory is valid
            target_valid = os.path.commonpath([absp_wdir, absp_target]) == absp_wdir
            if not target_valid:
                    return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
            
            # confirm file_path doesn't refer to a directory
            if os.path.isdir(absp_target):
                  return f"Error: Cannot write to \"{file_path}\" as it is a directory"

            # validate target file is a file
            #if not os.path.isfile(absp_target):
            #    return f"Error: File not found or is not a regular file: \"{file_path}\""

            # confirm all parent directories of file_path exist
            os.makedirs(os.path.dirname(absp_target), exist_ok=True)

            # open file in write mode    
            with open(absp_target, "w") as file:
                file.write(content)

            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
            return f"Error: exception - {e}"
    
# Gemini API schema to describe the function for LLM callers    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Safely creates or overwrites files in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="relative path from the working directory of the file to be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content that will be written to the file designated by file_path",
            ),
        },
    ),
)

    
