from wsqluse.wsqluse import Wsqluse
from wsqluse.tests import test_cfg as tc
import unittest


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sqlshell = Wsqluse(tc.db_name, tc.db_user, tc.db_pass, tc.db_host)

    def test_get_table_dict_succes(self):
        command = "SELECT * FROM users"
        response = self.sqlshell.get_table_dict(command)
        self.assertTrue(response['status'] == 'success' and type(response['info']) == list)

    def test_get_table_dict_failed_error(self):
        command = "SELECT * FROM users where username=None"
        response = self.sqlshell.get_table_dict(command)
        self.assertTrue(response['status'] == 'failed')

    def test_get_table_dict_failed_nodata(self):
        command = "SELECT * FROM users where username='NOASKAS'"
        response = self.sqlshell.get_table_dict(command)
        self.assertTrue(response['status'] == 'failed')

if __name__ == '__main__':
    unittest.main()