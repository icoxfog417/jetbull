from jetbull.cloud_ml.entity import ModelEntity


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
        created = self._item_to_model(None, api_response)
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

    @classmethod
    def _item_to_model(cls, iterator, item):
        return ModelEntity.create(item)
