## Course Overview

### Model Training Process
- We trained various models in our initial notebook (`duration-prediction.ipynb`)
- Oftentimes, we want to go back and check the performance of different models
- Could make notes of scores within a notebook, or in a spreadsheet, etc.

### Benefits of Experiment Tracking and Model Management
- A better approach is to **log** all of our metrics to a specific location (**experiment tracker** )to preserve history
- We can also save our models to a **model registry**, which keeps our models in storage
    - Usually goes hand-in-hand with experiment trackers to save metrics and models in the same place
    - We will see examples of this with **MLflow**
        - https://mlflow.org/

### Reasons for ML Pipelines
- Instead of manually changing parameters/arguments in a notebook, we could do all this stuff in a **pipeline**
- There are various tools and best practices for this
- We will be converting notebooks to pipelines
- Example workflow, in order of (required) execution:
    - Step 1: Load and prepare data
    - Step 2: Vectorize our DataFrame into a **feature matrix**
    - Step 3: Train the model
        - Can be organized to keep running on different models until something in the vectorize step changes
- We can **parameterize** our pipelines to input different data and models into them
- We can then execute the pipeline with a simple script with different arguments/parameters
    ```bash
        python python_pipeline.py \
            --train_data='./data/training.parquet' \
            --validation_data='./data/validation.parquet'
    ```
- This is very easy to reproduce
- We will be doing this with **Prefect** (an **orchestrator**) and **Kubeflow pipelines**

### Model Deployment
- The output of a pipeline is a model (and sometimes a vectorizer)
- We need to take this model and start using it
- This is typically done by putting the model into some ML service
    - i.e., users using their phone to order a taxi through an app (*communicate with our service*)
- There are various ways to deploy a model

### Model Monitoring
- Once a model is deployed and users are interacting with it, we need to make sure that its performance doesn't degrade
- We do this via **monitoring**, which can be configured to send MLEs alerts if something goes wrong
    - Sometimes humans can be excluded and we can just re-execute the pipeline but with new data to produce a new model that we will deploy automatically
        - This requires a *lot* of trust in our ML system(s)

### Best Practices
- Our idea is to automate as much as possible
- Each step of our workflow is some code, and this **code must be maintainable, tested, cleaned, and well-documented**
    - i.e., how do we package our pipelines and web services (in Docker), how do we deploy models, what practices we should use, etc.

### Processes
- MLOps is not just about tools and coding, it is also about people and processes
    - MLEs and data scientists do not work in isolation
- We want everyone to work together efficiently and that we are approaching the correct problem in the right way