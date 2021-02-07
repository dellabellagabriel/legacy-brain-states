import os.path as op
import os
import time

import numpy as np
import scipy.io as sio
import h5py

import mne
from nice import Markers
from nice.markers import (SymbolicMutualInformation)

def computeWSMI(file_to_compute, word_to_compute, output_path, sample_rate, channels, trials, samples_per_trial, tau):
    #file_to_compute: path to the mat file 
    #word_to_compute: variable name of the imported mat file (samples x channel)
    #output_path: path for exported mat files
    #sample_rate: sample rate in samples per second
    #channels: number of channels
    #trials: number of trials
    #samples_per_trial: samples per trial
    #tau: distance between "atoms" in a symbol

    MAT_FULLNAME = file_to_compute
    STD_MONTAGE = 'GSN-HydroCel-128'
    SAMPLE_RATE = sample_rate
    CHANNELS = channels
    TRIALS = trials
    SAMPLES_PER_TRIAL = samples_per_trial
    TAU = tau

    MAT_BASENAME = op.basename(MAT_FULLNAME).split('.')[0]
    MAT_VAR = word_to_compute
    FIF_FILENAME = output_path + '/' + MAT_BASENAME +'-'+ word_to_compute +'-epo.fif'
    HDF5_FILENAME = output_path + '/' + MAT_BASENAME +'-'+ word_to_compute +'-markers.hdf5'
    MAT_OUTPUT = output_path + '/' + MAT_BASENAME +'-'+ word_to_compute +'-wsmi.mat'

    start_time = time.time()

    #we import the mat file, it will be imported as samples x channel numpy array
    #Note: this won't work for certain matlab versions. Use the code commented below for older versions
    print('Loading mat file: ' + MAT_BASENAME + " - " + word_to_compute)
    healthy = {}
    sio.loadmat(MAT_FULLNAME, healthy)
    healthyData = np.array(healthy[MAT_VAR])

    # --- Code for matlab older versions
    # this method imports the variable as channel x samples so we have to transpose
    #with h5py.File(MAT_FULLNAME, 'r') as f:
    #    healthyData = np.array(f[MAT_VAR]).transpose()
    # --- End of code for older matlab versions

    # create info for mne container
    montage = mne.channels.make_standard_montage(STD_MONTAGE)
    channel_names = montage.ch_names
    sfreq = SAMPLE_RATE
    info = mne.create_info(channel_names, sfreq, ch_types='eeg', montage=montage)
    info['description'] = 'egi/256'

    #we reshape the array to trials x samples x channel
    healthyData = np.reshape(healthyData, (TRIALS,SAMPLES_PER_TRIAL,CHANNELS))

    #we reshape the array to trials x channels x samples for EpochsArray()
    healthyData = np.transpose(healthyData, (0, 2, 1))

    epochs = mne.EpochsArray(healthyData, info)
    epochs.save(FIF_FILENAME, overwrite=True)

    #we import the fif file
    epochs = mne.read_epochs(FIF_FILENAME, preload=True)

    #compute wsmi
    m_list = [
        SymbolicMutualInformation(
        tmin=None, tmax=0.6, method='weighted', backend='python', tau=TAU,
        method_params={'nthreads': 'auto', 'bypass_csd': False}, comment='weighted'),
    ]

    mc = Markers(m_list)
    mc.fit(epochs)

    #save the hdf5 file
    mc.save(HDF5_FILENAME, overwrite=True)

    print('Converting hdf5 to mat...')
    filename = HDF5_FILENAME
    with h5py.File(filename, "r") as f:
        # List all groups
        a_group_key = list(f.keys())[0]

        # Get the data
        data_labels = list(f[a_group_key])
        data = f['nice']

        values = list(data['marker']['SymbolicMutualInformation']['weighted']['key_data_'])

        sio.savemat(MAT_OUTPUT, {'data': values})
    
    #delete the fif file
    os.remove(FIF_FILENAME)

    print('Execution time: ', str(time.time() - start_time), 'sec')