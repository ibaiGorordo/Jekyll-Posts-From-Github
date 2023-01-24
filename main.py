from RepoToPost import RepoToPost
from GithubParser import GithubParser

access_token = None
github_user = 'ibaiGorordo'

parser = GithubParser(access_token)
repositories = parser(github_user)

RepoToPost.write_posts(repositories)
