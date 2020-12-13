#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 12:45:39 2020

@author: Sam Frederick
"""
import pandas as pd
import os
import shutil as sh
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
sns.set_style('darkgrid')


def MOI_Import(filename):
    """
    Parameters
    ----------
    filename : string
        Filename of dataset. Can be relative, but need to set cwd to folder
        where data are placed.

    Returns
    -------
    dataset : Pandas DataFrame
        Dataset with principal moments of interia, ellipticity for each 
        recorded timestamp in datafile.
    """
    # Read textfile as csv
    dataset = pd.read_csv(filename,
                          delimiter='\s+',
                          header=0)

    # Round the time column, set as index
    dataset['t'] = round(dataset['t'], 4)
    dataset = dataset.set_index('t', drop=True)

    # Compute ellipticity using Izz(t=0) for I_0 denominator term
    dataset['ellip'] = (dataset.Izz - dataset.Ixx)/(dataset.loc[0.0, 'Izz'])

    return dataset


def Plot_MOI_Ellip(df, savefig=False):
    """
    """
    fig, axs = plt.subplots(2,1,figsize=(9,7))
    plt.subplots_adjust(hspace=.35)
    
    axs[0].set_title('Principal Moments of Inertia')
    axs[0].plot(df.index, df.Ixx, df.index, df.Iyy, df.index, df.Izz)
    
    axs[0].legend(labels=['Ixx', 'Iyy', 'Izz'])
    axs[1].set_title('Stellar Ellipticity')
    axs[1].plot(df.index, df.ellip, c='purple')
    axs[1].legend(labels=['Ellipticity'])

    if savefig:
        today = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig('201206_MOI_ellip_'+today+'.png', dpi=300)


# -----------------------------------------------------------------------------
data_path = '/media/sam/BE48068348063B23/Simulation_Results/201206/'
extern_drive_path = '/media/sam/ASTRO_DATA/201206/'

# Copy every tenth data file from data directory to external drive
for cwd, folders, files in os.walk(data_path):
    for filename in files:
        if 'data' in filename:
            file_n = int(filename.replace('data.','').replace('.vtk',''))
            if file_n % 10 == 0:
                # Only write if file not in folder
                if not os.path.exists(extern_drive_path+filename):
                    sh.copyfile(data_path+filename, extern_drive_path+filename)
