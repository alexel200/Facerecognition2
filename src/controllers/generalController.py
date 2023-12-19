import json
import os
import uuid

# Import other dependencies
import cv2
import numpy as np
import pandas as pd

import tensorflow as tf
from flask import request, app, Response
from pymongo import MongoClient

from src.modelFiles.layers import L1Dist

client = MongoClient("mongodb+srv://alexel200:yAXXQHGA1xGIXjiJ@facedetection.ckah3mj.mongodb.net/", 27017)
db = client.faceDetection

# Load image from file and conver to 100x100px
def preprocess(file_path):
    # Read in image from file path
    byte_img = tf.io.read_file(file_path)
    # Load in the image
    img = tf.io.decode_jpeg(byte_img)

    # Preprocessing steps - resizing the image to be 100x100x3
    img = tf.image.resize(img, (100, 100))
    # Scale image to be between 0 and 1
    img = img / 255.0

    # Return image
    return img


def uploadPhoto():
    uploaded_file = request.files['image']
    user = request.form['user']
    savePhoto(uploaded_file, user)
    return "Success"

def savePhoto(img, user, isVerificationFolder = False):
    # Folder definition
    BASE_PATH = os.path.dirname(os.path.join(app.current_app.config['BASE_PATH'], 'src'))
    USER_VERIFICATION_FOLDER = os.path.join(BASE_PATH, 'images', 'verification', user)
    USER_FOLDER = os.path.join(BASE_PATH, 'images', 'users', user)

    fileFullPath = ""
    if(isVerificationFolder):
        if(not os.path.exists(USER_VERIFICATION_FOLDER)):
            os.mkdir(USER_VERIFICATION_FOLDER)
        filename = '{}.jpg'.format(uuid.uuid1())
        fileFullPath = os.path.join(USER_VERIFICATION_FOLDER, filename)
    else:
        if (not os.path.exists(USER_FOLDER)):
            os.mkdir(USER_FOLDER)
        filename = '{}.jpg'.format(uuid.uuid1())
        fileFullPath = os.path.join(USER_FOLDER, filename)

    img.save(os.path.join(fileFullPath))
    #img = cv2.imread(fileFullPath)
    #data_aug(img, USER_VERIFICATION_FOLDER if isVerificationFolder else USER_FOLDER, 9 if isVerificationFolder else 18)
    if(not isVerificationFolder):
        img = cv2.imread(fileFullPath)
        data_aug(img, USER_FOLDER, 18)

    return fileFullPath
def verifyUser():
    #get Request Data
    uploaded_file = request.files['image']
    user = request.form['user']

    # Folder definition
    BASE_PATH = os.path.dirname(os.path.join(app.current_app.config['BASE_PATH'], 'src'))
    USER_VERIFICATION_FOLDER = os.path.join(BASE_PATH, 'images', 'verification', user)
    USER_FOLDER = os.path.join(BASE_PATH, 'images', 'users', user)
    MODEL_FILES_PATH = os.path.join(BASE_PATH, 'modelFiles')

    # Global Parameters
    # Specify thresholds
    detection_threshold = 0.75
    verification_threshold = 0.75

    modelFile = os.path.join(MODEL_FILES_PATH, 'siamesemodelv2.h5')
    model = tf.keras.models.load_model(modelFile, custom_objects={'L1Dist': L1Dist})
    #Saved user verification file
    pathImg = savePhoto(uploaded_file, user, True)

    # Build results array
    results = []
    for image in os.listdir(USER_FOLDER):
        #for userImage in os.listdir(USER_VERIFICATION_FOLDER):
            #input_img = preprocess(os.path.join(USER_VERIFICATION_FOLDER, userImage))
        input_img = preprocess(pathImg)
        validation_img = preprocess(os.path.join(USER_FOLDER, image))
        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        results.append(result)

    # Detection Threshold: Metric above which a prediciton is considered positive
    detection = np.sum(np.array(results) > detection_threshold)

    # Verification Threshold: Proportion of positive predictions / total positive samples
    print("Len of user_folder", len(os.listdir(USER_FOLDER)))
    verification = detection / len(os.listdir(USER_FOLDER))
    verified = verification > verification_threshold
    print('verification', verification, end="\n")
    print('verified', verified, end="\n")
    print('results', results)
    print('detection', detection)
    resp = dict({'verification': verification, 'verified': verified, 'detection': detection})
    os.remove(pathImg)
    return json.dumps(resp, default=str)

def data_aug(img, savedPath, iterationNumber):
    for i in range(iterationNumber):
        img = tf.image.stateless_random_brightness(img, max_delta=0.02, seed=(1,2))
        img = tf.image.stateless_random_contrast(img, lower=0.6, upper=1, seed=(1,3))
        # img = tf.image.stateless_random_crop(img, size=(20,20,3), seed=(1,2))
        img = tf.image.stateless_random_flip_left_right(img, seed=(np.random.randint(100),np.random.randint(100)))
        img = tf.image.stateless_random_jpeg_quality(img, min_jpeg_quality=90, max_jpeg_quality=100, seed=(np.random.randint(100),np.random.randint(100)))
        img = tf.image.stateless_random_saturation(img, lower=0.9,upper=1, seed=(np.random.randint(100),np.random.randint(100)))

        fullpathImage = os.path.join(savedPath, '{}.jpg'.format(uuid.uuid1()))
        cv2.imwrite(os.path.join(fullpathImage), img.numpy())

def general():
    baseVariables, variables, trainingData, modelMetrics = [], [], [], []
    metrics = []
    mixTrainingVariables = []

    results = db.training.distinct('variables')
    for result in results:
        baseVariables.append(result)

    results = db.training.find()
    for result in results:
        variables.append(result.get('variables'))
        trainingData.append(result.get('trainingData'))
        modelMetrics.append(result.get('model_metrics_name'))

    auxEpoch = 0
    for index, training in enumerate(trainingData):
        for i, epoch in enumerate(training):
            tmp = epoch
            if 'epoch' in variables[index]:
                auxEpoch = variables[index]['epoch']
                del variables[index]['epoch']
            variables[index]['totalEpochs'] = auxEpoch
            tmp.update(variables[index])
            mixTrainingVariables.append(tmp)

        auxModel = modelMetrics[index][0]
        auxModel.update(variables[index])
        metrics.append(auxModel)

    df = pd.json_normalize(mixTrainingVariables)

    cols = list(df.columns)
    for col in cols:
        if(col != 'initialTime' or col != 'finalTime'):
            df[col] = df[col].astype(float)
        else:
            df[col] = pd.to_datetime(df[col], unit='ms')
    df['epochDuration'] = df.finalTime - df.initialTime
    del df['finalTime']
    del df['initialTime']

    cols = set(df.columns) - {'BATCH', 'BUFFER_SIZE', 'CLEAN_MODEL', 'PREFETCH', 'epoch'}
    df1 = df[list(cols)]

    finalAnalysis = json.loads(df1.groupby('LEARNING_RATE').describe().to_json(orient='index'))

    df = pd.json_normalize(metrics)
    cols = set(df.columns) - {'BATCH', 'BUFFER_SIZE', 'CLEAN_MODEL', 'PREFETCH', 'epoch'}
    df1 = df[list(cols)]
    cols = list(df1.columns)
    df1 = df1.astype(float)
    #for col in cols:
    #    df1[col] = df1[col].astype(float)
    general = df1.describe(include='all').to_json()

    modelStatistics = dict()

    modelStatistics['groupByLearningRate'] = json.loads(df1.groupby('LEARNING_RATE').describe(include='all').to_json(orient='index'))
    modelStatistics['general'] = json.loads(general)

    return {'baseVariables': baseVariables, 'finalAnalysis':finalAnalysis, 'trainingData': mixTrainingVariables, 'modelMetrics': modelStatistics}
