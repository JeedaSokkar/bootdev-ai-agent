import os
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "...",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(abs_working_dir, directory))

        if not target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = ""

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            result += f"{item}: file_size={size} bytes, is_dir={is_dir}\n"

        return result

    except Exception as e:
        return f"Error: {e}"