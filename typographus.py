#-*- coding: cp1251 -*-
'''
�������� ������ 0.1 ������� ������
�������� �������: 

��������� �� ������ PHP ������ http://rmcreative.ru/blog/post/tipograf
�������� ������ ������� �����������.
������� � ������ Lookahead � Lookbehind � Python regEx ��������� ������ ����
��������� ���� �������� ������. ��������� ��������� ������ �������.
��� ������� ����� � ������������ � PEP8.
���� testTypographus.py �������� ���� ����� �����������, ������� ��� ���������
� ������� ������ (��� ���� �� � ������� ��������).

�����: ����������� �����
�����: kigorw@gmail.com
����: http://www.kigorw.com/

�������� ������ ������ ��� ��� ������, ������� ���� ��������� ������
� ��������� �� �������� �������.

� ��� ����� ��� ���������� ������!
'''
import re


class Typographus:
    
       
    encoding = None
    
    sym = {
      'nbsp': u'&nbsp;',
      'lnowrap': u'<span style="white-space:nowrap">',
      'rnowrap': u'</span>',

      'lquote': u'�',
      'rquote': u'�',
      'lquote2': u'�',
      'rquote2': u'�',
      'mdash': u'�',
      'ndash': u'�',
      'minus': u'�', #�����. �� ������ ������� +, ���� �� ���� �������

      'hellip': u'�',
      'copy': u'�',
      'trade': u'<sup>�</sup>',
      'apos': u'&#39;',   # ��. http://fishbowl.pastiche.org/2003/07/01/the_curse_of_apos
      'reg': u'<sup><small>�</small></sup>',
      'multiply': u'&times;',
      '1/2': u'&frac12;',
      '1/4': u'&frac14;',
      '3/4': u'&frac34;',
      'plusmn': u'&plusmn;',
      'rarr': u'&rarr;',
      'larr': u'&larr;',
       'rsquo': u'&rsquo;'
   }
    
    safeBlocks = {
      u'<pre[^>]*>': u'<\/pre>',
      u'<style[^>]*>': u'<\/style>',
      u'<script[^>]*>': u'<\/script>',
      u'<!--': u'-->',
       u'<code[^>]*>': u'<\/code>',
   }
   
   
    def __init__(self, encoding = None):
        self.encoding = encoding
   
   
    def addSafeBlock(self, openTag, closeTag):
        self.safeBlocks[openTag] = closeTag
   
   
    def setSym(self, sym, entity):
        self.sym[sym] = entity
   
   
    def setOpt(self, key, value):
        self.options[key] = value
   
   
    def convertE(opt = False):
        self.setOpt[self.CONVERT_E] = opt
   

    def getSafeBlockPattern(self):
        pattern = u'(';
        for key, value in self.safeBlocks.items():
            pattern += u"%s.*%s|" % (key, value)
      
        pattern+= u'<[^>]*[\s][^>]*>)';
        return pattern
    
    
    def removeRedundantBlocks(self, str):
        blocks = {}
        def replace(m):
            value = m.group()
            if(len(value)==3):
                return value
            
            key = u'<%s>' % (len(blocks))
            blocks[key] = value;
            return key;
        
        pattern = self.getSafeBlockPattern() 
       
        str = re.compile(pattern, re.U).sub(replace, str);
        
        str = re.compile(ur"</?.*?/?>", re.U).sub(replace, str);
        
        return {"replaced": str, "blocks": blocks}
    
    
    def return_blocks_to_string(self, str, blocks):
        for key, value in blocks.items():
            str = str.replace(key, value)
        
        return str
        
        

    def process(self, str):
        value = self.removeRedundantBlocks(str)
        
        str = value["replaced"]
        blocks = value["blocks"]
      
        str = self.typo_text(str)
            
        str = self.return_blocks_to_string(str, blocks)
        return str
      
               
    def apply_rules(self, rules, str):
        for rule in rules:
            pat = rule["pat"]
            rep = rule["rep"]
            mod = rule.get("mod", re.X)
            str = re.compile(pat, mod).sub(rep, str);
        return str
            
    
    def typo_text(self, str):
        sym = self.sym
        if (str.strip() == ''):
            return ''
        
        html_tag = u''
        hellip = u'\.{3,5}'
             
        #�����
        word = u'[a-zA-Z�-��-�_]'
        phrase_begin = ur"(?:%s|%s|\n)" %(hellip, word)
        
        #����� �����
        phrase_end = ur"(?:%s|%s|\n)" %(hellip, word)

        #����� ���������� (��������� � ����� - ��������� ������!)
        punctuation = u'[?!:,;]'
        
        #������������
        abbr = u'(?:���|���|���|��|��|���|���)';
        #�������� � �����
        prepos = u'�|�|��|���|�|���|�|�|�|�|�|��|��|���|��|���|��|��|��|��|��|��|���|��|��|��|��|���|����|����|�����|'        
        prepos +=u'���|���|����|���|���|����|���|��|���|��|���|���|��|���|��|���|�����|�����|������|�����|�����|������|���|���|�'
        metrics = u'��|��|�|��|�|��|�|��|��|��|dpi|px';
        
        shortages = u'�|��|���|���|c|��|�|���|�';

        money = u'���\.|����\.|����|�\.�\.';
        counts = u'���\.|���\.';
        
        any_quote = u'(?:%s|%s|%s|%s|&quot;|")' %(sym['lquote'], sym['rquote'], sym['lquote2'], sym['rquote2'])
        
        rules_strict = [
        # ����� �������� ��� ��������� -> ���� ������
        {"pat": u'\s+', "rep": u' '},
        # ������� ����� �� � ���. ���� ��� ���� � �� ������.
        {"pat": u'([^,])\s(�|��)\s', "rep": u'\g<1>, \g<2> '}
        ]
        

        rules_symbols = [
            #������ �����.
            #TODO: ������� �������
            {"pat": u'([^!])!!([^!])', "rep": u'\g<1>!\g<2>'},        
            {"pat": u'([^?])\?\?([^?])', "rep": u'\g<1>?\g<2>'},
            {"pat": u'(\w);;(\s)', "rep": u'\g<1>;\g<2>'},
            {"pat": u'(\w)\.\.(\s)', "rep": u'\g<1>.\g<2>'},
            {"pat": u'(\w),,(\s)', "rep": u'\g<1>,\g<2>'},
            {"pat": u'(\w)::(\s)', "rep": u'\g<1>:\g<2>'},
                    
            {"pat": u'(!!!)!+', "rep": u'\g<1>'},
            {"pat": u'(\?\?\?)\?+', "rep": u'\g<1>'},
            {"pat": u'(;;;);+', "rep": u'\g<1>'},
            {"pat": u'(\.\.\.)\.+', "rep": u'\g<1>'},
            {"pat": u'(,,,),+', "rep": u'\g<1>'},
            {"pat": u'(:::):+\s', "rep": u'\g<1>'},
        
            #�������� ����������
            {"pat": u'!\?', "rep": u'?!'},
            #����� (c), (r), (tm)
            {"pat": u'\((c|�)\)', "rep": sym['copy'], "mod": re.I},
            {"pat": u'\(r\)', "rep": sym['reg'], "mod": re.I},
            {"pat": u'\(tm\)', "rep": sym['trade'], "mod": re.I},
        
            #�� 2 �� 5 ����� ����� ������ - �� ���� ���������� (������ - �� ��������� ��������).
            {"pat": hellip, "rep": sym['hellip']},

            #����������� ��� 1/2 1/4 3/4
            {"pat": u'\b1/2\b', "rep": sym['1/2']},
            {"pat": u'\b1/4\b', "rep": sym['1/4']},
            {"pat": u'\b3/4\b', "rep": sym['3/4']},

            #L�'����
            {"pat": u"([a-zA-Z])'([�-��-�])", "rep": u'\g<1>%s\g<2>' % sym['rsquo'], "mod": re.I},
        
            {"pat": u"'", "rep": sym['apos']}, #str_replace?
      
            # ������� 10x10, ���������� ���� + ������� ������ �������
            {"pat": u'(\d+)\s{0,}?[x|X|�|�|*]\s{0,}(\d+)', "rep": u'\g<1>%s\g<2>' % sym['multiply']},
        
            #+-
            {"pat": u'([^\+]|^)\+-', "rep": u'\g<1>%s' % sym['plusmn']},
        
           #�������
           {"pat": u'([^-]|^)->', "rep": u'\g<1>%s' % sym['rarr']},
           {"pat": u'<-([^-]|$)', "rep": u'%s\g<1>' % sym['larr']}
        ]


        rules_quotes = [
            # �������� ������������ �������
           {"pat": u'([^"]\w+)"(\w+)"', "rep": u'\g<1> "\g<2>"'},
           {"pat": u'"(\w+)"(\w+)', "rep": u'"\g<1>" \g<2>'},
           #���������� ������� � ������. ������� ������� ���������.
           #((?:�|�|�|�|&quot;|"))((?:\.{3,5}|[a-zA-Z�-��-�_]|\n))
           {"pat": u"(%s)(%s)" % (any_quote, phrase_begin), "rep": u'%s\g<2>' % sym['lquote']},
           
           #((?:(?:\.{3,5}|[a-zA-Z�-��-�_])|[0-9]+))((?:�|�|�|�|&quot;|"))
           {"pat": "((?:%s|(?:[0-9]+)))(%s)" % (phrase_end, any_quote), "rep": u'\g<1>%s' % sym['rquote']},
           
           {"pat": sym['rquote'] + any_quote, "rep": sym['rquote']+sym['rquote']},
           {"pat": any_quote + sym['lquote'], "rep": sym['lquote']+sym['lquote']}
        ]
        
        rules_braces = [
         #�������� ������ �� �����
         {"pat": u'(%s)\(' % word, "rep": u'\g<1> ('},
          #�������� ������ �� �������
         {"pat": u'\(\s', "rep": u'(', "mod": re.S},
         {"pat": u'\s\)', "rep": u')', "mod": re.S},
         ]

        rules_main = [
         #�������� ���� �� �����
         {"pat": u'(\w)- ', "rep": u'\g<1> - '},

         #����� � �������������� �������� ��������! ���� �� �������� @todo ������������ ���������
       #  {"pat": u'(%s)+(%s|%s)' % (phrase_end, punctuation, sym['hellip']), "rep": u'\g<1>\g<2>'},
       #  {"pat": u'(%s)(%s)' % (punctuation, phrase_begin), "rep": u'\g<1> \g<2>'},
      
          #��� ����� ��������
          {"pat": u'(\w)\s(?:\.)(\s|$)', "rep": u'\g<1>.\g<2>'},

          #����������� �������� ����������� � ����������� ���� �������������
          #  ������ �� ���� &nbsp;?
          # ! �������� ����������� ���� ����� ��������� ������ !
          {"pat": u'(%s)\s+"(.*)"' % abbr, "rep": u'%s\g<1> "\g<2>"%s' % (sym['rnowrap'], sym['lnowrap'])},

          #������ �������� ���������� �� ������������ � ���� �����.
          #��������: ���. ������, �. �������
          #������ ������, ���� ��� ���. � ����� ���� ������ �� ������ ������. :)
          {"pat": u'(^|[^a-zA-Z�-��-�])(%s)\.?\s?([�-�0-9]+)' % shortages, "rep": u'\g<1>\g<2>.%s\g<2>' % sym['nbsp'], "mod": re.S},

          #�� �������� ���., �. � �.�. �� ������.
          {"pat": u'(���|�|����|���|���)\.?\s*(\d+)', "rep": u'\g<1>.%s\g<2>' % sym['nbsp'], "mod": re.S|re.I},

          #�� ��������� 2007 �., ������� ������, ���� ��� ���. ������ �����, ���� � ���.
         {"pat": u'([0-9]+)\s*([��])\.\s', "rep": u'\g<1>%s\g<2>. ' % sym['nbsp'], "mod": re.S},
         
         #����������� ������ ����� ������ � �������� ���������
          {"pat": u'([0-9]+)\s*(%s)' % metrics, "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},
         
         #��������� � ��������
          {"pat": u'(\s%s)(\d+)' % metrics, "rep": u'\g<1><sup>\g<2></sup>'},   

         #���� ������ ��� ��� ����� ������ ������ � �� ���� �������� ����. 
         # + ������ ��������� ������ ����� ����, ��������: ������ � ����, ������ � �������� �������.
         {"pat": u'(\s+)(--?|�|&mdash;)(?=\s)', "rep": sym['nbsp']+sym['mdash']},
         {"pat": u'(^)(--?|�|&mdash;)(?=\s)', "rep": sym['mdash']},

         # ���� ������, ������������ � ����� ������ ������� � �� ���� ��������� ����.
         {"pat": u'(?<=\d)-(?=\d)', "rep": sym['ndash']},

         # ������ ��������� � ����� ������ �������� � ����� - ����� ���� � i @todo ������������ ���������
         #{"pat": u'(?<=\s|^|\W)(%s)(\s+)' % prepos, "rep": u'\g<1>'+sym['nbsp'], "mod": re.I},

         # ������ �������� ������� ��, ��, �� �� ��������������� �����, ��������: ��� ��, ���� ��, ��� ��.
         {"pat": u"(?<=\S)(\s+)(�|��|�|��|��|��|����|���)(?=[\s)!?.])", "rep": sym['nbsp'] + u'\g<2>'},

         # ����������� ������ ����� ���������.
         {"pat": u'([�-�A-Z]\.)\s?([�-�A-Z]\.)\s?([�-��-�A-Za-z]+)', "rep": u'\g<1>\g<2>%s\g<3>' % sym['nbsp'], "mod": re.S},

         # ���������� ���� �� ���������� �� �����.         
         {"pat": u'(\d+)\s?(%s)' % counts, "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},
      
         #��� � �������� ������
         {"pat": u'(\d+|%s)\s?��s' % counts, "rep": u'\g<1>%s�.�.' % sym['nbsp']},
          
         # �������� �����, ���������� ������� � ������ ������.
         {"pat": u'(\d+|%s)\s?(%s)' %(counts, money), "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},

         #����� ������ ��������� ����� ���������� � �������� v.
         {"pat": u'([v�]\.) ?([0-9])', "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.I},
         {"pat": u'(\w) ([v�]\.)', "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.I},
      
         #% �� ���������� �� �����
         {"pat": u'([0-9]+)\s+%', "rep": u'\g<1>%'}
        ]
        
        str = self.apply_rules(rules_quotes, str);
        
        #��������� ������.
        i = 0
        lev = 5
        matchLeftQuotes = re.compile(u'�(?:[^�]*?)�')#����� ��� �������� ����� ������
        matchRightQuotes = re.compile(u'�(?:[^�]*?)�')
        
        replaceOuterQuotes = re.compile(u'�([^�]*?)�(.*?)�')
        replaceRightQuotes = re.compile(u'�([^�]*?)�')
        while  i<5 and matchLeftQuotes.match(str):
            i+=1
            rep = u'�\g<1>%s\g<2>%s' % (sym['lquote2'], sym['rquote2'])
            str = replaceOuterQuotes.sub(rep, str)
            i+=1
            while i<lev and matchRightQuotes.match(str):
                i+=1
                str = replaceRightQuotes.sub(sym['rquote2'] + u'\g<1>�', str);
            
        #self.f.write("dfklsdkjflds" + str)   
        str = self.apply_rules(rules_strict, str);        
        str = self.apply_rules(rules_main, str);
        str = self.apply_rules(rules_symbols, str);
        str = self.apply_rules(rules_braces, str);
       
        return str;
