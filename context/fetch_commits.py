"""
This file contains the code for fetching the commits that involve a particular file in the repository.
"""

import os
import subprocess

def fetch_commits(file_path):
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
            commit = {"hash": commit_hash, "date": date, "message": message}
            
            # Get the changes and other files modified in the commit
            diff_command = f"git diff-tree --no-commit-id --name-status -r {commit_hash}"
            diff_output = subprocess.check_output(diff_command, shell=True, cwd=directory)
            decoded_diff = diff_output.decode("utf-8")
            modified_files = decoded_diff.strip().split("\n")
            
            changes = []
            for modified_file in modified_files:
                if modified_file:
                    change_type, file_name = modified_file.split("\t", 1)
                    changes.append({"type": change_type, "file": file_name})
            
            commit["changes"] = changes
            commits.append(commit)

    return commits

# Example usage
file_path = "./readme.md"
commits = fetch_commits(file_path)
print(commits)
