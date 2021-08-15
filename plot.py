import subprocess
import random
import time
import os
import csv
import glob
import getpass
from pathlib import Path
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
sns.set()
sns.set_theme(style="whitegrid")
sns.set_palette("bright")

colors = sns.color_palette("bright", 4)

def plotIndividualData(algorithm):
    processor_list = np.array(getProcessorList())
    for i, procesor in enumerate(processor_list):
        fig =  plt.figure(figsize=(24, 12))
        G = matplotlib.gridspec.GridSpec(3,3)
        ax0 = plt.subplot(G[0,0])
        ax1 = plt.subplot(G[0,1], sharey=ax0)
        ax2 = plt.subplot(G[0,2], sharey=ax0)
        ax3 = plt.subplot(G[1,:], sharex=ax0)
        ax4 = plt.subplot(G[2,:], sharex=ax0)
        print(procesor)
        filename = f'./results/processors/{procesor}/result_{algorithm}.txt'
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            array_size = []
            time_spent = []
            PAPI_L1_TCM = []
            PAPI_L2_TCM = []
            PAPI_L3_TCM = []
            DATA_BYTES = []
            NUM_INSTRUCTIONS = []
            PAPI_TOT_INS = []
            theorical_instructions_per_second = []
            papi_instructions_per_second = []
            for row in csv_reader:
                if line_count == 0:
#                     print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    array_size.append(int(row[0]))
                    time_spent.append(float(row[1]))
                    PAPI_L1_TCM.append(int(row[2]))
                    PAPI_L2_TCM.append(int(row[3]))
                    PAPI_L3_TCM.append(int(row[4]))
                    DATA_BYTES.append(int(row[5]))
                    NUM_INSTRUCTIONS.append(int(row[6]))
                    PAPI_TOT_INS.append(int(row[7]))
                    papi_instructions_per_second.append(int(row[7]) / float(row[1]))
                    theorical_instructions_per_second.append(int(row[6]) / float(row[1]))
                    line_count += 1
                    
            ax0.plot(DATA_BYTES, PAPI_L1_TCM, label=procesor.replace('_', ' '), color=colors[i])
            ax0.set_xlabel('Bytes')
            ax0.set_ylabel('L1 MISS')
            ax0.set_title('Bytes x L1 Miss')
            ax0.margins(x=0.005, y=0.01)
            ax0.grid()
            ax0.legend()
            ax0.set_yscale('log', basey=10)
            ax0.set_xscale('log', basex=2)
                    
            ax1.plot(DATA_BYTES, PAPI_L2_TCM, label=procesor.replace('_', ' '), color=colors[i])
            ax1.set_xlabel('Bytes')
            ax1.set_ylabel('L2 MISS')
            ax1.set_title('Bytes x L2 Miss')
            ax1.margins(x=0.005, y=0.01)
            ax1.grid()
            ax1.legend()
            ax1.set_yscale('log', basey=10)
            ax1.set_xscale('log', basex=2)
                    
            ax2.plot(DATA_BYTES, PAPI_L3_TCM, label=procesor.replace('_', ' '), color=colors[i])
            ax2.set_xlabel('Bytes')
            ax2.set_ylabel('L3 MISS')
            ax2.set_title('Bytes x L3 Miss')
            ax2.margins(x=0.005, y=0.01)
            ax2.grid()
            ax2.legend()
            ax2.set_yscale('log', basey=10)
            ax2.set_xscale('log', basex=2)
            
            ax3.plot(DATA_BYTES, papi_instructions_per_second, label=procesor.replace('_', ' '), color=colors[i])
            ax3.set_xlabel('Bytes')
            ax3.set_ylabel('Instructions/s')
            ax3.set_title('Bytes x Instructions/s')
            ax3.margins(x=0.005, y=0.01)
            ax3.grid()
            ax3.legend()
            ax3.set_xscale('linear')
            
            ax4.plot(DATA_BYTES, time_spent, label=procesor.replace('_', ' '), color=colors[i])
            ax4.set_xlabel('Bytes')
            ax4.set_ylabel('Elapsed time')
            ax4.set_title('Bytes x Elapsed time')
            ax4.margins(x=0.005, y=0.01)
            ax4.grid()
            ax4.legend()
            ax4.set_yscale('linear')
            ax4.set_xscale('linear')
        
            if 'quick' in algorithm:
                ax1.set_ylim((8.894826701741161, 1371239.756431956))
                ax2.set_ylim((8.894826701741161, 1371239.756431956))
                ax3.set_ylim((2062528.8310025309, 7442400.797822733))
                ax4.set_ylim((-0.16529001236000002, 29.44429124836))
            elif 'merge' in algorithm:
                ax1.set_ylim((7.166842524222215, 533414.2597775133))
                ax2.set_ylim((7.166842524222215, 533414.2597775133))
                ax3.set_ylim((2609156.8676255187, 12525188.689335998))
                ax4.set_ylim((-0.14750971194899998, 27.138481396449))

        plt.subplots_adjust(hspace=0.4)
        fig.suptitle(algorithm.replace('_', ' ').title(), fontsize=16)
        # plt.show()
        fig.savefig(f'./charts/{algorithm}/{procesor}.png', bbox_inches = 'tight', dpi=300)
    

def plotData(algorithm):
    processor_list = np.array(getProcessorList())
    fig =  plt.figure(figsize=(24, 12))
    G = matplotlib.gridspec.GridSpec(3,3)
    ax0 = plt.subplot(G[0,0])
    ax1 = plt.subplot(G[0,1], sharey=ax0)
    ax2 = plt.subplot(G[0,2], sharey=ax0)
    ax3 = plt.subplot(G[1,:], sharex=ax0)
    ax4 = plt.subplot(G[2,:], sharex=ax0)
    for i, procesor in enumerate(processor_list):
        print(procesor)
        filename = f'./results/processors/{procesor}/result_{algorithm}.txt'
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            array_size = []
            time_spent = []
            PAPI_L1_TCM = []
            PAPI_L2_TCM = []
            PAPI_L3_TCM = []
            DATA_BYTES = []
            NUM_INSTRUCTIONS = []
            PAPI_TOT_INS = []
            theorical_instructions_per_second = []
            papi_instructions_per_second = []
            for row in csv_reader:
                if line_count == 0:
#                     print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    array_size.append(int(row[0]))
                    time_spent.append(float(row[1]))
                    PAPI_L1_TCM.append(int(row[2]))
                    PAPI_L2_TCM.append(int(row[3]))
                    PAPI_L3_TCM.append(int(row[4]))
                    DATA_BYTES.append(int(row[5]))
                    NUM_INSTRUCTIONS.append(int(row[6]))
                    PAPI_TOT_INS.append(int(row[7]))
                    papi_instructions_per_second.append(int(row[7]) / float(row[1]))
                    theorical_instructions_per_second.append(int(row[6]) / float(row[1]))
                    line_count += 1
                    
            ax0.plot(DATA_BYTES, PAPI_L1_TCM, label=procesor.replace('_', ' '))
            ax0.set_xlabel('Bytes')
            ax0.set_ylabel('L1 MISS')
            ax0.set_title('Bytes x L1 Miss')
            ax0.margins(x=0.005, y=0.01)
            ax0.grid()
            ax0.legend()
            ax0.set_yscale('log', basey=10)
            ax0.set_xscale('log', basex=2)
                    
            ax1.plot(DATA_BYTES, PAPI_L2_TCM, label=procesor.replace('_', ' '))
            ax1.set_xlabel('Bytes')
            ax1.set_ylabel('L2 MISS')
            ax1.set_title('Bytes x L2 Miss')
            ax1.margins(x=0.005, y=0.01)
            ax1.grid()
            ax1.legend()
            ax1.set_yscale('log', basey=10)
            ax1.set_xscale('log', basex=2)
                    
            ax2.plot(DATA_BYTES, PAPI_L3_TCM, label=procesor.replace('_', ' '))
            ax2.set_xlabel('Bytes')
            ax2.set_ylabel('L3 MISS')
            ax2.set_title('Bytes x L3 Miss')
            ax2.margins(x=0.005, y=0.01)
            ax2.grid()
            ax2.legend()
            ax2.set_yscale('log', basey=10)
            ax2.set_xscale('log', basex=2)
            
            ax3.plot(DATA_BYTES, papi_instructions_per_second, label=procesor.replace('_', ' '))
            ax3.set_xlabel('Bytes')
            ax3.set_ylabel('Instructions/s')
            ax3.set_title('Bytes x Instructions/s')
            ax3.margins(x=0.005, y=0.01)
            ax3.grid()
            ax3.set_xscale('linear')
    
            ax4.plot(DATA_BYTES, time_spent, label=procesor.replace('_', ' '))
            ax4.set_xlabel('Bytes')
            ax4.set_ylabel('Elapsed time')
            ax4.set_title('Bytes x Elapsed time')
            ax4.margins(x=0.005, y=0.01)
            ax4.grid()
            ax4.legend()
            ax4.set_yscale('linear')
            ax4.set_xscale('linear')
    plt.subplots_adjust(hspace=0.4)
    fig.suptitle(algorithm.replace('_', ' ').title(), fontsize=16)
    # plt.show()
    fig.savefig(f'./charts/{algorithm}.png', bbox_inches = 'tight', dpi=300)

def getProcessorList():
    dirlist = []
    for filename in os.listdir("./results/processors/"):
        if os.path.isdir(os.path.join("./results/processors/",filename)):
            dirlist.append(filename)
    if '.ipynb_checkpoints' in dirlist:
        dirlist.remove('.ipynb_checkpoints')
    return dirlist

for filename in ['merge_sort.cpp', 'quick_sort.cpp']:
    plotData(filename[:-4])
    plotIndividualData(filename[:-4])