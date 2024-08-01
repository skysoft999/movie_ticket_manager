import json
import unittest
from api.v1.booking import app

class TestTicketController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ticket_sorting_api(self):
        pass

    def test_sorting_service(self):
        pass
    
    def test_ticket_validators(self):
        pass

if __name__ == "__main__":
    unittest.main()