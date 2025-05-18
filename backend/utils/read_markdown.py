def read_markdown(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
