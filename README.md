# brain-states
This is a toolbox for computing EEG brain states by using wSMI, sliding window and k-means clustering

## Required
You will need to have the following packages and programs
* Python 3.x
* NumPy (https://numpy.org/)
* SciPy (https://www.scipy.org/)
* h5py (https://www.h5py.org/)
* MNE (https://mne.tools/stable/index.html)
* NICE Tools (https://github.com/nice-tools/nice)
* MATLAB
* EEGLAB Toolbox (https://sccn.ucsd.edu/eeglab/index.php)

# Functions
* filtering: Applies a bandpass filter and subsampling
* stationary-wsmi: Computes the wSMI matrix for the whole session
* dynamic-wsmi: Uses the sliding window technique and computes a wSMI matrix for every window
* k-means: Using the result from dynamic-wsmi the windows are classified into centroids using the k-means clustering algorithm

# Examples
You can find examples for every function in the "example" folder.
