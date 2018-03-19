
import os
import sys
from sklearn.metrics import classification_report
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from datasets import MyDatasets
from preprocessor import ColumnEncoder, DropColumn, CategoricalToNumerical
from jetbull.model_process import ModelProcess
from model import model
from api import api


# Prepare data
root = os.path.join(os.path.dirname(__file__), "example-data")
dataset = MyDatasets(root)
resource = dataset.telecom_data.load(on_cloud=True)

# Make model training pipeline
pipe = ModelProcess([
    ("delete phone number", DropColumn("phone number")),
    ("state encoding", ColumnEncoder("state")),
    ("international plan conversion",
     CategoricalToNumerical("international plan", {"yes": 1, "no": 0})),
    ("voice mail plan conversion",
     CategoricalToNumerical("voice mail plan", {"yes": 1, "no": 0})),
    ("churn", CategoricalToNumerical("churn", {True: 1, False: 0})),
    ("model", model)
])

# Train
train_x, test_x, train_y, test_y = resource.train_test_split()
pipe.train(train_x, train_y)

preds = pipe.predict(test_x)
print("Evaluate the Model")
print(classification_report(test_y, preds))

# Update API
api.update(pipe, test_x, test_y)
print("Update API threshold")
print(api.thresholds)

# Save Model and API
