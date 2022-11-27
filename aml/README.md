To deploy model registered in Azure ML using managed online endpoints:

#### Build the Docker image in the ```env``` folder with the conda dependencies, and push it to you Azure Container Registry. Sample code here:
```
docker build -t amlhuduaacr.azurecr.io/repo/env:v1 .
docker push amlhuduaacr.azurecr.io/repo/env:v1
```

#### Then run the following code in the Azure ML compute instance
```

az login
az extension add -n ml
az account set -s "<subscription name>"
az configure --defaults workspace=amlworkshopacename group=rgname
az ml online-endpoint create  -f aml/endpoint.yml
az ml online-deployment create  -f aml/deployment.yml

```
