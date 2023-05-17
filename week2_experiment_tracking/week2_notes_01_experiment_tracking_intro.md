## Experiment Tracking Introduction
- **Experiment** = the whole ML process of building a model
- **Experiment run** = each *trial* of an ML experiment
- **Run artifact** = any files generated during an ML run
- **Experiment metadata**: the parameters/information related to an ML experiment
- **Experiment tracking** = the process of saving/keeping track of ***relevant* information** of ML experiments (ex: version, source code, environment, data, model, hyperparameters, metrics, etc.)
    - "Relevant" information depends on the experiment being run
    - Data Scientis and/or MLE's may want to try different versions of the data

### Why is Experiment Tracking Important?
- 3 main reasons:
    - **Reproducibility** = science experiments should be reproducible
    - **Organization** = multiple people may be working on an ML experiment
    - **Optimization** = (of the ML model)