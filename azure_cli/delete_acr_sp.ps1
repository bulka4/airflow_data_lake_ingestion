# delete specified service principal
param(
    [string] $SP_ID
)
az ad sp delete --id $SP_ID