import sys, argparse, os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib.gridspec as gridspec

fig_typeface = 'Helvetica'
# fig_family   = 'sans-serif'
fig_family   = 'monospace'
fig_style    = 'normal'

def smooth_bin(n, b, bin_min, bin_max):

    b = b.astype(float)
    loc = [np.arange(len(b))[(b>=i-0.01) & (b<=i+0.1)] for i in np.arange(bin_min, bin_max, 0.1)]
    n_sbin = [n[i[:-1]] for i in loc]
    smooth_n = [np.sum(i) for i in n_sbin]
    smooth_b = np.arange(bin_min, bin_max, 0.1)+0.05

    return smooth_n, smooth_b

def get_data(df_temp, mode):
    if 'mm' in mode:
        data = df_temp['Unnamed: 9']
    else:
        _temp1 = df_temp['列6'].to_numpy()
        _temp2 = df_temp['列7'].to_numpy()
        _temp3 = df_temp['列8'].to_numpy()
        data = np.concatenate((_temp1, _temp2, _temp3))

    return data

def plotting_9PF(df, mode, binsize=0.02):
        
    f, ax = plt.subplots(
        6, 1, figsize=(5, 4.5), facecolor='white', dpi=200, 
        gridspec_kw={'hspace': 0.05, 'wspace': 0.}
        )

    bin_min_box = []; bin_max_box = []; y_max_box = []
    for idx, ii, zz in zip(
        range(6), [3,4,5,3,4,5],['X','X','X','Y','Y','Y']
        ):
        df_temp = df[df['列1'] == f'{zz}-{ii}']
        data = get_data(df_temp, mode)
        
        bin_min = np.round(np.min(data), decimals=1)-0.1
        bin_max = np.round(np.max(data), decimals=1)
        bin_min_box.append(bin_min)
        bin_max_box.append(bin_max)

        # main axis
        n, b, _ = ax[idx].hist(
            data, range=(bin_min, bin_max),
            bins=int((bin_max-bin_min)//binsize)+1)

        # percentage axis
        ax_tx = ax[idx].twinx() 
        smooth_n, smooth_b = smooth_bin(n, b, bin_min, bin_max)
        ax_tx.plot(
            smooth_b, (smooth_n/np.sum(n))*100, '.-', color='tab:red', lw=0.8)

        ax_tx.tick_params(
            axis='both', which='both', labelsize='x-small', direction='in', 
            width=.7, colors='tab:red')
        ax_tx.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax_tx.yaxis.label.set_color('tab:red')

        ax[idx].set_ylabel(f'{zz}-{ii}',  size='small', style=fig_style, family=fig_family)
        y_max_box.append(np.max(n))
        ax[idx].set_ylim(0, np.round(np.max(n))+5 )
        ax_tx.set_ylim(0, np.round(np.max((smooth_n/np.sum(n)))*100)+5 )

    for ii in range(6):
        ax[ii].tick_params(axis='both', which='both', labelsize='x-small', direction='in', width=.7)
        ax[ii].set_xlim(np.min(bin_min_box), np.max(bin_max_box))
        ax[ii].xaxis.set_minor_locator(AutoMinorLocator(5))
        ax[ii].yaxis.set_minor_locator(AutoMinorLocator(5))
        if ii != 5:
            ax[ii].set_xticklabels([])

    sub_save = 'Max-Min' if 'mm' in mode else 'Raw'
    ax[0].set_title(f'9 Points Flatness {sub_save}', size='small', style=fig_style, family=fig_family)
    ax[5].set_xlabel(f'Deformation Distribution', size='small', style=fig_style, family=fig_family)
    # ax.legend(fontsize=4.5, 
                # ncol=1, facecolor='none', 

    f.text(
        0.95, 0.5, 'Percentage (%)', size='small', style=fig_style, 
        family=fig_family, ha='center', va='center', rotation=270,
        color='tab:red')
    
    f.savefig(f'{input_file.split(".")[0]}_9PF {sub_save}.pdf', format='pdf', bbox_inches='tight')


def plotting_4SF(df, binsize=0.02):
    mode='raw'
    f, ax = plt.subplots(
        4, 1, figsize=(4, 3.5), facecolor='white', dpi=200, 
        gridspec_kw={'hspace': 0.05, 'wspace': 0.}
        )

    bin_min_box = []; bin_max_box = []; y_max_box = []
    for idx, ii, zz in zip(
        range(4), [1,2,1,2],['X','X','Y','Y']
        ):
        df_temp = df[df['列1'] == f'{zz}-{ii}']
        data = get_data(df_temp, 'raw')
        
        bin_min = np.round(np.min(data), decimals=1)-0.1
        bin_max = np.round(np.max(data), decimals=1)
        bin_min_box.append(bin_min)
        bin_max_box.append(bin_max)

        # main axis
        n, b, _ = ax[idx].hist(
            data, range=(bin_min, bin_max),
            bins=int((bin_max-bin_min)//binsize)+1)

        # percentage axis
        ax_tx = ax[idx].twinx() 
        smooth_n, smooth_b = smooth_bin(n, b, bin_min, bin_max)
        ax_tx.plot(
            smooth_b, (smooth_n/np.sum(n))*100, '.-', color='tab:red', lw=0.8)

        ax_tx.tick_params(
            axis='both', which='both', labelsize='x-small', direction='in', 
            width=.7, colors='tab:red')
        ax_tx.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax_tx.yaxis.label.set_color('tab:red')

        ax[idx].set_ylabel(f'{zz}-{ii}',  size='small', style=fig_style, family=fig_family)
        y_max_box.append(np.max(n))
        ax[idx].set_ylim(0, np.round(np.max(n))+5 )
        ax_tx.set_ylim(0, np.round(np.max((smooth_n/np.sum(n)))*100)+5 )

    for ii in range(4):
        ax[ii].tick_params(axis='both', which='both', labelsize='x-small', direction='in', width=.7)
        ax[ii].set_xlim(np.min(bin_min_box), np.max(bin_max_box))
        ax[ii].xaxis.set_minor_locator(AutoMinorLocator(5))
        ax[ii].yaxis.set_minor_locator(AutoMinorLocator(5))
        if ii != 3:
            ax[ii].set_xticklabels([])

    ax[0].set_title(f'Four Sides Flatness Raw', size='small', style=fig_style, family=fig_family)
    ax[3].set_xlabel(f'Deformation Distribution', size='small', style=fig_style, family=fig_family)
    # ax.legend(fontsize=4.5, 
                # ncol=1, facecolor='none', 

    f.text(
        0.95, 0.5, 'Percentage (%)', size='small', style=fig_style, 
        family=fig_family, ha='center', va='center', rotation=270,
        color='tab:red')
    
    sub_save = 'Max-Min' if 'mm' in mode else 'Raw'
    f.savefig(f'{input_file.split(".")[0]}_4SF {sub_save}.pdf', format='pdf', bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog        = 'Simple code to plot deformation data',
        description = '''
        Simple code to plot deformation data.
        ''',
        epilog = "Created by Shih-Yun Tang Jun 4, 2022")
    parser.add_argument("filename", action="store",
                        help="Enter the file name under same dir", type=str)
    parser.add_argument("-binsize", dest="binsize", action="store",
                        help="bin size for histogram, default=0.02",
                        type=str,   default='0.02')
    # parser.add_argument('--version', action='version',  version='%(prog)s 0.5')
    args = parser.parse_args()
    
    input_file = args.filename
    print(f'Process {input_file}...')

    df = pd.read_excel(input_file)
    df = df[df['列1'].str.contains('X|Y').fillna(False)]
    
    try:
        print(f'plotting 9PF Max-Min')
        plotting_9PF(df, mode='mm', binsize=0.02)
    except:
        print('Error on processing 9PF Max-Min')
    
    try:
        print(f'plotting 9PF Raw')
        plotting_9PF(df, mode='raw', binsize=0.02)
    except:
        print('Error on processing 9PF Raw')
    
    try:
        print(f'plotting 4SF Raw')
        plotting_4SF(df, binsize=0.02)
    except:
        print('Error on processing 4SF Raw')

    print('Done')