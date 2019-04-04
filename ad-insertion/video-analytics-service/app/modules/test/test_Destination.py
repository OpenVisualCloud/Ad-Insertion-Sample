import sys, os
sys.path.append(os.path.dirname(__file__) + "/../../")

import unittest
import common

import modules.Destination as Destination

class TestDestination(unittest.TestCase):

    def test_create_instance(self):
        request = {
            "destination": {
                "type": "kafka"
            }
        }
        MockKafkaDestination = type("MockKafkaDestination", (object,), {
            "__init__": lambda self, destination: None
        })
        Destination.destination_types['kafka'] = MockKafkaDestination

        result = Destination.create_instance(request)

        self.assertIsInstance(result, MockKafkaDestination)

if __name__ == '__main__':
    unittest.main()