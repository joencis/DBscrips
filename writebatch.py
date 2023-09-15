import csv
import boto3
import time

start_time = time.time()

# Set up AWS credentials and region
clientConfig = {
    'region_name': '',
    'aws_access_key_id': '',
    'aws_secret_access_key': ''
}

# Create DynamoDB client
dynamodbClient = boto3.client('dynamodb', **clientConfig)

# Specify your DynamoDB table name
tableName = 'harveyTimedRecords'

# Read the CSV file
csv_file = '264.csv'

# Define a list to hold rows that were not written
not_written_rows = []

# Define a list to hold batch write requests
batch_write_requests = []

# Track the number of successfully written items
successful_items_count = 0

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    for row_number, row in enumerate(csv_reader, start=1):
        # Check if any required field is empty
        try:
            # Assign null for empty fields
            item = {
                'id': {'S': row[0]},
                'time': {'N': row[1]},
                'vBat': {'N': row[2].strip()} if row[2].strip() else {'NULL': True},
                'vPv': {'N': row[3].strip()} if row[3].strip() else {'NULL': True},
                'pLoad': {'N': row[4].strip()} if row[4].strip() else {'NULL': True},
                'pBat': {'N': row[5].strip()} if row[5].strip() else {'NULL': True},
                'xSoC': {'N': row[6].strip()} if row[6].strip() else {'NULL': True},
                'iBat': {'N': row[7].strip()} if row[7].strip() else {'NULL': True},
                'vLoad': {'N': row[8].strip()} if row[8].strip() else {'NULL': True},
                'pPv': {'N': row[9].strip()} if row[9].strip() else {'NULL': True}
            }
            
            # Create the PutRequest
            put_request = {
                'PutRequest': {
                    'Item': item
                }
            }
            
            # Add the PutRequest to the batch write requests list
            batch_write_requests.append(put_request)

            # Perform batch writes for every 25 items
            if len(batch_write_requests) == 25:
                # Create the BatchWriteItem request
                batch_write_item_request = {
                    'RequestItems': {
                        tableName: batch_write_requests
                    }
                }
                
                # Send the BatchWriteItem request
                response = dynamodbClient.batch_write_item(**batch_write_item_request)
                
                # Count the number of successfully written items
                successful_items_count += len(batch_write_requests)
                
                # Clear the batch write requests list
                batch_write_requests.clear()
                
                print(f'BatchWriteItem successful. Current count: {successful_items_count}')

        except Exception as e:
            print(f'Error writing item at row {row_number}: {str(e)}')
            not_written_rows.append(row)

# Write the remaining batch write requests
if batch_write_requests:
    # Create the BatchWriteItem request for remaining items
    batch_write_item_request = {
        'RequestItems': {
            tableName: batch_write_requests
        }
    }
    
    # Send the BatchWriteItem request for remaining items
    response = dynamodbClient.batch_write_item(**batch_write_item_request)
    
    # Count the number of successfully written items
    successful_items_count += len(batch_write_requests)
    
    # Clear the batch write requests list
    batch_write_requests.clear()
    
    print(f'BatchWriteItem successful for remaining items. Current count: {successful_items_count}')

# Write the rows that were not written to a new CSV file
if not_written_rows:
    not_written_csv_file = 'failed-rows.csv'
    with open(not_written_csv_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(not_written_rows)
    print(f'Rows that were not written are saved to {not_written_csv_file}.')

end_time = time.time()
total_time = end_time - start_time

print(f"The script took {total_time} seconds to run.")
