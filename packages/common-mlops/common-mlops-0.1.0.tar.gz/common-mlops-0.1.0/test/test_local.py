#!/usr/bin/env python

import unittest
from mlops.local import Local


class TestLocal(unittest.TestCase):
    CONST_LOCAL_FILE_NAME = 'data/TaraContextData.csv'

    def setUp(self):
        self.local_file_name = self.CONST_LOCAL_FILE_NAME

        self.local = Local()

    @unittest.skip("Skipping in CI/CD pipeline because the CSV file is not in the repository")
    def test_print_data(self):
        # Assert 1: Just check for some exception
        try:
            self.local.print_data()
        except Exception:
            self.fail('Unexpected exception raised')


if __name__ == "__main__":
    unittest.main()
