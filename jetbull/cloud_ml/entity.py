class ModelEntity():

    def __init__(self, name, description,
                 default_version=None, regions=(),
                 online_prediction_logging=None):
        self.name = name
        self.description = description
        self.default_version = default_version
        self.regions = regions
        self.online_prediction_logging = online_prediction_logging

    def to_resource(self):
        r = {
            "name": self.name,
            "description": self.description
        }
        if len(self.regions) > 0:
            r["regions"] = self.regions
        if self.online_prediction_logging is not None:
            r["regions"] = self.online_prediction_logging
        return r

    @classmethod
    def create(cls, item):
        return cls(
            name=item.get("name", ""), description=item.get("description", ""),
            default_version=item.get("defaultVersion", None),
            regions=item.get("regions", []),
            online_prediction_logging=item.get("onlinePredictionLogging", None))


class JobEntity():

    def __init__(self, job_id,
                 job_input=None, job_output=None,
                 state=None, error="",
                 create_time=None, start_time=None, end_time=None,
                 train=True):
        self.job_id = job_id
        self.job_input = job_input
        self.job_output = job_output
        self.state = state
        self.error = error
        self.create_time = create_time
        self.start_time = start_time
        self.end_time = end_time
        self.train = train

    @classmethod
    def create(cls, item):
        job = cls(
            job_id=item.get("jobId", ""), state=item.get("state", ""),
            error=item.get("error", ""),
            create_time=item.get("createTime", ""),
            start_time=item.get("startTime", ""),
            end_time=item.get("endTime", None))

        if "trainingInput" in item:
            job.train = True
            job.job_input = JobInput.create(item.get("trainingInput", {}))
            job.job_output = item.get("trainingOutput", None)
        else:
            job.train = False
            job.job_input = item.get("predictionInput", None)
            job.job_output = item.get("predictionOutput", None)
        return job

    def to_resource(self):
        r = {
            "jobId": self.job_id
        }
        if self.train:
            r["trainingInput"] = self.job_input.to_resource()
        else:
            r["predictionInput"] = self.job_input.to_resource()
        return r


class JobInput():

    def __init__(self,
                 scale_tir="BASIC", master_type="",
                 worker_type="", parameter_server_type="",
                 worker_count=-1, parameter_server_count=-1,
                 package_uris=(), python_module="", args=(),
                 hyperparameters=None, region="", job_dir="",
                 runtime_version="", python_version="3.5"
                 ):
        self.scale_tir = scale_tir
        self.master_type = master_type
        self.worker_type = worker_type
        self.parameter_server_type = parameter_server_type
        self.worker_count = worker_count
        self.paramer_server_count = parameter_server_count
        self.package_uris = package_uris
        self.python_module = python_module
        self.args = args
        self.hyperparameters = hyperparameters
        self.region = region
        self.job_dir = job_dir
        self.runtime_version = runtime_version
        self.python_version = python_version

    @classmethod
    def create(cls, item):
        return cls(
            scale_tir=item.get("scaleTier", ""),
            master_type=item.get("masterType", ""),
            worker_type=item.get("workerType", ""),
            parameter_server_type=item.get("parameterServerType", ""),
            worker_count=int(item.get("workerCount", -1)),
            parameter_server_count=int(item.get("parameterServerCount", -1)),
            package_uris=item.get("packageUris", []),
            python_module=item.get("pythonModule", ""),
            args=item.get("args", []),
            hyperparameters=item.get("hyperparameters", None),
            region=item.get("region", ""),
            job_dir=item.get("jobDir", ""),
            runtime_version=item.get("runtimeVersion", ""),
            python_version=item.get("pythonVersion", "")
        )

    def to_resource(self):
        r = {
            "scaleTier": self.scale_tir,
            "packageUris": self.package_uris,
            "pythonModule": self.python_module,
            "region": self.region,
            "pythonVersion": self.python_version
        }
        if self.master_type:
            r["masterType"] = self.master_type
        if self.worker_type:
            r["workerType"] = self.worker_type
        if self.parameter_server_type:
            r["parameterServerType"] = self.parameter_server_type
        if self.worker_count > 0:
            r["workerCount"] = str(self.worker_count)
        if self.paramer_server_count > 0:
            r["parameterServerCount"] = str(self.paramer_server_count)
        if len(self.args) > 0:
            r["args"] = self.args
        if self.hyperparameters is not None:
            r["hyperparameters"] = self.hyperparameters.to_resource()
        if self.job_dir:
            r["jobDir"] = self.job_dir
        if self.runtime_version:
            r["runtimeVersion"] = self.runtime_version

        return r
