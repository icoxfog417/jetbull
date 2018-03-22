import os
import shutil
import subprocess
from subprocess import PIPE


class ModelResource():

    def __init__(self,
                 root,
                 package_root,
                 model_name="",
                 setup_root="",
                 on_cloud=False):

        self._root = root
        self._package_root = package_root
        self.model_name = os.path.basename(package_root)
        self._setup_root = setup_root  # relative path
        self.on_cloud = on_cloud

    @property
    def setup_location(self):
        if not self._setup_root:
            return self._package_root
        else:
            return os.path.join(self._package_root, self._setup_root)

    @property
    def root(self):
        if self.on_cloud:
            return os.path.basename(self._root)
        else:
            return self._root

    @property
    def resource_path(self):
        return os.path.join(self.root, self.model_name)

    @property
    def resource_dir(self):
        return self.model_name

    @property
    def source_dir(self):
        return os.path.join(self.resource_dir, "source")

    @property
    def job_dir(self):
        return os.path.join(self.resource_dir, "training")

    @property
    def job_path(self):
        return os.path.join(self.resource_path, "training")

    @property
    def model_dir(self):
        return os.path.join(self.job_dir, "models")

    @property
    def model_path(self):
        return os.path.join(self.job_path, "models")

    def archive(self):
        setup_location = self._package_root
        script_path = os.path.join(setup_location, "setup.py")
        if not os.path.exists(script_path):
            raise Exception("setup.py does not exist at {}.".format(
                setup_location))

        delete = False
        if self._setup_root:
            # Execute setup.py another location
            setup_location = self.setup_location
            _script_path = os.path.join(setup_location, "setup.py")

            # Check the existence of setup.py on another location
            if os.path.isfile(_script_path):
                raise Exception("setup.py already exist at {}".format(
                                setup_location))

            # Copy setup.py
            shutil.copyfile(script_path, _script_path)
            script_path = _script_path
            delete = True  # Delete copied file after execution

        setup_location = os.path.abspath(setup_location)
        script_path = os.path.abspath(script_path)
        try:
            p = subprocess.Popen("python setup.py sdist", shell=True,
                                 cwd=setup_location, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            stdout = stdout.decode("utf-8")
            print(stdout)
        except Exception as ex:
            if delete:
                os.remove(script_path)
            raise ex

        if delete and os.path.isfile(script_path):
            os.remove(script_path)

        # Check the generated files
        logs = stdout.split("\n")
        logs = [log.strip() for log in logs]
        package = ""
        package_path = ""
        if "running egg_info" in logs:
            egg_log = logs[logs.index("running egg_info") + 1]
            kind, egg_info = egg_log.split(" ")
            if kind == "writing":
                egg_dir = os.path.dirname(egg_info)
            else:
                egg_dir = egg_info
            egg_dir = os.path.join(setup_location, egg_dir)
            if os.path.isdir(egg_dir):
                shutil.rmtree(egg_dir)
        if "running check" in logs:
            package_log = logs[logs.index("running check") + 1]
            _, package = package_log.split(" ")
            package_path = os.path.join(setup_location,
                                        "dist/" + package + ".tar.gz")

        package_path = os.path.abspath(package_path)
        return package, package_path

    def make_model_file_name(self, extention="", staging=False, version=-1):
        name = self.model_name
        if staging:
            name = name + "_staging"
        elif version > 0:
            name = name + "_" + str(version)

        _file_name = name + extention
        return _file_name
