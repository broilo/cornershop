import pandas as pd
import numpy as np
from datetime import (datetime, date)
import geopy.distance
import joblib
import json

class preprocess:
    
    # Replace Missing Values
    def replaceNull(df, col, change):
        """ss
        Describe the function!
        """
        df[col] = df[col].replace(np.nan, change)

    # Expand dates, create day of the week column and transform time to pure number
    def dateTimeConverter(dataset, col):
        """
        Describe the function!
        """
        day_of_week = list(pd.to_datetime(dataset[col], format='%Y-%m-%d').dt.dayofweek)
        dataset['day_of_week'] = day_of_week
        dataset[[col+'_DATE', col+'_HOUR']] = dataset[col].str.split(" ", expand=True)
        dataset[[col+'_HOUR', col+'_HOUR2']] = dataset[col+'_HOUR'].str.split("+", expand=True)
        dataset[[col+'_HH', col+'_MIN', col+'_SEC']] = dataset[col+'_HOUR'].str.split(":", expand=True)
        dataset['pure_time'] = dataset[col+'_HH'].astype(int) + (dataset[col+'_MIN'].astype(int) / 60) + (dataset[col+'_SEC'].astype(float) / 3600)
        
        dataset['day_of_week'] = dataset['day_of_week'].map(
            {
                0:'monday',
                1:'tuesday',
                2:'wednesday',
                3:'thursday',
                4:'friday',
                5:'saturday',
                6:'sunday'
            }
        )
        del dataset[col+'_HOUR2'], dataset[col+'_HH'], dataset[col+'_MIN'], dataset[col+'_SEC']

    # Calculate the distance between the deliver and the branch location
    def calculateDistance(dataset, latX, lngX, latY, lngY):
        """
        Describe the function!
        """
        coordsX = list(zip(dataset[latX], dataset[latX]))
        coordsY = list(zip(dataset[latY], dataset[latY]))

        dataset['coordsX'] = coordsX
        dataset['coordsY'] = coordsY
        dist = []

        for i in range(len(dataset)):
            distCalc = geopy.distance.distance(coordsX[i], coordsY[i]).km
            dist.append(distCalc)

        dataset['distance'] = dist

    # Calculate number of type of itens, weight and distinct itens per order
    def calculateItem(dataset, colUnit, colQuantity):
        """
        Describe the function!
        """
        no_item = []
        weight = []

        for i in range(len(dataset)):
            if dataset[colUnit][i] == 'UN':
                no_item.append(dataset[colQuantity][i])
                weight.append(0)
            elif dataset[colUnit][i] == 'KG':
                no_item.append(1)
                weight.append(dataset[colQuantity][i])
            else:
                no_item.append(np.nan)
                weight.append(np.nan)

        dataset['no_item'] = no_item
        dataset['weight'] = weight
        dataset['item'] = 1

    # Freeze Outliers in the corresponding listed values
    def getOutliers(dataset, file, ifHigh=True):
        """
        This function imports the outlier dictionary and apply it
        freezing values in a given dataset.

        Args:
            dataset (object/spreadsheet): The dataset under analysis.
            file (json): Dictionary containing the outliers entries.
            ifHigh (boolean): If True then freeze above percentile, else freeze below.

        Returns:
            dataset (object/spreadsheet): With freezed outlier values.
        """   
        with open(file, 'r') as convert_file: 
            outlier = json.load(convert_file)

        for key in outlier:
            if ifHigh:
                dataset.loc[dataset[key] > outlier[key], key] = outlier[key]
            else:
                dataset.loc[dataset[key] < outlier[key], key] = outlier[key]