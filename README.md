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

#### Step 4: Azure ML for model training
Now that the ML-ready dataset is saved in parquet format in the ```curated``` zone, one can use Azure ML for model training such as Designer and Auto ML

#### Step 5: Azure ML for model deployment
Go to the ```aml``` folder for model deployment to serve the trained model as a REST API for inferencing
