clear;
close all;

% Read data from csv file
dataTable = readtable('sensor_data_2023-11-27.csv', 'Delimiter', ',');
validationTable = readtable('sensor_data_2023-11-30.csv', 'Delimiter', ',');

% Extract timestamp and numerical data
timestamps = table2cell(dataTable(:, 1));
numericalData = table2array(dataTable(:, 2:end));

timestampsVal = table2cell(validationTable(:, 1));
numericalDataVal = table2array(validationTable(:, 2:end));

% Normalise numerical data
normalisedData = normalize(numericalData);
normalisedFullData = [timestamps, num2cell(normalisedData)];
normalisedFullDataTable = cell2table(normalisedFullData, 'VariableNames', [dataTable.Properties.VariableNames(1), strcat(dataTable.Properties.VariableNames(2:end), '_normalised')]);

normalisedDataVal = normalize(numericalDataVal);
normalisedValidationFullData = [timestampsVal, num2cell(normalisedDataVal)];
normalisedValidationFullDataTable = cell2table(normalisedValidationFullData, 'VariableNames', [validationTable.Properties.VariableNames(1), strcat(validationTable.Properties.VariableNames(2:end), '_normalised')]);

% Get input and measured variables
X = normalisedFullDataTable{:, [2, 3, 5, 6, 7, 8, 9, 10]}; % exclude timestamp and GSR
Y = normalisedFullDataTable{:, 4}; % GSR at column 4

XValidation = normalisedValidationFullDataTable{:, [2, 3, 5, 6, 7, 8, 9, 10]}; % exclude timestamp and GSR
YValidation = normalisedValidationFullDataTable{:, 4}; % GSR at column 4

% Split data into training and testing sets
trainRatio = 0.8;
splitIdx = round(trainRatio * length(X));
XTrain = X(1:splitIdx, :);
YTrain = Y(1:splitIdx);
XTest = X(splitIdx+1:end, :);
YTest = Y(splitIdx+1:end);

% Define neural network architecture
inputSize = size(XTrain, 8); % Number of input variables i.e. 8
hiddenLayerSize = 12;
outputSize = 1; % Number of measured variables i.e. 1 for GSR

net = feedforwardnet(hiddenLayerSize);
net.trainParam.showWindow = false;

% Train neural network
net = train(net, XTrain', YTrain');

% Make predictions on the test and validation sets
YPredTest = net(XTest');
YPredValidation = net(XValidation');

% Calulate RMSEs
rmseValidation = sqrt(mean((YPredValidation - YValidation').^2));
rmseTest = sqrt(mean((YPredTest - YTest').^2));

% Display RMSE values
disp(['Root Mean Squared Error on Test Set: ', num2str(rmseTest)]);
disp(['Root Mean Squared Error on Validation Set: ', num2str(rmseValidation)]);

% Plot actual vs predicted for training + testing set
figure;
plot(YTest, 'b', 'DisplayName', 'Actual');
hold on;
plot(YPredTest, 'r', 'DisplayName', 'Predicted');
xlabel('Time (samples)');
ylabel('Normalised GSR Value');
title('Actual vs. Predicted GSR Values (Test Set)');
legend('show');
hold off;

% Plot actual vs predicted for validation set
figure;
plot(YValidation, 'b', 'DisplayName', 'Actual');
hold on;
plot(YPredValidation, 'r', 'DisplayName', 'Predicted');
xlabel('Time (samples)');
ylabel('Normalised GSR Value');
title('Actual vs. Predicted GSR Values (Validation Set)');
legend('show');
hold off;
