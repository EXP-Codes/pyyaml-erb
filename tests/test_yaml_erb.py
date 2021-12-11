# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
# ----------------------------------------------------------------------
# 把父级目录（项目根目录）添加到工作路径，以便在终端也可以执行单元测试
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import unittest
import src.erb.yml as yaml


class TestYamlERB(unittest.TestCase):

    def test_load(self) :
        SETTING_PATH =  './config/settings.yml'
        with open(SETTING_PATH, 'r', encoding='utf-8') as file :
            settings = yaml.load(file.read())
            
            self.assertEqual(settings['base']['filepath'], './tmp/or.cache')
            self.assertEqual(settings['base']['charset'], 'utf-8')
            self.assertEqual(settings['base']['loop_interval'], 10800)
            self.assertIsNone(settings['base']['app_name'])
            self.assertEqual(settings['base']['threadpool']['worker'], 10)
            
            self.assertEqual(settings['database']['dbtype'], 'mysql')
            self.assertEqual(settings['database']['host'], '127.0.0.1')
            self.assertEqual(settings['database']['port'], 3306)
            self.assertIsNone(settings['database']['db_name'])
            self.assertIsNone(settings['database']['username'])
            self.assertIsNone(settings['database']['password'])
            self.assertIsNone(settings['database']['encoding'])

            self.assertEqual(settings['arg_list'][0], 'exp')
            self.assertEqual(settings['arg_list'][1], 12.34)
            self.assertIsNotNone(settings['arg_list'][2])
            self.assertEqual(settings['arg_list'][3], '')
            self.assertTrue(settings['arg_list'][4])
            self.assertFalse(settings['arg_list'][5])
            self.assertIsNotNone(settings['arg_list'][6])
            


if __name__ == '__main__':
    unittest.main()

