import flask
from flask import request
from flask_restplus import Resource, abort
from main.util.dto import MLDTO
import _pickle as pickle

api = MLDTO.api
data = MLDTO.data
with open("C:\\Users\\1572172\\PycharmProjects\\flask\\backend\\src\\main\\util\\model.pkl", 'rb') as f:
    model = pickle.load(f)


@api.route('/wine')
class MLCollection(Resource):
    @api.expect(data)
    def post(self):
        """Predict's a fake wine. Requires an array with 11 variables:
        Input variables (based on physicochemical tests):
        1 - fixed acidity
        2 - volatile acidity
        3 - citric acid
        4 - residual sugar
        5 - chlorides
        6 - free sulfur dioxide
        7 - total sulfur dioxide
        8 - density
        9 - pH
        10 - sulphates
        11 - alcohol
        Output variable (based on sensory data):
        12 - quality (score between 0 and 10)"""
        json_data = request.json['data']
        if len(json_data) != 11:
            abort(400, "Data requires 11 parameters")
        prediction = model.predict([json_data]).tolist()
        response = {'predictions': prediction}
        return flask.jsonify(response)
