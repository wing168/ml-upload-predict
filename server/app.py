from flask import Flask, request, jsonify
import logging
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd


AWS_ACCESS_ID = os.environ['AWS_ACCESS_ID']
AWS_SECRET = os.environ['AWS_SECRET']

s3_client = boto3.client(
    's3',
    'eu-west-2',
    aws_access_key_id=AWS_ACCESS_ID,
    aws_secret_access_key=AWS_SECRET,
)

app = Flask(__name__)

# Use this for getting list of model files on S3
@app.route("/", methods=['GET'])
def get_models_list():
    
    return jsonify({
        "id": AWS_ACCESS_ID,
        "secret": AWS_SECRET,
    })


# Use this for getting signed URL
@app.route("/signed", methods=['POST'])
def get_signed():

    data = request.get_json()

    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': 'hosted-models',
                'Key': data['id'],
            }
        )

        return jsonify({
            'url': url,
        })
    except ClientError as e:
            logging.error(e)
            return jsonify({
                'error': e
            })

# Use this for returning predictions
@app.route("/predict", methods=['POST'])
def predict_models():

    data = request.get_json()

    # Get the model and zip file
    if (not os.path.exists('tmp/model.bin')):
        s3_client.download_file('hosted-models', 'model.bin', 'tmp/model.bin')
    
    if (not os.path.exists('tmp/load_predict.py')):
        s3_client.download_file('hosted-models', 'load_predict.py', 'tmp/load_predict.py')

    # Load model by calling load_predict module in load_predict.py

    from tmp.load_predict import load_predict

    df = pd.DataFrame(data, index=[0])

    result = load_predict(df, 'tmp/model.bin')    

    return jsonify({
        "prediction": str(result[0])
    })

# TODO:
# Extract zip and import python script as a module
# Read direct from S3 - ie without having to download model file

# source <venv>/Scripts/activate

# /signed GET & PUT
# /predict?model=:model
# root GET models