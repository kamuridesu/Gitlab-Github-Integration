import json
import random
import string
import subprocess as sp
from subprocess import PIPE


def generate_random_code():
	return str("".join([random.choice(string.ascii_letters + str(string.digits)) for _ in range(5)]))


def read_json(file_path: str) -> str:
    # return json.loads((pathlib.Path(__file__).parent.absolute() / file_path).read_text(encoding="utf-8"))
    with open(file_path, "r") as f:
        return json.load(f)


def run_bash_to_sync_commits(gitlab_ssh_url: str, github_ssh_url: bool, gitlab: bool = False, github: bool = False) -> None:
    if gitlab:
        print("bash", "./github_sync.sh", gitlab_ssh_url, github_ssh_url)
        sp.run(["bash", "./github_sync.sh", gitlab_ssh_url, github_ssh_url], stdout=PIPE, stderr=PIPE)
    if github:
        sp.run(["bash", "./gitlab_sync.sh", github_ssh_url, gitlab_ssh_url], stdout=PIPE, stderr=PIPE)
