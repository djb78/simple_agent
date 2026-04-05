import os
import config

def get_file_content(working_directory, file_path):
    try:
        # get absolute path to target file
        absp_wdir = os.path.abspath(working_directory)
        absp_target = os.path.normpath( os.path.join(absp_wdir, file_path) )

        # verify that the absolute path of the target directory is valid
        target_valid = os.path.commonpath([absp_wdir, absp_target]) == absp_wdir
        if not target_valid:
                return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        # validate target file is a file
        if not os.path.isfile(absp_target):
                return f"Error: File not found or is not a regular file: \"{file_path}\""
                
        # get oontent
        MAX_CHARS = 10000 # should be set in config.py
        file = open(absp_target, "r")
        content = file.read(MAX_CHARS)

        # check for truncation
        if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content        
    except Exception as e:
          return f'Error: exception - {e}'
        
