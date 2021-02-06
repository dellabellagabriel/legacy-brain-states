function y = bandpass(datastruct)
    % Applies a bandpass filter and subsampling. 
    %datastruct must be a struct with the following fields:
    %import_path: Path to files for import (without filenames and without
    %final slash). It will process every mat file in that directory
    %varname: variable name inside the imported mat file. This variable has
    %to be a sample x channel matrix.
    %export_path: Path to export the mat files
    %initial_sample_rate: Initial sample rate
    %final_sample_rate: Desired final sample rate
    %band_high: highest frequency in the band
    %band_low: lowest frequency in the band
    %channels: number of channels
    %set_path: (optional) path for exporting set files. If the field
    %doesn't exist or is left empty it won't export set files.

    path_to_files = datastruct.import_path;
    save_mat_to = datastruct.export_path;
    matvar_name = datastruct.varname;
    sample_rate = datastruct.final_sample_rate;
    hpfreq = datastruct.band_high;
    lpfreq = datastruct.band_low;
    channels = datastruct.channels;
    display(channels)
    original_sample_rate = datastruct.initial_sample_rate;
    
    save_set_flag = false;
    if isfield(datastruct, 'set_path')
        if ~isempty(datastruct.set_path)
            save_set_to = datastruct.set_path;
            save_set_flag = true;
        end
    end

    files = dir(strcat(path_to_files, '/*.mat'));
    filenames = {files(:).name};

    for i=1:length(filenames)
        display(strcat('Processing ...', filenames{i}))

        load(strcat(path_to_files, '/', filenames{i}), matvar_name);
        word_data = word1';
        %we export word_data to the base workspace for EEGLAB
        assignin('base','word_data',word_data)
        whos word_data
        clear word1;

        display(filenames{i})
        display(original_sample_rate)
        EEG = pop_importdata('dataformat','array','nbchan',channels,'data','word_data','setname',filenames{i},'srate',original_sample_rate,'pnts',0,'xmin',0);
        EEG = pop_resample(EEG, sample_rate);
        EEG = pop_eegfiltnew(EEG, hpfreq, lpfreq);
        word1 = EEG.data';
        file_wo_ext = strsplit(filenames{i}, '.');
        
        if save_set_flag == true
            EEG = pop_saveset( EEG,  'filename', char(file_wo_ext(1)), 'filepath', save_set_to); 
        end
        output_name = strcat(save_mat_to, '/', file_wo_ext(1));
        save(char(output_name), matvar_name);

    end

end
