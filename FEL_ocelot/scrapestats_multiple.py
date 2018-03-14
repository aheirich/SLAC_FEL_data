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
months = ["2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-05","2017-06","2017-07"] # format "YYYY-MM"
df_pickles = ["ocelotscrapes_" + month + ".pkl" for month in months]

#plotdir = df_pickle[:df_pickle.find('.pkl')] + '/'
plotdir = 'all/'
try: os.makedirs(plotdir) # make a space for plots
except: pass

if 'df_pickles' in locals():
    df = pd.DataFrame()
    for df_pickle in df_pickles:
        data = pd.read_pickle(df_pickle)
        df = df.append(data,ignore_index=True)

    # print keys
    keys = df.keys()
    print "keys: ", keys

    # print quads
    quads = keys[np.array([key[:4]=='QUAD' for key in keys])]
    quads = [quad.replace(":","_") for quad in quads]
    print "quads: ", quads
    
    # Turn interactive plotting off
    plt.ioff()

    # beam energy vs time
    df.plot(kind='scatter', x='ts', y='BEND_DMP1_400_BDES', c='GDET_FEE1_241_ENRCHSTBR', vmin=0, vmax=5, alpha=0.5, title='Beam energy vs time', cmap='jet') # create figure with plot
    #plt.colorbar()
    plt.savefig(plotdir+'BEND_DMP1_400_BDES'+'_vs_'+'ts'+'.png') # save figure
    plt.close() # close figure to save memory

    # do some cuts

    # plot trends
    for quad in quads:
        df.query('abs('+quad+') < 120.').plot(kind='scatter', x='BEND_DMP1_400_BDES', y=quad, c='GDET_FEE1_241_ENRCHSTBR', vmin=0, vmax=5, alpha=0.5, title=quad+' vs beam energy (colored by GDET)', cmap='jet') # create figure with plot
        plt.savefig(plotdir+quad+'_vs_'+'BEND_DMP1_400_BDES_(GDET_FEE1_241_ENRCHSTBR).png') # save figure
        plt.close() # close figure to save memory
        
        df.query('abs('+quad+') < 120.').plot(kind='scatter', x='BEND_DMP1_400_BDES', y=quad, c='ts', vmin=df['ts'].min(), vmax=df['ts'].max(), alpha=0.5, title=quad+' vs beam energy (colored by ts)', cmap='jet') # create figure with plot
        plt.savefig(plotdir+quad+'_vs_'+'BEND_DMP1_400_BDES_(ts).png') # save figure
        plt.close() # close figure to save memory

    #plt.show()

else:
    print "Need to specify a pickle to import the DataFrame from"