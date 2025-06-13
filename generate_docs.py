import os

OUTPUT_FILENAME = "all_source_code.md"

EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    "venv",
    ".vscode",
}

EXCLUDE_FILES = {
    OUTPUT_FILENAME,
    "generate_docs.py",
    "shop.db",
    "shop.db-journal"
}

LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".html": "html",
    ".css": "css",
    ".md": "markdown",
    ".txt": "text",
    ".json": "json",
}

def generate_source_code_markdown():
    print("🚀 Starting source code compilation into Markdown...")
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as outfile:
        outfile.write("# Project Source Code\n\n")
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            files.sort()
            for filename in files:
                if filename in EXCLUDE_FILES:
                    continue
                file_path = os.path.join(root, filename)
                _, extension = os.path.splitext(filename)
                language = LANGUAGE_MAP.get(extension, "")
                md_file_path = file_path.replace("\\", "/")
                outfile.write(f"## File: `{md_file_path}`\n\n")
                outfile.write(f"```{language}\n")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {e}")
                outfile.write("\n```\n\n---\n\n")
                print(f"   Processed: {file_path}")
    print(f"\n✅ Successfully generated all source code into `{OUTPUT_FILENAME}`")

if __name__ == "__main__":
    generate_source_code_markdown()
