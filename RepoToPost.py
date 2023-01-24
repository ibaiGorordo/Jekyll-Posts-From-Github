import re
from tqdm import tqdm
from GithubParser import GithubParser


class RepoToPost:

    @staticmethod
    def write_posts(repositories, post_dir_path="../../_posts"):
        print("Writing posts...")
        for repository in tqdm(repositories):
            RepoToPost.write_post(repository, post_dir_path)
        print("Finished writing posts!")

    @staticmethod
    def write_post(repository, post_dir_path):
        contents = repository.repo.get_contents("README.md").decoded_content.decode('utf-8')
        contents = RepoToPost.remove_title(contents)
        contents = RepoToPost.fix_image_links(contents)
        contents = RepoToPost.fix_urls(contents)

        img_url, alt_text = RepoToPost.get_header_img(contents)

        file_path = RepoToPost.get_post_path(repository, post_dir_path)
        title = repository.name.replace('-', ' ')
        creation_date = repository.creation_date.strftime('%Y-%m-%d %H:%M:%S %z')
        last_update_date = repository.last_update_date.strftime('%Y-%m-%d %H:%M:%S %z')

        with open(file_path, 'w', encoding="utf-8") as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write(f'title: {title}\n')
            f.write(f'date: {creation_date}\n')
            f.write(f'last_modified_at: {last_update_date}\n')
            f.write(f'url: {repository.url}\n')

            if img_url:
                f.write(f'image:\n')
                f.write(f'  path: {img_url}\n')
                f.write(f'  alt: {alt_text}\n') if alt_text else None
            if repository.topics:
                f.write(f'tags: [{", ".join(repository.topics)}]\n')
            f.write(f'categories: ["Repository", {repository.language}]\n')
            f.write('---\n')
            f.write(contents)

    @staticmethod
    def get_post_path(repository, post_dir_path) -> str:
        creation_date = repository.creation_date.strftime("%Y-%m-%d")
        return f"{post_dir_path}/{creation_date}-{repository.name}.md"

    @staticmethod
    def remove_title(contents) -> str:
        if contents.startswith('# '):
            return contents.split('\n', 1)[1]
        return contents

    @staticmethod
    def fix_image_links(contents) -> str:
        for content in contents.split('\n'):
            if RepoToPost.is_image(content):
                fixed_content = content.replace('blob', 'raw')
                contents = contents.replace(content, fixed_content)
        return contents

    @staticmethod
    def fix_urls(contents) -> str:
        for content in contents.split('\n'):
            if RepoToPost.is_unwrapped_url(content):
                urls = re.findall(r'(http[s]?://[^\s\*]+)', content)

                fixed_content = content
                for url in urls:
                    fixed_content = fixed_content.replace(url, f'[{url}]({url})')
                contents = contents.replace(content, fixed_content)
        return contents

    @staticmethod
    def get_header_img(contents) -> tuple:
        for content in contents.split('\n'):
            if RepoToPost.is_image(content):
                return RepoToPost.get_image_data(content)
        return None, None

    @staticmethod
    def get_image_data(content) -> tuple:
        url = content.split('(')[1].split(')')[0]
        alt = content.split('[')[1].split(']')[0]
        return url, alt

    @staticmethod
    def is_image(content) -> bool:
        return '![' in content and ']' in content and '(' in content and ')' in content

    @staticmethod
    def is_unwrapped_url(content) -> bool:
        return 'http' in content and \
            '[' not in content and ']' not in content \
            and '(' not in content and ')' not in content \
            and 'clone' not in content


if __name__ == '__main__':

    access_token = None
    username = 'ibaiGorordo'

    parser = GithubParser(access_token)
    repositories = parser(username)

    RepoToPost.write_posts(repositories)
