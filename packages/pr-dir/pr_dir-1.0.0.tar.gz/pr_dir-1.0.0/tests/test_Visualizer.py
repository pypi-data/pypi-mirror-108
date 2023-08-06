import unittest
from print_dir.visualizer import Visualizer


class test_Visualizer(unittest.TestCase):

    gt_dir = ['d1', 'd2', 'f1.txt', 'f2.docx', 'f3.py', 'r4.svg']
    d_dir = ['test_dir', '|_ 📁 d1', '|_ 📁 d2', '|_ 📃 f1.txt', '|_ 📃 f2.docx', '|_ 📃 f3.py', '|_ 📃 r4.svg']
    cd_dir = ['tests', '|_ 📁 test_dir', '|_ 📁 __pycache__', '|_ 📃 test_Visualizer.py', '|_ 📃 __init__.py']

    def test_get_content(self):
        test = Visualizer('tests/test_dir')
        self.assertEqual(test._get_content(), self.gt_dir)

    def test_dir(self):
        test = Visualizer('tests/test_dir')
        self.assertEqual(test.dir(), self.d_dir)

    def test_cd(self):
        test = Visualizer('tests/test_dir')
        test.cd('..')
        self.assertEqual(test.dir(), self.cd_dir)
