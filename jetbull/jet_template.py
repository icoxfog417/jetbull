class JetTemplate():

    def __init__(self, credential_path=""):
        self.credential_path = credential_path
        self.__client = None

    def get_client(self):
        if self.__client is None:
            self.__client = self.make_client()
        return self.__client

    def make_client(self):
        raise Exception("You have to implements how to create cloud client")

    def jet(self, on_cloud, when_cloud, when_local):
        if on_cloud:
            return when_cloud
        else:
            return when_local
