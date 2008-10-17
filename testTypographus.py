# -*- coding: cp1251 -*-

import unittest
from typographus import Typographus


class TestTypographus(unittest.TestCase):
    html = u'<code>as "</code><p>������ - "�����"</p>'
    beforeRemoveBlocks = u"<code>dsfdsf</code>���� <div id='sd'>dfdf</div><pre>dsf</pre>"
    afterRemoveBlocks = u"<0>���� <1>dfdf<3><2>"
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
        str = self.t.process(u'<br style="">����� ���� � ��� "����"')
        self.assertEquals(str, u'<br style="">����� ���� � ��� �����')
     
   
    def test_with_tags(self):        
        str = self.t.process(self.html)
        self.assertEquals(str, u'<code>as "</code><p>������&nbsp;� �������</p>')
        
      
    def test_inner_quotes(self):
        str = self.t.process(u'"��� "����� �������""')
        self.assertEquals(str, u'���� ������ �������')
   
   
    def test_redundant_signs(self):
        str = self.t.process(u'����!!!! �������...  ����� ���')
        self.assertEquals(str, u'����!!! ������� ����� ���')
    
        
    def test_miss_comma(self):
        str = self.t.process(u'��������� � �� ��� ���?')
        self.assertEquals(str, u'���������, � �� ��� ���?')
     
      
    def test_braces(self):
        str = self.t.process(u'�� ���( ������� �� ) ����� �������')
        self.assertEquals(str, u'�� ��� (������� ��) ����� �������')
    
if __name__ == '__main__':
    unittest.main()
