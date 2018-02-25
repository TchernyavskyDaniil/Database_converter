import unittest
from codecs import open as open

from dbd_to_ram import DbdToRam
from ram_to_dbd import RamToDbd
from xdb_to_ram import XdbToRam

from utils.ram_to_xdb import RamToXdb


class ParsingTest(unittest.TestCase):
    def compare(self, path1, path2):
        diffs = ""
        with open(path1, 'r', 'utf8') as source_file, \
                open(path2, 'r', 'utf8') as result_file:

            i = 0
            for source_line in source_file:
                i += 1
                result_line = result_file.readline()
                if i == 1:
                    continue
                if source_line.split() != result_line.split():
                    diffs += '\norigin line {} : {} \nnew line {} : {}'.format(i, source_line, i, result_line)

            if diffs == "":
                print("Diffs not found. Files are equal.")

            source_file.close()
            result_file.close()
            return diffs

    def test_downloading(self):
        """
                xdb->ram->dbd->ram->xdb
        """
        xdb2ram = XdbToRam('D:/dankaloh/Database_converter/source/tasks.xml')
        schema = xdb2ram.parse()
        ram2dbd = RamToDbd('test_db1.db', schema)
        ram2dbd.generate(False)
        dbd2ram = DbdToRam('test_db1.db')
        schema = dbd2ram.parse()
        ram2xdb = RamToXdb('test1.xml', schema)
        ram2xdb.generate(False)
        diffs = self.compare('D:/dankaloh/Database_converter/source/tasks.xml', 'test1.xml')
        equal = True if diffs == "" else False
        self.assertTrue(equal, msg=diffs)
