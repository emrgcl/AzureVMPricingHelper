import os
import re
from stdlib_list import stdlib_list

def get_imports_from_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    patterns = [
        r'^import (\S+)',
        r'^from (\S+) import'
    ]
    
    imports = set()
    for line in file_content.split('\n'):
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                imports.add(match.group(1).split('.')[0])

    return imports

def get_non_standard_libs(directory):
    standard_libs = set(stdlib_list())
    non_standard_libs = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = get_imports_from_file(file_path)
                non_standard_libs.update(imports.difference(standard_libs))

    return non_standard_libs

def save_requirements(libs, file_name='requirements.txt'):
    with open(file_name, 'w') as file:
        for lib in sorted(libs):
            file.write(f'{lib}\n')
    return file_name

if __name__ == '__main__':
    directory = input("Enter the directory path to scan: ")
    non_standard_libs = get_non_standard_libs(directory)
    file_name = save_requirements(non_standard_libs)
    print(f"Non-standard libraries saved to {file_name}")
