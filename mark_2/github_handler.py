from github import Github
from github.GithubException import GithubException

class GitHubHandler:
    def __init__(self, token, repo_owner, repo_name):
        self.github = Github(token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")

    def get_new_issues(self):
        return self.repo.get_issues(state='open', labels=['ai-coder'])

    def create_branch(self, branch_name):
        try:
            main_branch = self.repo.get_branch("main")
            self.repo.create_git_ref(f"refs/heads/{branch_name}", main_branch.commit.sha)
            print(f"Created branch: {branch_name}")
        except GithubException as e:
            print(f"Error creating branch: {e}")

    def create_pull_request(self, branch_name, description, issue_number):
        try:
            pr = self.repo.create_pull(
                title=f"AI Coder: Update for issue #{issue_number}",
                body=description,
                head=branch_name,
                base="main"
            )
            print(f"Created pull request: {pr.html_url}")
        except GithubException as e:
            print(f"Error creating pull request: {e}")
