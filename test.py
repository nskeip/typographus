﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from typographus import Typographus

class TestPunctuation(unittest.TestCase):
    
    def setUp(self):
        self._typo = Typographus()
        
    def assert_typo(self, expect, input):
        self.assertEqual(expect, self.typo(input))
    
    def typo(self, string):
        return self._typo.process(string)
		
    def testmath(self):
        self.assert_typo(u'5+6&minus;7&plusmn;8', u'5+6-7+-8')
        self.assert_typo(u'===', u'============')
        self.assert_typo(u'++', u'+++++++++++')
    
    def testrepeats(self):
        self.assert_typo(u'!!!', u'!!!!!!!!!!!!!!')
        self.assert_typo(u'!', u'!!')
        self.assert_typo(u'???', u'??????????')
        self.assert_typo(u'?', u'??')
    
    def testarrows(self):
        self.assert_typo(u'&rarr;', u'----->')
        self.assert_typo(u'&larr;', u'<-------')
    
    def testmultiply(self):
        self.assert_typo(u'6&times;7', u'6x7')
    
    def testnowrap(self):
        self.assert_typo(u'<span style="white-space: nowrap;">ООО &laquo;Рога и Копыта&raquo;</span>',
                         u'ООО "Рога и Копыта"')
    
if __name__ == '__main__':
    unittest.main()