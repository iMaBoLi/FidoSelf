from github import Github
from FidoSelf import config
import base64

class Git:
    def __init__(self, token=config.GIT_TOKEN, repo="iMaBoLi/FidoSelf"):
        self.token = base64.b64decode(token).decode('utf-8')
        self.git = Github(self.token)
        self.repo = self.git.get_repo(repo)

    def create(self, content, newfile, branch="main"):
        try:
            self.repo.create_file(newfile, f"Create {newfile.split('/')[-1]}", content, branch=branch)
            return True
        except Exception as error:
            return error

    def update(self, file, content, branch="main"):
        try:
            contents = self.repo.get_contents(file, ref=branch)
            self.repo.update_file(contents.path,  f"Update {file.split('/')[-1]}", content, contents.sha, branch=branch)
            return True
        except Exception as error:
            return error

    def delete(self, file, branch="main"):
        try:
            contents = self.repo.get_contents(file, ref=branch)
            self.repo.delete_file(contents.path,  f"Remove {file.split('/')[-1]}", contents.sha, branch=branch)
            return True
        except Exception as error:
            return error
