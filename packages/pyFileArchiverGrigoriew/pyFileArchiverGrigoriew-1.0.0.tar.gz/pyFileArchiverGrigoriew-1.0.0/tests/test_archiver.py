import unittest
import filecmp
import hashlib
import shutil
from os import getcwd, remove, mkdir
from os.path import join
from pyFileArchiver.archiver import arcZip, arcExtract


class TestArchiver(unittest.TestCase):
    test_path = join(getcwd(), 'tests', 'test_folders')

    def test_arcZip_1(self):
        arcZip(join(self.test_path, 'Test1.zip'), [
            join(self.test_path, 'test_folder_1', 'documents'),
            join(self.test_path, 'test_folder_1', '3.py')
        ])

        with open(join(self.test_path, 'for_test_1.zip'), 'rb') as outputArc, open(join(self.test_path, 'Test1.zip'),
                                                                                   'rb') as inputArc:
            hashOut = hashlib.sha256(outputArc.read()).digest()
            hashIn = hashlib.sha256(inputArc.read()).digest()

            self.assertEqual(hashOut, hashIn)

        remove(join(self.test_path, 'Test1.zip'))

    def test_arcZip_2(self):
        arcZip(join(self.test_path, 'Test2.zip'), [join(self.test_path, 'test_folder_2')], '.txt')

        with open(join(self.test_path, 'for_test_2.zip'), 'rb') as outputArc, open(join(self.test_path, 'Test2.zip'),
                                                                                   'rb') as inputArc:
            hashOut = hashlib.sha256(outputArc.read()).digest()
            hashIn = hashlib.sha256(inputArc.read()).digest()

            self.assertEqual(hashOut, hashIn)

        remove(join(self.test_path, 'Test2.zip'))

    def test_arcZip_3(self):
        arcZip(join(self.test_path, 'Test3.zip'), [join(self.test_path, 'test_folder_2')])

        with open(join(self.test_path, 'for_test_3.zip'), 'rb') as outputArc, open(join(self.test_path, 'Test3.zip'),
                                                                                   'rb') as inputArc:
            hashOut = hashlib.sha256(outputArc.read()).digest()
            hashIn = hashlib.sha256(inputArc.read()).digest()

            self.assertEqual(hashOut, hashIn)

        remove(join(self.test_path, 'Test3.zip'))

    def test_arcExtract_1(self):
        mkdir(join(self.test_path, 'arc_test'))
        arcExtract(join(self.test_path, 'for_test_3.zip'), join(self.test_path, 'arc_test'))

        compare = filecmp.dircmp(join(self.test_path, 'arc_test'), join(self.test_path, 'test_folder_2'))
        self.assertTrue(not len(compare.left_only) and not len(compare.right_only))

        shutil.rmtree(join(self.test_path, 'arc_test'))


if __name__ == '__main__':
    unittest.main()
