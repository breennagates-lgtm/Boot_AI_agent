import os
import subprocess
import types
from google.genai import types





def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_file = os.path.commonpath([absolute_working_dir, target_file_path]) == absolute_working_dir
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, cwd=absolute_working_dir, timeout=30)

        output= ""
        if result.returncode!=0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += f"No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file= types.FunctionDeclaration( 
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory with optional command-line arguments, capturing and returning the output and errors",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Command-line argument to pass to the Python file",
                ),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)