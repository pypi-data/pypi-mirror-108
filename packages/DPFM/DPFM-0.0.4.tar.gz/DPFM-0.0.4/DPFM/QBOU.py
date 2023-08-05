import sys
import numpy as np
import xlrd
import re
import pandas as pd
from netCDF4 import Dataset


def QBOU(datapath):
    inp0 = Dataset(datapath, 'r')

    Time_Julian = inp0.variables['Time_Julian']
    Location = inp0.variables['Location']
    CTD_Conductivity = inp0.variables['CTD_Conductivity']
    CTD_Temperature = inp0.variables['CTD_Temperature']
    CTD_Pressure = inp0.variables['CTD_Pressure']
    Time = inp0.variables['Time']

    output = np.zeros((len(Time_Julian[0]), 11))
    Time = np.array(Time)
    Location = np.array(Location)
    Temperature = np.array(CTD_Temperature)
    Salinity = np.array(CTD_Conductivity)
    Depth = (np.array(CTD_Pressure)*10000)/(1025*9.8)

    for i in range(len(output)):
        for j in range(4):
            output[i][j] = int(Time.T[i][j])
        for k in range(2):
            output[i][6 + k] = Location.T[i][k]
        output[i, 8] = Temperature.T[i][0]
        output[i, 9] = Salinity.T[i][0]
        output[i, 10] = Depth.T[i][0]
    return output