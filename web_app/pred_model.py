import os
import pickle

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression 

# Define location of persisted statistical models
MODEL_FILEPATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "stat_models",
    "latest_model.pkl")

# Define and train a model used for predictions in the web app
def train_and_persist_model():
    print("INFO: begin model definition and training")

    X, y       = load_iris(return_X_y=True)
    classifier = LogisticRegression()
    # Fit the model
    print("INFO: fitting the classifier model")
    classifier.fit(X, y)

    # Persist the model to disk
    print("INFO: save the classifier model to disk")
    with open(MODEL_FILEPATH, "wb") as model_file:
        pickle.dump(classifier, model_file)

    print("INFO: model saved to disk")
    return classifier

# Load the classifer from disk
def load_model():
    print("INFO: loading model from disk...")
    with open(MODEL_FILEPATH, "rb") as model_file:
        saved_model = pickle.load(model_file)

    return saved_model

# Execute model train and fit if run via script execution
if __name__ == "__main__":
    print("INFO: training and saving classifier model")
    train_and_persist_model()

    # Load model from disk
    clf = load_model()
    print("INFO: classifer model:", clf)

    # Load iris data - to execute a test prediction
    X, y = load_iris(return_X_y=True)
    inputs_pred = X[:2, :]

    # Generate predictions
    result = clf.predict(inputs_pred)
    print("INFO: prediction test results:", result)
