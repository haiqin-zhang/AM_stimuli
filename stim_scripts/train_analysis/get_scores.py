import pandas as pd
import mido
import ast
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
import os

from train_utils import *

"""
Simple file to get the scores and 
"""

#PARAMETERS
#define the number of cycles in the training
numcycles = 2
exampleset = midi_target('../raw_training_files_wurli/passive listening.mid')
fullset = exampleset*numcycles

root_dir = "/Users/cindyzhang/Documents/M2/Audiomotor_Piano/AM_stimuli/stim_scripts/train_analysis/raw_keystrokes"
output_dir = "/Users/cindyzhang/Documents/M2/Audiomotor_Piano/AM_stimuli/stim_scripts/train_analysis/scores"


files = glob.glob(os.path.join(root_dir, '**', '*.csv'), recursive=True)

for sub_file in files:
   
    sub_name = sub_file.split('.')[0][-2:]
    print("Processing ", sub_name)

    subj_res = resp_pd(sub_file, fullset)    
    subj_res.to_csv(os.path.join(output_dir, f'scores_sub_{sub_name}.csv'), index=False)