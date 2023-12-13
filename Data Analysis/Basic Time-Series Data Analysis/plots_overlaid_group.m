clear;
close all;

% Read data from csv file
dataTable = readtable('sensor_data_all_headings.csv', 'Delimiter', ',');

% Extract timestamp and numerical data
timestamps = table2cell(dataTable(:, 1));
numericalData = table2array(dataTable(:, 2:end));

% Normalise numerical data
normalisedData = normalize(numericalData);

normalisedFullData = [timestamps, num2cell(normalisedData)];
normalisedFullDataTable = cell2table(normalisedFullData, 'VariableNames', [dataTable.Properties.VariableNames(1), strcat(dataTable.Properties.VariableNames(2:end), '_normalised')]);

% Convert timestamps to datetime format
timeStamps = datetime(normalisedFullData(:, 1), 'InputFormat', 'yyyy-MM-dd_HH-mm-ss');

% Variables to exclude in each figure
excludedSets = {...
    {'stemp_normalised', 'shumidity_normalised', 'apitemperature_normalised', 'apihumidity_normalised'}, ...
    {'apitemperature_normalised', 'apihumidity_normalised', 'pm10_normalised', 'pm25_normalised', 'so2_normalised', 'no2_normalised'}, ...
    {'stemp_normalised', 'shumidity_normalised', 'pm10_normalised', 'pm25_normalised', 'so2_normalised', 'no2_normalised'} ...
};

titlelabels = {'API Pollution on GSR', 'Sensor Temperature and Humidity on GSR', 'API Temperature and Humidity on GSR'};

% Define time ranges to exclude
excludedTimeRanges = {...
    {datetime('2023-11-27 15:30:00'), datetime('2023-11-28 11:15:00')}, ...
    {datetime('2023-11-28 17:23:00'), datetime('2023-11-29 11:24:30')}, ...
    {datetime('2023-11-29 17:23:30'), datetime('2023-11-30 11:38:00')}, ...
    {datetime('2023-11-30 17:42:00'), datetime('2023-12-01 14:15:00')} ...
};

% Create a new figure for each excluded set
for i = 1:length(excludedSets)
    excludedSet = excludedSets{i};
    
    % Create a new figure for each variable group
    figure;
    
    % Loop through each normalised variable and plot on the same figure
    for j = 2:size(normalisedFullData, 2)
        % Check if the variable should be excluded
        if any(strcmp(normalisedFullDataTable.Properties.VariableNames{j}, excludedSet))
            continue; % Skip excluded variables
        end

        % Smooth data using a moving average
        smoothedData = movmean(cell2mat(normalisedFullData(:, j)), 3);

        % Exclude excluded time periods
        for k = 1:numel(excludedTimeRanges)
            excludedRange = excludedTimeRanges{k};
            indicesToExclude = timeStamps >= excludedRange{1} & timeStamps <= excludedRange{2};
            smoothedData(indicesToExclude) = NaN;
        end

        % Plot smoothed data
        plot(timeStamps, smoothedData, 'DisplayName', normalisedFullDataTable.Properties.VariableNames{j});

        hold on;
    end

    title(titlelabels{i});
    xlabel('Time');
    grid on;
    
    % Set x-axis range + maximise window width
    xlim([datetime('2023-11-27 08:00:00'), datetime('2023-12-01 22:00:00')]);
    set(gcf, 'Position',  [0, 100, 2560, 500])

    legend('Location', 'Best');
    hold off;
end
