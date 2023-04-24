"""
Various git utilies for usage by the agents.
"""

import os
import subprocess
import requests

def execute_git_command(git_command, cwd):
    output = subprocess.check_output(git_command, shell=True, cwd=cwd)
    return output.decode("utf-8")

def create_branch(branch_name, repo_path):
    git_command = f"git checkout -b {branch_name}"
    execute_git_command(git_command, repo_path)

def get_current_changes(repo_path):
    git_command = "git diff"
    return execute_git_command(git_command, repo_path)

def commit_changes(commit_message, repo_path):
    git_command = f"git add . && git commit -m '{commit_message}'"
    execute_git_command(git_command, repo_path)

def get_current_branch(repo_path):
    git_command = "git symbolic-ref --short HEAD"
    return execute_git_command(git_command, repo_path).strip()

def list_branches(repo_path):
    git_command = "git branch"
    output = execute_git_command(git_command, repo_path)
    return output.split("\n")

def create_pull_request(repo_path, title, head, base, body):
    # Extract the repository owner and name from the remote URL
    git_command = "git config --get remote.origin.url"
    remote_url = execute_git_command(git_command, repo_path).strip()
    owner, repo_name = remote_url.split("/")[-2:]
    repo_name = repo_name.replace(".git", "")

    token = os.environ.get("GITHUB_TOKEN")
    if (token is None):
        raise Exception("GITHUB_TOKEN environment variable is not set.")

    # Create a pull request using the GitHub API
    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    headers = {"Authorization": f"token {token}"}
    data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body,
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create pull request: {response.text}.")