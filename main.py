import numpy as np
import pandas as pd
import xgboost as xgb
import joblib


def init_data(bmi_min, bmi_max, height_min, height_max, mode, gender):
    bmi_frame = np.random.uniform(bmi_min, bmi_max, 3000)
    bmi_frame = np.around(bmi_frame, decimals=1)
    height_frame = np.random.uniform(height_min, height_max, 3000)
    height_frame = np.around(height_frame, decimals=0)

    data = {
        "BMI": bmi_frame,
        "Height": height_frame,
        "Gender": gender,
        "Mode": mode,
    }

    df = pd.DataFrame(data, index=None)
    return df


def init_frame_male():
    frame_mode_1_2 = init_data(15, 18.4, 150, 170, "1_2", "Male")
    frame_mode_2 = init_data(15, 18.4, 171, 185, "2", "Male")
    frame_mode_1 = init_data(18.5, 22.9, 150, 170, "1", "Male")
    frame_mode_4 = init_data(18.5, 22.9, 171, 185, "4", "Male")
    frame_mode_1_3 = init_data(23, 26, 150, 170, "1_3", "Male")
    frame_mode_3 = init_data(23, 26, 170, 185, "3", "Male")
    frames = [frame_mode_1_2, frame_mode_2, frame_mode_1, frame_mode_4, frame_mode_1_3, frame_mode_3]
    result = pd.concat(frames)
    return result


def init_model_xgboost():
    df = pd.read_excel("data.xlsx", engine='openpyxl')
    d_gender = {
        "Male": 1
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
    file_name = 'finalized_model.sav'
    joblib.dump(model, file_name)


def load_model():
    filename = 'finalized_model.sav'
    model = joblib.load(filename)

    data_test = {
        "BMI": [18],
        "Height": [171],
        "Gender": [1],
    }
    df_test = pd.DataFrame(data_test, index=None)
    test = xgb.DMatrix(df_test)
    prediction = model.predict(test)
    print(prediction)


load_model()
