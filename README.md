# DBscrips
Python's boto3 library scripts for DynamoDB data migration

Scripts README
This script fetches the schema (attribute definitions and key schema) of a DynamoDB table using the Boto3 library for AWS DynamoDB.

Prerequisites
Python 3.x installed on your system.
Boto3 library installed. You can install it using pip install boto3.
Configuration
Before running the script, you need to provide the necessary configuration parameters:

table_name: The name of the DynamoDB table from which you want to fetch the schema.
region_name: The AWS region in which the DynamoDB table is located.
access_key_id: Your AWS access key ID with appropriate permissions to access the DynamoDB table.
secret_access_key: Your AWS secret access key associated with the access key ID.
Make sure to replace the placeholder values in the script with the appropriate values for your AWS environment.

Usage
Save the script in a Python file (e.g., fetch_dynamodb_schema.py).
Open a terminal or command prompt.
Navigate to the directory where the script is saved.
Run the script by executing the following command: python fetch_dynamodb_schema.py.
The script will connect to the specified DynamoDB table and retrieve the attribute definitions and key schema.
The attribute definitions and key schema will be printed to the console.

getschema.py:
This script, getschema.py, is a Python script that fetches the schema (attribute definitions and key schema) of a DynamoDB table using the Boto3 library for AWS DynamoDB.
downloaddb.py:
This script, named downloaddb.py, exports the contents of a DynamoDB table to a CSV file using the Boto3 library for AWS DynamoDB.
writebatch.py:
Example usage of dynamodbClient.batch_write_item() on script named writebatch.py, writes data from a CSV file to an AWS DynamoDB table in batches using the Boto3 library on a microgrid related DB.

Note
Ensure that the AWS credentials provided have sufficient permissions to describe the specified DynamoDB table.
Make sure you have network connectivity and appropriate AWS credentials configured on your system.
Disclaimer: This script accesses AWS resources. Make sure to secure and protect your AWS credentials.
