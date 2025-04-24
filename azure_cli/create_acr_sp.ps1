# That script is creating a service principal with a goven role to the specified Azure Container Registry.
# before running this script we need to login using below command:
# az login
# parameter registry_name is a name of Azure Container Registry to which we want to authenticate (without the azurecr.io)
# parameter principal_name is a name of service principal which we will create (must be unique in AD tenant)
# parameter role is a role we want to assign to the created service principal (acrpush or acrpull)

param(
    [string]$registry_name
    ,[string]$principal_name
    ,[string]$role
)

# Modify for your environment.
# ACR_NAME: The name of your Azure Container Registry
# SERVICE_PRINCIPAL_NAME: Must be unique within your AD tenant
$ACR_NAME=$registry_name
$SERVICE_PRINCIPAL_NAME=$principal_name

# Obtain the full registry ID
$ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query "id" --output tsv)
# echo $registryId

# Create the service principal with rights scoped to the registry.
# Default permissions are for docker pull access. Modify the '--role'
# argument value as desired:
# acrpull:     pull only
# acrpush:     push and pull
# owner:       push, pull, and assign roles
$PASSWORD=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role $role --query "password" --output tsv)
$USER_NAME=$(az ad sp list --display-name $SERVICE_PRINCIPAL_NAME --query "[].appId" --output tsv)

# Output the service principal's credentials; use these in your services and
# applications to authenticate to the container registry.
write-output "Service principal ID: $USER_NAME"
write-output "Service principal password: $PASSWORD"