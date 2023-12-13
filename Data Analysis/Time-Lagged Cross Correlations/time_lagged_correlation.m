clear;
close all;

% Read data from csv file
dataTable = readtable('sensor_data_2023-11-27.csv', 'Delimiter', ',');

% Extract timestamp and numerical data
timestamps = table2cell(dataTable(:, 1));
numericalData = table2array(dataTable(:, 2:end));

% Normalise numerical data
normalisedData = normalize(numericalData);

normalisedFullData = [timestamps, num2cell(normalisedData)];
normalisedFullDataTable = cell2table(normalisedFullData, 'VariableNames', [dataTable.Properties.VariableNames(1), strcat(dataTable.Properties.VariableNames(2:end), '_normalised')]);

% Extract column names excluding timestamps
variableNames = normalisedFullDataTable.Properties.VariableNames(2:end);

% Find index of 'gsr' in the variable names
gsrIndex = find(strcmp(variableNames, 'gsr_normalised'));

% Specify time lag in minutes
samplingRate = 4; % minutes per sample
maxTimeLag = 60*5; % maximum desired time lag in minutes

% Initialise arrays to store results
results = cell(3, length(variableNames));

% Loop through each variable and calculate cross-correlation
for i = 1:length(variableNames)
    % Extract the current variable
    currentVariable = normalisedFullDataTable{:, i + 1}; % ignoring timestamp column
    
    % Calculate cross-correlation with 'gsr'
    [crossCorr, lag] = xcorr(currentVariable, normalisedFullDataTable{:, gsrIndex + 1}, maxTimeLag/samplingRate, 'coeff');
    
    % Extract coefficients and lags for negative time lags
    negativeLags = lag <= 0;
    crossCorrNeg = crossCorr(negativeLags);
    
    % Find peak value and respective time lag using highest absolute value
    [~, maxAbsIndex] = max(abs(crossCorrNeg));
    peakValue = crossCorrNeg(maxAbsIndex);
    peakTimeLag = lag(negativeLags);
    peakTimeLag = peakTimeLag(maxAbsIndex);
    
    % Result arrays
    results{1, i} = variableNames{i};
    results{2, i} = peakTimeLag*samplingRate;
    results{3, i} = peakValue;
    
    % Plot cross-correlation for each variable
    figure;
    plot(lag(negativeLags), crossCorrNeg);
    hold on;
    plot(peakTimeLag, peakValue, 'ro', 'MarkerSize', 10);
    title(['Cross-Correlation between ', variableNames{i}, ' and gsr (Negative Time Lags)']);
    xlabel('Time Lag (minutes)');
    ylabel('Cross-Correlation Coefficient');
    legend('Cross-Correlation', 'Peak');
    hold off;
end

disp(results);
