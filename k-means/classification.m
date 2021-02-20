function y = classification( datastruct )
    %Classification takes the whole series and centroids 
    %previously calculated with brainstates() and classifies
    %each real matrix as one of the centroids

    import_path = datastruct.import_path;
    n_windows = datastruct.n_windows;
    n_channels = datastruct.n_channels;
    centroids = datastruct.centroids;
    
    files = dir(strcat(import_path, '/*.mat'));
    filenames = {files(:).name};
    
    dataset = zeros(n_windows*length(filenames), n_channels*n_channels);
    for i=1:length(filenames)
       display(strcat('Processing ...', filenames{i}))
       
       load(strcat(import_path, '/', filenames{i}), 'data');
       datanew = reshape(data, n_windows, n_channels*n_channels);
        
       dataset((i-1)*n_windows+1:i*n_windows, :) = datanew;
    end
    
    distances = pdist2(dataset, centroids, 'cityblock');
    [~, km] = min(distances');
    y = km';

end

