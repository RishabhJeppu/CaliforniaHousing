import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, app, jsonify, url_for, render_template

app = Flask(__name__)
## Load the model
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scalar = pickle.load(open("scaling.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_api():
    data = request.json["data"]
    new_data = scalar.fit_transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    return jsonify({"prediction": output[0]})


if __name__ == "__main__":
    app.run(debug=True)
