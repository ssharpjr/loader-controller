import unittest
import loader_controller

class TestWoScan(object):
    def setUp(self):
        self.get_wo_scan = loader_controller.get_wo_scan()

    def test_get_wo_scan_returns_correct_value(self):
        self.assertEqual(12345678, self.get_wo_scan(wo_id))


if __name__ == '__main__':
    unittest.main()

