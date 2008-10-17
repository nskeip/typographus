# -*- coding: cp1251 -*-

import unittest
from typographus import Typographus


class TestTypographus(unittest.TestCase):
    html = u'<code>as "</code><p>Привет - "шмель"</p>'
    beforeRemoveBlocks = u"<code>dsfdsf</code>вася <div id='sd'>dfdf</div><pre>dsf</pre>"
    afterRemoveBlocks = u"<0>вася <1>dfdf<3><2>"
    t = Typographus()


    def getRemoveBlocksResult(self):
        return self.t.removeRedundantBlocks(self.beforeRemoveBlocks)
    
    
    def test_remove_blocks(self):
        str = self.getRemoveBlocksResult()["replaced"]
        self.assertEquals(str, self.afterRemoveBlocks)
    
    def test_remove_and_return_blocks(self):
        value = self.getRemoveBlocksResult()
        returnedBlocks = self.t.return_blocks_to_string(value["replaced"], value["blocks"])
        self.assertEquals(returnedBlocks, self.beforeRemoveBlocks)
        
    def test_quotes(self):
        str = self.t.process(u'<br style="">Капец тебе о сын "Неба"')
        self.assertEquals(str, u'<br style="">Капец тебе о сын «Неба»')
     
   
    def test_with_tags(self):        
        str = self.t.process(self.html)
        self.assertEquals(str, u'<code>as "</code><p>Привет&nbsp;— «шмель»</p>')
        
      
    def test_inner_quotes(self):
        str = self.t.process(u'"ООО "Латин продукт""')
        self.assertEquals(str, u'«ООО „Латин продукт“»')
   
   
    def test_redundant_signs(self):
        str = self.t.process(u'Хохо!!!! Негодяи...  Конец вам')
        self.assertEquals(str, u'Хохо!!! Негодяи… Конец вам')
    
        
    def test_miss_comma(self):
        str = self.t.process(u'Бармалюша а ты где был?')
        self.assertEquals(str, u'Бармалюша, а ты где был?')
     
      
    def test_braces(self):
        str = self.t.process(u'йо мае( подумал он ) пацан реально')
        self.assertEquals(str, u'йо мае (подумал он) пацан реально')
    
if __name__ == '__main__':
    unittest.main()
