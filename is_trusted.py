import os
import subprocess

from github import Github


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def get_current_branch():
    label = subprocess.check_output(["git branch | grep \* | cut -d ' ' -f2"])
    return label.decode().strip()


def verify(repo_name):
    g = Github(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    repo = g.get_repo(repo_name)

    branches = list(repo.get_branches())
    branch_names = [b.name for b in branches]

    current_branch = get_current_branch()
    print('[Branch Verifier] Current branch name is', current_branch)

    if current_branch not in branch_names:
        raise SystemExit('Untrusted branch detected')


if __name__ == '__main__':
    verify()
