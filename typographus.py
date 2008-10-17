#-*- coding: cp1251 -*-
'''
Типограф версия 0.1 волевой выпуск
Страница проекта: 

Построено на основе PHP версии http://rmcreative.ru/blog/post/tipograf
Обладает схожим набором функционала.
Отличия в работе Lookahead и Lookbehind в Python regEx заставило автора кода
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
'''
import re


class Typographus:
    
       
    encoding = None
    
    sym = {
      'nbsp': u'&nbsp;',
      'lnowrap': u'<span style="white-space:nowrap">',
      'rnowrap': u'</span>',

      'lquote': u'«',
      'rquote': u'»',
      'lquote2': u'„',
      'rquote2': u'“',
      'mdash': u'—',
      'ndash': u'–',
      'minus': u'–', #соотв. по ширине символу +, есть во всех шрифтах

      'hellip': u'…',
      'copy': u'©',
      'trade': u'<sup>™</sup>',
      'apos': u'&#39;',   # см. http://fishbowl.pastiche.org/2003/07/01/the_curse_of_apos
      'reg': u'<sup><small>®</small></sup>',
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
             
        #Слово
        word = u'[a-zA-Zа-яА-Я_]'
        phrase_begin = ur"(?:%s|%s|\n)" %(hellip, word)
        
        #Конец слова
        phrase_end = ur"(?:%s|%s|\n)" %(hellip, word)

        #Знаки препинания (троеточие и точка - отдельный случай!)
        punctuation = u'[?!:,;]'
        
        #Аббревиатуры
        abbr = u'(?:ООО|ОАО|ЗАО|ЧП|ИП|НПФ|НИИ)';
        #Предлоги и союзы
        prepos = u'а|в|во|вне|и|или|к|о|с|у|о|со|об|обо|от|ото|то|на|не|ни|но|из|изо|за|уж|на|по|под|подо|пред|предо|'        
        prepos +=u'про|над|надо|как|без|безо|что|да|для|до|там|ещё|их|или|ко|меж|между|перед|передо|около|через|сквозь|для|при|я'
        metrics = u'мм|см|м|км|г|кг|б|кб|мб|гб|dpi|px';
        
        shortages = u'г|гр|тов|пос|c|ул|д|пер|м';

        money = u'руб\.|долл\.|евро|у\.е\.';
        counts = u'млн\.|тыс\.';
        
        any_quote = u'(?:%s|%s|%s|%s|&quot;|")' %(sym['lquote'], sym['rquote'], sym['lquote2'], sym['rquote2'])
        
        rules_strict = [
        # Много пробелов или табуляций -> один пробел
        {"pat": u'\s+', "rep": u' '},
        # Запятые после «а» и «но». Если уже есть — не ставим.
        {"pat": u'([^,])\s(а|но)\s', "rep": u'\g<1>, \g<2> '}
        ]
        

        rules_symbols = [
            #Лишние знаки.
            #TODO: сделать красиво
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
        
            #Занятная комбинация
            {"pat": u'!\?', "rep": u'?!'},
            #Знаки (c), (r), (tm)
            {"pat": u'\((c|с)\)', "rep": sym['copy'], "mod": re.I},
            {"pat": u'\(r\)', "rep": sym['reg'], "mod": re.I},
            {"pat": u'\(tm\)', "rep": sym['trade'], "mod": re.I},
        
            #От 2 до 5 знака точки подряд - на знак многоточия (больше - мб авторской задумкой).
            {"pat": hellip, "rep": sym['hellip']},

            #Спецсимволы для 1/2 1/4 3/4
            {"pat": u'\b1/2\b', "rep": sym['1/2']},
            {"pat": u'\b1/4\b', "rep": sym['1/4']},
            {"pat": u'\b3/4\b', "rep": sym['3/4']},

            #LО'Лайт
            {"pat": u"([a-zA-Z])'([а-яА-Я])", "rep": u'\g<1>%s\g<2>' % sym['rsquo'], "mod": re.I},
        
            {"pat": u"'", "rep": sym['apos']}, #str_replace?
      
            # Размеры 10x10, правильный знак + убираем лишние пробелы
            {"pat": u'(\d+)\s{0,}?[x|X|х|Х|*]\s{0,}(\d+)', "rep": u'\g<1>%s\g<2>' % sym['multiply']},
        
            #+-
            {"pat": u'([^\+]|^)\+-', "rep": u'\g<1>%s' % sym['plusmn']},
        
           #Стрелки
           {"pat": u'([^-]|^)->', "rep": u'\g<1>%s' % sym['rarr']},
           {"pat": u'<-([^-]|$)', "rep": u'%s\g<1>' % sym['larr']}
        ]


        rules_quotes = [
            # Разносим неправильные кавычки
           {"pat": u'([^"]\w+)"(\w+)"', "rep": u'\g<1> "\g<2>"'},
           {"pat": u'"(\w+)"(\w+)', "rep": u'"\g<1>" \g<2>'},
           #Превращаем кавычки в ёлочки. Двойные кавычки склеиваем.
           #((?:«|»|„|“|&quot;|"))((?:\.{3,5}|[a-zA-Zа-яА-Я_]|\n))
           {"pat": u"(%s)(%s)" % (any_quote, phrase_begin), "rep": u'%s\g<2>' % sym['lquote']},
           
           #((?:(?:\.{3,5}|[a-zA-Zа-яА-Я_])|[0-9]+))((?:«|»|„|“|&quot;|"))
           {"pat": "((?:%s|(?:[0-9]+)))(%s)" % (phrase_end, any_quote), "rep": u'\g<1>%s' % sym['rquote']},
           
           {"pat": sym['rquote'] + any_quote, "rep": sym['rquote']+sym['rquote']},
           {"pat": any_quote + sym['lquote'], "rep": sym['lquote']+sym['lquote']}
        ]
        
        rules_braces = [
         #Оторвать скобку от слова
         {"pat": u'(%s)\(' % word, "rep": u'\g<1> ('},
          #Слепляем скобки со словами
         {"pat": u'\(\s', "rep": u'(', "mod": re.S},
         {"pat": u'\s\)', "rep": u')', "mod": re.S},
         ]

        rules_main = [
         #Оторвать тире от слова
         {"pat": u'(\w)- ', "rep": u'\g<1> - '},

         #Знаки с предшествующим пробелом… нехорошо! пока не работает @todo переработать регулярку
       #  {"pat": u'(%s)+(%s|%s)' % (phrase_end, punctuation, sym['hellip']), "rep": u'\g<1>\g<2>'},
       #  {"pat": u'(%s)(%s)' % (punctuation, phrase_begin), "rep": u'\g<1> \g<2>'},
      
          #Для точки отдельно
          {"pat": u'(\w)\s(?:\.)(\s|$)', "rep": u'\g<1>.\g<2>'},

          #Неразрывные названия организаций и абревиатуры форм собственности
          #  почему не один &nbsp;?
          # ! названия организаций тоже могут содержать пробел !
          {"pat": u'(%s)\s+"(.*)"' % abbr, "rep": u'%s\g<1> "\g<2>"%s' % (sym['rnowrap'], sym['lnowrap'])},

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

         # Знак дефиса, ограниченный с обоих сторон цифрами — на знак короткого тире.
         {"pat": u'(?<=\d)-(?=\d)', "rep": sym['ndash']},

         # Нельзя оставлять в конце строки предлоги и союзы - убира слеш с i @todo переработать регулярку
         #{"pat": u'(?<=\s|^|\W)(%s)(\s+)' % prepos, "rep": u'\g<1>'+sym['nbsp'], "mod": re.I},

         # Нельзя отрывать частицы бы, ли, же от предшествующего слова, например: как бы, вряд ли, так же.
         {"pat": u"(?<=\S)(\s+)(ж|бы|б|же|ли|ль|либо|или)(?=[\s)!?.])", "rep": sym['nbsp'] + u'\g<2>'},

         # Неразрывный пробел после инициалов.
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
      
         #% не отделяется от числа
         {"pat": u'([0-9]+)\s+%', "rep": u'\g<1>%'}
        ]
        
        str = self.apply_rules(rules_quotes, str);
        
        #Вложенные кавыки.
        i = 0
        lev = 5
        matchLeftQuotes = re.compile(u'«(?:[^»]*?)«')#мачит две соседние левые елочки
        matchRightQuotes = re.compile(u'»(?:[^«]*?)»')
        
        replaceOuterQuotes = re.compile(u'«([^»]*?)«(.*?)»')
        replaceRightQuotes = re.compile(u'»([^«]*?)»')
        while  i<5 and matchLeftQuotes.match(str):
            i+=1
            rep = u'«\g<1>%s\g<2>%s' % (sym['lquote2'], sym['rquote2'])
            str = replaceOuterQuotes.sub(rep, str)
            i+=1
            while i<lev and matchRightQuotes.match(str):
                i+=1
                str = replaceRightQuotes.sub(sym['rquote2'] + u'\g<1>»', str);
            
        #self.f.write("dfklsdkjflds" + str)   
        str = self.apply_rules(rules_strict, str);        
        str = self.apply_rules(rules_main, str);
        str = self.apply_rules(rules_symbols, str);
        str = self.apply_rules(rules_braces, str);
       
        return str;
