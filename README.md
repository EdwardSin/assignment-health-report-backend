# Assignment - Health Declartion Backend

## Description:
This is the backend of the assignment of Health Covid Covid-19 declaration form.
Kindly refer to assignment-frontend for the Design Ideas.

## Development:
To run locally:
```
sam local start-api
```
To run target lambda function locally:
```
sam local invoke [FUNCTION_LOGICAL_ID]
```

## Deployment
AWS permission is required to deploy to the AWS Cloud.
```bash
sam build --use-container
sam deploy --guided
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name assignment-backend
```