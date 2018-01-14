clear all; close all; clc;

%%set parameters
web = 1; %how many search engines
numPerURL = 1; %how many URLS per search engine
crawlCount = 5; %how many links are being crawled per URL

searchName = {'google';'gScholar';'Bing';'Yahoo'};

%TermName = {'GMO';'Genetically Modified Organism';'Transgenic'};
TermName = {'GMO'};

numVars = 13;
word = length(TermName);

%% organize all the data
for wordi = 1:word

    %load data
    load(strcat(TermName{wordi,1},'/',TermName{wordi,1},'.mat'));
    disp ("The value of obj array:"), disp (obj_arr);
    disp ("Actually a structure not an array:"), disp (obj_arr);

    %load(strcat('crawlData_',TermName{wordi,1},'.mat'));

    if numPerURL == 1
        crawlDat = squeeze(obj_arr); clear obj_arr
    else
        crawlDat = obj_arr; clear obj_arr
    end

    for urli = 1:numPerURL
    %denote what website the URLS are coming from - as set in python code
    if urli <= (numPerURL*1); webi = 1; %google
    elseif urli >= (numPerURL*1) && urli <= (numPerURL*2); webi = 2; %gScholar
    elseif urli >= (numPerURL*2) && urli <= (numPerURL*3); webi = 3; %bing
    elseif urli >= (numPerURL*3) && urli <= (numPerURL*4); webi = 4; %yahoo
    end

    for n = 1:length(crawlDat)
        cd{n,1} = double(crawlDat{n,1}(1,1));
        cd{n,2} = double(crawlDat{n,1}(1,2));
        cd{n,3} = crawlDat{n,2};
    end; clear n crawlDat

    cd = sortrows(cd,[2,1]);

    for n = 1:numVars
        crawlDat{n,1} = cd{n,3};
    end

    for c = 2:crawlCount+1
        temp_cd = find(cell2mat(cd(:,2)) == c);

        for v = 1:numVars
            crawlDat{v,c} = cd{temp_cd(v,1),3};
        end; clear temp_cd
    end
    end

    DataFinal{webi+1,wordi+1}{urli,1} = crawlDat; clear crawlDat
    DataFinal{webi,1} = searchName{webi,1};
    DataFinal{1,wordi} = searchTerm{wwordi,1};

end

%%

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %beginning of analysis
    for webi = 1:web
        for urli = 1:numPerURL

            %overview
            for n = 1:8
                DataFinal{3,webi}{n,1} = DataFinal{2,webi}{1,urli+1}{n,1};
                DataFinal{3,webi}{n,urli+1} = DataFinal{2,webi}{1,urli+1}{n,2};
            end; clear n
            DataFinal{3,4} = 'overview';

            %readability - read-able
            for n = 1:13
                DataFinal{4,webi}{n,1} = DataFinal{2,webi}{4,urli+1}{n,1};
                DataFinal{4,webi}{n,urli+1} = DataFinal{2,webi}{4,urli+1}{n,2};
            end; clear n
            DataFinal{4,4} = 'readable: read-able';

            %readability - pato
            for n = 1:13
                DataFinal{5,webi}{n,1} = DataFinal{2,webi}{4,urli+1}{n,1};
                DataFinal{5,webi}{n,urli+1} = DataFinal{2,webi}{4,urli+1}{n,3};
            end; clear n
            DataFinal{5,4} = 'readable: pato';
        end
    end; clear webi urli

    %mean and sd. prepare plot array
    DataFinal{7,1}{1,1} = 'means';
    var = [1,2,3,4,5,6,8]';

    for webi = 1:web
        %overview
        for n = 1:7
            for u = 2:numPerURL+1
                if isempty(DataFinal{3,webi}{var(n,1),u}) == 0;
                    temp(n,u-1) = DataFinal{3,webi}{var(n,1),u};
                else
                    temp(n,u-1) = NaN;
                end
            end; clear u

            DataFinal{8,webi}{n,1} = DataFinal{3,webi}{var(n,1),1};
            DataFinal{8,webi}{n,2} = nanmean(temp(n,:));
            DataFinal{8,webi}{n,3} = nanstd(temp(n,:));
        end; clear n

        DataFinal{8,4} = 'overview';

        plotData{webi,1} = temp; clear temp

        %readability: read-able
        for n = 1:13
            for u = 2:numPerURL+1
                if isempty(DataFinal{4,webi}{n,u}) == 0;
                    temp(n,u-1) = DataFinal{4,webi}{n,u};
                else
                    temp(n,u-1) = NaN;
                end
            end; clear u

            DataFinal{9,webi}{n,1} = DataFinal{4,webi}{n,1};
            DataFinal{9,webi}{n,2} = nanmean(temp(n,:));
            DataFinal{9,webi}{n,3} = nanstd(temp(n,:));
        end; clear n

        DataFinal{9,4} = 'readable: read-able';

        plotData{webi,2} = temp; clear temp

        %readability: pato
        for n = 1:13
            for u = 2:numPerURL+1
                if isempty(DataFinal{5,webi}{n,u}) == 0;
                    temp(n,u-1) = DataFinal{5,webi}{n,u};
                else
                    temp(n,u-1) = NaN;
                end
            end; clear u

            DataFinal{10,webi}{n,1} = DataFinal{5,webi}{n,1};
            DataFinal{10,webi}{n,2} = nanmean(temp(n,:));
            DataFinal{10,webi}{n,3} = nanstd(temp(n,:));
        end; clear n

        DataFinal{10,4} = 'readable: pato';

        plotData{webi,3} = temp; clear temp

    end; clear n webi var

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %calculate sentiment ratio
    for webi = 1:web
        for n = 1:numPerURL
            temp(1,n) = plotData{webi,1}(4,n)/plotData{webi,1}(6,n); %pos/neg
        end

        plotData{webi,1}(8,:) = temp; clear temp
    end; clear webi n

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %normalize readability metrics

    %set what age level values we're interested in
    metricAvg(1,1) = 8; %grade level
    metricAvg(2,1) = 65; %FK reading ease
    metricAvg(3,1) = 8; %FK grade level
    metricAvg(4,1) = 8; %Gunning Fog
    metricAvg(5,1) = 25.5; %SMOG
    metricAvg(6,1) = 8; %Coleman
    metricAvg(7,1) = 9; %Automated Readability Index

    for webi = 1:web
        for n = 1:7
            %find min and max values for each metric
            tempMin = min([plotData{webi,2}(n,:) metricAvg(n,1)]);
            tempMax = max([plotData{webi,2}(n,:) metricAvg(n,1)]);

            %normalize
            for i = 1:numPerURL
                NplotData{webi,2}(n,i) = (plotData{webi,2}(n,i) - tempMin)/(tempMax-tempMin);
                metricAvg(n,2) = (metricAvg(n,1) - tempMin)/(tempMax-tempMin);
            end; clear tempMin tempMax
        end
    end; clear webi n i

    %save data for each keyword for later plot comparison
    dataFinal{wordi,1} = DataFinal; clear DataFinal
    MetricAvg{wordi,1} = metricAvg; clear metricAvg
    PlotData{wordi,1} = plotData; clear plotData
    normPlotData{wordi,1} = NplotData; clear NplotData

    %end
%clear wordi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        %%%%% PLOT PLOT PLOT PLOT %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% plotting parameters
colors = {'b';'r';'g'};
markers = {'o';'^';'s'};
webLoc = [.35 .55 .75
          .40 .60 .80
          .45 .65 .85]';

%% plot info- frex
var = [8,9,10,11,12,13]';
Labels = {'FK Reading Ease', 'FK grade level', 'Gunning Fog'...
    'SMOG Index','Coleman Liau','Automated Readability Index','num sents'...
    'num words','num cWords','%complex words','avg words per sent','avg syl per word'};

figure(); set(gcf,'Color','w');

%set variable to plot
for z = 1:length(var)
    subplot(2,3,z)
    n = var(z,1);

    for wordi = 1:word
        %set data to plot
        plotData = PlotData{wordi,1};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),plotData{webi,2}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),'ko','MarkerSize',6,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),(nanstd(plotData{webi,2}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %graph parameters- variable dependent
        if n == 12
            plot([.4,1],[14,14],'--k'); plot([.4,1],[17,17],'--k');
        end

        if n == 13
            plot([.4,1],[1.6,1.6],'--k');
        end
    end

    %graph parameters- all graphs
    title(Labels{1,n-1}); xlim([.2 webLoc(3,word)+.15]);
    set(gca,'xcolor','w','XTick',[],'box','off');

    if n == 13
        set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
        legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','southoutside','Orientation','horizontal');
    end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');

end; clear n Labels z var plotData wordi h

%% plot info- sentiment
var = [4,6,5]';
Labels = {'num words','num sents','num cWords','pos Senti','neut Senti'...
    'neg Senti','frex Term','sent ratio'};

figure(); set(gcf,'Color','w');

%set variable to plot
for z = 1:length(var)
    subplot(1,3,z)
    n = var(z,1);

    for wordi = 1:word
        %set data to plot
        plotData = PlotData{wordi,1};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),plotData{webi,1}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(plotData{webi,1}(n,:)),'ko','MarkerSize',6,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(plotData{webi,1}(n,:)),(nanstd(plotData{webi,1}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %graph parameters- variable dependent
        if n == 4
            ylim([0 1]);
            set(gca,'xcolor','w','XTick',[]); hold on;
        end

        if n == 5 || n == 6
            ylim([0 1]);
            set(gca,'xcolor','w','ycolor','w','XTick',[]); hold on;
        end
    end

    %graph parameters- all graphs
    title(Labels{1,n}); xlim([.2 webLoc(3,word)+.15]);
    set(gca,'xcolor','w','XTick',[],'box','off');

    if n == 5
        set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
        legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','southoutside','Orientation','horizontal');
    end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');

end; clear n Labels z var plotData wordi h

%% plot text complexity variables
Labels = {'FK Reading Ease', 'FK grade level', 'Gunning Fog'...
    'SMOG Index','Coleman Liau','Automated Readability Index','num sents'...
    'num words','num cWords','%complex words','avg words per sent','avg syl per word'};

figure(); set(gcf,'Color','w');

for n = 2:7 %set this to 13 to double up on the counts (same as fig above)
    subplot(1,6,n-1)

    for wordi = 1:word
        %set data to plot
        plotData = PlotData{wordi,1};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),plotData{webi,2}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),'ko','MarkerSize',6,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),(nanstd(plotData{webi,2}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %thresholds for each variable- set to grade 8
        if n == 2;
            plot([.4,1],[60,60],'--k'); plot([.4,1],[70,70],'--k');
        end

        if n == 3 || n == 4 || n == 6;
            plot([.4,1],[8,8],'--k');
        end

        if n == 5;
            plot([.4,1],[21,21],'--k'); plot([.4,1],[30,30],'--k');
        end

        if n == 7;
            plot([.4,1],[9,9],'--k');
        end

        %graph parameters- variable dependent
        if n == 2
            ylim([0,100]);
            set(gca, 'XTick', [],'xcolor', 'w','box','off');

        elseif n == 3
            ylim([0,30]);
            set(gca, 'XTick', [],'xcolor', 'w','box','off');

        elseif n > 3
            ylim([0,30]);
            set(gca,'xcolor','w','ycolor','w','XTick',[],'box','off'); hold on;
        end
    end

    %graph parameters- all graphs
    title(Labels{1,n-1}); xlim([.2 webLoc(3,word)+.15]);

    if n == 7
        set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
        legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','southoutside','Orientation','horizontal');
    end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');

end; clear n Labels plotData wordi h

%% plot text complexity variables- NORMALIZED
Labels = {'FK Reading Ease', 'FK grade level', 'Gunning Fog'...
    'SMOG Index','Coleman Liau','Automated Readability Index','num sents'...
    'num words','num cWords','%complex words','avg words per sent','avg syl per word'};

figure(); set(gcf,'Color','w');

for n = 2:7 %set this to 13 to double up on the counts (same as fig above)
    subplot(1,6,n-1)

    for wordi = 1:word
        %set data to plot
        NplotData = normPlotData{wordi,1};
        metricAvg = MetricAvg{wordi,1};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),NplotData{webi,2}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(NplotData{webi,2}(n,:)),'ko','MarkerSize',6,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(NplotData{webi,2}(n,:)),(nanstd(NplotData{webi,2}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %plot range for predefined grade level
        plot([.4,1],[metricAvg(n,2),metricAvg(n,2)],'--k');

        %graph parameters- variable dependent
        if n == 2
            set(gca, 'XTick', [],'xcolor', 'w','box','off');
        else
            set(gca,'xcolor','w','ycolor','w','XTick',[],'box','off'); hold on;
        end
    end

    %graph parameters- all graphs
    title(Labels{1,n-1}); xlim([.2 webLoc(3,word)+.15]); ylim([-.1 1.1]);
    ylabel('normalized score');

    if n == 7
        set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
        legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','southoutside','Orientation','horizontal');
    end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica'); hold off;

end; clear n Labels NplotData metricAvg wordi h

%% readability mean plots
Labels = {'FK Reading Ease', 'FK grade level', 'Gunning Fog'...
    'SMOG Index','Coleman Liau','Automated Readability Index','num sents'...
    'num words','num cWords','%complex words','avg words per sent','avg syl per word'};

barLoc = [2 7 12
          3 8 13
          4 9 14]';

figure(); set(gcf,'Color','w');

for n = 2:7 %set this to 13 to double up on the counts (same as fig above)
    subplot(1,6,n-1)

    for wordi = 1:word
        %set data to plot
        plotData = PlotData{wordi,1};

        for webi = 1:web
            h(:,webi) = bar(barLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),'FaceColor',colors{webi,1},'EdgeColor','k'); hold on
            errorbar(barLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),(nanstd(plotData{webi,2}(n,:))/sqrt(Tot_url)),'k'); hold on
        end

        %thresholds for each variable- set to grade 8
        if n == 2;
            plot([0 16],[60,60],'--k'); plot([0 16],[70,70],'--k');
        end

        if n == 3 || n == 4 || n == 6;
            plot([0 16],[8,8],'--k');
        end

        if n == 5;
            plot([0 16],[21,21],'--k'); plot([0 16],[30,30],'--k');
        end

        if n == 7;
            plot([0 16],[9,9],'--k');
        end
        %graph parameters- variable dependent
        if n == 2
            ylim([0,100]);
            set(gca, 'XTick', [],'xcolor', 'w','box','off');

        elseif n == 3
            ylim([0,25]);
            set(gca, 'XTick', [],'xcolor', 'w','box','off');

        elseif n > 3
            ylim([0,25]);
            set(gca,'YTick', [],'xcolor', 'w','ycolor', 'w','box','off'); hold on
        end
    end

    %graph parameters- all graphs
    title(Labels{1,n-1}); xlim([0 barLoc(3,word)+2]);

        if n == 7
            legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','northeast');
        end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');
end; clear n Labels plotData wordi h
