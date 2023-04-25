"""
This file contains the code for fetching the commits that involve a particular file in the repository.
"""

import os
import subprocess
from typing import List, Dict, Union
from dataclasses import dataclass

@dataclass
class Change:
    change_type: str
    file: str

@dataclass
class Commit:
    commit_hash: str
    date: str
    message: str
    changes: List[Change]

def fetch_commits(file_path: str) -> List[Commit]:
    if not os.path.exists(file_path):
        raise ValueError("Invalid file path")

    directory = os.path.dirname(file_path)
    git_command = f"git log --pretty=format:'%H %ad %s' --date=short -- {file_path}"
    output = subprocess.check_output(git_command, shell=True, cwd=directory)
    decoded_output = output.decode("utf-8")
    lines = decoded_output.split("\n")

    commits = []
    for line in lines:
        if line:
            commit_hash, date, message = line.split(" ", 2)
            
            # Get the changes and other files modified in the commit
            diff_command = f"git diff-tree --no-commit-id --name-status -r {commit_hash}"
            diff_output = subprocess.check_output(diff_command, shell=True, cwd=directory)
            decoded_diff = diff_output.decode("utf-8")
            modified_files = decoded_diff.strip().split("\n")
            
            changes = []
            for modified_file in modified_files:
                if modified_file:
                    change_type, file_name = modified_file.split("\t", 1)
                    changes.append(Change(change_type, file_name))
            
            commits.append(Commit(commit_hash, date, message, changes))

    return commits


# Example usage
file_path = "./readme.md"
commits = fetch_commits(file_path)
print(commits)
