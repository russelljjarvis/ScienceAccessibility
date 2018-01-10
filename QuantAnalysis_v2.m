clear all; close all; clc;

%%set parameters
web = 4; %how many search engines
numPerURL = 50; %how many URLS per search engine
Tot_url = numPerURL*web; %how many URLS for all search engines

TermName = {'GMO';'genetically modified organism'}; %CASE SENSITIVE
%TermName = {'GMO'};

word = length(TermName);

%% organize all the data
for wordi = 1:word

    %load data
    load(strcat('textData_',TermName{wordi,1},'.mat'));

    %organize data
    for urli = 1:Tot_url

        %%denote what website the URLS are coming from
        if urli <= (numPerURL*1); webi = 1; %google
        elseif urli >= (numPerURL*1) && urli <= (numPerURL*2); webi = 2; %google scholar
        elseif urli >= (numPerURL*2) && urli <= (numPerURL*3); webi = 3; %bing
        elseif urli >= (numPerURL*3) && urli <= (numPerURL*4); webi = 4; %yahoo
        end

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %pull data out of large array to begin organization (python to mat)
        %Summary Data
        SumDat = obj_arr{urli,1};
        for n = 1:length(SumDat)
            sumDat{n,1} = double(SumDat{n,1}(1,1)); sumDat{n,2} = double(SumDat{n,1}(1,2)); sumDat{n,3} = SumDat{n,2};
        end; clear n SumDat

        sumDat = sortrows(sumDat,[2,1]);

        for n = 1:length(sumDat)
            temp_sum(n,1) = sumDat{n,2};
        end; clear n

        cut_sum = min(find(temp_sum(:,1)==2)); clear temp_sum
        x = 1;
        for n = cut_sum:length(sumDat)

            SummaryDat{x,1} = sumDat{x,3}; SummaryDat{x,2} = sumDat{n,3};

            x = x + 1;
        end; clear sumDat x cut_sum n

        %words per sentence
        WperS = double(obj_arr{urli,2});
        WperS = sortrows(WperS,1);

        %syllables per word in each sentence
        sentSyl = double(cell2mat(obj_arr{urli,3}(:,1)));
        sentSyl(:,3) = cell2mat(obj_arr{urli,3}(:,2));
        sentSyl = sortrows(sentSyl,[1,2]);

        %frex of top words
        FrexTop = obj_arr{urli,4};
        for n = 1:length(FrexTop)
            frexTop{n,1} = double(FrexTop{n,1}(1,1)); frexTop{n,2} = double(FrexTop{n,1}(1,2)); frexTop{n,3} = FrexTop{n,2};
        end; clear n FrexTop

        frexTop = sortrows(frexTop,[2,1]);

        for n = 1:length(frexTop)
            temp_ftop(n,1) = frexTop{n,2};
        end; clear n

        cut_ftop = min(find(temp_ftop(:,1)==2)); clear temp_ftop
        x = 1;
        for n = cut_ftop:length(frexTop)

            freqTop{x,1} = frexTop{x,3}; freqTop{x,2} = frexTop{n,3};

            x = x + 1;
        end; clear frexTop x cut_ftop n

        %parts of speech
        PS = obj_arr{urli,5};
        for n = 1:length(PS)
            ps{n,1} = double(PS{n,1}(1,1)); ps{n,2} = double(PS{n,1}(1,2)); ps{n,3} = PS{n,2};
        end; clear n PS

        ps = sortrows(ps,[2,1]);

        for n = 1:length(ps)
            temp_ps(n,1) = ps{n,2};
        end; clear n

        cut_ps = min(find(temp_ps(:,1)==2)); clear temp_ps
        x = 1;
        for n = cut_ps:length(ps)

            PofS{x,1} = ps{x,3}; PofS{x,2} = ps{n,3};

            x = x + 1;
        end; clear ps x cut_ps n

        %freq of all words
        fM = obj_arr{urli,6};
        for n = 1:length(fM)
            fm{n,1} = double(fM{n,1}(1,1)); fm{n,2} = double(fM{n,1}(1,2)); fm{n,3} = fM{n,2};
        end; clear n fM

        fm = sortrows(fm,[2,1]);

        for n = 1:length(fm)
            temp_fm(n,1) = fm{n,2};
        end; clear n

        cut_fm = min(find(temp_fm(:,1)==2)); clear temp_fm
        x = 1;
        for n = cut_fm:length(fm)

            frexAll{x,1} = fm{x,3}; frexAll{x,2} = fm{n,3};

            x = x + 1;
        end; clear fm x cut_fm n

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %sentence data
        for senti = 1:size(WperS,1)
            check = find(sentSyl(:,1) == (senti-1));

            WperS(senti,4) = nanmean(sentSyl(check,3)); %mean num syllables per word per senttence

            cws = find(sentSyl(check,3) >= 3); %check for words with syllable count > 3
            WperS(senti,3) = length(cws); %num complex words per sentence
        end; clear senti check cws

        %determine number of complex words
        SummaryDat{16,1} = 'Total Complex Words'; SummaryDat{16,2} = sum(WperS(:,3));
        SummaryDat{17,1} = 'Mean Complex Words per Sentence'; SummaryDat{17,2} = nanmean(WperS(:,3));
        SummaryDat{18,1} = 'Mean Words per Sentence'; SummaryDat{18,2} = nanmean(WperS(:,2));
        SummaryDat{19,1} = 'Mean Syllables per Word per Sentence'; SummaryDat{19,2} = nanmean(WperS(:,4));

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        for n = 2:length(PofS)
            WordInfo{1,1} = 'sent Val'; WordInfo{n,1} = sentSyl(n-1,1);
            WordInfo{1,2} = 'word Val'; WordInfo{n,2} = sentSyl(n-1,2);
            WordInfo{1,3} = 'word'; WordInfo{n,3} = PofS(n-1,1);
            WordInfo{1,4} = 'Part of Speech'; WordInfo{n,4} = PofS(n-1,2);
            WordInfo{1,5} = 'Num Syllable'; WordInfo{n,5} = sentSyl(n-1,3);
        end; clear PofS sentSyl numChar n

        for senti = 1:size(WperS,1)
            sentInfo{1,1} = 'Sent Num'; sentInfo{1,senti+1} = WperS(senti,1);
            sentInfo{2,1} = 'Num Words'; sentInfo{2,senti+1} = WperS(senti,2);
            sentInfo{3,1} = 'Num Complex Words'; sentInfo{3,senti+1} = WperS(senti,3);
            sentInfo{4,1} = 'Mean Syls per Word'; sentInfo{4,senti+1} = WperS(senti,4);
        end; clear senti WperS

        GenInfo{1,1} = 'Num words'; GenInfo{1,2} = SummaryDat{1,2};
        GenInfo{2,1} = 'Num complex Words'; GenInfo{2,2} = SummaryDat{16,2};
        GenInfo{3,1} = 'Num Sents'; GenInfo{3,2} = SummaryDat{2,2};
        GenInfo{4,1} = 'Words per Sentence'; GenInfo{4,2} = SummaryDat{18,2};
        GenInfo{5,1} = 'Complex Words per Sentence'; GenInfo{5,2} = SummaryDat{17,2};
        GenInfo{6,1} = 'Syllables per Word per Sentence'; GenInfo{6,2} = SummaryDat{19,2};

        GenInfo{7,1} = 'frex Term'; GenInfo{7,2} = SummaryDat{3,2};
        GenInfo{8,1} = 'Grade Level'; GenInfo{8,2} = SummaryDat{6,2};
        GenInfo{9,1} = 'Flesch Reading Ease'; GenInfo{9,2} = SummaryDat{7,2};
        GenInfo{10,1} = 'SMOG Index'; GenInfo{10,2} = SummaryDat{8,2};
        GenInfo{11,1} = 'Coleman Liau'; GenInfo{11,2} = SummaryDat{9,2};
        GenInfo{12,1} = 'Automated Readability Index'; GenInfo{12,2} = SummaryDat{10,2};
        GenInfo{13,1} = 'Gunning Fog'; GenInfo{13,2} = SummaryDat{11,2};
        GenInfo{14,1} = 'Dale Chall Score'; GenInfo{14,2} = SummaryDat{12,2}; clear SummaryDat

        %create a single data output file for each url for long-term storage
        DataFinal{2,webi}{1,urli+1} = GenInfo; clear GenInfo; DataFinal{2,webi}{1,1} = 'Overview';
        DataFinal{2,webi}{2,urli+1} = WordInfo; clear WordInfo; DataFinal{2,webi}{2,1} = 'Word Info';
        DataFinal{2,webi}{3,urli+1} = sentInfo; clear sentInfo; DataFinal{2,webi}{3,1} = 'Sentence Info';
        DataFinal{2,webi}{4,urli+1} = frexAll; clear frexAll; DataFinal{2,webi}{4,1} = 'Frex All Words ';
        DataFinal{2,webi}{5,urli+1} = freqTop; clear freqTop; DataFinal{2,webi}{5,1} = 'Frex Top Words';

    end

    %clean up
    DataFinal{1,1} = 'Google';DataFinal{1,2} = 'gScholar'; DataFinal{1,3} = 'Bing'; DataFinal{1,4} = 'Yahoo';

    for webi = 1:web
        DataFinal{2,webi} = reshape(DataFinal{2,webi}(~cellfun('isempty',DataFinal{2,webi})),size(DataFinal{2,webi},1),numPerURL+1);
    end; clear obj_arr urli webi
    DataFinal{2,5} = 'All Data';

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %organize overview data into a single cell array
    for webi = 1:web
        for urli = 1:numPerURL

            %overview
            for n = 1:size(DataFinal{2,1}{1,2},1)
                if urli == 1
                    DataFinal{3,webi}{n,1} = DataFinal{2,webi}{1,urli+1}{n,1};
                    DataFinal{3,webi}{n,urli+1} = DataFinal{2,webi}{1,urli+1}{n,2};
                else
                    DataFinal{3,webi}{n,urli+1} = DataFinal{2,webi}{1,urli+1}{n,2};
                end
            end; clear n
        end
    end; clear webi urli
    DataFinal{3,5} = 'Overview';

    %%mean and sd. prepare plot array
    for webi = 1:web
        %overview
        for n = 1:size(DataFinal{2,1}{1,2},1)
            for u = 2:numPerURL+1
                if isempty(DataFinal{3,webi}{n,u}) == 0;
                    temp(n,u-1) = double(DataFinal{3,webi}{n,u});
                else
                    temp(n,u-1) = NaN;
                end
            end; clear u

            DataFinal{4,webi}{n,1} = DataFinal{3,webi}{n,1};
            DataFinal{4,webi}{n,2} = nanmean(temp(n,:));
            DataFinal{4,webi}{n,3} = nanstd(temp(n,:));
        end; clear n

        DataFinal{5,webi} = temp; clear temp
    end; clear n webi var
    DataFinal{4,5} = 'Mean & SD';
    DataFinal{5,5} = 'Data to Plot';

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%normalize readability metrics

    %set what age level values we're interested in
    metricAvg(1,1) = 8; %grade level
    metricAvg(2,1) = 65; %FK reading ease
    metricAvg(3,1) = 25.5; %SMOG
    metricAvg(4,1) = 8; %Coleman
    metricAvg(5,1) = 9; %Automated Readability Index
    metricAvg(6,1) = 8; %Gunning Fog

    for webi = 1:web

        TempWeb = DataFinal{5,webi}(8:13,:);
        for n = 1:size(metricAvg)
            %find min and max values for each metric
            tempMin = min([TempWeb(n,:) metricAvg(n,1)]);
            tempMax = max([TempWeb(n,:) metricAvg(n,1)]);

            %normalize
            for u = 1:numPerURL
                DataFinal{6,webi}(n,u) = (TempWeb(n,u) - tempMin)/(tempMax-tempMin);
                metricAvg(n,2) = (metricAvg(n,1) - tempMin)/(tempMax-tempMin);
            end; clear tempMin tempMax
        end
    end; clear webi n i TempWeb u
    DataFinal{6,5} = 'Normalized Readability Values';

    %save data for each keyword for later plot comparison
    dataFinal{wordi,2} = DataFinal; clear DataFinal; dataFinal{wordi,1} = TermName{wordi,1};
    MetricAvg{wordi,2} = metricAvg; clear metricAvg; MetricAvg{wordi,1} = TermName{wordi,1};

end;

%clear wordi urli Tot_url

error('warning - plotting ahead');
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% PLOT PLOT PLOT PLOT %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% plotting parameters
colors = {'b';'r';'g';'m'};
markers = {'o';'^';'s';'o'};
webLoc = [.35 .55 .75 .95
          .40 .60 .80 1
          .45 .65 .85 1.05]';

Labels = {'# words','# cWords','# Sentences','words per sent','cWords per Sent'...
         'Syllables per Word','frexTerm','Grade Level','FK Reading Ease', 'SMOG','Coleman Liau',...
         'Automated Readability Index', 'Gunning Fog','Dale Chall'};

%% plot info- frex
var = [1,2,3,4,5,6]';

figure(); set(gcf,'Color','w');

%set variable to plot
for z = 1:length(var)
    subplot(2,3,z)
    n = var(z,1);

    for wordi = 1:word
        %set data to plot
        plotData = dataFinal{wordi,2};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),plotData{5,webi}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(plotData{5,webi}(n,:)),'ko','MarkerSize',5,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),(nanstd(plotData{webi,2}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %graph parameters- variable dependent
%         if n == 12
%             plot([.4,1],[14,14],'--k'); plot([.4,1],[17,17],'--k');
%         end
%
%         if n == 13
%             plot([.4,1],[1.6,1.6],'--k');
%         end
    end

    %graph parameters- all graphs
    title(Labels{1,n}); xlim([.2 webLoc(4,word)+.15]);
    set(gca,'xcolor','w','XTick',[],'box','off');

%     if n == 13
%         set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
%         legend(h(1,:), {'google';'gScholar';'bing';'yahoo'},'box','off','Location','southoutside','Orientation','horizontal');
%     end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');

end; clear n z var plotData wordi h

%% plot text complexity variables
var = [8,9,10,11,12,13,14]';

figure(); set(gcf,'Color','w');

for z = 1:length(var) %set this to 13 to double up on the counts (same as fig above)
    subplot(2,4,z)
    n = var(z,1);

    for wordi = 1:word
        %set data to plot
        plotData = dataFinal{wordi,2};

        for webi = 1:web
            h(:,webi) = plot(webLoc(webi,wordi),plotData{5,webi}(n,:),'color',colors{webi,1},'marker',markers{wordi,1},'MarkerSize',5); hold on
            plot(webLoc(webi,wordi),nanmean(plotData{5,webi}(n,:)),'ko','MarkerSize',5,'MarkerFaceColor','k');
            %errorbar(webLoc(webi,wordi),nanmean(plotData{webi,2}(n,:)),(nanstd(plotData{webi,2}(n,:))/sqrt(Tot_url)),'k');
        end; clear webi

        %thresholds for each variable- set to grade 8
%         if n == 2;
%             plot([.4,1],[60,60],'--k'); plot([.4,1],[70,70],'--k');
%         end
%
%         if n == 3 || n == 4 || n == 6;
%             plot([.4,1],[8,8],'--k');
%         end
%
%         if n == 5;
%             plot([.4,1],[21,21],'--k'); plot([.4,1],[30,30],'--k');
%         end
%
%         if n == 7;
%             plot([.4,1],[9,9],'--k');
%         end
%
%         %graph parameters- variable dependent
%         if n == 2
%             ylim([0,100]);
%             set(gca, 'XTick', [],'xcolor', 'w','box','off');
%
%         elseif n == 3
%             ylim([0,30]);
%             set(gca, 'XTick', [],'xcolor', 'w','box','off');
%
%         elseif n > 3
%             ylim([0,30]);
%             set(gca,'xcolor','w','ycolor','w','XTick',[],'box','off'); hold on;
%         end
    end

    %graph parameters- all graphs
    title(Labels{1,n}); xlim([.2 webLoc(4,word)+.15]);

%     if n == 7
%         set(h(:,1), 'Color','b'); set(h(:,2), 'Color','r'); set(h(:,3), 'Color','g')
%         legend(h(1,:), {'google';'yahoo';'bing'},'box','off','Location','southoutside','Orientation','horizontal');
%     end

    set(findall(gcf,'-property','FontSize'),'FontSize',12,'FontName','Helvetica');

end; clear n plotData wordi h var

%% readability mean bar plots

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
end; clear n plotData wordi h
