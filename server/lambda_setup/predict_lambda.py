import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd
import sys

sys.path.insert(0, '/tmp/')
sys.path.append('/tmp/')

def lambda_handler(event, context):

    data = event['data'] or {}

    s3_client = boto3.client('s3')

    if (not os.path.exists('tmp/model.bin')):
        s3_client.download_file('hosted-models', 'model.bin', '/tmp/model.bin')
    
    if (not os.path.exists('tmp/load_predict.py')):
        s3_client.download_file('hosted-models', 'load_predict.py', '/tmp/load_predict.py')

    # Load model by calling load_predict module in load_predict.py

    from tmp.load_predict import load_predict

    df = pd.DataFrame(data, index=[0])

    result = load_predict(df, 'tmp/model.bin')    

    return {
        "prediction": str(result[0])
    }