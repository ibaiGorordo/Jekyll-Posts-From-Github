import datetime
from tqdm import tqdm
from dataclasses import dataclass
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository


@dataclass
class Repository:
    name: str
    fullname: str
    creation_date: datetime
    last_update_date: datetime
    url: str
    topics: list
    language: str
    repo: object


class GithubParser:
    def __init__(self, token=None):
        self.g = Github(token)

    def __call__(self, username):
        return self.parse_repositories(username)

    def parse_repositories(self, username) -> list:
        repos = []

        repo_names = self.list_repositories(username)
        repo_count = repo_names.totalCount
        print(f"Found {repo_count} repositories for user {username}. Parsing...")
        for repo_name in tqdm(repo_names, total=repo_count):
            repo = self.g.get_repo(repo_name.full_name)
            name = repo_name.name.replace('-', ' ')
            topics = repo.get_topics()
            repository = Repository(name, repo.full_name, repo.created_at, repo.updated_at, repo.html_url, topics, repo.language, repo)
            repos.append(repository)
        print("Finished parsing repositories!")
        return repos

    def list_repositories(self, username) -> PaginatedList:
        return self.g.search_repositories(query='user:' + username)


if __name__ == '__main__':
    # TODO.md: Edit your token and username
    access_token = None
    username = 'ibaiGorordo'

    parser = GithubParser(access_token)
    repositories = parser(username)
    for repository in repositories:
        print(repository)
