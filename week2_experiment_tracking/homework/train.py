import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)

def run_train(data_path: str):
    # set the MLFlow URI to our backend
    mlflow.set_tracking_uri('sqlite:///mlflow.db')

    # set up to assign/append runs to our experiment (and create if it doesn't exist)
    mlflow.set_experiment('nyc_taxi_homework_week2')    
    
    # Turn on autologging
    # https://mlflow.org/docs/latest/tracking.html#automatic-logging
    # https://mlflow.org/docs/latest/python_api/mlflow.xgboost.html#mlflow.xgboost.autolog
    mlflow.sklearn.autolog()

    with mlflow.start_run():
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        print(f'RMSE: {rmse}')


if __name__ == '__main__':
    run_train()
