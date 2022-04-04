import pathlib
import json
import random
import string


def generate_random_code():
	return str("".join([random.choice(string.ascii_letters + str(string.digits)) for _ in range(5)]))


def read_json(file_path: str) -> str:
    # return json.loads((pathlib.Path(__file__).parent.absolute() / file_path).read_text(encoding="utf-8"))
    with open(file_path, "r") as f:
        return json.load(f)