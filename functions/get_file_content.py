
import types

import types
from google.genai import types
from config import MAX_CHARS
import os


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_file = os.path.commonpath([absolute_working_dir, target_file_path]) == absolute_working_dir
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a maximum character limit to prevent excessive output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)