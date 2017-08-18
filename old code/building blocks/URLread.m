clear all;
url = ['https://asunow.asu.edu/content/mining-extremism'...
       '-asu-tool-helps-predict-potential-threats'];
   
url = ['https://www.google.com/?gws_rd=ssl#q=GMO'];

html = urlread(url); clear url

txt = strtrim(html);
s = strfind(txt,'<p>');
f = strfind(txt,'</p>');

txt = txt(1,s(1,1):f(1,1));

% Use regular expressions to remove undesired markup.
txt = regexprep(txt,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

txt = strtrim(txt);
x = cellstr(txt);

x1 = regexprep(x, '&ldquo;', '"');
x1 = regexprep(x1, '&rdquo;', '"');
x1 = strrep(x1, '&rsquo;', ''''); %x1 = regexprep(x1, '&rsquo;', '''');
x1 = regexprep(x1, '&mdash;', '-');
x1 = regexprep(x1, '&amp;', '-');
x1 = regexprep(x1, '&tilde;', '~');
 
