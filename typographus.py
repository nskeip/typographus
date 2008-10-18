#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Типограф версия 0.1 волевой выпуск
Страница проекта: http://code.google.com/p/typo-py/

Построено на основе PHP версии http://rmcreative.ru/blog/post/tipograf
Обладает схожим набором функционала.
Отсутствие поддержки Lookahead в Python regEx заставило автора кода
придумать иной механизм замены. Результат получился вполне рабочим.
Код написан почти в соответствии с PEP8.
Файл testTypographus.py содержит юнит тесты функционала, который был необходим
в проекте автора (для него же и писался типограф).

Автор: Кононученко Игорь
Почта: kigorw@gmail.com
Сайт: http://www.kigorw.com/

Разрешаю менять данный код как угодно, просить меня исправить ошибки
и ссылаться на страницу проекта.

Я ищу людей для совместной работы!
"""

import re

class Typographus:
    
    encoding = None
    
    sym = {
      'nbsp': u'&nbsp;',
      
      'lnowrap': u'<span style="white-space: nowrap;">',
      'rnowrap': u'</span>',

      'lquote': u'&laquo;',
      'rquote': u'&raquo;',
      'lquote2': u'„',
      'rquote2': u'“',
      'mdash': u'&mdash;',
      'ndash': u'&ndash;',
      'minus': u'&minus;', #соотв. по ширине символу +, есть во всех шрифтах

      'hellip': u'&hellip;',
      'copy': u'&copy;',
      'trade': u'<sup>&trade;</sup>',
      'apos': u'&#39;',   # см. http://fishbowl.pastiche.org/2003/07/01/the_curse_of_apos
      'reg': u'<sup><small>&reg;</small></sup>',
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
    
    
    def removeRedundantBlocks(self, string):
        blocks = {}
        def replace(m):
            value = m.group()
            if(len(value)==3):
                return value
            
            key = u'<%s>' % (len(blocks))
            blocks[key] = value;
            return key;
        
        pattern = self.getSafeBlockPattern() 
       
        string = re.compile(pattern, re.U).sub(replace, string);
        
        string = re.compile(ur"</?.*?/?>", re.U).sub(replace, string);
        
        return {"replaced": string, "blocks": blocks}
    
    
    def return_blocks_to_string(self, string, blocks):
        for key, value in blocks.items():
            string = string.replace(key, value)
        return string
        
        

    def process(self, string):
        
        if type(string) is not unicode:
            raise Exception, u'only unicode instances allowed for Typographus'
        
        
        value = self.removeRedundantBlocks(string)
        
        string = value["replaced"]
        blocks = value["blocks"]
      
        string = self.typo_text(string)
            
        string = self.return_blocks_to_string(string, blocks)
        return string
      
               
    def apply_rules(self, rules, string):
        for rule in rules:
            mod = re.X
            if type(rule) is dict:
                pat = rule["pat"]
                rep = rule["rep"]
                mod = rule.get("mod", re.X)
            elif type(rule) is tuple:
                pat, rep = rule[:2]
                if len(rule) == 3:
                    mod = rule[2]
            else:
                raise Exception, 'unknown rule type: %s' % repr(rule)
            mod += re.UNICODE
            try:
                string = re.compile(pat, mod).sub(rep, string)
            except UnicodeDecodeError:
                print type(string), repr(pat)
        return string
            
    
    def typo_text(self, string):
                
        def nowrap(string):
            return u'<nowrap>%s</nowrap>' % string
            return sym['lnowrap'] + string + sym['rnowrap']
        
        sym = self.sym
        if (string.strip() == ''):
            return ''
        
        html_tag = u''
        hellip = u'\.{3,5}'
             
        #Слово
        word = u'[a-zA-Zа-яА-Я_]'
        phrase_begin = ur"(?:%s|%s|\n)" %(hellip, word)
        
        #Конец слова
        phrase_end = ur"(?:%s|%s|\n)" %(hellip, word)

        #Знаки препинания (троеточие и точка - отдельный случай!)
        punctuation = u'[?!:,;]'
        
        #Аббревиатуры
        abbr = ur'(?:ООО|ОАО|ЗАО|ЧП|ИП|НПФ|НИИ)'
        
        #Предлоги и союзы
        prepos = u'а|в|во|вне|и|или|к|о|с|у|о|со|об|обо|от|ото|то|на|не|ни|но|из|изо|за|уж|на|по|под|подо|пред|предо|'        
        prepos +=u'про|над|надо|как|без|безо|что|да|для|до|там|ещё|их|или|ко|меж|между|перед|передо|около|через|сквозь|для|при|я'
        metrics = u'мм|см|м|км|г|кг|б|кб|мб|гб|dpi|px'
        
        shortages = u'г|гр|тов|пос|c|ул|д|пер|м'
        
        money = u'руб\.|долл\.|евро|у\.е\.'
        counts = u'млн\.|тыс\.'
        
        any_quote = u'(?:%s|%s|%s|%s|&quot;|")' % (sym['lquote'], sym['rquote'], sym['lquote2'], sym['rquote2'])
        
        brace_open = ur'(?:\(|\[|\{)'
        brace_close = ur'(?:\)|\]|\})'

        rules_strict = (
            
            # много пробелов или табуляций -> один пробел
            (ur'\s+', u' '),
            
            # запятые после "а" и "но"
            (ur'(?<=[^,])(?=\s(?:а|но)\s)', ur','),
            
        )

        rules_symbols = (

            # лишние знаки.
            (r'!!!+', r'!!!'),
            (r'(?<!!)!!(?!!)', '!'),

            (r'\?\?\?+', r'???'),
            (r'(?<!\?)\?\?(?!\?)', r'?'),
            
            (r';+', r';'),
            (r':+', r':'),
            (r',+', r','),
            
            (r'\+\++', '++'),
            (r'--+', '--'),
            (r'===+', '==='),
            
            # занятная комбинация
            (ur'!\?', u'?!'),
            
            # знаки (c), (r), (tm)
            (ur'\([cс]\)', sym['copy'], re.I), # русский и латинский варианты
            (ur'\(r\)', sym['reg'], re.I),
            (ur'\(tm\)', sym['trade'], re.I),
        
            # автор неправ. скорее всего малолетки балуются
            (ur'\.\.+', sym['hellip']),
            
            # спецсимволы для 1/2 1/4 3/4
            (ur'\b1/2\b', sym['1/2']),
            (ur'\b1/4\b', sym['1/4']),
            (ur'\b3/4\b', sym['3/4']),

            # какая-то муть с апострофами
            (ur"(?<=%s)'(?=%s)" % (word, word), sym['rsquo']),
            (ur"'", sym['apos']),
            
            
            # размеры 10x10, правильный знак + убираем лишние пробелы
            (ur'(?<=\d)\s*[x|X|х|Х]\s*(?=\d)', sym['multiply']),
            
            # +-
            (r'\+-', sym['plusmn']),
           
            (r'(?<=\S)\s+(?=-+>+|<+-+)', sym['nbsp']), # неразрывные пробелы перед стрелками
            (r'(-+>+|<+-+)\s+(?=\S)', r'\1' + sym['nbsp']), # неразрывные пробелы после стрелок

            # стрелки
            (r'<+-+', sym['larr']),
            (r'-+>+', sym['rarr']),
           
        )


        rules_quotes = (
            
            # разносим неправильные кавычки
            #(ur'([^"]\w+)"(\w+)"', u'\g<1> "\g<2>"'),
            (ur'([^"]\S+)"(\S+)"', ur'\1 "\2"'),
            (ur'"(\S+)"(\S+)', ur'"\1" \2'),
            
            # превращаем кавычки в ёлочки. Двойные кавычки склеиваем.
            # ((?:«|»|„|“|&quot;|"))((?:\.{3,5}|[a-zA-Zа-яА-Я_]|\n))
            (u"(%s)(%s)" % (any_quote, phrase_begin), u'%s\g<2>' % sym['lquote']),
            
            # ((?:(?:\.{3,5}|[a-zA-Zа-яА-Я_])|[0-9]+))((?:«|»|„|“|&quot;|"))
            (ur"((?:%s|(?:[0-9]+)))(%s)" % (phrase_end, any_quote), u'\g<1>%s' % sym['rquote']),
            
            (sym['rquote'] + any_quote, sym['rquote']+sym['rquote']),
            (any_quote + sym['lquote'], sym['lquote']+sym['lquote']),
            
        )
        
        rules_braces = (
            
            # оторвать скобку от слова
            (ur'(?<=\S)(?=%s)' % brace_open, ' '),
            (ur'(?<=%s)(?=\S)' % brace_close, ' '),
            
            # слепляем скобки со словами
            (ur'(?<=%s)\s' % brace_open, ''),
            (ur'\s(?=%s)' % brace_close, ''),
            
        )

        rules_main = (
            
            # нахер пробелы перед знаками препинания
            (r'\s+(?=[\.,:;!\?])', ''),
            
            # а вот после - очень даже кстати
            (r'(?<=[\.,:;!\?])(?![\.,:;!\?\s])', ' '),
            
            # знак дефиса, ограниченный с обоих сторон цифрами — на минус.
            (r'(?<=\d)-(?=\d)', sym['minus']),
            
            # оторвать тире от слова
            (r'(?<=\w)-\s+', ' - '),
            
                     #Знаки с предшествующим пробелом… нехорошо! пока не работает @todo переработать регулярку
                   #  {"pat": u'(%s)+(%s|%s)' % (phrase_end, punctuation, sym['hellip']), "rep": u'\g<1>\g<2>'},
                   #  {"pat": u'(%s)(%s)' % (punctuation, phrase_begin), "rep": u'\g<1> \g<2>'},
      
                      #Для точки отдельно
                      # {"pat": u'(\w)\s(?:\.)(\s|$)', "rep": u'\g<1>.\g<2>'},

            # неразрывные названия организаций и абревиатуры форм собственности
            (ur'(%s)\s+"([^"]+)"' % abbr, nowrap(ur'\1 "\2"')),
          
          #Нельзя отрывать сокращение от относящегося к нему слова.
          #Например: тов. Сталин, г. Воронеж
          #Ставит пробел, если его нет. И точку тоже ставит на всякий случай. :)
          {"pat": u'(^|[^a-zA-Zа-яА-Я])(%s)\.?\s?([А-Я0-9]+)' % shortages, "rep": u'\g<1>\g<2>.%s\g<2>' % sym['nbsp'], "mod": re.S},

          #Не отделять стр., с. и т.д. от номера.
          {"pat": u'(стр|с|табл|рис|илл)\.?\s*(\d+)', "rep": u'\g<1>.%s\g<2>' % sym['nbsp'], "mod": re.S|re.I},

          #Не разделять 2007 г., ставить пробел, если его нет. Ставит точку, если её нет.
         {"pat": u'([0-9]+)\s*([гГ])\.\s', "rep": u'\g<1>%s\g<2>. ' % sym['nbsp'], "mod": re.S},
         
         #Неразрывный пробел между цифрой и единицей измерения
          {"pat": u'([0-9]+)\s*(%s)' % metrics, "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},
         
         #Сантиметр в квадрате
          {"pat": u'(\s%s)(\d+)' % metrics, "rep": u'\g<1><sup>\g<2></sup>'},   

         #Знак дефиса или два знака дефиса подряд — на знак длинного тире. 
         # + Нельзя разрывать строку перед тире, например: Знание — сила, Курить — здоровью вредить.
         {"pat": u'(\s+)(--?|—|&mdash;)(?=\s)', "rep": sym['nbsp']+sym['mdash']},
         {"pat": u'(^)(--?|—|&mdash;)(?=\s)', "rep": sym['mdash']},

         # Нельзя оставлять в конце строки предлоги и союзы - убира слеш с i @todo переработать регулярку
         #{"pat": u'(?<=\s|^|\W)(%s)(\s+)' % prepos, "rep": u'\g<1>'+sym['nbsp'], "mod": re.I},

             # Нельзя отрывать частицы бы, ли, же от предшествующего слова, например: как бы, вряд ли, так же.
             # {"pat": u"(?<=\S)(\s+)(ж|бы|б|же|ли|ль|либо|или)(?=[\s)!?.])", "rep": sym['nbsp'] + u'\g<2>'},
             (ur'(?<=\S)\s+(ж|бы|б|же|ли|ль|либо|или)(?!\w)', sym['nbsp'] + r'\1'),
         
         # # Неразрывный пробел после инициалов.
         {"pat": u'([А-ЯA-Z]\.)\s?([А-ЯA-Z]\.)\s?([А-Яа-яA-Za-z]+)', "rep": u'\g<1>\g<2>%s\g<3>' % sym['nbsp'], "mod": re.S},

         # Сокращения сумм не отделяются от чисел.         
         {"pat": u'(\d+)\s?(%s)' % counts, "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},
      
         #«уе» в денежных суммах
         {"pat": u'(\d+|%s)\s?уеs' % counts, "rep": u'\g<1>%sу.е.' % sym['nbsp']},
          
         # Денежные суммы, расставляя пробелы в нужных местах.
         {"pat": u'(\d+|%s)\s?(%s)' %(counts, money), "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.S},

         #Номер версии программы пишем неразрывно с буковкой v.
         {"pat": u'([vв]\.) ?([0-9])', "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.I},
         {"pat": u'(\w) ([vв]\.)', "rep": u'\g<1>%s\g<2>' % sym['nbsp'], "mod": re.I},

      
             # % не отделяется от числа
             # {"pat": u'([0-9]+)\s+%', "rep": u'\g<1>%'}
             {'pat': r'(?<=\d)\s+(?=%)', 'rep': ''}

        )

        for rule_set in (rules_strict, rules_main, rules_symbols, rules_braces, rules_quotes):
            string = self.apply_rules(rule_set, string)
        
        # вложенные кавычки
        i = 0
        lev = 5
        
        matchLeftQuotes = re.compile(u'«(?:[^»]*?)«')#мачит две соседние левые елочки
        matchRightQuotes = re.compile(u'»(?:[^«]*?)»')
        
        replaceOuterQuotes = re.compile(u'«([^»]*?)«(.*?)»')
        replaceRightQuotes = re.compile(u'»([^«]*?)»')
        while  i<5 and matchLeftQuotes.match(string):
            i+=1
            rep = u'%s\g<1>%s\g<2>%s' % (q['lq'], sym['lquote2'], sym['rquote2'])
            string = replaceOuterQuotes.sub(rep, string)
            i+=1
            while i<lev and matchRightQuotes.match(string):
                i+=1
                string = replaceRightQuotes.sub(sym['rquote2'] + u'\g<1>%s' % q['rq'], string);
        
        string = string.replace(u'<nowrap>', sym['lnowrap']).replace(u'</nowrap>', sym['rnowrap'])
        
        return string.strip()

def typo(string):
    return Typographus().process(string)