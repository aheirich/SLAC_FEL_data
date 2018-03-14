#!/usr/bin/env python

"""
OcelotScan*.mat data scraper
"""

# BEND_DMP1_400_BDES - beam energy in GeV
# GDET_FEE1_241_ENRCHSTBR - FEL pulse energy in mJ

# time_stamp - time in seconds (unique to each shot)
# ts - time in seconds (since 1970? 1900? 0AD?) (unique to each Ocelot scan)
# ts_str - time in date+time format (unique to each Ocelot scan)

# charge - beam charge in pC (added in July 2017)
# current - beam current in A (added July 2017)

verboseQ = False

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.io as sio # provides loadmat and savemat functions
#import os, urllib2, json
#import subprocess
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import os

# run ocelotscraper.py first
months = ["2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12"]
df_pickles = ["ocelotscrapes_" + month + ".pkl" for month in months]
print 'df_pickles', df_pickles


if 'df_pickles' in locals():
    df = pd.DataFrame()
    for df_pickle in df_pickles:
        data = pd.read_pickle(df_pickle)
        df = df.append(data,ignore_index=True)

    # print keys
    keys = df.keys()
    string = "keys: "
    for key in keys:
      string = string + key + ", "
    print string

    # print quads
    quads = keys[np.array([key[:4]=='QUAD' for key in keys])]
    quads = [quad.replace(":","_") for quad in quads]
    print "quads: ", quads
    rows, columns = df.shape
    for r in range(rows):
      string = ""
      for c in range(columns):
        if c > 0:
          string = string + ','
        string = string + str(df.iat[r, c]) 
      print string
