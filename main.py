import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.naive_bayes import GaussianNB


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


def init_frame_female():
    frame_mode_1_2 = init_data(15, 18.4, 150, 165, "1_2", "Female")
    frame_mode_2 = init_data(15, 18.4, 166, 175, "2", "Female")
    frame_mode_1 = init_data(18.5, 22.9, 150, 165, "1", "Female")
    frame_mode_4 = init_data(18.5, 22.9, 166, 175, "4", "Female")
    frame_mode_1_3 = init_data(23, 26, 150, 165, "1_3", "Female")
    frame_mode_3 = init_data(23, 26, 166, 175, "3", "Female")
    frames = [frame_mode_1_2, frame_mode_2, frame_mode_1, frame_mode_4, frame_mode_1_3, frame_mode_3]
    result = pd.concat(frames)
    return result


def init_frame_food_custom(protein, fiber, fat, canxi, starch, mode):
    protein_frame = np.random.uniform(protein["min"], protein["max"], 3000)
    protein_frame = np.around(protein_frame, decimals=0)

    fiber_frame = np.random.uniform(fiber["min"], fiber["max"], 3000)
    fiber_frame = np.around(fiber_frame, decimals=0)

    fat_frame = np.random.uniform(fat["min"], fat["max"], 3000)
    fat_frame = np.around(fat_frame, decimals=0)

    canxi_frame = np.random.uniform(canxi["min"], canxi["max"], 3000)
    canxi_frame = np.around(canxi_frame, decimals=0)

    starch_frame = np.random.uniform(starch["min"], starch["max"], 3000)
    starch_frame = np.around(starch_frame, decimals=0)

    data = {
        "Protein": protein_frame,
        "Fiber": fiber_frame,
        "Fat": fat_frame,
        "Canxi": canxi_frame,
        "Starch": starch_frame,
        "Mode": mode
    }
    df = pd.DataFrame(data, index=None)
    return df


def init_frame_food():
    frame_mode_1 = init_frame_food_custom({"max": 2, "min": 0}, {"max": 3, "min": 0}, {"max": 0, "min": 0},
                                          {"max": 3, "min": 3}, {"max": 3, "min": 0}, "1")
    frame_mode_1_2 = init_frame_food_custom({"max": 3, "min": 3}, {"max": 3, "min": 0}, {"max": 3, "min": 1},
                                            {"max": 3, "min": 3}, {"max": 3, "min": 0}, "1_2")
    frame_mode_2 = init_frame_food_custom({"max": 3, "min": 3}, {"max": 3, "min": 0}, {"max": 3, "min": 1},
                                          {"max": 0, "min": 2}, {"max": 3, "min": 0}, "2")
    frame_mode_4 = init_frame_food_custom({"max": 2, "min": 1}, {"max": 2, "min": 1}, {"max": 1, "min": 0},
                                          {"max": 0, "min": 2}, {"max": 3, "min": 0}, "4")
    frame_mode_1_3 = init_frame_food_custom({"max": 1, "min": 1}, {"max": 3, "min": 3}, {"max": 0, "min": 0},
                                            {"max": 3, "min": 3}, {"max": 3, "min": 0}, "1_3")
    frame_mode_3 = init_frame_food_custom({"max": 1, "min": 1}, {"max": 3, "min": 3}, {"max": 0, "min": 0},
                                          {"max": 2, "min": 0}, {"max": 3, "min": 0}, "3")
    frames = [frame_mode_1_2, frame_mode_2, frame_mode_1, frame_mode_4, frame_mode_1_3, frame_mode_3]
    result = pd.concat(frames)
    result.to_excel("food_data.xlsx", index=False)


def init_file_data():
    frame_male = init_frame_male()
    frame_female = init_frame_female()
    frame_all = [frame_male, frame_female]
    result = pd.concat(frame_all)
    result.to_excel("data.xlsx", index=False)
    return result


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
    file_name = 'finalized_model.sav'
    joblib.dump(model, file_name)


def load_model():
    filename = 'finalized_model.sav'
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
    file_name = 'finalized_model_food.sav'
    joblib.dump(clf, file_name)
    # predict = clf.predict([[3, 3, 3, 3, 2]])
    # print(predict)


def load_model_food():
    filename = 'finalized_model_food.sav'
    model = joblib.load(filename)
    predict = model.predict([[1, 3, 0, 0, 2]])
    print(predict)


# load_model()
# init_model_xgboost()
# init_file_data()
# init_frame_food()
load_model_food()
