import unittest
import requests

class TestAPI(unittest.TestCase):
    def test_api_response(self):
        response = requests.get('http://localhost:5000/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {'message': 'pong'})

if __name__ == '__main__':
    unittest.main()
