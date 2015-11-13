#!/usr/bin/env python
#
#  XXX  Identifying information about tests here.
#
#===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

# raise NotImplementedError(
#         'To customize, remove this line and customize where it says XXX')

import unittest

import os
import sys
sys.path.append('..')      # XXX Probably needed to import your code


class test_XXX_Test_Group_Name(unittest.TestCase):


    def setUp(self):
        ###  XXX code to do setup
        pass

    def tearDown(self):
        ###  XXX code to do tear down
        pass

    def test_XXX_Test_Name(self):
        #  Examples:
        self.assertEqual(pow(2,7,11), 7)
        self.assertEqual("RoSe".lower(), 'is a rose'[5:9])
        self.assertFalse((bool(0) and bool(1)))
        self.assertTrue((bool(1 ^ 0)))
        self.assertIn('fun', 'disfunctional')
        self.assertNotIn('crazy', 'disfunctional')
        with self.assertRaises(Exception):
        	raise Exception('test')
        # Unconditionally fail, for example in a try block that should raise
        # self.fail('Exception was not raised')


unittest.main()
