import os
from datetime import datetime
import shutil
import subprocess
import tarfile
import gzip
from subprocess import PIPE
from google.cloud import storage
from jetbull.cloud_ml.entity import JobEntity, JobInput


class Packager():

    def __init__(self, setup_root):
        self.setup_root = setup_root

    def archive(self, path=""):
        setup_py = self.setup_root
        if path:
            setup_py = os.path.join(setup_py, path)
        setup_py = os.path.join(setup_py, "setup.py")
        if not os.path.exists(setup_py):
            raise Exception("setup.py does not exist at {}.".format(setup_py))

        setup_root = os.path.abspath(self.setup_root)
        script_path = os.path.abspath(setup_py)
        root_script = os.path.join(setup_root, "setup.py")
        if os.path.isfile(root_script):
            raise Exception("setup.py already exist at {}".format(
                            self.setup_root))

        shutil.copyfile(script_path, root_script)
        p = subprocess.Popen("python setup.py sdist",
                             cwd=setup_root, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode("utf-8")
        print(stdout)
        os.remove(root_script)

        # deal with log
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
            egg_dir = os.path.join(self.setup_root, egg_dir)
            if os.path.isdir(egg_dir):
                shutil.rmtree(egg_dir)
        if "running check" in logs:
            package_log = logs[logs.index("running check") + 1]
            _, package = package_log.split(" ")
            package_path = os.path.join(self.setup_root,
                                        "dist/" + package + ".tar.gz")

        package_path = os.path.abspath(package_path)
        return package, package_path


class JobClient():

    def __init__(self, client, ml_root):
        self.ml_root = ml_root
        self._client = client

    @property
    def path(self):
        return "/projects/{}/jobs".format(self._client.project)

    def make_module_path(self, module, file_name):
        return "/".join(["training", module, file_name])

    @property
    def request(self):
        return self._client._connection.api_request

    def create(self,
               trainer_root, trainer_module,
               trainer_args=(), region="us-central1",
               runtime_version="1.4", python_version="3.5"):

        # make package and apload to GCS
        pkg = Packager(trainer_root)
        modules = trainer_module.split(".")
        path = ""
        if len(modules) > 1:
            path = "/".join(modules[:-1])
        module_name, archived_file_path = pkg.archive(path=path)
        file_name = os.path.basename(archived_file_path)
        module_path = self.make_module_path(module_name, file_name)
        client = storage.Client(project=self._client.project,
                                credentials=self._client._credentials)

        bucket = client.get_bucket(self.ml_root)
        blob = bucket.blob(module_path)
        blob.upload_from_filename(filename=archived_file_path)

        # make job input
        package_uri = "gs://" + self.ml_root + "/" + module_path
        job_input = JobInput(
            package_uris=(package_uri,),
            python_module=trainer_module,
            args=trainer_args, region=region,
            runtime_version=runtime_version,
            python_version=python_version
        )
        job_id = module_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        job_id = job_id.replace(".", "_").replace("-", "_")
        job = JobEntity(job_id=job_id, job_input=job_input, train=True)

        # send request
        api_response = self.request(
            method="POST", path=self.path, data=job.to_resource())
        created = self._item_to_job(None, api_response)
        return created

    def cancel(self, job):
        if isinstance(job, JobEntity):
            path = self.path + "/" + job.job_id
        else:
            path = self.path + "/" + job
        path += ":cancel"
        api_response = self.request(
            method="POST", path=path)

        if not api_response:
            return True
        else:
            return False

    @classmethod
    def _item_to_job(cls, iterator, item):
        return JobEntity.create(item)
