## MLFlow Setup
- Create a new (or activate a current) Anaconda environment named `zoom`
    - *If on the VM, create a new environment as well (if need be)*
- Install the following Python packages, if need be (either manually or via a `requirements.txt` with `pip install -r requirements.txt`):
    - `mlflow`
    - `jupyter`
    - `scikit-learn`
    - `pandas`
    - `seaborn`
    - `hyperopt` (Distributed asynchronous hyperparameter optimization: https://hyperopt.github.io/hyperopt/)
    - `xgboost` (optimized distributed gradient boosting library that implements ML algorithms under the Gradient Boosting framework: https://xgboost.readthedocs.io/en/stable/)
    - `fastparquet` (Python implementation of the parquet format, aiming to integrate into Python-based big data work-flows: https://pypi.org/project/fastparquet/)
    - `boto3` (use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    - **NOTE**: If you get an error about `py4j` and PySpark, install these all in a new environment for this course
        - *Or* downgrade it via: `pip install --force-reinstall -v "py4j==0.10.9.5"`
- Run `mlflow --version` and check the output (currently version 2.3.2)

### Launching the MLFlow UI and Running MLFlow
- In the Anaconda environment, run `mlflow ui --backend-store-uri sqlite:///mlflow.db`
    - This tells MLFlow that we want to store all the artifacts and metadata in SQLite
- You will get output that says the UI is being served at `http://127.0.0.1:5000`, which you can open in a web browser
- Import `mlflow` in the new version of the notebook, `duration-prediction_MLFlow.ipynb`
- Once we set the expirement `nyc_taxi_experiment_1`, reload the browser window of the UI to see it
- Once we do an MLFlow run in the notebook, we can see it in the browser once it's refreshed
    - We can see duration of the run, user (from the machine/computer), source, detected code version, models (if logged), metrics (if logged)
    - Clicking on the run, we can see all of the above as well as the tag(s), metric(s) and the parameter(s) we logged

### Hyperparameter Tuning Logging
