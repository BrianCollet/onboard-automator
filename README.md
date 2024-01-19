# Onboard Automator

**Onboard Automator** is a project inspired by [@madebygps'](https://github.com/madebygps) projects for the Azure AZ-104 that is designed to streamline and automate the onboarding process for new employees.

![Diagram](https://i.imgur.com/FT7RBtx.png)

## Azure Services Used

- Azure Blob Storage
- Azure Logic Apps
- Azure Function Apps
- Azure Resource Manager
- Azure Active Directory / Entra ID
- Office 365 / Outlook

## Workflow

1. HR initiates the onboarding process by uploading a CSV file containing details of new employees to an Azure Blob Storage folder.

2. A Logic App is configured to monitor the specified Azure Blob Storage folder. Once a CSV file is uploaded, the Logic App is triggered.

3. The Logic App first triggers an HTTP Function App coded in Python to convert the CSV file to JSON format and returns it to the Logic App.

4. The Logic App triggers another HTTP Function App, also coded in Python, to generate secure passwords for the new user accounts.

5. With the JSON data and generated passwords, user accounts are created in Azure Active Directory / Entra ID.

6. Temporary credentials are emailed to the manager for distribution to the respective employee(s).

7. Once all user accounts are successfully created, the original CSV file is moved to the _completed_ folder, and HR is notified via email.

## Getting Started

To use the Onboard Automator, follow these steps:

1. Create a new Resource Group

2. Create an App Registration in Entra ID

3. Assign the **Contributor** and **Role Based Access Control Administrator** roles to the app registration at either _Subscription_ or _Resource Group_ scope, or create your own custom role

4. Add **Federated Credentials** to the App Registration for Github Actions

5. Create the following Github secrets and populate with the details from your App Registration:

- **AZURE_TENANT_ID**
- **AZURE_SUBSCRIPTION_ID**
- **AZURE_CLIENT_ID**

6. Clone this repository locally

7. Update the following details for your environment:

   - [deploy_resources.yml](.github/workflows/deploy_resources.yml):

     - branch
     - RESOURCE_GROUP_NAME
     - FUNCTION_APP_NAME
     - FUNCTION_APP_SLOT

   - [functionAppArmParameters.json](./functionAppArmParameters.json):

     - app_service_plan_name
     - function_app_name
     - function_app_storage_account_name

   - [logicAppArmTemplate.json](./logicAppArmTemplate.json):
     - function_app_name
     - logic_app_name
     - csv_files_storage_account_name
     - logic_app_rbac - update if you want to assign an RBAC role to the Logic App's system-assigned managed identity other than [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor)
     - domain_name

8. Commit changes and push code to your Github repository

9. Once the Github Actions workflow succeeds, update the CI/CD settings of the Function App to point to your Github repository

10. Lastly, you need to authorize the Office 365 and Azure AD API connections in order for the Logic App to function. The Office 365 account should have a mailbox. The Azure AD account should have sufficient permissions to create a new user, etc.

## CSV File

[employees.csv](./employees.csv)

```
EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUMBER,HIRE_DATE,JOB_TITLE,DEPARTMENT,MANAGER_UPN
001,Michael,Scott,mscott@test.com,573-891-4321,08-23-2021,IT Manager,IT,admin@test.com
```

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | EMAIL           | PHONE_NUMBER | HIRE_DATE  | JOB_TITLE  | DEPARTMENT | MANAGER_UPN    |
| ----------- | ---------- | --------- | --------------- | ------------ | ---------- | ---------- | ---------- | -------------- |
| 001         | Michael    | Scott     | mscott@test.com | 573-891-4321 | 08-23-2021 | IT Manager | IT         | admin@test.com |

## Acknowledgments

- [@madebygps](https://github.com/madebygps)
- [Original repository](https://github.com/madebygps/projects)

## Future Additions

- Bicep deployment
- Terraform deployment
- Assign RBAC roles to users
