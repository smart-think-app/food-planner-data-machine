import pandas as pd
import xgboost as xgb
import joblib
from sklearn.naive_bayes import GaussianNB


def init_model_food_xg_boost():
    df = pd.read_excel("food_data.xlsx", engine='openpyxl')
    d_mode = {
        "1_2": 1,
        "2": 2,
        "1": 3,
        "4": 4,
        "1_3": 5,
        "3": 6
    }
    df["Mode"] = df["Mode"].map(d_mode)
    x = df[["Protein", "Fiber", "Fat", "Canxi", "Starch"]].to_numpy()
    y = df["Mode"].to_numpy()
    train = xgb.DMatrix(x, label=y)
    param = {
        "max_depth": 4,
        "eta": 0.3,
        "objective": "multi:softmax",
        "num_class": 7
    }
    epochs = 10
    model = xgb.train(param, train, epochs)
    data_test = {
        "Protein": [2],
        "Fiber": [2],
        "Fat": [0],
        "Canxi": [1],
        "Starch": [2]
    }
    df_test = pd.DataFrame(data_test, index=None)
    test = xgb.DMatrix(df_test)
    prediction = model.predict(test)
    print(prediction)
    # file_name = 'finalized_model.sav'
    # joblib.dump(model, file_name)


def init_model_food_nb():
    data = pd.read_excel("food_data.xlsx", engine='openpyxl')
    x = data[["Protein", "Fiber", "Fat", "Canxi", "Starch"]]
    y = data["Mode"]
    clf = GaussianNB()
    clf.fit(x, y)
    file_name = '../sav/finalized_model_food.sav'
    joblib.dump(clf, file_name)
    # predict = clf.predict([[3, 3, 3, 3, 2]])
    # print(predict)


def load_model_food():
    filename = '../sav/finalized_model_food.sav'
    model = joblib.load(filename)
    return model


def predict_mode_food(model, protein, fiber, canxi, fat, starch):
    predict = model.predict([[protein, fiber, fat, canxi, starch]])
    return predict
