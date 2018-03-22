import os
from datetime import datetime
import subprocess
from subprocess import PIPE
import shutil
from google.cloud import storage
from jetbull.cloud_ml.entity import JobInput
from jetbull.cloud_ml.job_client import JobClient


class ModelTask:

    def __init__(self, client, model_resource):
        self._client = client
        self.__mr = model_resource

    def upload_archive(self):
        """
        Make package and apload to GCS
        """
        module_name, archived_file = self.__mr.archive()
        file_name = os.path.basename(archived_file)

        s_client = storage.Client(project=self._client.project,
                                  credentials=self._client._credentials)
        bucket = s_client.get_bucket(self.__mr.root)
        source_path = os.path.join(self.__mr.source_dir, file_name)
        blob = bucket.blob(source_path)
        blob.upload_from_filename(filename=archived_file)
        return "gs://" + self.__mr.root + "/" + source_path

    def train(self, trainer_module, trainer_args=(),
              setup_root="",
              region="us-central1", runtime_version="1.4",
              python_version="3.5",
              on_cloud=False):
        self.__mr.on_cloud = on_cloud

        args = list(trainer_args)
        if not on_cloud:
            return self.train_on_local(trainer_module, trainer_args)
        else:
            args.append("-on-cloud")

        source_path = self.upload_archive()
        job_input = JobInput(
            package_uris=(source_path,),
            python_module=trainer_module,
            args=args, region=region,
            job_dir=("gs://" + self.__mr.job_path),
            runtime_version=runtime_version,
            python_version=python_version
        )
        job_id = self.__mr.model_name + "_train_"
        job_id += datetime.now().strftime("%Y%m%d_%H%M%S")
        client = JobClient(self._client)
        created = client.create(job_id, job_input, train=True)
        return created

    def train_on_local(self, trainer_module, trainer_args):
        location = os.path.abspath(self.__mr.setup_location)
        args = list(trainer_args)
        args.append("--job-dir")
        args.append(self.__mr.job_dir)

        script = "python -m {} {}".format(
                    trainer_module,
                    " ".join(args)
                )
        p = subprocess.Popen(script, shell=True,
                             cwd=location, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode("utf-8")
        if stdout:
            print(stdout)
            return {"status": True}
        else:
            stderr = stderr.decode("utf-8")
            print(stderr)
            return {"status": False}

    def store(self, path, on_cloud=False):
        self.__mr.on_cloud = on_cloud
        _, ext = os.path.splitext(path)
        model_file = self.__mr.make_model_file_name(ext)

        if on_cloud:
            model_path = os.path.join(self.__mr.model_dir, model_file)
            s_client = storage.Client(project=self._client.project,
                                      credentials=self._client._credentials)

            bucket = s_client.get_bucket(self.__mr.root)
            blob = bucket.blob(model_path)
            blob.upload_from_filename(filename=path)
            return "gs://" + self.__mr.root + "/" + model_path
        else:
            model_path = os.path.join(self.__mr.model_path, model_file)
            if not os.path.isdir(self.__mr.resource_path):
                os.mkdir(self.__mr.resource_path)
            if not os.path.isdir(self.__mr.job_path):
                os.mkdir(self.__mr.job_path)
            if not os.path.isdir(self.__mr.model_path):
                os.mkdir(self.__mr.model_path)

            try:
                shutil.copyfile(path, model_path)
            except Exception as ex:
                os.remove(path)
                raise ex
            os.remove(path)
            return model_path

    def staging(self, path):
        pass

    def deploy(self):
        pass

    def rollback(self):
        pass
