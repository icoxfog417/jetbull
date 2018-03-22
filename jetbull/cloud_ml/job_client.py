from jetbull.cloud_ml.entity import JobEntity


class JobClient():

    def __init__(self, client):
        self._client = client

    @property
    def path(self):
        return "/projects/{}/jobs".format(self._client.project)

    @property
    def request(self):
        return self._client._connection.api_request

    def create(self, job_id, job_input, train=True):
        job = JobEntity(job_id=job_id, job_input=job_input, train=train)
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
