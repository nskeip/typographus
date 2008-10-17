#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from typographus import Typographus

class TestPunctuation(unittest.TestCase):
    
    def setUp(self):
        self._typo = Typographus()
    
    def typo(self, string):
        return self._typo.process(string)
    
    def testcommon(self):
        self.assertEqual(u'Здравствуй, буква&nbsp;&mdash; буква А!',
            self.typo(u'Здравствуй ,буква- буква А !!'))
    
    def testmath(self):
        self.assertEqual(u'5+6&minus;7&plusmn;8',
            self.typo(u'5+6-7+-8'))
        self.assertEqual(u'===',
            self.typo(u'============'))
        self.assertEqual(u'++',
            self.typo(u'+++++++++++'))
    
    def testrepeats(self):
        self.assertEqual(u'!!!',
            self.typo(u'!!!!!!!!!!!!!!'))
        self.assertEqual(u'!',
            self.typo(u'!!'))
        self.assertEqual(u'???',
            self.typo(u'??????????'))
        self.assertEqual(u'?',
            self.typo(u'??'))
    
    def testarrows(self):
        self.assertEqual(u'&rarr;',
            self.typo(u'----->'))
        self.assertEqual(u'&larr;',
            self.typo(u'<-------'))
    
    def testmultiply(self):
        self.assertEqual(u'6&times;7',
            self.typo(u'6x7'))
    
    def testnowrap(self):
        self.assertEqual(u'<span style="white-space: nowrap;">ООО &laquo;Рога и Копыта&raquo;</span>',
            self.typo(u'ООО "Рога и Копыта"'))
    
if __name__ == '__main__':
    unittest.main()