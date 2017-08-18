clear all; close all; clc;

%%set parameters
web = 3; %how many search engines
numPerURL = 25; %how many URLS per search engine
Tot_url = numPerURL*web; %how many URLS for all search engines

TermName = {'GMO';'GenModOrg';'Transgenic'};
%TermName = {'GMO';'Transgenic'};

word = length(TermName);

%% organize all the data
for wordi = 1:word 
    
    %load data
    load(strcat('textAnalysis_',TermName{wordi,1},'.mat'));

    %organize data
    for urli = 1:Tot_url
        
        %%denote what website the URLS are coming from - as set in python code
        if urli <= (numPerURL*1); webi = 1; %google
        elseif urli >= (numPerURL*1) && urli <= (numPerURL*2); webi = 2; %yahoo
        elseif urli >= (numPerURL*2) && urli <= (numPerURL*3); webi = 3; %bing
        end
        
        %pull data out of large array to begin organization
        numWords = double(cell2mat(obj_arr(urli,1)));
        numSents = double(cell2mat(obj_arr(urli,2)));
        WperS = double(obj_arr{urli,3});
        WperS = sortrows(WperS,1);
        sentSyl = double(cell2mat(obj_arr{urli,4}));
        sentSyl = sortrows(sentSyl,[1,2]);
        frexTop = cell2mat(obj_arr(urli,5));
        fM = obj_arr{urli,6};
        frexTerm = cell2mat(obj_arr(urli,7));
        PS = obj_arr{urli,8};
        SA = obj_arr{urli,9};
        fAll = obj_arr{urli,10};
        Read = obj_arr{urli,11};
        numChar = double(cell2mat(obj_arr{urli,12}));
        numChar = sortrows(numChar,[1,2]);
        
        for n = 1:length(fM)
            fm{n,1} = double(fM{n,1}(1,1)); fm{n,2} = double(fM{n,1}(1,2)); fm{n,3} = fM{n,2};
        end; clear n fM
        
        for n = 1:length(PS)
            ps{n,1} = double(PS{n,1}(1,1)); ps{n,2} = double(PS{n,1}(1,2)); ps{n,3} = PS{n,2};
        end; clear n PS
        
        for n = 1:length(SA)
            sa{n,1} = double(SA{n,1}(1,1)); sa{n,2} = double(SA{n,1}(1,2)); sa{n,3} = SA{n,2};
        end; clear n SA
        
        for n = 1:length(fAll)
            Fall{n,1} = double(fAll{n,1}(1,1)); Fall{n,2} = double(fAll{n,1}(1,2)); Fall{n,3} = fAll{n,2};
        end; clear n fAll
        
        for n = 1:length(Read)
            read{n,1} = double(Read{n,1}(1,1)); read{n,2} = double(Read{n,1}(1,2)); read{n,3} = Read{n,2};
        end; clear n Read
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %sort data to get out of python data types and arrary conventions

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
        %%%%%%%%%%%%%%%%%%%%%%%%
        sa = sortrows(sa,[2,1]);
        
        for n = 1:length(sa)
            temp_sa(n,1) = sa{n,2};
        end; clear n
        
        cut_sa = min(find(temp_sa(:,1)==2)); clear temp_sa
        x = 1;
        for n = cut_sa:length(sa)
            
            SA{x,1} = sa{x,3}; SA{x,2} = sa{n,3};
            
            x = x + 1;
        end; clear sa x cut_sa n
        
        for n = 1:3
            if isnumeric(str2num(SA{n,2})) == 1
                SA{n,2} = str2num(SA{n,2});
            else
                SA{n,2} = NaN
            end
        end; clear n
        %%%%%%%%%%%%%%%%%%%%%%%
        fm = sortrows(fm,[2,1]);
        
        for n = 1:length(fm)
            temp_fm(n,1) = fm{n,2};
        end; clear n
        
        cut_fm = min(find(temp_fm(:,1)==2)); clear temp_fm
        x = 1;
        for n = cut_fm:length(fm)
            
            frexMost{x,1} = fm{x,3}; frexMost{x,2} = fm{n,3};
            
            x = x + 1;
        end; clear fm x cut_fm n
        %%%%%%%%%%%%%%%%%%%%%%%%%
        Fall = sortrows(Fall,[2,1]);
        
        for n = 1:length(Fall)
            temp_fall(n,1) = Fall{n,2};
        end; clear n
        
        cut_fall = min(find(temp_fall(:,1)==2)); clear temp_fall
        x = 1;
        for n = cut_fall:length(Fall)
            
            frexAll{x,1} = Fall{x,3}; frexAll{x,2} = Fall{n,3};
            
            x = x + 1;
        end; clear Fall x cut_fall n
        %%%%%%%%%%%%%%%%%%%%%%%%%%%
        read = sortrows(read,[2,1]);
        
        for n = 1:length(read)
            temp_rd(n,1) = read{n,2};
        end; clear n
        
        cut_rd = min(find(temp_rd(:,1)==2)); clear temp_rd
        x = 1;
        for n = cut_rd:length(read)
            
            Read{x,1} = read{x,3}; Read{x,2} = read{n,3};
            x = x + 1;
        end; clear read x cut_rd n
        
        Read{11,2}(regexp(Read{11,2},'%')) = [];
        
        for n = 1:13
            Read{n,2} = str2num(Read{n,2});
        end; clear n
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %sentence data
        for senti = 1:size(WperS,1)
            check = find(sentSyl(:,1) == (senti-1));
            WperS(senti,3) = nanmean(sentSyl(check,3)); %num syllables per word per senttence
            WperS(senti,5) = nanmean(numChar(check,3)); %num char per word per sentence
            
            cws = sentSyl(check,3) >= 3; %check for words with syllable count > 3
            WperS(senti,4) = sum(cws); %num complex words per sentence
        end; clear senti check cws
        
        %determine number of complex words
        CWs = sum(WperS(:,4));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %Flesch Kincaid Reading Ease
        %    206.835 - 1.015 x (words/sentences) - 84.6 x (syllables/words)
        Read{2,3} = 206.835 - 1.015 * nanmean(WperS(:,2)) - 84.6 * nanmean(WperS(:,3));
        
        %Flesch Kincaid Grade Level
        %    0.39 x (words/sentences) + 11.8 x (syllables/words) - 15.59
        Read{3,3} = .39 * ( nanmean(WperS(:,2)) ) + 11.8 * ( nanmean(WperS(:,3)) ) - 15.59;
        
        %Gunning Fog Score
        %   0.4 x ( (words/sentences) + 100 x (complexWords/words) )
        Read{4,3} = 0.4 * ( nanmean(WperS(:,2))  + 100 * ( CWs/numWords ) );
        
        %SMOG Index
        %   1.0430 x sqrt( 30 x complexWords/sentences ) + 3.1291
        Read{5,3} = 1.0430 * sqrt( 30 * (nanmean(WperS(:,4))) ) + 3.1291;
        
        %Coleman Liau Index
        %   5.89 x (characters/words) - 0.3 x (sentences/words) - 15.8
        Read{6,3} = 5.89 * ( nanmean(numChar(:,3)) ) - 0.3 * (numSents/numWords) - 15.8;
        
        %Automated Readability Index (ARI)
        %   4.71 x (characters/words) + 0.5 x (words/sentences) - 21.43
        Read{7,3} = 4.71 * ( nanmean(numChar(:,3)) ) + 0.5 * (nanmean(WperS(:,2))) - 21.43;
        
        Read{8,3} = numSents; Read{9,3} = numWords;
        Read{10,3} = CWs; Read{11,3} = (CWs/numWords)*100;
        Read{12,3} = nanmean(WperS(:,2)); Read{13,3} = nanmean(WperS(:,3));
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        for n = 2:length(PofS)
            WordInfo{1,1} = 'sent Val'; WordInfo{n,1} = sentSyl(n,1);
            WordInfo{1,2} = 'word Val'; WordInfo{n,2} = sentSyl(n,2);
            WordInfo{1,3} = 'word'; WordInfo{n,3} = PofS(n,1);
            WordInfo{1,4} = 'Part of Speech'; WordInfo{n,4} = PofS(n,2);
            WordInfo{1,5} = 'Num Syllable'; WordInfo{n,5} = sentSyl(n,3);
            WordInfo{1,6} = 'Num Characters'; WordInfo{n,6} = numChar(n,3);
        end; clear PofS sentSyl numChar n
        
        GenInfo{1,1} = 'Num words'; GenInfo{1,2} = numWords; clear numWords
        GenInfo{2,1} = 'Num Sents'; GenInfo{2,2} = numSents; clear numSents
        GenInfo{3,1} = 'Num complex Words'; GenInfo{3,2} = CWs; clear CWs
        GenInfo{4,1} = 'Pos Sentiment'; GenInfo{4,2} = SA{3,2};
        GenInfo{5,1} = 'Neu Sentiment'; GenInfo{5,2} = SA{2,2};
        GenInfo{6,1} = 'Neg Sentiment'; GenInfo{6,2} = SA{1,2}; clear SA
        GenInfo{7,1} = 'Top Word'; GenInfo{7,2} = frexTop; clear frexTop
        GenInfo{8,1} = 'frex Term'; GenInfo{8,2} = frexTerm; clear frexTerm
        
        for senti = 1:size(WperS,1)
            sentInfo{1,1} = 'Sent Num'; sentInfo{1,senti+1} = WperS(senti,1);
            sentInfo{2,1} = 'Words per Sent'; sentInfo{2,senti+1} = WperS(senti,2);
            sentInfo{3,1} = 'cWords per Sent'; sentInfo{3,senti+1} = WperS(senti,4);
            sentInfo{4,1} = 'Syls per word'; sentInfo{4,senti+1} = WperS(senti,3);
            sentInfo{5,1} = 'Chars per word'; sentInfo{5,senti+1} = WperS(senti,5);
        end; clear senti WperS
        
        %create a single data output file for each url for long-term storage
        DataFinal{2,webi}{1,urli+1} = GenInfo; clear GenInfo; DataFinal{2,webi}{1,1} = 'Overview';
        DataFinal{2,webi}{2,urli+1} = sentInfo; clear sentInfo; DataFinal{2,webi}{2,1} = 'sent info';
        DataFinal{2,webi}{3,urli+1} = WordInfo; clear WordInfo; DataFinal{2,webi}{3,1} = 'word info';
        DataFinal{2,webi}{4,urli+1} = Read; clear Read; DataFinal{2,webi}{4,1} = 'readability';
        DataFinal{2,webi}{5,urli+1} = frexAll; clear frexAll; DataFinal{2,webi}{5,1} = 'frexAll ';
        DataFinal{2,webi}{6,urli+1} = frexMost; clear frexMost; DataFinal{2,webi}{6,1} = 'Frex10';
    end
    
    %clean up
    DataFinal{1,1} = 'google';DataFinal{1,2} = 'yahoo'; DataFinal{1,3} = 'bing'; DataFinal{2,4} = 'all data';
    
    for webi = 1:web
        DataFinal{2,webi} = reshape(DataFinal{2,webi}(~cellfun('isempty',DataFinal{2,webi})),size(DataFinal{2,webi},1),numPerURL+1);
    end; clear obj_arr urli webi
    
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
    
end; clear wordi

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
