import os
import logging
import boto3
from flask import current_app
from botocore.exceptions import ClientError


# upload to our S3 bucket
def upload_S3(file_name, bucket, object_name=None):


    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY'], 
                             aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])
    
    try:
        response = s3_client.upload_file(os.path.join(current_app.config['TEMP'], file_name), bucket, object_name)
        remove_tmp_file(os.path.join(current_app.config['TEMP'], file_name))
    except ClientError as e:
        logging.error(e)
        return False
    
    return True



def remove_tmp_file(file):
    os.remove(file)
