import unittest
from codecs import open as open


from ram_to_xdb import RamToXdb
from xdb_to_ram import XdbToRam


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

    def test_parsing(self):
        """
                xdb->ram->xdb
        """
        xdb2ram = XdbToRam('source/tasks.xdb')
        schema = xdb2ram.parse()
        ram2xdb = RamToXdb('test1.xml', schema)
        ram2xdb.generate()
        diffs = self.compare('source/tasks.xdb', 'test1.xml')
        equal = True if diffs == "" else False
        self.assertTrue(equal, msg=diffs)
