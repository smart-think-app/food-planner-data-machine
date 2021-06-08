import pandas as pd
import xgboost as xgb
import joblib


def init_model_xgboost():
    df = pd.read_excel("data.xlsx", engine='openpyxl')
    d_gender = {
        "Male": 1,
        "Female": 2,
    }

    d_mode = {
        "1_2": 1,
        "2": 2,
        "1": 3,
        "4": 4,
        "1_3": 5,
        "3": 6
    }
    df["Gender"] = df["Gender"].map(d_gender)
    df["Mode"] = df["Mode"].map(d_mode)
    x = df[["BMI", "Height", "Gender"]].to_numpy()
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
    file_name = '../sav/finalized_model.sav'
    joblib.dump(model, file_name)


def load_model():
    filename = '../sav/finalized_model.sav'
    model = joblib.load(filename)

    data_test = {
        "BMI": [18],
        "Height": [168],
        "Gender": [2],
    }
    df_test = pd.DataFrame(data_test, index=None)
    test = xgb.DMatrix(df_test)
    prediction = model.predict(test)
    print(prediction)