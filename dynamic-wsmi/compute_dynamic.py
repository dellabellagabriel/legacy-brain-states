from dynamic_wsmi import computeWSMI
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
        print('Ignoring ' + subject_filename + ' since it was found in progress.txt')
        continue
        
    computeWSMI(
        file_to_compute=subject,
        word_to_compute='word1',
        output_path='../examples/dataset/dynamic-wsmi',
        sample_rate=200,
        channels=128,
        samples_per_trial=480,
        tau=8,
        total_time=24,
        window_size=12,
        window_offset=1
    )
    f = open("progress.txt", "a").write(subject_filename + ',')