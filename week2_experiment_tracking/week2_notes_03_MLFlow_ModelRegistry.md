## Introduction
- Imagine a data scientist at your company has, in the past, implemented an ML model
- Now, they have come up with a newer version that they are happier with
- So, they want *you* to deploy it to PROD
- But, you have some questions: What has changed? Should the hyperparemeter be updated? Is there any new or updated preprocessing for the model? What is the environment (and what are they dependencies and their versions) that are needed to run this model?
- The data scientist may not have this or initially supplied it
- *This is not very efficient*
- Also, imagine there's an incident in PROD and we need to roll back the model, but you don't know where that earlier version is located
- OR we decide we want to just train the model from scratch if we cannot run the earlier version again
- BUT there would be no link between the model and the code (dataset, hyperparameters, etc.) used to run it
- What we need is that the data scientist to have stored all of this information in some experiment tracking tool
- The **model registry** can make all of this easier

### Model Registry
- Before, we looked at how to **log** experiment and experiment run data (parameters, metrics, artifacts, even models, etc.)
- For this, we used a *locally-running* **tracking server** to store this information
- In some cases, after some time, the number of models being stored in the MLFlow tracking server will have grown significantly
- We then may decide that some of those models are PROD-ready, in which case we can **register** those models into the MLFlow **model registry**
    - The data scientist does *not* in charge of deploying the model, just in charge of deciding which models are ready for PROD and then registering them
    - **i.e., the model registry only lists models that have been determined to be ready for PROD**
        - It does *NOT* do the deployment
- This way, if some deployment engineer has to find out what models are ready to be deployed to production, they can just look at the model registry, which is where they *should* be stored
    - There, they can inspect the hyperparameters, metrics, the performance, etc.
- And based on this information, they can decide where to send the model in the **the model registry's 3 different stages**
    - Staging
    - Production
    - **Archive**
        - After some time, we may decide to archive models (maybe they have degraded)
            - These can always be retrieved if we need to roll back some deployment
- These **stages are just labels**
    - Again, the registry does *not* do the deployment
    - **The model registry should be complemented with some CI/CD code before/in order to do deployment**

## MFlow Model Comparison
- In the UI, say we have 4 scikit-learn models created over some recent experiment runs and autologgin has saved these models along with some information (metrics, artifacts, etc.)
- We can sort these models by our metrics (in our case, error via RMSE)
- To dive deeper, let's say after this last experiment run, we want to identify which models are ready to be deployed
- In the "Models" column, we can click on a specific model from an experiment run to open up a web page with its description and information
- On the model's experiment run page, we can look at the run's duration (an important thing to note about a model), its metric(s), say RMSE, and the model's *size* (a *second* important thing to note about a model)
    - Note: Duration doesn't matter *too* much once in PROD, but it does generally indicate that a certain model is larger
- Then, look at the next model, say the one with the second-"best" error metric, and note it's metric value, run duration, and size
- Continue this with the rest of the models
- **The comparison amongst these values (size, duration, score) are important things to note about models**
    - Say one model has a slightly worse RMSE but runs in 5 seconds and is 9MB compared to model with a slightly better RMSE but runs in 5 minutes and is 400MB?
    - *This trade-off must be considered*

## Promoting to the Model Registry
- In MLFlow, on the model's experiment run page, we can select the model directory under "Artifacts" and click "Register Model" on the right
- Then, we need to select the model (if created), or create one (if not)
- If we create a model, we name it, maybe something like `nyc-taxi-regressor`
- Once we click "register, then we see that the "Register Model" button disappears and we get a link to version 1 of the registered model
- We can then select another model, click "Register Model" for it, select the *same* model, and get a link version *2* of the model
- We now have the "Model" registry tab at the top of the UI
- We will see a list of all registerd models (you likely just have the one, `nyc-taxi-regressor`)
- Clicking on a model, we can see all of the versions of it (you should just have maybe 2 versions)
    - We can add some descriptions and tags (for easier search and retrieval) on this page
- We can then see each registered model version's details by clicking on it
    - We can again add some descriptions and tags (for easier search and retrieval) on this page, for a specific model version (such as tag name of "model" and value of "xgboost" or "gradient-boosting-regressor)
- Here we also see the link to this model's run, which brings us back to the page of parameters, metrics, artifacts, etc. for that model (run)
- This means we now have **model lineage**: we can link models to their experiment runs that trained them

## Assigning Models to Stages
- On a specific model version's page, at the top, we can see "Stage: None" to start (if we haven't already assigned a model to a stage)
- We can move our model versions to "Staging" if we want to at this time from this page
- This would be when we (as the data scientist, in this case) would want to let developers/engineers know that we want these models moved to Staging by looking at the registry and deciding (based on different ideas/goals/measurements/requirements) which ones would be moved

