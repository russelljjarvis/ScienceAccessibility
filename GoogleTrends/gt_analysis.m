clear all; close all; clc

filename = 'GMO_gt_data';
delimiter = ','; startRow = 3; formatSpec = '%s%f%f%f%[^\n\r]';

fileID = fopen(filename,'r');

textscan(fileID, '%[^\n\r]', startRow-1, 'WhiteSpace', '', 'ReturnOnError', false);
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'ReturnOnError', false);
fclose(fileID); clearvars filename delimiter startRow formatSpec fileID ans;

for n = 1:length(dataArray)-1
    if n == 1
        for x = 1:length(dataArray{1,1})
            temp = strsplit(dataArray{1,n}{x,1},'-');
            
            GMOdat(x,n+1) = str2double(temp{1,1});
            GMOdat(x,n) = str2double(temp{1,2}); clear temp
        end
    else
        GMOdat(:,n+1) = dataArray{1,n}(:,1);
    end
end; clear dataArray n x 
%%
%plot raw data
figure()
    plot(GMOdat(:,3),'k'); hold on;
    plot(GMOdat(:,4),'r'); hold on;
    plot(GMOdat(:,5),'b'); hold on;
    legend('GMO','Genetically Modified Organism','Transgenic'); hold on;
    legend('Location','northwest'); hold on; legend('boxoff');
    ylabel('search count');

%normalize to zero
citeCount(:,1) = GMOdat(:,4)./GMOdat(:,3);
citeCount(:,2) = GMOdat(:,5)./GMOdat(:,3);

figure()
   plot(citeCount(:,1),'r'); hold on;
   plot(citeCount(:,2),'b'); hold on;
   plot([0 160],[1,1],'--k'); hold on;
   ylim([-.2 1.2]);


    
