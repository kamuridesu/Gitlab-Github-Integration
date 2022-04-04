import requests
try:
    from src import helpers
except:
    from .src import helpers


class GithubManager:
    def __init__(self, config_file: str, username: str):
        self.username = username
        tokens: dict = helpers.read_json(config_file)
        self.GITHUB_API_TOKEN: str = tokens["GITHUB_API_TOKEN"]
        self.endpoints: dict = {
            "get_repos": f"https://api.github.com/users/{self.username}/repos",
            "create_repo": f"https://api.github.com/user/repos",
            "delete_repo": f"https://api.github.com/repos/{self.username}/%reponame%"
        }
        self.headers = {"Authorization": f"token {self.GITHUB_API_TOKEN}"}

    def get_user_repos(self) -> list:
        req = requests.get(self.endpoints['get_repos'])
        if req.status_code == 200:
            return req.json()

    def search_repo(self) -> list:
        repos: list = self.get_user_repos()
        repo_names: list = []
        for repo in repos:
            repo_names.append(repo['name'])
        return repo_names

    def create_repo(self, reponame: str) -> dict:
        repos: list = self.get_user_repos()
        repo_names: list = []
        for repo in repos:
            repo_names.append(repo['name'])

        if reponame in repo_names:
            reponame = reponame + helpers.generate_random_code()
        post = requests.post(self.endpoints['create_repo'], json={"name": reponame}, headers=self.headers)
        if post.status_code == 201:
            d = post.json()
            return {"ssh_url": d['ssh_url'], "name": d['name']}

    def delete_repo(self, reponame: str) -> bool:
        repos: list = self.get_user_repos()
        for repo in repos:
            if reponame == repo['name']:
                post = requests.delete(self.endpoints['delete_repo'].replace(r"%reponame%", str(repo['name'])), headers=self.headers)
                print(post)
                if post.status_code == 204:
                    return True
                break
        return False


ghubman = GithubManager("tokens.json", "kamuridesu")
print(ghubman.delete_repo("test_integration"))