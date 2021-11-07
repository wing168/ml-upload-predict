from flask import Flask, request, jsonify
import logging
import boto3
from botocore.exceptions import ClientError
import os
import zipfile
import xgboost
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

    # Get the model and zip file
    s3_client.download_file('hosted-models', 'model.bin', 'tmp/model.bin')


    bst = xgboost.Booster()

    bst.load_model('tmp/model.bin')

    def fill_missing_values(data, list, fill):
        """
        For an input dataset, this function will fill the missing values based on the list defined and the fill_type (only options are median, mean and values)
        """

        for i in range(len(list)):
            if fill == "median":
                data[list[i]+"_cleaned"] = data[list[i]].fillna(value=data[list[i]].median())
            elif fill == "mean":
                data[list[i]+"_cleaned"] = data[list[i]].fillna(value=data[list[i]].mean())
            else:
                data[list[i]+"_cleaned"] = data[list[i]].fillna(value=fill)
        return data

    def convert_cat_to_num(data):
        """
        Takes an input dataset and converts all the categorical variables into numeric.
        """

        new_data = data

        for label, content in new_data.items():
            if not pd.api.types.is_numeric_dtype(content):
                # new_data[label] = content.astype("category").cat.as_ordered()
                new_data[label] = pd.Categorical(content).codes + 1
            
        return new_data

    df = pd.read_csv("./__mocks__/predict.csv")

    #Convert string to categorical
    df = convert_cat_to_num(df)

    #Fill missing values

    #Median for vh_age, vh_speed, vh_weight and population
    df = fill_missing_values(df, list=["vh_age", "vh_speed","vh_weight", "vh_value"], fill="median")

    #Driver related factors will be filled with 999
    df = fill_missing_values(df, list=["drv_age2", "drv_age_lic2"], fill=999)

    # initial tests without using year 4 data

    modelVars = [item for item, content in df.items()]

    # Drop some variables here

    modelVars.remove('id_policy')

    #DMatrix

    DMatPredict = xgboost.DMatrix(df[modelVars])

    #Predict

    result = bst.predict(DMatPredict)

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