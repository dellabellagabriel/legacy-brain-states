addpath ../../k-means/

% compute centroids
data = struct();
data.import_path = '../dataset/dynamic-wsmi';
data.export_path = '../dataset/k-means';
data.k = 3;
data.distance = 'cityblock';
data.replicates = 100;
data.subsample_factor = 1;
data.n_windows = 13;
data.n_channels = 128;

brainstates(data)

% classify matrices
load('../dataset/k-means/centroids.mat', 'C')
data.centroids = C;
states = classification(data);

% probability distribution and transition probability
[prob, trans] = probdist(states, 3);

