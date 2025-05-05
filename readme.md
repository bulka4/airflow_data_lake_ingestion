# Intro
This is the Airflow app containerized using Docker. It can be ran on a local computer using Docker or it can be deployed on Azure Linux VM using Azure Pipelines and the azure-pipelines.yml YAML file.

# App deployment
In order to deploy this app we can create a CI/CD pipeline in Azure DevOps which will be performing following actions:
1. Build a Docker image using code from this repository and push it to the Azure Container Registry (ACR).
2. Pull a Docker image from ACR onto an Azure Linux VM and run it.

Before we create such a pipeline we need to create proper resources in Azure and Azure DevOps at first. We can do that automatically using Terraform and DevOps Rest API. Code and more documentation about doing this can be found in the azure_terraform and azure_devops_rest_api repositories respectively. Here are the high level steps we need to do in order to deploy this app:
1. **Prepare the Docker compose file** - We need to modify this file like it is described below in this documentation in the 'Docker compose file' section.
2. **Create Agent pool** - Using the 'azure_devops_rest_api' repository, ci_cd_setup > agent_pool_setup > setup.py script.
3. **Create ACR and Service Principal** - Using the 'azure_terraform' repository, create_acr module.
4. **Create an Azure Linux VM** - Using the 'azure_terraform' repository, create_linux_vm module.
5. **Create Variable group, Service connection and generate a YAML file** - Using the 'azure_devops_rest_api' repository, ci_cd_setup > acr_push_and_pull_setup > setup.py script.
6. **Create a CI/CD pipeline** - We need to move the generated YAML file to the repository with the Airflow app and set up a CI/CD pipeline in DevOps website. When creating a pipeline we need to choose an option to use an existing YAML file from repository.

# Agent pool
Here we will add Agents which will be used to perform actiones defined in the CI/CD pipeline. Agent is a software which we will install on the created Azure Linux VM and it will be performing steps defined in our CI/CD pipeline.

# ACR and Service Principal
ACR is used for storing Docker images. Our CI/CD pipeline will be pushing Docker images here and then pulling them onto the VM. Service Principal will be used for authentication when pulling and pushing images.

# Azure Linux VM
This is a VM which will be running our application as a Docker container and also here we will install an Azure Pipelines Self Hosted Agent which will be performing steps defined in our CI/CD pipeline.

# Variable group
The Variable group which we will create in DevOps Library will be used to store confidential credentials for the Service Principal used for authentication when pulling and pushing Docker images. Those credentials will be then used in the generated YAML file.

# Service connection
The Service connection which we will create in DevOps will be used for pushing Docker images to the ACR. It will be used in the generated YAML file.

# YAML file
We will generate the YAML file which is defining steps which needs to be performed in the CI/CD pipeline. Here is a high level overview of what we are defining in that YAML file:
- What Agent pool will be used.
- What Variable group will be used.
- Service connection ID which will be used for pushing Docker images to the ACR.
- Bash script used for pulling and running a Docker image. More details about that script are provided in the documentation in the azure_devops_rest_api repository.

# Docker compose file
We need to define a proper Docker image in the docker-compose.yaml file depending on if we want to run the Docker conainer locally or deploy it on Azure Linux VM.

If we want to run it locally then we need to specify in the docker-compose.yaml file the following image:
![alt text](images/image1.png)

And if we want to deploy in to the Azure Linux VM using the CI/CD pipelines created using the 'azure_devops_rest_api' repository, then we need to replace it with this image:
![alt text](images/image2.png)

Both lines are included in the docker-compose.yaml file. We just need leave the proper one and comment the other one.

In the second scenario we are using the environment variables to get the image name. Those variables will be created on the VM running the image before pulling the image during the CI/CD pipeline. It is described more detailed in the 'azure_devops_rest_api' repository.