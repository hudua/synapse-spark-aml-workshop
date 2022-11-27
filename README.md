# synapse-spark-aml-workshop

#### Step 1: Data lake structure
Set-up common data lake structure to
* ```raw```: this is where you can upload the sample sensor CSV file
* ```delta```: this is where you save the delta tables
* ```curated```: this is where you can save the ML-ready and ML-predictions datasets

#### Step 2: Spark pool in Synapse
Create a spark pool in Synapse Analytics and make sure to upload the ```requirements.txt``` file to install additional libraries

#### Step 3: Spark analysis
Run the delta table and feature engineering / modeling scripts to
* Create delta table and enable SQL-queries
* Run feature engineering and modeling
* Register model with Azure ML and mlflow
* Even save the ML-ready dataset back in the data lake so Azure ML can be used for modeling too
