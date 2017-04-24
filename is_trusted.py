import os
import sys
import subprocess

from github import Github


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def get_current_branch():
    label = subprocess.check_output(r"""git branch | grep \* | cut -d ' ' -f2""", shell=True)
    return label.decode().strip()


def is_internal_pull(repo):
    last_commit = subprocess.check_output(
        """git log -n 2 --pretty=format:"%H" | tail -1""", shell=True
        ).decode()
    prs = list(repo.get_pulls())
    print('[Branch Verifier] PR last sha is', last_commit)
    return last_commit in set(i.head.sha for i in prs)

def is_internal_branch(repo):
    branches = list(repo.get_branches())
    branch_names = [b.name for b in branches]
    current_branch = get_current_branch()
    print('[Branch Verifier] Current branch name is', current_branch)
    return current_branch in branch_names

def verify(repo_name):
    print('[Branch Verifier] Verifying repo:', repo_name)
    g = Github(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    repo = g.get_repo(repo_name)

    if not any([is_internal_branch(repo), is_internal_pull(repo)]):
        raise SystemExit('Untrusted branch detected')

    print('[Branch Verifier] Branch is valid')


if __name__ == '__main__':
    verify(sys.argv[1])
