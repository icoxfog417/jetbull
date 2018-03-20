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
    def _item_to_model(cls, iterator, item):
        return cls(
            item.get("name", ""), item.get("description", ""),
            item.get("defaultVersion", None), item.get("regions", []),
            item.get("onlinePredictionLogging", None))
