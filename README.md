# learn-azure-fastapi

Read this note: https://dinhanhthi.com/note/simple-azure-fastapi-app/#update-image-and-re-deploy-app-service-e1cee

## Setting up

With docker,

> [!NOTE]
> Change the names with yours!

```bash
# build docker image
docker build -t v2acr2.azurecr.io/v2daimg --platform=linux/amd64 .

# use compose.yaml (recommended)
docker compose up -d
# or using
docker run --name v2da --platform=linux/amd64 -dp 8000:8000 -dp 2222:2222 -v ./app:/app v2acr2.azurecr.io/v2daimg

# ssh to the container
ssh -p 2222 root@localhost
# password (checl Dockerfile): "Docker!"
# http://localhost:8000
# http://localhost:8000/docs
```

`prod` must be swapped with `preprod`. In case you want to manually trigger `prod`,

```bash
# build for Azure Container Registry
# (not recommended)
# login first
az login
az acr login --name v2acr2
# build image
docker build -t v2acr2.azurecr.io/v2daimg:prod --platform=linux/amd64 .
# push to ACR (no need if setting up auto deploy via Github)
docker push v2acr2.azurecr.io/v2daimg:prod
```

Without docker.

```bash
# create condata env
conda create -n v2da python=3.11
conda activate v2da
pip install -r app/requirements.txt

# dev
fastapi dev app/app.py

# prod
fastapi run app/app.py

# http://localhost:8000
# http://localhost:8000/docs
```

## Deployment

Don't connect to Github Action for production on Azure (branch `main`), we will use [swap](https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots?tabs=portal#swap-two-slots) from preprod for this slot.

Only branches `dev` and `preprod` have relation with Azure via Github Action. They will be automatically deployed on push.

**Workflow**: working on `dev` 👉 push to Github for test 👉 (wait for auto deployment on Azure via Github Action for slot `dev`) 👉 if everything is OK 👉 merge on `preprod` and push to Github 👉 (wait for auto deployment on Azure via Github Action for slot `preprod`) 👉 final tests.... 👉 swap `preprod` and `prod`.