from stationary_wsmi import computeWSMI
import glob
import os

#we list all mat files in a directory
files = glob.glob('../examples/dataset/filtered/*.mat')
#this file saves the progress by writing the filename when it finishes. If you run it again it won't process
#files in this list
progress = open('progress.txt', 'r').read()

for subject in files:
    subject_filename = os.path.basename(subject)
    if subject_filename in progress:
        continue
        
    computeWSMI(
        file_to_compute=subject,
        word_to_compute='word1',
        output_path='../examples/dataset/stationary-wsmi',
        sample_rate=200,
        channels=128,
        trials=10,
        samples_per_trial=480,
        tau=8
    )
    f = open("progress.txt", "a").write(subject_filename + ',')