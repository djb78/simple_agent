from functions.run_python_file import run_python_file

print("TEST: main.py")
print(run_python_file("calculator", "main.py"))
print("TEST: main.py \"3 + 5\"")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("TEST: tests.py")
print(run_python_file("calculator", "tests.py"))
print("TEST: ../main.py")
print(run_python_file("calculator", "../main.py"))
print("TEST: nonexistent.py")
print(run_python_file("calculator", "nonexistent.py"))
print("TEST: lorem.txt")
print(run_python_file("calculator", "lorem.txt"))
