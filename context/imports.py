"""
This helps determine which files import which ones, in a JavaScript/TypeScript project. 
"""

import os
import re
from typing import Dict, List, Set

def get_import_map(folder: str) -> Dict[str, Set[str]]:
    import_map = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".js") or file.endswith(".ts") or file.endswith(".tsx"):
                file_path = os.path.join(root, file)
                imports = get_imported_files(file_path)
                for imported_file in imports:
                    resolved_path = os.path.normpath(os.path.join(root, imported_file))
                    if resolved_path not in import_map:
                        import_map[resolved_path] = set()
                    import_map[resolved_path].add(file_path)
    return import_map

def get_imported_files(filepath: str) -> List[str]:
    with open(filepath, "r") as file:
        content = file.read()
    
    import_regex = re.compile(r"import .*?['\"](.*?)['\"]", re.MULTILINE)
    matches = import_regex.findall(content)
    
    return [match for match in matches if not match.startswith("http")]

def get_importing_files(filepath: str, folder: str) -> List[str]:
    import_map = get_import_map(folder)
    return list(import_map.get(filepath, set()))

# Example usage
folder = "/path/to/your/typescript/project"

import_map = get_import_map(folder)
print("Import Map:")
print(import_map)

filepath = "/path/to/your/typescript/project/some/file.ts"
importing_files = get_importing_files(filepath, folder)
print(f"Files importing {filepath}:")
print(importing_files)
