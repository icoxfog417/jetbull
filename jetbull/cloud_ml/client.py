from google.cloud.client import ClientWithProject
from jetbull.cloud_ml._http import Connection
from google.api_core import page_iterator
from jetbull.cloud_ml.model_client import ModelClient
from jetbull.cloud_ml.job_client import JobClient


class Client(ClientWithProject):

    SCOPE = (
        "https://www.googleapis.com/auth/devstorage.full_control",
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/cloud-platform")

    def __init__(self, project=None, credentials=None, _http=None):
        super(Client, self).__init__(
                project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)

    @property
    def model(self):
        return ModelClient(self)

    def job(self, ml_root):
        return JobClient(self, ml_root)

    def models(self, max_results=None, page_token=None):
        model_client = ModelClient(self)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=self._connection.api_request,
            path=model_client.path,
            item_to_value=ModelClient._item_to_model,
            items_key="models",
            page_token=page_token,
            max_results=max_results)

    def jobs(self, ml_root, filter="", max_results=None, page_token=None):
        job_client = JobClient(self, ml_root)
        extra_params = {}
        extra_params["filter"] = filter
        return page_iterator.HTTPIterator(
            client=self,
            api_request=self._connection.api_request,
            path=job_client.path,
            item_to_value=JobClient._item_to_job,
            items_key="jobs",
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params)
