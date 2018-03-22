import os
from jetbull.model_resource import ModelResource


class DemoModelResource(ModelResource):

    def __init__(self):
        super().__init__(
            root=os.path.join(os.path.dirname(__file__),
                              "./example-data/jetbull-ml"),
            package_root=os.path.join(os.path.dirname(__file__)),
            setup_root="../"
        )
