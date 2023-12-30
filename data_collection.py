import ast
import csv
import dataclasses
import os

DIR_PATH = "/Users/aku314/Downloads/django-main/"


@dataclasses.dataclass
class CustomFunction:
    name: str
    body: str
    context: str
    file_name: str


def walk(node, context, lines, file_name):
    res = []
    if isinstance(node, ast.ClassDef):
        for el in node.body:
            res.extend(walk(el, context + node.name + ";", lines, file_name))
    elif isinstance(node, ast.FunctionDef):
        start_line = node.body[0].lineno
        end_line = node.body[-1].end_lineno
        function_body = "".join(lines[start_line - 1:end_line])
        res.append(
            CustomFunction(name=node.name, body=function_body, context=context,
                           file_name=file_name))
        for el in node.body:
            res.extend(walk(el, context + node.name + ";", lines, file_name))
    else:
        if hasattr(node, 'body'):
            for el in node.body:
                res.extend(walk(el, context, lines, file_name.removeprefix(DIR_PATH)))
    return res


def find_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def write_in_csv(fun_list):
    header = ['Name', 'Body', 'Context', 'File name']
    csv_file_path = 'django.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, 'excel-tab')
        writer.writerow(header)
        for func in fun_list:
            writer.writerow([func.name, func.body, func.context, func.file_name])


if __name__ == '__main__':
    files = find_python_files(DIR_PATH)

    fun_data = []
    for file in files:
        with open(file, 'r') as f:
            try:
                lines = f.readlines()
                tree = ast.parse("".join(lines))
                fun_data.extend(walk(tree, "", lines, f.name))
            except:
                print("Error with file " + file)

    write_in_csv(fun_data)
