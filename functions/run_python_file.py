import os
import subprocess

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