# general
import warnings
import time
import gc

#data
import pandas as pd
import numpy as np
from datetime import (datetime, date)
import geopy.distance
import json

#preprocess
from _preprocess import *

#model
import joblib

### Global Variables
PATH_DATA = "../data/"
PATH_FILES = "../notebooks/"
DATASET = "20220329_merged_predict.csv"
MODEL = '20220403_set4_XGBRegressor.sav'
OUTLIER_HIGH = "20220401_outlier_dict_high.txt"
OUTLIER_LOW = "20220401_outlier_dict_low.txt"
DATE = time.strftime("%Y%m%d")

### List of Resources
selected = [
    'order_id', #-> index!
    'on_demand',
    'seniority',
    'found_rate',
    'picking_speed',
    'accepted_rate',
    'rating',
    'quantity',
    'item',
    'day_of_week',
    'pure_time',
    'distance',
    'no_item'
]

features_set4 = [
    'seniority_41dc7c9e385c4d2b6c1f7836973951bf',
    'seniority_50e13ee63f086c2fe84229348bc91b5b',
    'seniority_6c90661e6d2c7579f5ce337c3391dbb9',
    'seniority_bb29b8d0d196b5db5a5350e5e3ae2b1f',
    'on_demand',
    'pure_time',
    'found_rate',
    'picking_speed',
    'accepted_rate',
    'rating',
    'distance',
    'no_item',
    'quantity',
    'item'
]

def missingValues(data):
    # found_rate
    preprocess.replaceNull(data, 'found_rate', data.groupby(by='order_id').median()['found_rate'].median())
    # accepted_rate
    preprocess.replaceNull(data, 'accepted_rate', data.groupby(by='order_id').median()['accepted_rate'].median())
    # rating
    preprocess.replaceNull(data, 'rating', data.groupby(by='order_id').median()['rating'].median())
    # quantity
    preprocess.replaceNull(data, 'quantity', data['quantity'].median())

def featureEngineering(data):
    # Creating the resources: day_of_week and pure_time
    preprocess.dateTimeConverter(data, 'promised_time')
    # Creating the resource: distance
    preprocess.calculateDistance(data, 'lat_order', 'lng_order', 'lat_storebranch', 'lng_storebranch')
    # Creating the resources: number of itens, weight and distinct items per order
    preprocess.calculateItem(data, 'buy_unit', 'quantity')    

def groupAgg(data, cols):
    data = data[cols].groupby(by=[
        'order_id',
        'seniority',
        'on_demand',
        'day_of_week'
    ], as_index=False).agg(
        {
            'pure_time':['mean'],
            'found_rate':['mean'],
            'picking_speed':['mean'],
            'accepted_rate':['mean'],
            'rating':['mean'],
            'distance':['mean'],
            'no_item':['sum'],
            'quantity':['sum'],
            'item':['sum']
        }
    ).copy()
    data.columns = data.columns.droplevel(1)
    return data
    
def main():
        
    print("Running...")
    
    # Load Data
    df = pd.read_csv(PATH_DATA + DATASET, sep=',' )
    
    # Preprocess
    missingValues(df)
    
    # Feature Engineering
    featureEngineering(df)

    # Group and Aggregate
    df = groupAgg(df, selected)

    # Encoding
    df = pd.get_dummies(df, columns = ['seniority'])
    
    # Importing Outlier Dictionary
    preprocess.getOutliers(df, PATH_FILES + OUTLIER_HIGH, ifHigh=True)
    preprocess.getOutliers(df, PATH_FILES + OUTLIER_LOW, ifHigh=False)
    
    # Load Model & Predict
    
    model = joblib.load(PATH_FILES + MODEL)
    y_hat = model.predict(df[features_set4])
    
    # Save Predictions
    df['y_hat'] = y_hat
    df[['order_id','y_hat']].to_csv(DATE + "_outputs.csv", sep=',', index=False)
    
    print("Done!")
        
if __name__ == "__main__":
    main()
