import os
from wsgiref import types
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_file = os.path.commonpath([absolute_working_dir, target_file_path]) == absolute_working_dir
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, ensuring the file path is valid and does not point to a directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)   