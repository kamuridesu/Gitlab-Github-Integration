from gitlabmanager import GitlabManager
from githubmanager import GithubManager


class Sync:
    def __init__(self, config_file: str, gitlab_id: str, github_username: str) -> None:
        self.gitlab_id = gitlab_id
        self.github_username = github_username
        self.gitlab_manager = GitlabManager(config_file, gitlab_id)
        self.github_manager = GithubManager(config_file, github_username)
    
    def sync_repos(self) -> None:
        gitlab_repos = self.gitlab_manager.get_user_repos()
        github_repos = self.github_manager.get_user_repos()
        for gitlab_repo in gitlab_repos:
            if gitlab_repo['name'] not in github_repos:
                self.github_manager.create_repo(gitlab_repo['name'])
        for github_repo in github_repos:
            if github_repo['name'] not in gitlab_repos:
                self.gitlab_manager.create_repo(github_repo['name'])
        for gitlab_repo in gitlab_repos:
            if gitlab_repo['name'] in github_repos:
                self.gitlab_manager.delete_repo(gitlab_repo['name'])
        for github_repo in github_repos:
            if github_repo['name'] in gitlab_repos:
                self.github_manager.delete_repo(github_repo['name'])