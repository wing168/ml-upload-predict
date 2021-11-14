import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

def lambda_handler(event, context):

    data = event['data'] or {}

    AWS_ACCESS_ID = os.environ['AWS_ACCESS_ID']
    AWS_SECRET = os.environ['AWS_SECRET']

    s3_client = boto3.client(
        's3',
        'eu-west-2',
        aws_access_key_id=AWS_ACCESS_ID,
        aws_secret_access_key=AWS_SECRET,
    )

    if (not os.path.exists('tmp/model.bin')):
        s3_client.download_file('hosted-models', 'model.bin', 'tmp/model.bin')
    
    if (not os.path.exists('tmp/load_predict.py')):
        s3_client.download_file('hosted-models', 'load_predict.py', 'tmp/load_predict.py')

    # Load model by calling load_predict module in load_predict.py

    from tmp.load_predict import load_predict

    df = pd.DataFrame(data, index=[0])

    result = load_predict(df, 'tmp/model.bin')    

    return {
        "prediction": str(result[0])
    }