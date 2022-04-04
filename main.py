from gitlabmanager import GitlabManager
from githubmanager import GithubManager


class Sync:
    def __init__(self, config_file: str, gitlab_id: str, github_username: str) -> None:
        self.gitlab_id = gitlab_id
        self.github_username = github_username
        self.gitlab_manager = GitlabManager(config_file, gitlab_id)
        self.github_manager = GithubManager(config_file, github_username)

    def run_sync(self, lab: bool = False, hub: bool = False) -> None:
        if lab:
            self.gitlab_manager.run_sync(self.github_manager.get_user_repos())
        if hub:
            self.github_manager.run_sync(self.gitlab_manager.get_user_repos())


if __name__ == "__main__":
    sync = Sync("tokens.json", "9218219", "kamuridesu")
    sync.run_sync(lab=True, hub=False)