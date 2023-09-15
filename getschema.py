import csv
import boto3
import time


def get_table_schema(table_name, region_name, access_key_id, secret_access_key):
    client_config = {
        'region_name': region_name,
        'aws_access_key_id': access_key_id,
        'aws_secret_access_key': secret_access_key
    }
    dynamodb = boto3.client('dynamodb', **client_config)

    response = dynamodb.describe_table(TableName=table_name)

    # Extract attribute definitions
    attribute_definitions = response['Table']['AttributeDefinitions']
    
    # Extract key schema
    key_schema = response['Table']['KeySchema']
    
    return attribute_definitions, key_schema

# Specify your table name, region, access key ID, and secret access key
table_name = ''
region_name = ''
access_key_id = ''
secret_access_key = ''

# Retrieve the table schema
attribute_definitions, key_schema = get_table_schema(table_name, region_name, access_key_id, secret_access_key)

# Print attribute definitions
print("Attribute Definitions:")
for attribute in attribute_definitions:
    print(attribute['AttributeName'], attribute['AttributeType'])

# Print key schema
print("\nKey Schema:")
for key in key_schema:
    print(key['AttributeName'], key['KeyType'])

