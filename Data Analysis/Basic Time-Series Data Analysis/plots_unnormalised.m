clear;
close all;

% Read data from csv file
dataTable = readtable('sensor_data_all_headings.csv', 'Delimiter', ',');

% Extract timestamp and numerical data
timeStamps = datetime(dataTable{:, 1}, 'InputFormat', 'yyyy-MM-dd_HH-mm-ss');
numericalData = table2array(dataTable(:, 2:end));

fullDataTable = [table(timeStamps), array2table(numericalData, 'VariableNames', dataTable.Properties.VariableNames(2:end))];

% Convert timestamps to datetime format
timeStamps = datetime(fullDataTable{:, 1}, 'InputFormat', 'yyyy-MM-dd_HH-mm-ss');

labels = {'API Humidity (%)', 'API Temperature (deg C)', 'GSR', 'NO2 (ug/m3)', 'PM10 (ug/m3)', 'PM2.5 (ug/m3', 'Sensor Humidity (%)', 'SO2 (ug/m3)', 'Sensor Temperature (deg C)'};

% Loop through each variable and plot
for i = 2:size(fullDataTable, 2)
    figure;  % Create a new figure for each variable
    
    % Find time differences
    timeDifferences = diff(timeStamps);

    % Identify points where time diff is less than 1 hour
    validPoints = find(timeDifferences < hours(1));

    % Plot line segments for each valid points
    for j = 1:length(validPoints)
        startIndex = validPoints(j);
        endIndex = startIndex + 1;

        plot(timeStamps(startIndex:endIndex), fullDataTable{startIndex:endIndex, i}, 'Color', 'blue');
        hold on;
    end
    
    title(dataTable.Properties.VariableNames{i});
    xlabel('Time');
    ylabel(labels{i-1});
    grid on;

    % Set x-axis range + maximise window width
    xlim([datetime('2023-11-27 08:00:00'), datetime('2023-12-01 22:00:00')]);
    set(gcf, 'Position',  [0, 100, 2560, 500])

    hold off;
end
