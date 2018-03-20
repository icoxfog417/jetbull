import subprocess


class Package():

    def __init__(self, project_root, module=""):
        self.project_root = project_root
        self.module = module

    def archive(self):
        targets = subprocess.check_output(["git", "ls-files"])
        # packaging targets files
        return targets
