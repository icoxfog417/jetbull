# jetbull

Give machine learning process wings to cloud.

* Execution on the local and the cloud.
  * You want to check process on local, but simultaneously you want to run it on the cloud when training the model or dealing with the huge data source. 
* Data Dependency Management
  * You have to keep attention to the dependency of the model to data. To avoid missing the re-training timing.
* Training Chain Management
  * If you update a model, you have to care the other models that are related to the updated model. These model require the re-training.

`jetbull` helps you to tackle above problems.

## How `jetbull` works

* `jetbull` is based on [`sklearn.pipeline.Pipeline`](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).
* When running on the cloud, `jetbull` use [`Apache Beam`](https://beam.apache.org/) ([Cloud Dataflow](https://cloud.google.com/dataflow/docs/?hl=en)) for data process and [Cloud ML Engine](https://cloud.google.com/ml-engine/reference/?hl=ja) to train the model.


```py
from jetbull.process import Process
from dataset.sales import Sales  # Your dataset
from preprocess import StandardScaler, LabelEndoer  # Your preprocessor
from model import UserRankModel  # Your model


samples = Sales.query("date > 2018/1/1")
samples = Sales.freezed.samples.get()

# Make process
process = Process(
    (StandardScaler, "normalize sales"),
    (LabelEncoder, "labels to nubmers"),
    (UserRankModel(), "predict the user rank", model=True)
)


# Train on local
process.train(samples)

# Train on Cloud
process.train({
    "data": Sales.freezed.sales_2017,
    "staging": dataset.staging,
    "deploy": False
})

# Deploy on Cloud
process.train({
    "data": Sales.freezed.sales_2017,
    "staging": dataset.staging,
    "deploy": True
})

# Predict
user_rank = process.predict("John")
if user_rank == "A":
    print("You are good customer for us!")

```


## Requirements

* [scikit-learn](http://scikit-learn.org/)
* [apache-beam](https://beam.apache.org/get-started/quickstart-py/)
* [google-cloud](https://github.com/GoogleCloudPlatform/google-cloud-python)
