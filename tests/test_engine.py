import unittest
from core.engine import BaseEngine

class TestBaseEngine(unittest.TestCase):
    def test_initialization(self):
        engine = BaseEngine()
        self.assertIsNotNone(engine)

if __name__ == '__main__':
    unittest.main()
