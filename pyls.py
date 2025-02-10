import json
import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# Load the JSON structure from the file
def load_structure(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return json.load(f)

# Convert size to human-readable format
def human_readable_size(size: int) -> str:
    for unit in ['B', 'K', 'M', 'G']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}T"

# Format the time modified
def format_time(epoch_time: int) -> str:
    return datetime.fromtimestamp(epoch_time).strftime('%b %d %H:%M')

# Print the contents of the directory
def print_contents(contents: List[Dict[str, Any]], long_format: bool, reverse: bool, sort_by_time: bool, filter_type: Optional[str], path: str) -> None:
    if sort_by_time:
        contents.sort(key=lambda x: x['time_modified'], reverse=reverse)
    elif reverse:
        contents.reverse()

    if filter_type:
        contents = [item for item in contents if (filter_type == 'dir' and 'contents' in item) or (filter_type == 'file' and 'contents' not in item)]

    for item in contents:
        if long_format:
            size = human_readable_size(item['size'])
            time_modified = format_time(item['time_modified'])
            print(f"{item['permissions']} {size} {time_modified} {path}/{item['name']}")
        else:
            print(item['name'], end=' ')
    if not long_format:
        print()

# Navigate through the structure based on the path
def navigate_structure(structure: Dict[str, Any], path: str) -> Optional[List[Dict[str, Any]]]:
    if path == '.' or path == '':
        return structure['contents']
    
    parts = path.split('/')
    current_contents = structure['contents']
    
    for part in parts:
        found = False
        for item in current_contents:
            if item['name'] == part:
                found = True
                if 'contents' in item:
                    current_contents = item['contents']
                else:
                    return [item]  # Return the file itself
                break
        if not found:
            print(f"error: cannot access '{path}': No such file or directory")
            return None
    return current_contents

# Main function to handle command-line arguments and execute the program
def main():
    parser = argparse.ArgumentParser(description="Python ls-like utility")
    parser.add_argument('path', nargs='?', default='.', help='Path to list (default: current directory)')
    parser.add_argument('-A', action='store_true', help='Include hidden files')
    parser.add_argument('-l', action='store_true', help='Use long listing format')
    parser.add_argument('-r', action='store_true', help='Reverse order')
    parser.add_argument('-t', action='store_true', help='Sort by time modified')
    parser.add_argument('--filter', choices=['file', 'dir'], help='Filter by file type')

    args = parser.parse_args()

    structure = load_structure('structure.json')
    contents = navigate_structure(structure, args.path)

    if contents is not None:
        if not args.A:
            contents = [item for item in contents if not item['name'].startswith('.')]
        print_contents(contents, args.l, args.r, args.t, args.filter, args.path)

if __name__ == "__main__":
    main()