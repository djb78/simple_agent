
# get_files_info.py
import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory='.'):
    try:
        # get absolute path to target directory
        absp_wdir = os.path.abspath(working_directory)
        absp_target = os.path.normpath( os.path.join(absp_wdir, directory) )

        # verify that the absolute path of the target directory is valid
        target_valid = os.path.commonpath([absp_wdir, absp_target]) == absp_wdir
        if not target_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # validate target directory is a directory
        if not os.path.isdir(absp_target):
            return f'Error: "{directory}" is not a directory'

        # contents = []
        contents_strings = []
        for child in os.listdir(absp_target):
            child_path = os.path.normpath( os.path.join(absp_target, child) )
            child_size = os.path.getsize(child_path)
            child_isdir = os.path.isdir(child_path)
            # child_isfile = os.path.isfile(child)

            # contents.append( (child, child_size, child_isdir) )

            contents_strings.append(f"- {child}: file_size={child_size} bytes, is_dir={child_isdir}")
        return "\n".join(contents_strings)
    except Exception as e:
        return f"Error: exception - {e}"
    
# Gemini API schema to describe the function for LLM callers    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)