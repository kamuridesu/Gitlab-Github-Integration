import requests
try:
	from src import helpers
except:
	from .src import helpers


class GitlabManager:
	def __init__(self, config_file: str, user_id: str):
		self.user_id = user_id
		tokens: dict = helpers.read_json(config_file)
		self.GITLAB_API_TOKEN: str = tokens["GITLAB_API_TOKEN"]
		self.endpoints: dict = {
			"get_repos": f"https://gitlab.com/api/v4/users/{self.user_id}/projects?private_token={self.GITLAB_API_TOKEN}",
			"create_repo": f"https://gitlab.com/api/v4/projects?name=%reponame%",
			"delete_repo": f"https://gitlab.com/api/v4/projects/%repo_id%"
		}
		self.headers = {"Content-type": "application/json", "PRIVATE-TOKEN": self.GITLAB_API_TOKEN}

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
		post = requests.post(self.endpoints['create_repo'].replace(r"%reponame%", reponame), headers=self.headers)
		if post.status_code == 201:
			d = post.json()
			return {"ssh_url": d['ssh_url_to_repo'], "name": d['name']}

	def delete_repo(self, reponame: str) -> bool:
		repos: list = self.get_user_repos()
		for repo in repos:
			if reponame == repo['name']:
				repo_id: int = (repo['id'])
				post = requests.delete(self.endpoints['delete_repo'].replace(r"%repo_id%", str(repo_id)), headers=self.headers)
				if post.status_code == 202:
					return True
				break
		return False

	def run_sync(self, user_repos: list) -> bool:
		user_repos.append({"name": "YeyApp"})
		repos: list = self.get_user_repos()
		repo_names: list = []
		for repo in repos:
			repo_names.append({repo['name']: repo['ssh_url_to_repo']})

		for repo in user_repos:
			if repo['name'] not in [list(x.keys())[0] for x in repo_names]:
				print(f"Creating repo {repo['name']}")
				created = self.create_repo(repo['name'])
				if created:
					print(f"Syncing repo {repo['name']}")
					helpers.run_bash_to_sync_commits(created['ssh_url'], repo['ssh_url'], True, False)
					break
				# repo_names.append(repo['name'])


# glabMan = GitlabManager("tokens.json", 9218219)
# print(glabMan.delete_repo("test_integration"))