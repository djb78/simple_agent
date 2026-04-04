
#test_get_files_info.py

from functions.get_files_info import get_files_info

def add_indentation(result):
    result_lines = result.split("\n")
    indented_lines = []
    for line in result_lines:
        indented_lines.append(f"  {line}")
    return "\n".join(indented_lines)

def get_result(sub_directory):
    result = get_files_info("calculator", sub_directory)  
    if sub_directory == '.':
        sub_directory = 'current'
    else:
        sub_directory = f"'{sub_directory}'"
      
    return f"Result for {sub_directory} directory:\n{add_indentation(result)}"

print( get_result(".") )
print( get_result("pkg") ) 
print( get_result("/bin") )
print( get_result("../") )
