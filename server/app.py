from flask import Flask, request, jsonify
import logging
import boto3
from botocore.exceptions import ClientError
import os


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

    return "<h1>POST presigned URL</h1>"


# Use this for returning predictions
@app.route("/predict", methods=['POST'])
def predict_models():
    return "<h1>Predict models</h1>"

# source <venv>/Scripts/activate

# /signed GET & PUT
# /predict?model=:model
# root GET models