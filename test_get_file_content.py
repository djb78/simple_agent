from functions.get_file_content import get_file_content

lorem = get_file_content("calculator", "lorem.txt")
if len(lorem) < 10000:
    print("lorem.txt is too short")    
if lorem[-1] is not ']':
    print("missing truncation message")
else:
    print(f"lorem.txt is longer than 10000 characters, truncation message present")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))

