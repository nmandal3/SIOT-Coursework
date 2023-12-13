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

% Calculate Pearson correlation coefficients and p-values
[correlationCoefficients, pValues] = corr(table2array(normalisedFullDataTable(:, 2:end)), 'rows', 'pairwise');

% Get PCCs and p-values for GSR with other variables
gsrCorrelations = correlationCoefficients(gsrIndex, :);
gsrPValues = pValues(gsrIndex, :);

% Make result array
resultArray = [variableNames; num2cell(gsrCorrelations); num2cell(gsrPValues)];
disp(resultArray);
