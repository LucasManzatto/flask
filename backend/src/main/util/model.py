import _pickle as pickle
from sklearn import linear_model
import pandas as pd

# loading our data as a panda
df = pd.read_csv('winequality-red.csv', delimiter=";")

# getting only the column called quality
label = df['quality']

# getting every column except for quality
features = df.drop('quality', axis=1)
# creating and training a model

regr = linear_model.LinearRegression()
regr.fit(features, label)

# serializing our model to a file called model.pkl
pickle.dump(regr, open("model.pkl", "wb"))

# loading a model from a file called model.pkl
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

print(regr.predict([[7.4, 0.66, 0, 1.8, 0.075, 13, 40, 0.9978, 3.51, 0.56, 9.4]]).tolist())
