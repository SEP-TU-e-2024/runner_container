# Azure setup
This document explains how to use and set up the VM Application publishing.

## Usage
There is a GitHub Actions workflow in place that will create a new VM Application version each time a tag is made.
The label of this tag defines the version of the VM Application, which should be in format `x.y.z.`, e.g. `1.1.4`.

To tag the most recent commit, use for example `git tag 0.0.29`. Then, to push it, use `git push origin 0.0.29`. This will then start the workflow, and it should automatically publish the VM Application Version.

## Initial setup
There are a few things that you should do initially to set up the workflow. Some of these are in Azure, some are on GitHub Actions.
Follow all the following steps to fully set up this workflow.

### Create initial VM Application version
1. Open the Azure Portal, and navigate to VM application versions.
2. Hit Create, and specify the resource group and the region.
3. Fill in a low version number (e.g. 0.0.1), and pick some command for install and uninstall script (it doesn't matter).
4. Hit Browse on the Source application package, and pick or create the storage account for storing the application zip files.
5. Then select the storage account, and create or select the container to use. Upload any file for testing and select it.
6. Back in the VM application version creation screen, select or create a compute gallery.
7. Create an VM application definition (hit 'Create new' on it), here you specify the VM application definition name. Leave it on Linux.

### Create App Registration
1. Head over to the App registrations page on the Azure Portal.
2. Start creating a new application, and give it a recognizable name. You can leave the remaining options as-is.
3. Create a secret for it in Manage > Certificates & secrets > Client secrets. Add a description, and an expiration time.
4. Make sure to copy the secret value and store it somewhere for now, as you won't be able to view it again later.
5. Go to your subscriptions page, and select the subscription you are hosting the app on. 
6. Go to Access control (IAM), and add a role assignment for role Contributor (in the Privileged administrator roles tab). In the members tab, select User, group or service principal (the app is the latter), and under Select members search for the name of the app that you previously chose. In case it doesn't show up in the search bar, and normal users also don't show up, you might not have the right permissions, consider doing this on the account of the person that owns the subscriptions.

### Set up Storage Account
1. Head over to the Storage accounts page on the Azure Portal.
2. Select your storage account, and open the Settings > Configuration tab.
3. Here, set 'Allow Blob anonymous access' to Enabled if not already done so.
4. Go to Data storage > Containers, and select the same container you created / selected previously. Click Change access level at the top, and select 'Blob' and hit OK.
5. Go to the Access control (IAM) tab, and add a role assignment for the Job function role 'Storage Blob Data Contributor', and under Select members search for the name of the app that you previously chose. In case it doesn't show up in the search bar, and normal users also don't show up, you might not have the right permissions, consider doing this on the account of the person that owns the subscriptions.

### GitHub Actions Variables & Secrets
You are now done with the Azure side of the setup. All that is left is configuring the GitHub Actions workflow. For these, the following variables need to be set (repository settings > Secrets and variables > Actions > Variables), which can be either in the repository or organization:
```
AZURE_APP_STORAGE: the name of your storage account
AZURE_APP_STORAGE_CONTAINER: the name of your storage container
AZURE_APP_STORAGE_GALLERY: the name of the compute gallery
AZURE_LOCATION: the location of your initial VM application version
AZURE_RESOURCE_GROUP: the name of the resource group the VM application version is under
AZURE_VM_APPLICATION_NAME: the name of your VM application definition
```

Furthermore, you need to set up the secret for authentication. On the same page as you were, navigate to Secrets at the top. Here, you can create a (repository or organisation) secret, named `AZURE_CREDENTIALS`. This should contain the following data:
```json
{
  "clientId": "<Application (client) ID, found under the App registrations page for your app>",
  "clientSecret": "<client secret that you previously stored>",
  "subscriptionId": "<Subscription ID, can e.g. be found under the subscriptions page>",
  "tenantId": "<Directory (tenant) ID, found under the App registrations page for your app>"
}
```
