import boto3
import csv
import time

# Set up AWS credentials
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region_name = ''  # Update with your desired AWS region

# Set up DynamoDB table details
table_name = 'dbconfig'

# Set up CSV file details
csv_file_name = 'dynamodb_data.csv'

# Create DynamoDB client
dynamodb = boto3.client('dynamodb',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=aws_region_name)

# Scan the DynamoDB table to retrieve all items
def scan_table():
    response = dynamodb.scan(TableName=table_name)
    return response

# Handle throttling exceptions with exponential backoff
def handle_throttling_exception(retries):
    max_retries = 5
    base_sleep_time = 0.1

    sleep_time = base_sleep_time * (2 ** retries)
    time.sleep(sleep_time)

    if retries >= max_retries:
        raise Exception("Max retries exceeded. Throttling exception still persists.")

    return retries + 1

# Perform the scan operation with retries
def perform_scan():
    retries = 0
    while True:
        try:
            response = scan_table()
            return response
        except dynamodb.exceptions.ProvisionedThroughputExceededException:
            retries = handle_throttling_exception(retries)

response = perform_scan()

# Extract the items from the response
items = response['Items']

# Paginate through all items if the table has more than the maximum limit (1 MB)
while 'LastEvaluatedKey' in response:
    retries = 0
    while True:
        try:
            last_evaluated_key = response['LastEvaluatedKey']
            response = perform_scan()
            items.extend(response['Items'])
            print(f"Downloaded {len(items)} items so far...")
            break
        except dynamodb.exceptions.ProvisionedThroughputExceededException:
            retries = handle_throttling_exception(retries)

# Extract attribute names from the first item
attribute_names = list(items[0].keys())

# Open the CSV file for writing
with open(csv_file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=attribute_names)

    # Write the header row
    writer.writeheader()

    # Write each item as a row in the CSV file
    total_items = len(items)
    for index, item in enumerate(items, 1):
        writer.writerow(item)
        print(f"Progress: {index}/{total_items}", end='\r')

print("Download complete!")
