%EEGLAB must be opened! 

eeglab
addpath ../../filtering/

data = struct();
data.import_path = '../dataset/raw';
data.export_path = '../dataset/filtered';
data.set_path = '../dataset/setfiles'; %optional
data.varname = 'word1';
data.final_sample_rate = 200;
data.band_high = 40;
data.band_low = 0.1;
data.channels = 128;
data.initial_sample_rate = 250;

bandpass(data)