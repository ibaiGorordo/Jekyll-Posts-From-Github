import datetime
from tqdm import tqdm
from dataclasses import dataclass
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository


@dataclass
class Repository:
    name: str
    creation_date: datetime
    last_update_date: datetime
    url: str
    repo: object


class GithubParser:
    def __init__(self, token=None):
        self.g = Github(token)

    def __call__(self, username):
        return self.parse_repositories(username)

    def parse_repositories(self, username) -> list:
        repos = []

        repo_names = self.list_repositories(username)
        print(f"Found {repo_names.totalCount} repositories for user {username}. Parsing...")
        for repo_name in tqdm(repo_names):
            repo = self.g.get_repo(repo_name.full_name)
            name = repo_name.name.replace('-', ' ')
            repository = Repository(name, repo.created_at, repo.updated_at, repo.html_url, repo)
            repos.append(repository)
        print("\nFinished parsing repositories!")
        return repos

    def list_repositories(self, username) -> PaginatedList:
        return self.g.search_repositories(query='user:' + username)


if __name__ == '__main__':
    # TODO: Edit your token and username
    access_token = None
    username = 'ibaiGorordo'

    parser = GithubParser(access_token)
    repositories = parser(username)
    for repository in repositories:
        print(repository)
