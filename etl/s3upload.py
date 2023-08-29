# csv_upload_script.py

import os
import boto3

def upload_csv_files(source_folder, bucket_name):
    s3 = boto3.client('s3')
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                s3_path = os.path.relpath(file_path, source_folder)  # Calculate relative path
                s3_key = os.path.join(bucket_name, s3_path.replace(os.path.sep, '/'))  # Convert path separators to S3-style
                s3.upload_file(file_path, bucket_name, s3_key)
                print(f"{file_path} uploaded to {s3_key}")

