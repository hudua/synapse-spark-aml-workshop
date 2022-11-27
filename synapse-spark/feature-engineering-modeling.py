# Check that you can query the delta table via SQL
%%sql
select * from wsibdb.sensordata

# Select it and convert to Pandas for feature engineering
df = spark.sql('select * from wsibdb.sensordata').toPandas()
print('Spark dataframe from Delta table queried')

# Run some correlation and create model dataset
df[['rpm','angle','temperature','humidity','windspeed','power']].astype(float).corr()
model_dataset = df[['windspeed','power']].astype(float)
print("Here is the correlation...", model_dataset.corr())

# Save in curated zone as a ML-ready dataset
spark.createDataFrame(model_dataset).write.mode("overwrite").parquet('abfss://synapse@adlsgenhuduaname.dfs.core.windows.net/curated/mlready/mldata.parquet')

# Visualize the data
model_dataset.plot.scatter(x = 'humidity',y='power')

# Now do model training
train_test_split_ratio = 0.7

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

print("Now we train linear regression model based on train/test split")
eva_model = LinearRegression()

X = np.array(model_dataset['humidity']).reshape(-1, 1)
y = np.array(model_dataset['power']).reshape(-1, 1)
X_train, X_test, X_train, y_test = train_test_split(X, y, test_size = 1-train_test_split_ratio)

eva_model.fit(X_train, X_train)
y_pred = eva_model.predict(X_test)
abs_error = np.mean(np.abs(y_pred - y_test))
print("Here is the absolute error", abs_error)

print("Now we train model on the entire dataset")
model = LinearRegression()
model.fit(X,y)

# Now we set up integration with Azure ML
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Workspace, Model, Experiment
interactive_auth = InteractiveLoginAuthentication(tenant_id="<tenant-id>")

ws = Workspace(
        workspace_name = "amlhuduaname",
        subscription_id = "subid",
        resource_group = 'rgworkshop'
    )

# Now we can use mlflow with Azure ML as backend server to track experiments and metrics
import datetime
import mlflow

mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
experiment_name = 'mlops_end2end'
mlflow.set_experiment(experiment_name)

print("Now we use mlflow to track experiments")

with mlflow.start_run() as mlflow_run:
    mlflow.log_param("trainingdatetime", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mlflow.log_metric("train_test_split", train_test_split_ratio)
    mlflow.log_metric("abs_error", abs_error)
import pickle, os

# Now we can register the model in Azure ML for model deployment

print("Now we use Azure ML to register model in AML registry")

pickle.dump(model, open('model.pkl', 'wb'))
model = Model.register(workspace = ws,
                       model_name="mlopsmodel",
                       model_path = "model.pkl",
                       description = 'Regression Model'
                      )
