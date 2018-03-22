import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.cloud_ml.client import Client  # noqa
from jetbull.cloud_ml.entity import JobEntity  # noqa
from demo.model_resource import DemoModelResource  # noqa


CREDENTIAL = os.path.join(os.path.dirname(__file__), "../credential.json")


def main():
    client = Client.from_service_account_json(CREDENTIAL)
    job = client.job(DemoModelResource)

    # train on local
    created = job.train(
        trainer_module="demo.trainer.task",
        trainer_args=(
            "-credential-path", CREDENTIAL,
            "-n-estimators", "40"
            )
    )

    # train on cloud
    created = job.train(
        trainer_module="demo.trainer.task",
        trainer_args=(
            "-n-estimators", "40"
            ),
        region="asia-east1", on_cloud=True
    )


if __name__ == "__main__":
    main()
