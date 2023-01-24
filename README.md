# Jekyll-Posts-From-Github
 Automatically generate Jekyll posts from all the README files of a Github user.

![Jekyll-Posts-From-Github](https://jekyllrb.com/img/octojekyll.png)

## Why?

I wanted to create a blog that would automatically update with all the README files of my Github repositories. This way, I could write a README file for each of my projects and have it automatically show up on my blog.


## What is this?

This is a simple script that will generate Jekyll posts from the README file for all the repositories of a Github user.

## How to use it?

1. Clone this repository into a folder of your Jekyll project (something like "_scripts").
2. Open the file "main.py" and change the value of the variable `github_user` and `access_token` to your user name and [Github access token](https://github.com/settings/tokens).
3. Run the script with the command "python main.py".
```shell
cd <your-jekyll-project-folder>
mkdir _scripts
cd _scripts
git clone https://github.com/ibaiGorordo/Jekyll-Posts-From-Github.git
cd Jekyll-Posts-From-Github
pip install -r requirements.txt
python main.py
```

## How does it work?
- The script will get all the information from the user's repositories using the [PyGithub library](https://pygithub.readthedocs.io/en/latest/).
- The script extracts the following content from each repository:
    - name
    - url
    - creation_date
    - last_update_date
    - topics
    - programming language
    - PyGithub Repository object
- It will then create a Jekyll post for each repository, using the README file as the content of the post.
- The following information is added to the header of the post:
    - title
    - date
    - last_modified_at
    - url
    - image (path and alt) for the first image in the README file
    - tags (based on the repository's topics)
    - categories (["repository", {programming language}])
- To avoid having a duplicate title, it deletes the first line of the README file if it is a title (i.e. starts with "# ").
- Because bare URLs are not properly converted to links by Jekyll, it will convert any bare URL to a link in Markdown.
- Finally, it also fixes the image url for images in stored in Github repositories (i.e. it will add the raw url to the image).

## References
- [Jekyll](https://jekyllrb.com/)
- [PyGithub](https://pygithub.readthedocs.io/en/latest/)
