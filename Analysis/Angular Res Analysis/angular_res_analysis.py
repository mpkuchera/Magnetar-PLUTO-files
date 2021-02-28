#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 09:53:01 2021

@author: samfrederick
"""
analysis_dir = ('/Users/samfrederick/Documents/GitHub/'
                'Magnetar-PLUTO-files/Analysis')
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from datetime import datetime
os.chdir(analysis_dir + '/Ellipticity Analysis')
from MOI_analysis import MOI_Import

sns.set_style('darkgrid')

os.chdir(analysis_dir + '/Angular Res Analysis')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def Errfill(xdata, ydata, yerr, color=None, alpha_fill=0.3, ax=None):
    """
    Error margin fill function
    Author: Tony Yu
    Link to code: 
    https://tonysyu.github.io/plotting-error-bars.html#.XVtPkS2ZPRY
    """
    ax = ax if ax is not None else plt.gca()
    
    if color is None:
        color = ax._get_lines.color_cycle.next()
        
    if np.isscalar(yerr) or len(yerr) == len(ydata):
        ymin = ydata - yerr
        ymax = ydata #+ yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    #ax.plot(xdata, ydata, color=color)
    ax.fill_between(xdata, ymax, ymin, color=color, alpha=alpha_fill)

def ImportData():
    # Angular resolution = 8 along polar axis (0, pi)
    ntheta8_loc = '/Users/samfrederick/Angular_Resolution_Tests/ntheta_8'
    os.chdir(ntheta8_loc)
    ntheta8 = MOI_Import(ntheta8_loc + '/' + 'InertiaTensorData.csv')
    ntheta8.dropna(axis=1, how='all')
    
    # Angular resolution = 16 along polar axis (0, pi)
    ntheta16_loc = '/Users/samfrederick/Angular_Resolution_Tests/ntheta_16'
    os.chdir(ntheta16_loc)
    ntheta16 = MOI_Import(ntheta16_loc + '/' + 'InertiaTensorData.csv')
    
    ntheta32_loc = ('/Users/samfrederick/Documents/GitHub/'
                    'Magnetar-PLUTO-files/Analysis/Ellipticity Analysis')
    os.chdir(ntheta32_loc)
    ntheta32 = MOI_Import(ntheta32_loc + '/' + '201206_InertiaTensor.csv')

    ntheta8 = Normalize(ntheta8)
    ntheta16 = Normalize(ntheta16)
    ntheta32 = Normalize(ntheta32)
    
    return ntheta8, ntheta16, ntheta32

def Normalize(df):

    for moi in ['Ixx', 'Iyy', 'Izz']:
        df[moi + '_normalized'] = df[moi]  / df.loc[0, moi]
    #df[[col for col in df_t8.columns if col.endswith('_normalized')]].plot()
    return df

def NormalizedMOIDataframe():
    """
    Combine dataframes at each angular resolution into a single dataframe
    """
    theta8_norm_df = ntheta8[[col for col in ntheta8.columns 
                              if (col.endswith('_normalized') or 
                                  col == 'ellip')]]
    theta16_norm_df = ntheta16[[col for col in ntheta16.columns 
                              if (col.endswith('_normalized') or 
                                  col == 'ellip')]]
    theta32_norm_df = ntheta32[[col for col in ntheta32.columns 
                              if (col.endswith('_normalized') or 
                                  col == 'ellip')]]
    
    norm_df = theta8_norm_df.join(theta16_norm_df,
                                  lsuffix='_theta8').join(theta32_norm_df, 
                                                          lsuffix='_theta16', 
                                                          rsuffix='_theta32')

    return norm_df

def Plots(norm_df, savefig=False):
    """
    Plot moments of inertia Izz, Ixx for various angular resolutions. Values 
    are normalized by the MOI values at t = 0 for comparison. Also plot
    corresponding ellipticity (via original data where error value is equal to
    the ellipticity at t = 0). 
    """
    # Drop index values with no MOI values, sort df alphabetic by MOI name                                    
    norm_df = norm_df.dropna()
    #norm_df = norm_df.reindex(sorted(norm_df.columns), axis=1)

    n_res = len([col for col in norm_df.columns if col.startswith('Ixx')])                                   

    n_colors = np.arange(1, n_res + 1)
    pad = 1
    norm = mpl.colors.Normalize(vmin=n_colors.min()-3*pad,
                                vmax=n_colors.max()+pad)
    
    Ixx_cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues)
    Ixx_cmap.set_array([])
    
    Izz_cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.OrRd)
    Izz_cmap.set_array([])
    
    ellip_cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.BuPu)
    ellip_cmap.set_array([])
                                                           
    fig, ax = plt.subplots(3, 2, figsize=(9, 5))
    z = 0
    for plt_idx, res in enumerate(['theta8', 'theta16', 'theta32']):
        i, j, k = 0 + z, 0 + z, 0 + z
        for col in norm_df:
            if col.endswith(res):
                
                # Ellipticity plots
                if col.startswith('ellip'):
                    color = ellip_cmap.to_rgba(k + 1)
                    ax[plt_idx, 1].plot(norm_df.index, norm_df[col], c=color,
                            label=col)
                    eps_0 = norm_df.loc[0, col]
                    Errfill(norm_df.index, norm_df[col], eps_0, color=color, 
                            ax=ax[plt_idx, 1])
                
                # MOI plots
                elif col.startswith('Ixx') or col.startswith('Izz'):
                    if col.startswith('Ixx'):
                        color = Ixx_cmap.to_rgba(i + 1)
                    if col.startswith('Izz'):
                        color = Izz_cmap.to_rgba(j + 1)
                    ax[plt_idx, 0].plot(norm_df.index, norm_df[col], c=color,
                            label=col)

        # y limits for ellip plots, include horiz line at y = 0 
        ax[plt_idx, 1].set_ylim(-0.15, 0.15)
        ax[plt_idx, 1].axhline(y=0, color='#949494',
                               linestyle='--')
        
        # y limits for MOI plots
        ax[plt_idx, 0].set_ylim(0.20, 1.1)
                    
                    

        ax[plt_idx, 0].legend(labels=['$I_{xx}$', '$I_{zz}$'],
                              fontsize=10)
        ax[plt_idx, 1].legend(labels=['$\epsilon$'], loc='upper left',
                              fontsize=10)
        plt.subplots_adjust(left=.3, right=.98, wspace=.3,
                            top=.925, bottom=.09)
        
        plt.text(-0.6, 0.5, 'a) $\Delta_{\\theta,\phi} = \\frac{\pi}{8}$',
                 horizontalalignment='center',
                 verticalalignment='center', transform=ax[0,0].transAxes,
                 fontsize=14)
        plt.text(-0.6, 0.5, 'b) $\Delta_{\\theta,\phi} = \\frac{\pi}{16}$',
                 horizontalalignment='center',
                 verticalalignment='center', transform=ax[1,0].transAxes,
                 fontsize=14)
        plt.text(-0.6, 0.5, 'c) $\Delta_{\\theta,\phi} = \\frac{\pi}{32}$',
                 horizontalalignment='center',
                 verticalalignment='center', transform=ax[2,0].transAxes,
                 fontsize=14)
        
        z += 1
    
    ax[2, 0].set_xlabel('Time (s)', fontsize=10)
    ax[2, 1].set_xlabel('Time (s)', fontsize=10)
    ax[0, 0].set_title('Normalized Principal\n Moments of Inertia',
                       fontsize=10)
    ax[0, 1].set_title('Ellipticity', fontsize=10)

    if savefig:
        today = datetime.now().strftime('%Y%m%d_%H%M')
        os.chdir(analysis_dir + '/Angular Res Analysis')
        plt.savefig('Angular_Res_Comparison.png', dpi=300)

ntheta8, ntheta16, ntheta32 = ImportData()
norm_df = NormalizedMOIDataframe()
norm_df = norm_df.loc[:20, :]
Plots(norm_df, savefig=True)
