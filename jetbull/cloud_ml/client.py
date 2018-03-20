from google.cloud.client import ClientWithProject
from jetbull.cloud_ml._http import Connection
from google.api_core import page_iterator
from jetbull.cloud_ml.entity import ModelEntity


class Client(ClientWithProject):

    SCOPE = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(self, project=None, credentials=None, _http=None):
        super(Client, self).__init__(
                project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)

    @property
    def model(self):
        return ModelClient(self)

    def models(self, max_results=None, page_token=None):
        model_client = ModelClient(self)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=self._connection.api_request,
            path=model_client.path,
            item_to_value=ModelEntity._item_to_model,
            items_key="models",
            page_token=page_token,
            max_results=max_results)


class ModelClient():

    def __init__(self, client):
        self._client = client

    @property
    def path(self):
        return "/projects/{}/models".format(self._client.project)

    @property
    def request(self):
        return self._client._connection.api_request

    def create(self, model):
        api_response = self.request(
            method="POST", path=self.path, data=model.to_resource())
        created = ModelEntity._item_to_model(None, api_response)
        return created

    def delete(self, model):
        if isinstance(model, ModelEntity):
            path = self.path + "/" + model.name
        else:
            path = self.path + "/" + model
        api_response = self.request(
            method="DELETE", path=path)
        if "response" in api_response:
            return True
        else:
            return False
